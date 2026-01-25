
from JoKeRUB import bot, l313l
#By Source joker @ucriss
from telethon import events, functions, types, Button
from datetime import timedelta
from JoKeRUB.utils import admin_cmd
import asyncio
from ..Config import Config
import os, asyncio, re, traceback
from os import system
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon;from telethon import functions
from telethon.tl.types import ChannelParticipantsAdmins as cpa

from telethon.tl.functions.channels import CreateChannelRequest as ccr

from JoKeRUB import bot, l313l
from telethon import Button, events
from datetime import datetime
from JoKeRUB.utils import admin_cmd
from ..Config import Config
import asyncio, aiohttp, random, json, requests, re, time, os
import logging
import uuid
logging.getLogger().setLevel(logging.WARNING)

# إعدادات الملفات
accounts_file = "accounts/accounts_data.json"
os.makedirs("accounts", exist_ok=True)
os.makedirs("generated_images", exist_ok=True)
os.makedirs("temp_images", exist_ok=True)

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "NanoBananaBot"

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
    accounts = load_accounts()
    return [acc for acc in accounts if acc.get('user_id') == user_id]

def delete_user_accounts(user_id):
    """حذف جميع حسابات مستخدم معين"""
    accounts = load_accounts()
    user_accs_before = len(get_user_accounts(user_id))
    
    # الاحتفاظ بحسابات المستخدمين الآخرين فقط
    remaining_accounts = [acc for acc in accounts if acc.get('user_id') != user_id]
    
    save_accounts(remaining_accounts)
    return user_accs_before

def delete_expired_accounts(user_id=None):
    """حذف الحسابات المنتهية (5/5)"""
    accounts = load_accounts()
    deleted_count = 0
    
    remaining_accounts = []
    for acc in accounts:
        if user_id and acc.get('user_id') != user_id:
            remaining_accounts.append(acc)
            continue
            
        if acc.get('use_count', 0) >= 5:
            deleted_count += 1
            continue  # تخطي الحساب المنتهي (حذفه)
        else:
            remaining_accounts.append(acc)
    
    save_accounts(remaining_accounts)
    return deleted_count

# ========== دوال إنشاء البريد باستخدام temp-mail.io ==========
async def create_temp_mail():
    """إنشاء بريد مؤقت باستخدام temp-mail.io"""
    try:
        # إنشاء عنوان بريد إلكتروني عشوائي
        random_name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(10))
        domains = ["1secmail.com", "1secmail.org", "1secmail.net"]
        domain = random.choice(domains)
        
        email = f"{random_name}@{domain}"
        
        return email, email  # نعيد الإيميل مرتين لأن temp-mail لا يحتاج كلمة مرور
        
    except Exception as e:
        print(f"Error creating temp mail: {e}")
        return None, None

async def get_messages_from_temp_mail(email):
    """الحصول على الرسائل من temp-mail.io"""
    try:
        # تقسيم الإيميل إلى اسم و دومين
        username, domain = email.split('@')
        
        # رابط API للحصول على الرسائل
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    messages = await response.json()
                    return messages
                else:
                    return []
                    
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []

async def get_message_content(email, message_id):
    """الحصول على محتوى رسالة محددة"""
    try:
        username, domain = email.split('@')
        
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    message_data = await response.json()
                    return message_data
                else:
                    return None
                    
    except Exception as e:
        print(f"Error getting message content: {e}")
        return None

async def wait_for_verification_code_temp_mail(email, timeout=300):
    """انتظار كود التحقق من temp-mail.io"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            messages = await get_messages_from_temp_mail(email)
            
            for message in messages:
                # تحميل محتوى الرسالة
                message_data = await get_message_content(email, message['id'])
                
                if message_data:
                    # البحث في محتوى الرسالة
                    text_content = message_data.get('textBody', '') or message_data.get('htmlBody', '')
                    
                    # البحث عن كود التحقق (6 أرقام)
                    matches = re.findall(r'\b\d{6}\b', text_content)
                    if matches:
                        return matches[0]
                    
                    # أو البحث عن أنماط أخرى للكود
                    matches = re.findall(r'code[:\s]*(\d{6})', text_content, re.IGNORECASE)
                    if matches:
                        return matches[0]
                        
                    matches = re.findall(r'verification[:\s]*(\d{6})', text_content, re.IGNORECASE)
                    if matches:
                        return matches[0]
            
            await asyncio.sleep(10)  # انتظار 10 ثواني قبل المحاولة مجدداً
            
        except Exception as e:
            print(f"Error waiting for verification code: {e}")
            await asyncio.sleep(10)
    
    return None

# ========== دوال NanoBanana ==========
async def create_nanabanana_account():
    email, _ = await create_temp_mail()
    
    if not email:
        return None, None, None
    
    nana_headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    # الحصول على CSRF token
    csrf_response = requests.get("https://nanabanana.ai/api/auth/csrf", headers=nana_headers)
    csrf_token = None
    csrf_cookie = None
    
    if csrf_response.text:
        try:
            csrf_data = json.loads(csrf_response.text)
            csrf_token = csrf_data.get("csrfToken")
        except:
            pass
    
    if '__Host-authjs.csrf-token' in csrf_response.cookies:
        csrf_cookie = csrf_response.cookies.get('__Host-authjs.csrf-token')
    
    cookies_dict = csrf_response.cookies.get_dict()
    
    # إعداد رؤوس طلب التحقق
    verification_headers = {**nana_headers, 'Content-Type': "application/json", 'origin': "https://nanabanana.ai", 'referer': "https://nanabanana.ai/ar/ai-image"}
    
    # إضافة الكوكيز
    cookie_str = f"__Host-authjs.csrf-token={csrf_cookie}"
    for key, value in cookies_dict.items():
        if key != '__Host-authjs.csrf-token':
            cookie_str += f"; {key}={value}"
    
    verification_headers['Cookie'] = cookie_str
    
    # إرسال طلب التحقق
    verification_payload = {"email": email}
    verification_response = requests.post(
        "https://nanabanana.ai/api/auth/email-verification", 
        data=json.dumps(verification_payload), 
        headers=verification_headers
    )
    
    print(f"Email verification response: {verification_response.status_code}")
    
    # انتظار كود التحقق
    code = await wait_for_verification_code_temp_mail(email)
    
    if not code:
        print("No verification code received")
        return None, None, None
    
    print(f"Received verification code: {code}")
    
    # إتمام التسجيل
    callback_headers = {
        **nana_headers, 
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-auth-return-redirect': "1", 
        'origin': "https://nanabanana.ai", 
        'referer': "https://nanabanana.ai/ar/ai-image",
        'Cookie': cookie_str
    }
    
    callback_payload = {
        'email': email, 
        'code': code, 
        'redirect': "false", 
        'csrfToken': csrf_token, 
        'callbackUrl': "https://nanabanana.ai/ar/ai-image"
    }
    
    final_response = requests.post(
        "https://nanabanana.ai/api/auth/callback/email-verification", 
        data=callback_payload, 
        headers=callback_headers
    )
    
    print(f"Final response status: {final_response.status_code}")
    
    # استخراج session token
    final_cookies = final_response.cookies.get_dict()
    session_token = None
    if '__Secure-authjs.session-token' in final_cookies:
        session_token = final_cookies['__Secure-authjs.session-token']
    
    if session_token:
        return email, "temp_mail_no_password", session_token
    else:
        print(f"No session token found. Cookies: {final_cookies}")
        return None, None, None

def upload_image(image_path):
    url = "https://nanabanana.ai/api/upload"
    try:
        if not os.path.exists(image_path):
            return None
        
        with open(image_path, 'rb') as f:
            file_content = f.read()
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'origin': "https://nanabanana.ai",
            'referer': "https://nanabanana.ai/ar/ai-image",
        }
        
        files = [('file', (os.path.basename(image_path), file_content, 'image/jpeg'))]
        response = requests.post(url, files=files, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("url")
        else:
            return None
    except:
        return None

def create_or_edit_image(session_token, prompt, image_urls=None):
    url = "https://nanabanana.ai/api/image-generation-nano-banana/create"
    payload = {
        "prompt": prompt,
        "output_format": "png",
        "image_size": "auto",
        "enable_pro": False,
        "width": 1024,
        "height": 1024,
        "steps": 20,
        "guidance_scale": 7.5,
        "is_public": False
    }
    
    if image_urls:
        payload["image_urls"] = image_urls
    
    cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'Cookie': cookie_string
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        task_id = data.get("task_id")
        return task_id
    else:
        return None

def check_status(task_id, session_token, max_attempts=40, delay=5):
    url = "https://nanabanana.ai/api/image-generation-nano-banana/status"
    cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'Cookie': cookie_string
    }
    
    for attempt in range(max_attempts):
        payload = {"taskId": task_id}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "generations" in data and len(data["generations"]) > 0:
                generation = data["generations"][0]
                status = generation.get("status", "unknown")
                if status == "succeed":
                    image_url = generation.get("url", "")
                    return image_url
                elif status == "failed":
                    return None
        time.sleep(delay)
    return None

def download_image(image_url, account_email):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            safe_email = account_email.replace("@", "_").replace(".", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/image_{safe_email}_{timestamp}.png"
            
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
        else:
            return None
    except:
        return None

async def get_or_create_account(user_id):
    """الحصول على حساب نشط أو إنشاء حساب جديد بشكل متزامن"""
    # أولاً: حذف الحسابات المنتهية تلقائياً
    deleted_expired = delete_expired_accounts(user_id)
    if deleted_expired > 0:
        print(f"تم حذف {deleted_expired} حساب منتهي تلقائياً للمستخدم {user_id}")
    
    accounts = load_accounts()
    user_accs = get_user_accounts(user_id)
    
    # البحث عن حساب نشط (أقل من 5 استخدامات)
    for acc in user_accs:
        if acc.get('use_count', 0) < 5:
            return acc
    
    # إذا لم يوجد حساب نشط، إنشاء حساب جديد
    try:
        email, password, session_token = await create_nanabanana_account()
        if session_token:
            new_account = {
                'user_id': user_id,
                'email': email,
                'password': password,
                'session_token': session_token,
                'use_count': 0,
                'created_at': datetime.now().isoformat()
            }
            accounts.append(new_account)
            save_accounts(accounts)
            return new_account
    except Exception as e:
        print(f"خطأ في إنشاء حساب جديد: {e}")
    
    return None

# ========== دوال مساعدة ==========
async def safe_edit(event, text, buttons=None):
    """تعديل الرسالة بأمان مع منع الأخطاء"""
    try:
        if buttons:
            await event.edit(text, buttons=buttons)
        else:
            await event.edit(text)
    except Exception as e:
        # إذا كانت الرسالة نفسها، أرسل رسالة جديدة
        try:
            if buttons:
                await event.respond(text, buttons=buttons)
            else:
                await event.respond(text)
        except:
            pass

# ========== القائمة والأزرار ==========
menu = '''
🎨 **بوت إنشاء وتعديل الصور باستخدام الذكاء الاصطناعي**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("‹ : إنشاء صورة جديدة 🎚 : ›", data="create_image"), 
        Button.inline("‹ :🪞 تعديل صوره : ›", data="edit_image"),
    ],
    [
        Button.inline("‹ : حـسـابـاتــي 📜 : ›", data="my_accounts"),
        Button.inline("‹ :🎐 انشاء حساب : ›", data="new_account"),
    ],
    [
        Button.url("المـطور", "https://t.me/Lx5x5")
    ]
]

# ========== تخزين الحالات الجارية ==========
user_sessions = {}  # تخزين العمليات الجارية

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None  # 'waiting_prompt', 'waiting_photo'
        self.prompt = None
        self.photo_path = None

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]

# ========== الإنلاين ==========
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        
        if query.startswith("صور") and event.query.user_id == bot.uid:
            buttons = Button.url(" اضغط هنا ", f"https://t.me/{joker}?start=edit")
            result = builder.article(
                title="🎨 بوت تعديل الصور",
                description="اضغط للدخول إلى بوت تعديل الصور",
                text="**🎨 قم بالضغط على الزر لبدء استخدام بوت تعديل الصور**",
                buttons=buttons
            )
        await event.answer([result] if result else None)

# الأمر .تعديل_الصور
@bot.on(admin_cmd(outgoing=True, pattern="صور"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "صور")
    await response[0].click(event.chat_id)
    await event.delete()

# ========== الأمر الرئيسي ==========
@tgbot.on(events.NewMessage(pattern="/edit", func=lambda x: x.is_private))
async def start(event):
    if event.sender_id == bot.uid:
        await safe_edit(event, menu, buttons=keyboard)
     
# ========== أمر /cancel ==========
@tgbot.on(events.NewMessage(pattern="/cancel", func=lambda x: x.is_private))
async def cancel_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state:  # إذا كان هناك عملية جارية
        # تنظيف أي ملفات مؤقتة
        if session.photo_path and os.path.exists(session.photo_path):
            try:
                os.remove(session.photo_path)
            except:
                pass
        
        # مسح الجلسة
        clear_user_session(user_id)
        
        await event.respond("**✅ تم إلغاء العملية والعودة للقائمة الرئيسية**", buttons=keyboard)
    else:
        await event.respond("**⚠️ لا توجد عملية جارية للإلغاء**", buttons=keyboard)

# ========== زر العودة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"back_to_menu")))
async def back_to_menu_handler(event):
    user_id = event.sender_id
    clear_user_session(user_id)
    await safe_edit(event, menu, buttons=keyboard)

# ========== زر إنشاء صورة جديدة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"create_image")))
async def create_image_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_prompt'
    
    # زر المطور فقط
    developer_button = [
        [Button.url("المـطور", "https://t.me/Lx5x5")]
    ]
    
    await safe_edit(
        event,
        "**✍️ أرسل وصف الصورة التي تريد إنشاءها:**\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية",
        buttons=developer_button
    )

# ========== معالجة الرسائل للإنشاء ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid))
async def handle_prompt_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    # تجاهل الأوامر
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt':
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        session.prompt = prompt
        
        # عرض رسالة الانتظار
        await event.respond("**⏳ جاري إنشاء الصورة...**")
        
        account = await get_or_create_account(user_id)
        if not account:
            await event.respond("**❌ فشل في إنشاء أو استرجاع الحساب**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # تحديث الاستخدامات
        accounts = load_accounts()
        for acc in accounts:
            if acc.get('session_token') == account['session_token']:
                acc['use_count'] = acc.get('use_count', 0) + 1
                save_accounts(accounts)
                break
        
        task_id = create_or_edit_image(account['session_token'], prompt)
        if task_id:
            await event.respond(f"**✅ تم بدء إنشاء الصورة\n📝 رقم المهمة: {task_id}**")
            
            image_url = check_status(task_id, account['session_token'])
            if image_url:
                filename = download_image(image_url, account['email'])
                if filename:
                    await bot.send_file(event.chat_id, filename, caption=f"**✅ تم إنشاء الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                    os.remove(filename)
                else:
                    await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
            else:
                await event.respond("**❌ فشل في إنشاء الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في بدء العملية**", buttons=keyboard)
        
        clear_user_session(user_id)

# ========== زر تعديل صورة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"edit_image")))
async def edit_image_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_photo'
    
    # زر المطور فقط
    developer_button = [
        [Button.url("المـطور", "https://t.me/Lx5x5")]
    ]
    
    await safe_edit(
        event,
        "**📤 أرسل الصورة التي تريد تعديلها:**\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية",
        buttons=developer_button
    )

# ========== معالجة الصور للتعديل ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.media))
async def handle_photo_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photo':
        # حفظ الصورة
        photo_path = await event.download_media(file="temp_images/")
        session.photo_path = photo_path
        
        # طلب وصف التعديل
        session.state = 'waiting_prompt_edit'
        
        await event.respond("**✍️ أرسل وصف التعديل المطلوب:**\n\n"
                           "يمكنك إرسال `/cancel` لإلغاء العملية")

@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and not x.media))
async def handle_edit_prompt_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt_edit' and session.photo_path:
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            if os.path.exists(session.photo_path):
                try:
                    os.remove(session.photo_path)
                except:
                    pass
            clear_user_session(user_id)
            return
        
        await event.respond("**⏳ جاري معالجة الصورة...**")
        
        account = await get_or_create_account(user_id)
        if not account:
            await event.respond("**❌ فشل في إنشاء أو استرجاع الحساب**", buttons=keyboard)
            if os.path.exists(session.photo_path):
                try:
                    os.remove(session.photo_path)
                except:
                    pass
            clear_user_session(user_id)
            return
        
        # رفع الصورة
        uploaded_url = upload_image(session.photo_path)
        
        # تنظيف الملف المؤقت
        if os.path.exists(session.photo_path):
            try:
                os.remove(session.photo_path)
            except:
                pass
        
        if not uploaded_url:
            await event.respond("**❌ فشل في رفع الصورة**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # إنشاء الصورة المعدلة
        task_id = create_or_edit_image(account['session_token'], prompt, [uploaded_url])
        
        if task_id:
            # تحديث عدد الاستخدامات
            accounts = load_accounts()
            for acc in accounts:
                if acc.get('session_token') == account['session_token']:
                    acc['use_count'] = acc.get('use_count', 0) + 1
                    save_accounts(accounts)
                    break
            
            await event.respond(f"**✅ تم بدء تعديل الصورة\n📝 رقم المهمة: {task_id}**")
            
            image_url = check_status(task_id, account['session_token'])
            if image_url:
                filename = download_image(image_url, account['email'])
                if filename:
                    await bot.send_file(event.chat_id, filename, caption=f"**✅ تم تعديل الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                    os.remove(filename)
                else:
                    await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
            else:
                await event.respond("**❌ فشل في تعديل الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في بدء العملية**", buttons=keyboard)
        
        clear_user_session(user_id)

# ========== حساباتي ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"my_accounts")))
async def my_accounts_handler(event):
    try:
        # حذف الحسابات المنتهية أولاً
        deleted_count = delete_expired_accounts(event.sender_id)
        
        accounts = get_user_accounts(event.sender_id)
        
        if not accounts:
            response = "**📭 لا توجد حسابات مرفوعة بعد.**"
            await event.respond(response, buttons=keyboard)
            return
        
        response = "**📋 حساباتك:**\n\n"
        
        for i, acc in enumerate(accounts, 1):
            use_count = acc.get('use_count', 0)
            email = acc['email']
            created_date = acc.get('created_at', 'غير معروف')[:10]
            
            response += f"**{i}. {email}**\n"
            response += f"   استخدامات: {use_count}/5\n"
            response += f"   تاريخ: {created_date}\n"
            
            if use_count >= 5:
                response += "   ⚠️ **الحساب منتهي**\n"
            else:
                response += "   ✅ **الحساب نشط**\n"
            
            response += "\n"
        
        if deleted_count > 0:
            response += f"\n🗑️ **تم حذف {deleted_count} حساب منتهي تلقائياً**\n"
        
        # إضافة زر حذف جميع الحسابات
        delete_buttons = [
            [Button.inline("🗑️ حذف جميع الحسابات", data="delete_all_accounts")],
            [Button.inline("🔙 رجوع", data="back_to_menu")]
        ]
        
        await safe_edit(event, response, buttons=delete_buttons)
        
    except Exception as e:
        error_msg = f"**❌ حدث خطأ في عرض الحسابات:**\n```{str(e)}```"
        await event.respond(error_msg, buttons=keyboard)

@tgbot.on(events.CallbackQuery(data=re.compile(b"delete_all_accounts")))
async def delete_all_accounts_handler(event):
    try:
        # تأكيد الحذف
        confirm_buttons = [
            [Button.inline("✅ نعم، احذف الكل", data="confirm_delete_all")],
            [Button.inline("❌ لا، إلغاء", data="my_accounts")]
        ]
        
        await safe_edit(
            event,
            "**⚠️ هل أنت متأكد من حذف جميع حساباتك؟**\n"
            "❌ هذه العملية لا يمكن التراجع عنها!\n"
            "🗑️ سيتم حذف جميع الحسابات نهائياً.",
            buttons=confirm_buttons
        )
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)

@tgbot.on(events.CallbackQuery(data=re.compile(b"confirm_delete_all")))
async def confirm_delete_all_handler(event):
    try:
        deleted_count = delete_user_accounts(event.sender_id)
        
        await safe_edit(
            event,
            f"**✅ تم حذف {deleted_count} حساب بنجاح!**\n"
            f"🗑️ تم مسح جميع حساباتك من قاعدة البيانات.",
            buttons=keyboard
        )
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)

# ========== انشاء حساب ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"new_account")))
async def new_account_handler(event):
    try:
        await safe_edit(event, "**⏳ جاري إنشاء حساب جديد...**")
        
        email, password, session_token = await create_nanabanana_account()
        if session_token:
            accounts = load_accounts()
            new_account = {
                'user_id': event.sender_id,
                'email': email,
                'password': password,
                'session_token': session_token,
                'use_count': 0,
                'created_at': datetime.now().isoformat()
            }
            accounts.append(new_account)
            save_accounts(accounts)
            
            await safe_edit(
                event,
                f"**✅ تم إنشاء حساب جديد!**\n\n"
                f"📧 `{email}`\n"
                f"🔑 `{password}`\n\n"
                f"**تم الحفظ تلقائياً.**",
                buttons=keyboard
            )
        else:
            await safe_edit(event, "**❌ فشل في إنشاء الحساب**", buttons=keyboard)
            
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)

print("✅ تم تحميل بوت تعديل الصور بنجاح مع استخدام temp-mail.io!")
