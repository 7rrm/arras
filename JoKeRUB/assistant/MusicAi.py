import requests
import json
import re
import time
import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# استيراد من Config بدلاً من input()
from JoKeRUB import bot as tgbot
from ..Config import Config

print("🎵 بوت AIMusicGen - بإستخدام mail.tm فقط")

BASE_URL = "https://aimusicgen.ai"
Bot_Username = Config.TG_BOT_USERNAME

# ========== إعدادات الملفات ==========
accounts_file = "music_accounts.json"
os.makedirs("accounts", exist_ok=True)
os.makedirs("songs", exist_ok=True)

# ========== فئة جلسة المستخدم ==========
class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None  # 'waiting_desc', 'waiting_lyrics', 'waiting_title'
        self.lyrics = None
        self.title = None
        self.styles = None
        self.prompt = None

user_sessions = {}

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]

# ========== دوال إدارة الحسابات ==========
def load_accounts():
    if not os.path.exists(accounts_file):
        return []
    with open(accounts_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_accounts(accounts):
    with open(accounts_file, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)

def get_user_accounts(user_id):
    """الحصول على جميع حسابات المستخدم"""
    accounts = load_accounts()
    return [acc for acc in accounts if acc.get('user_id') == str(user_id)]

def add_account(user_id, email, password, session_token, uid):
    """إضافة حساب جديد"""
    accounts = load_accounts()
    new_account = {
        'user_id': str(user_id),
        'email': email,
        'password': password,
        'session_token': session_token,
        'uid': uid,
        'created_at': datetime.now().isoformat(),
        'use_count': 0  # استخدامات مفتوحة - فقط للتتبع
    }
    accounts.append(new_account)
    save_accounts(accounts)
    return new_account

# ========== دوال mail.tm ==========
def create_mailtm_account():
    """إنشاء حساب على mail.tm"""
    try:
        base_url = "https://api.mail.tm"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        # الحصول على دومين
        domains_resp = requests.get(f"{base_url}/domains", headers=headers, timeout=10)
        if domains_resp.status_code != 200:
            return None, None, None
            
        domains_data = domains_resp.json()
        domain = domains_data.get("hydra:member", [{}])[0].get("domain", "")
        if not domain:
            return None, None, None
        
        # إنشاء بريد عشوائي
        username = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(12))
        email = f"{username}@{domain}"
        password = f"Pass{random.randint(1000, 9999)}!"
        
        # إنشاء حساب
        account_payload = {"address": email, "password": password}
        account_resp = requests.post(f"{base_url}/accounts", json=account_payload, headers=headers, timeout=10)
        if account_resp.status_code not in [200, 201]:
            return None, None, None
        
        # الحصول على التوكن
        token_payload = {"address": email, "password": password}
        token_resp = requests.post(f"{base_url}/token", json=token_payload, headers=headers, timeout=10)
        if token_resp.status_code != 200:
            return None, None, None
            
        token_data = token_resp.json()
        token = token_data.get("token", "")
        
        return email, password, token
        
    except Exception as e:
        print(f"خطأ في إنشاء حساب mail.tm: {e}")
        return None, None, None

def get_mailtm_verification(token):
    """انتظار رابط التحقق من mail.tm"""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Authorization": f"Bearer {token}"
    }
    
    for _ in range(30):  # 30 محاولة × 2 ثانية = 60 ثانية
        try:
            messages_resp = requests.get("https://api.mail.tm/messages", headers=headers, timeout=10)
            if messages_resp.status_code == 200:
                messages_data = messages_resp.json()
                messages = messages_data.get("hydra:member", [])
                
                for msg in messages:
                    sender = msg.get('from', {}).get('address', '')
                    if 'aimusicgen.ai' in sender:
                        msg_id = msg["id"]
                        msg_resp = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers, timeout=10)
                        if msg_resp.status_code == 200:
                            full_msg = msg_resp.json()
                            text_content = full_msg.get('text', '') + full_msg.get('html', '')
                            links = re.findall(r'https://aimusicgen\.ai/api/auth/callback/email\?[^\s"\']+', text_content)
                            if links:
                                return links[0]
        except:
            pass
        time.sleep(2)
    
    return None

# ========== دوال AIMusicGen ==========
def get_csrf_token(session):
    """الحصول على CSRF token"""
    try:
        response = session.get(f"{BASE_URL}/api/auth/csrf", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("csrfToken")
    except:
        pass
    return None

def send_login_request(session, email, csrf_token):
    """إرسال طلب تسجيل الدخول"""
    url = f"{BASE_URL}/api/auth/signin/email"
    payload = {
        'email': email,
        'callbackUrl': "/",
        'redirect': "false",
        'csrfToken': csrf_token,
        'json': "true"
    }
    headers = {
        'origin': "https://aimusicgen.ai",
        'referer': "https://aimusicgen.ai/login",
    }
    try:
        response = session.post(url, data=payload, headers=headers, timeout=15)
        return response.status_code == 200
    except:
        return False

def verify_account(session, verify_url):
    """تفعيل الحساب عبر رابط التحقق"""
    headers = {
        'referer': 'https://aimusicgen.ai/login',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
    }
    try:
        response = session.get(verify_url, headers=headers, timeout=15, allow_redirects=True)
        return True
    except:
        return False

def get_session_data(session):
    """الحصول على بيانات الجلسة"""
    headers = {
        'content-type': "application/json",
        'referer': "https://aimusicgen.ai/",
    }
    try:
        response = session.get(f"{BASE_URL}/api/auth/session", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and 'user' in data:
                return data['user'].get('id'), data['user'].get('email')
    except:
        pass
    return None, None

def initialize_user(session, uid):
    """تهيئة المستخدم في النظام"""
    url = f"{BASE_URL}/api/user"
    payload = {"user_id": uid}
    headers = {'Content-Type': 'application/json'}
    try:
        response = session.post(url, json=payload, headers=headers, timeout=15)
        return response.status_code == 200
    except:
        return False

def generate_lyrics(prompt, uid):
    """توليد كلمات الأغنية"""
    url = f"{BASE_URL}/api/lyrics-generate"
    payload = {
        "prompt": prompt,
        "model": "google/gemini-3",
        "userId": uid
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('title', 'أغنية جديدة'),
                'tags': data.get('tags', 'Arabic, Pop, Male Vocal'),
                'lyrics': data.get('lyrics', '')
            }
    except:
        pass
    return None

def create_song(session, lyrics, title, styles, uid, email):
    """إنشاء أغنية"""
    url = f"{BASE_URL}/api/song"
    payload = {
        "lyrics_mode": True,
        "instrumental": False,
        "lyrics": lyrics,
        "description": "",
        "title": title,
        "styles": styles,
        "style_negative": "",
        "type": "custom",
        "model": "v5.0",
        "user_id": uid,
        "user_email": email,
        "is_private": False,
        "is_original": False
    }
    headers = {
        'Content-Type': 'application/json',
        'origin': "https://aimusicgen.ai",
        'referer': "https://aimusicgen.ai/create",
    }
    try:
        response = session.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_song_status(session, music_id):
    """التحقق من حالة الأغنية"""
    url = f"{BASE_URL}/api/music-library/getStatus"
    params = {'musicId': music_id}
    headers = {
        'referer': "https://aimusicgen.ai/create",
    }
    try:
        response = session.get(url, params=params, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def wait_for_completion(session, music_ids, max_wait=180, check_interval=10):
    """انتظار اكتمال الأغاني"""
    start_time = time.time()
    completed = []
    
    while time.time() - start_time < max_wait:
        remaining = [mid for mid in music_ids if mid not in [s.get('music_id') for s in completed]]
        if not remaining:
            break
            
        for music_id in remaining:
            status_data = get_song_status(session, music_id)
            if status_data and status_data.get('success'):
                song = status_data['data']
                if song.get('status') == 2:  # مكتمل
                    audio = song.get('audio', '')
                    if audio and audio.strip():
                        completed.append(song)
        
        if len(completed) < len(music_ids):
            time.sleep(check_interval)
    
    return completed

def download_song(audio_url, song_name):
    """تحميل الأغنية"""
    if not audio_url or not audio_url.strip():
        return None
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(audio_url, headers=headers, stream=True, timeout=30)
        if response.status_code == 200:
            os.makedirs('songs', exist_ok=True)
            # تنظيف اسم الملف
            safe_name = re.sub(r'[^\w\-_\. ]', '_', song_name)
            file_path = f"songs/{safe_name}.mp3"
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return file_path
    except:
        pass
    return None

# ========== الدوال الرئيسية ==========
async def create_aimusicgen_account(user_id):
    """إنشاء حساب جديد على AIMusicGen"""
    try:
        # 1. إنشاء حساب mail.tm
        email, password, mail_token = create_mailtm_account()
        if not email or not mail_token:
            return None, "❌ فشل في إنشاء بريد مؤقت"
        
        # 2. إنشاء جلسة requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        
        # 3. الحصول على CSRF token
        csrf_token = get_csrf_token(session)
        if not csrf_token:
            return None, "❌ فشل في الحصول على رمز الحماية"
        
        # 4. إرسال طلب تسجيل الدخول
        if not send_login_request(session, email, csrf_token):
            return None, "❌ فشل في إرسال طلب التسجيل"
        
        # 5. انتظار رابط التحقق
        verify_url = get_mailtm_verification(mail_token)
        if not verify_url:
            return None, "❌ لم يصل رابط التحقق"
        
        # 6. تفعيل الحساب
        if not verify_account(session, verify_url):
            return None, "❌ فشل في تفعيل الحساب"
        
        # 7. الحصول على بيانات الجلسة
        uid, user_email = get_session_data(session)
        if not uid:
            return None, "❌ فشل في الحصول على بيانات الجلسة"
        
        # 8. تهيئة المستخدم
        initialize_user(session, uid)
        
        # 9. حفظ الحساب في قاعدة البيانات
        new_account = {
            'user_id': str(user_id),
            'email': email,
            'password': password,
            'session': session.cookies.get_dict(),  # حفظ الكوكيز
            'uid': uid,
            'created_at': datetime.now().isoformat(),
            'use_count': 0
        }
        
        accounts = load_accounts()
        accounts.append(new_account)
        save_accounts(accounts)
        
        return new_account, f"✅ **تم إنشاء حساب جديد!**\n📧 البريد: `{email}`\n🆔 المعرف: `{uid}`"
        
    except Exception as e:
        print(f"خطأ في إنشاء الحساب: {e}")
        return None, f"❌ حدث خطأ: {str(e)}"

async def get_or_create_account(user_id):
    """الحصول على حساب موجود أو إنشاء جديد"""
    accounts = get_user_accounts(user_id)
    
    if accounts:
        # استخدام أول حساب متاح
        account = accounts[0]
        
        # استعادة الجلسة من الكوكيز
        session = requests.Session()
        session.headers.update({
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        
        # استعادة الكوكيز
        if 'session' in account:
            session.cookies.update(account['session'])
        
        return {
            'session': session,
            'email': account['email'],
            'uid': account['uid']
        }
    
    # إذا لم يوجد حساب، إنشاء جديد
    account, message = await create_aimusicgen_account(user_id)
    if account:
        session = requests.Session()
        session.headers.update({
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        if 'session' in account:
            session.cookies.update(account['session'])
        
        return {
            'session': session,
            'email': account['email'],
            'uid': account['uid']
        }
    
    return None

# ========== واجهة Telegram ==========
menu_text = '''
🎵 **بوت إنشاء الموسيقى باستخدام الذكاء الاصطناعي**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("🎼 إنشاء أغنية جديدة", data="create_song"), 
        Button.inline("📝 إدخال كلمات يدوياً", data="manual_lyrics"),
    ],
    [
        Button.inline("📋 حساباتي", data="my_accounts"),
        Button.inline("➕ إنشاء حساب جديد", data="new_account"),
    ],
    [
        Button.url("المطور", "https://t.me/Lx5x5")
    ]
]

async def start_command(event):
    """بدء المحادثة"""
    await event.respond(menu_text, buttons=keyboard)

async def callback_handler(event):
    """معالجة نقرات الأزرار"""
    data = event.data.decode('utf-8')
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if data == "create_song":
        session.state = 'waiting_desc'
        await event.edit(
            "✍️ **أرسل وصفاً للأغنية:**\n\n"
            "مثال: 'أغنية حب رومانسية عن شروق الشمس'\n\n"
            "أو ارسل /cancel للإلغاء"
        )
    
    elif data == "manual_lyrics":
        session.state = 'waiting_lyrics'
        await event.edit(
            "📝 **أرسل كلمات الأغنية كاملة:**\n\n"
            "يمكنك تقسيمها إلى مقاطع\n\n"
            "أو ارسل /cancel للإلغاء"
        )
    
    elif data == "my_accounts":
        accounts = get_user_accounts(user_id)
        if not accounts:
            await event.edit("📭 **لا توجد حسابات بعد.**", buttons=keyboard)
        else:
            text = "📋 **حساباتك:**\n\n"
            for i, acc in enumerate(accounts, 1):
                text += f"**{i}. {acc['email']}**\n"
                text += f"   🆔: `{acc.get('uid', 'غير معروف')}`\n"
                text += f"   📅: {acc.get('created_at', 'غير معروف')[:10]}\n\n"
            
            await event.edit(text, buttons=keyboard)
    
    elif data == "new_account":
        await event.edit("⏳ **جاري إنشاء حساب جديد...**")
        account, message = await create_aimusicgen_account(user_id)
        await event.edit(message, buttons=keyboard)
    
    elif data == "back_to_menu":
        clear_user_session(user_id)
        await event.edit(menu_text, buttons=keyboard)

async def message_handler(event):
    """معالجة الرسائل النصية"""
    user_id = event.sender_id
    session = get_user_session(user_id)
    text = event.text
    
    if text.startswith('/cancel'):
        clear_user_session(user_id)
        await event.respond("✅ **تم الإلغاء.**", buttons=keyboard)
        return
    
    if session.state == 'waiting_desc':
        # توليد كلمات آلياً
        await event.respond("🤖 **جاري توليد الكلمات...**")
        
        # الحصول على حساب
        account_data = await get_or_create_account(user_id)
        if not account_data:
            await event.respond("❌ **فشل في الحصول على حساب.**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # توليد الكلمات
        lyrics_data = generate_lyrics(text, account_data['uid'])
        if not lyrics_data:
            await event.respond("❌ **فشل في توليد الكلمات.**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # حفظ البيانات
        session.lyrics = lyrics_data['lyrics']
        session.title = lyrics_data['title']
        session.styles = lyrics_data['tags']
        session.state = 'confirm_song'
        
        # عرض المعاينة
        preview = lyrics_data['lyrics'][:300] + "..." if len(lyrics_data['lyrics']) > 300 else lyrics_data['lyrics']
        
        confirm_keyboard = [
            [Button.inline("✅ إنشاء الأغنية", data="confirm_create")],
            [Button.inline("🔄 وصف آخر", data="create_song")],
            [Button.inline("🔙 رجوع", data="back_to_menu")]
        ]
        
        await event.respond(
            f"🎵 **{lyrics_data['title']}**\n"
            f"🏷️ **الأنماط:** {lyrics_data['tags']}\n\n"
            f"📝 **المعاينة:**\n{preview}\n\n"
            f"**اختر الإجراء التالي:**",
            buttons=confirm_keyboard
        )
    
    elif session.state == 'waiting_lyrics':
        # كلمات يدوية
        session.lyrics = text
        session.state = 'waiting_title'
        await event.respond(
            "📝 **أرسل عنوان الأغنية:**\n\n"
            "أو ارسل /cancel للإلغاء"
        )
    
    elif session.state == 'waiting_title':
        session.title = text
        session.styles = "Arabic, Pop, Male Vocal"
        session.state = 'confirm_song'
        
        confirm_keyboard = [
            [Button.inline("✅ إنشاء الأغنية", data="confirm_create")],
            [Button.inline("✏️ تعديل الكلمات", data="manual_lyrics")],
            [Button.inline("🔙 رجوع", data="back_to_menu")]
        ]
        
        await event.respond(
            f"✅ **تم حفظ العنوان:** {text}\n\n"
            f"**الآن يمكنك إنشاء الأغنية:**",
            buttons=confirm_keyboard
        )

async def confirm_create_handler(event):
    """معالجة إنشاء الأغنية"""
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if not all([session.lyrics, session.title, session.styles]):
        await event.respond("❌ **بيانات غير مكتملة.**", buttons=keyboard)
        clear_user_session(user_id)
        return
    
    await event.edit("🎵 **جاري إنشاء الأغنية...**")
    
    # الحصول على حساب
    account_data = await get_or_create_account(user_id)
    if not account_data:
        await event.respond("❌ **فشل في الحصول على حساب.**", buttons=keyboard)
        clear_user_session(user_id)
        return
    
    # إنشاء الأغنية
    song_result = create_song(
        account_data['session'],
        session.lyrics,
        session.title,
        session.styles,
        account_data['uid'],
        account_data['email']
    )
    
    if not song_result or not song_result.get('success'):
        await event.edit("❌ **فشل في إنشاء الأغنية.**", buttons=keyboard)
        clear_user_session(user_id)
        return
    
    # الحصول على معرفات الأغاني
    music_ids = [song['music_id'] for song in song_result['data']]
    
    await event.edit(f"✅ **تم إنشاء الأغنية!**\n\n🎯 جاري معالجة {len(music_ids)} نسخة...")
    
    # انتظار اكتمال المعالجة
    completed_songs = wait_for_completion(account_data['session'], music_ids, max_wait=180)
    
    if completed_songs:
        for song in completed_songs:
            audio_url = song.get('audio')
            if audio_url and audio_url.strip():
                # تحميل الأغنية
                song_name = f"{song.get('title', 'أغنية')}_{song['music_id'][:8]}"
                file_path = download_song(audio_url, song_name)
                
                if file_path:
                    # إرسال الأغنية
                    await event.respond(
                        f"🎵 **{song.get('title', 'أغنية')}**\n"
                        f"📧 الحساب: {account_data['email']}",
                        file=file_path
                    )
                    
                    # حذف الملف المؤقت
                    try:
                        os.remove(file_path)
                    except:
                        pass
        
        await event.respond(f"🎉 **اكتملت العملية!**\nتم معالجة {len(completed_songs)} أغنية.", buttons=keyboard)
    else:
        await event.respond("❌ **لم تكتمل أي أغنية.**", buttons=keyboard)
    
    clear_user_session(user_id)

# ========== تسجيل المعالجين ==========
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.NewMessage(pattern="/MusAi", func=lambda e: e.is_private))
    async def start_handler(event):
        await start_command(event)
    
    @tgbot.on(events.CallbackQuery())
    async def callback_processor(event):
        data = event.data.decode('utf-8')
        
        if data == "confirm_create":
            await confirm_create_handler(event)
        else:
            await callback_handler(event)
    
    @tgbot.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/')))
    async def message_processor(event):
        await message_handler(event)
    
    @tgbot.on(events.NewMessage(pattern="/cancell", func=lambda e: e.is_private))
    async def cancel_handler(event):
        user_id = event.sender_id
        clear_user_session(user_id)
        await event.respond("✅ **تم الإلغاء والعودة للقائمة.**", buttons=keyboard)

print("🎵 تم تحميل بوت AIMusicGen بنجاح!")
