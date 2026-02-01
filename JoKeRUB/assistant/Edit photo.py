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
logging.getLogger().setLevel(logging.WARNING)

# إعدادات الملفات
accounts_file = "accounts/accounts_data.json"
os.makedirs("accounts", exist_ok=True)
os.makedirs("generated_images", exist_ok=True)
os.makedirs("temp_images", exist_ok=True)

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "NanoBananaBot"

# ========== دوال البريد المؤقت (temp-mail.io) ==========
class TempMail:
    def __init__(self):
        self.base_url = "https://api.internal.temp-mail.io/api/v3"
        self.headers = {'Content-Type': 'application/json', 'x-cors-header': 'iaWg3pchvFx48fY'}
    
    def create_email(self):
        """إنشاء بريد إلكتروني جديد"""
        payload = {"min_name_length": 10, "max_name_length": 10}
        try:
            response = requests.post(f"{self.base_url}/email/new", 
                                    json=payload, 
                                    headers=self.headers, 
                                    timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('email')
        except Exception as e:
            print(f"Error creating email: {e}")
        return None
    
    def get_messages(self, email):
        """الحصول على الرسائل الواردة"""
        try:
            url = f"{self.base_url}/email/{email}/messages"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting messages: {e}")
        return []
    
    def wait_for_verification_code(self, email, timeout=300):
        """انتظار كود التحقق من nanabanana"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.get_messages(email)
            
            for message in messages:
                body_text = message.get('body_text', '')
                body_html = message.get('body_html', '')
                
                # البحث في نص الرسالة
                text_content = body_text + body_html
                
                # البحث عن كود 6 أرقام
                matches = re.findall(r'\b\d{6}\b', text_content)
                if matches:
                    return matches[0]
                
                # أو البحث عن رابط التحقق
                links = re.findall(r'https://nanabanana\.ai/api/auth/callback/email\?[^\s"\']+', text_content)
                if links:
                    # استخراج الكود من الرابط
                    match = re.search(r'code=(\d{6})', links[0])
                    if match:
                        return match.group(1)
            
            time.sleep(5)  # انتظار 5 ثواني بين المحاولات
        
        return None

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
            continue
        else:
            remaining_accounts.append(acc)
    
    save_accounts(remaining_accounts)
    return deleted_count

# ========== دوال NanoBanana (محدثة) ==========
# ========== دوال NanoBanana (محسّن مع إصلاح الأخطاء) ==========
class NanoBananaAPI:
    def __init__(self):
        self.base_url = "https://nanabanana.ai"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            'accept': "application/json, text/plain, */*",
            'accept-encoding': "gzip, deflate, br",
            'origin': self.base_url,
            'referer': f"{self.base_url}/ar/ai-image",
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        })
        self.csrf_token = None
        self.csrf_cookie = None
    
    def get_csrf_token(self):
        """الحصول على CSRF token"""
        try:
            print(f"🔍 جاري جلب CSRF من: {self.base_url}/api/auth/csrf")
            response = self.session.get(f"{self.base_url}/api/auth/csrf", timeout=10)
            print(f"📊 استجابة CSRF: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)
                    self.csrf_token = data.get("csrfToken")
                    print(f"✅ تم الحصول على CSRF Token: {self.csrf_token[:30]}..." if self.csrf_token else "❌ لم يتم الحصول على CSRF Token")
                except Exception as e:
                    print(f"❌ خطأ في تحليل JSON: {e}")
                    print(f"📝 النص المستلم: {response.text[:200]}")
            
            # البحث عن الكوكيز
            print(f"🔍 جاري البحث عن CSRF Cookie...")
            cookies_found = []
            for cookie in response.cookies:
                cookies_found.append(f"{cookie.name}={cookie.value[:30]}...")
            
            if cookies_found:
                print(f"🍪 الكوكيز الموجودة: {', '.join(cookies_found)}")
            
            csrf_cookie_names = ['__Host-authjs.csrf-token', 'csrf-token', 'X-CSRF-Token', 'csrf_token']
            for cookie_name in csrf_cookie_names:
                if cookie_name in response.cookies:
                    self.csrf_cookie = response.cookies.get(cookie_name)
                    print(f"✅ وجدت CSRF Cookie: {cookie_name} = {self.csrf_cookie[:30]}...")
                    break
            
            return self.csrf_token is not None
        except Exception as e:
            print(f"❌ خطأ في جلب CSRF: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def send_verification_request(self, email):
        """إرسال طلب التحقق بالبريد"""
        url = f"{self.base_url}/api/auth/email-verification"
        print(f"🚀 إرسال طلب تحقق إلى: {url}")
        print(f"📧 البريد المستخدم: {email}")
        
        headers = {
            'Content-Type': "application/json",
            'origin': self.base_url,
            'referer': f"{self.base_url}/ar/ai-image",
            'accept': "application/json, text/plain, */*",
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }
        
        # إضافة الكوكيز إذا وجدت
        if self.csrf_cookie:
            cookie_header = f"__Host-authjs.csrf-token={self.csrf_cookie}"
            print(f"🍪 إضافة CSRF Cookie: {self.csrf_cookie[:30]}...")
            headers['Cookie'] = cookie_header
        
        payload = {"email": email}
        print(f"📦 Payload: {json.dumps(payload)}")
        
        try:
            response = self.session.post(url, 
                                        json=payload, 
                                        headers=headers, 
                                        timeout=15)
            
            print(f"📊 استجابة التحقق: {response.status_code}")
            print(f"📝 نص الاستجابة: {response.text[:200]}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ طلب التحقق ناجح: {data}")
                    return True
                except:
                    print(f"⚠️ استجابة بدون JSON: {response.text[:100]}")
                    return True
            else:
                print(f"❌ فشل طلب التحقق: {response.status_code}")
                print(f"📝 نص الخطأ: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في إرسال طلب التحقق: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_account(self, email, code):
        """التحقق من الحساب باستخدام الكود"""
        url = f"{self.base_url}/api/auth/callback/email-verification"
        print(f"🔐 جاري التحقق من الحساب: {email}")
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': self.base_url,
            'referer': f"{self.base_url}/ar/ai-image",
            'accept': "*/*",
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }
        
        # إضافة الكوكيز
        if self.csrf_cookie:
            headers['Cookie'] = f"__Host-authjs.csrf-token={self.csrf_cookie}"
            print(f"🍪 استخدام CSRF Cookie للتحقق")
        
        payload = {
            'email': email,
            'code': str(code),
            'redirect': "false",
            'csrfToken': self.csrf_token,
            'callbackUrl': f"{self.base_url}/ar/ai-image"
        }
        
        print(f"📦 Payload التحقق: {payload}")
        
        try:
            response = self.session.post(url, 
                                        data=payload, 
                                        headers=headers, 
                                        timeout=15,
                                        allow_redirects=True)
            
            print(f"📊 استجابة التحقق: {response.status_code}")
            
            # طباعة الكوكيز المستلمة
            if response.cookies:
                print(f"🍪 الكوكيز المستلمة:")
                for cookie in response.cookies:
                    print(f"  - {cookie.name}: {cookie.value[:50]}...")
            
            # البحث عن session token في الكوكيز
            session_cookie_names = ['__Secure-authjs.session-token', 'session-token', 'auth_token', 'token']
            session_token = None
            
            for cookie_name in session_cookie_names:
                if cookie_name in response.cookies:
                    session_token = response.cookies.get(cookie_name)
                    print(f"✅ وجدت Session Token: {cookie_name} = {session_token[:50]}...")
                    break
            
            if not session_token:
                print(f"❌ لم يتم العثور على Session Token في الكوكيز")
                print(f"🔍 البحث في نص الاستجابة...")
                if response.text:
                    print(f"📝 نص الاستجابة: {response.text[:500]}")
            
            return session_token
            
        except Exception as e:
            print(f"❌ خطأ في التحقق: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_session_info(self):
        """الحصول على معلومات الجلسة"""
        try:
            headers = {
                'content-type': "application/json",
                'referer': "https://nanabanana.ai/",
            }
            response = self.session.get(f"{self.base_url}/api/auth/session", 
                                       headers=headers, 
                                       timeout=10)
            if response.status_code == 200:
                try:
                    data = json.loads(response.text)
                    if data and 'user' in data:
                        return data['user'].get('id'), data['user'].get('email')
                except:
                    pass
        except:
            pass
        return None, None
    
    def upload_image(self, image_path):
        """رفع صورة إلى السيرفر"""
        url = f"{self.base_url}/api/upload"
        try:
            if not os.path.exists(image_path):
                return None
            
            with open(image_path, 'rb') as f:
                file_content = f.read()
            
            files = [('file', (os.path.basename(image_path), file_content, 'image/jpeg'))]
            response = self.session.post(url, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("url")
        except Exception as e:
            print(f"Error uploading image: {e}")
        return None
    
    def create_image(self, session_token, prompt, image_urls=None):
        """إنشاء صورة جديدة"""
        url = f"{self.base_url}/api/image-generation-nano-banana/create"
        
        cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'Content-Type': "application/json",
            'Cookie': cookie_string
        }
        
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
        
        try:
            response = requests.post(url, 
                                   data=json.dumps(payload), 
                                   headers=headers, 
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("task_id")
        except Exception as e:
            print(f"Error creating image: {e}")
        
        return None
    
    def check_status(self, task_id, session_token, max_attempts=40, delay=5):
        """التحقق من حالة الصورة"""
        url = f"{self.base_url}/api/image-generation-nano-banana/status"
        
        cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'Content-Type': "application/json",
            'Cookie': cookie_string
        }
        
        for attempt in range(max_attempts):
            try:
                payload = {"taskId": task_id}
                response = requests.post(url, 
                                       data=json.dumps(payload), 
                                       headers=headers, 
                                       timeout=30)
                
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
            except Exception as e:
                print(f"Error checking status (attempt {attempt+1}): {e}")
            
            time.sleep(delay)
        
        return None

# ========== دوال مساعدة ==========
async def create_nanabanana_account():
    """إنشاء حساب جديد في nanabanana"""
    print("\n" + "="*50)
    print("🚀 بدء عملية إنشاء حساب جديد")
    print("="*50)
    
    # إنشاء بريد مؤقت
    temp_mail = TempMail()
    email = temp_mail.create_email()
    
    if not email:
        print("❌ فشل في إنشاء البريد المؤقت")
        return None, None, None
    
    print(f"✅ تم إنشاء البريد: {email}")
    
    # إعداد API
    api = NanoBananaAPI()
    
    # الحصول على CSRF token
    print("\n🔧 جاري الحصول على CSRF Token...")
    if not api.get_csrf_token():
        print("❌ فشل في الحصول على CSRF Token")
        return None, None, None
    
    # إرسال طلب التحقق
    print("\n📨 جاري إرسال طلب التحقق...")
    if not api.send_verification_request(email):
        print("❌ فشل في إرسال طلب التحقق")
        return None, None, None
    
    print(f"✅ تم إرسال طلب التحقق إلى: {email}")
    
    # انتظار كود التحقق
    print("\n⏳ جاري انتظار كود التحقق...")
    code = temp_mail.wait_for_verification_code(email)
    
    if not code:
        print("❌ لم يتم استلام كود التحقق")
        return None, None, None
    
    print(f"✅ تم استلام كود التحقق: {code}")
    
    # التحقق من الحساب
    print("\n🔐 جاري التحقق من الحساب...")
    session_token = api.verify_account(email, code)
    
    if not session_token:
        print("❌ فشل في التحقق من الحساب")
        return None, None, None
    
    print(f"✅ تم التحقق من الحساب بنجاح!")
    print(f"🔑 Session Token: {session_token[:50]}...")
    
    # الحصول على معلومات المستخدم (اختياري)
    try:
        user_id, user_email = api.get_session_info()
        if user_id:
            print(f"👤 معلومات المستخدم: ID={user_id}, Email={user_email}")
    except:
        print("⚠️ لم يتم الحصول على معلومات المستخدم (قد يكون هذا طبيعياً)")
    
    print("="*50)
    print("✅ اكتملت عملية إنشاء الحساب!")
    print("="*50 + "\n")
    
    return email, "temp_mail_no_password", session_token

def test_connection():
    """اختبار الاتصال بموقع nanabanana.ai"""
    print("\n" + "="*50)
    print("🔧 اختبار الاتصال ب nanabanana.ai")
    print("="*50)
    
    try:
        # اختبار الوصول إلى الموقع
        response = requests.get("https://nanabanana.ai", timeout=10)
        print(f"🌐 اختبار الموقع الرئيسي: {response.status_code}")
        
        # اختبار API
        response = requests.get("https://nanabanana.ai/api/auth/csrf", timeout=10)
        print(f"🔧 اختبار API CSRF: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ الاتصال يعمل بشكل صحيح")
        else:
            print(f"❌ مشكلة في الاتصال: {response.status_code}")
            print(f"📝 التفاصيل: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
    
    print("="*50)

# تشغيل اختبار الاتصال عند بدء التشغيل
test_connection()

def download_image(image_url, account_email):
    """تحميل الصورة"""
    try:
        response = requests.get(image_url, stream=True, timeout=30)
        if response.status_code == 200:
            safe_email = account_email.replace("@", "_").replace(".", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/image_{safe_email}_{timestamp}.png"
            
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

async def get_or_create_account(user_id):
    """الحصول على حساب نشط أو إنشاء حساب جديد"""
    # حذف الحسابات المنتهية أولاً
    deleted_expired = delete_expired_accounts(user_id)
    if deleted_expired > 0:
        print(f"تم حذف {deleted_expired} حساب منتهي للمستخدم {user_id}")
    
    accounts = get_user_accounts(user_id)
    
    # البحث عن حساب نشط
    for acc in accounts:
        if acc.get('use_count', 0) < 5:
            return acc
    
    # إنشاء حساب جديد
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
            
            # حفظ الحساب
            all_accounts = load_accounts()
            all_accounts.append(new_account)
            save_accounts(all_accounts)
            
            return new_account
    except Exception as e:
        print(f"Error creating account: {e}")
    
    return None

async def safe_edit(event, text, buttons=None):
    """تعديل الرسالة بأمان"""
    try:
        if buttons:
            await event.edit(text, buttons=buttons)
        else:
            await event.edit(text)
    except Exception as e:
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
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None
        self.prompt = None
        self.photo_path = None
        self.api = None

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
    
    if session.state:
        if session.photo_path and os.path.exists(session.photo_path):
            try:
                os.remove(session.photo_path)
            except:
                pass
        
        clear_user_session(user_id)
        await event.respond("**✅ تم إلغاء العملية**", buttons=keyboard)
    else:
        await event.respond("**⚠️ لا توجد عملية جارية**", buttons=keyboard)

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
    
    developer_button = [[Button.url("المـطور", "https://t.me/Lx5x5")]]
    
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
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt':
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        session.prompt = prompt
        
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
        
        # إنشاء الصورة
        api = NanoBananaAPI()
        task_id = api.create_image(account['session_token'], prompt)
        
        if task_id:
            await event.respond(f"**✅ تم بدء إنشاء الصورة\n📝 رقم المهمة: {task_id}**")
            
            # التحقق من الحالة
            image_url = api.check_status(task_id, account['session_token'])
            
            if image_url:
                filename = download_image(image_url, account['email'])
                if filename:
                    await bot.send_file(event.chat_id, filename, 
                                      caption=f"**✅ تم إنشاء الصورة بنجاح!\n📧 الحساب: {account['email']}**")
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
    
    developer_button = [[Button.url("المـطور", "https://t.me/Lx5x5")]]
    
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
        photo_path = await event.download_media(file="temp_images/")
        session.photo_path = photo_path
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
        api = NanoBananaAPI()
        uploaded_url = api.upload_image(session.photo_path)
        
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
        task_id = api.create_image(account['session_token'], prompt, [uploaded_url])
        
        if task_id:
            # تحديث الاستخدامات
            accounts = load_accounts()
            for acc in accounts:
                if acc.get('session_token') == account['session_token']:
                    acc['use_count'] = acc.get('use_count', 0) + 1
                    save_accounts(accounts)
                    break
            
            await event.respond(f"**✅ تم بدء تعديل الصورة\n📝 رقم المهمة: {task_id}**")
            
            image_url = api.check_status(task_id, account['session_token'])
            if image_url:
                filename = download_image(image_url, account['email'])
                if filename:
                    await bot.send_file(event.chat_id, filename, 
                                      caption=f"**✅ تم تعديل الصورة بنجاح!\n📧 الحساب: {account['email']}**")
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
        
        delete_buttons = [
            [Button.inline("🗑️ حذف جميع الحسابات", data="delete_all_accounts")],
            [Button.inline("🔙 رجوع", data="back_to_menu")]
        ]
        
        await safe_edit(event, response, buttons=delete_buttons)
        
    except Exception as e:
        error_msg = f"**❌ حدث خطأ:**\n```{str(e)}```"
        await event.respond(error_msg, buttons=keyboard)

@tgbot.on(events.CallbackQuery(data=re.compile(b"delete_all_accounts")))
async def delete_all_accounts_handler(event):
    confirm_buttons = [
        [Button.inline("✅ نعم، احذف الكل", data="confirm_delete_all")],
        [Button.inline("❌ لا، إلغاء", data="my_accounts")]
    ]
    
    await safe_edit(
        event,
        "**⚠️ هل أنت متأكد من حذف جميع حساباتك؟**\n"
        "❌ لا يمكن التراجع عن هذه العملية!",
        buttons=confirm_buttons
    )

@tgbot.on(events.CallbackQuery(data=re.compile(b"confirm_delete_all")))
async def confirm_delete_all_handler(event):
    try:
        deleted_count = delete_user_accounts(event.sender_id)
        await safe_edit(
            event,
            f"**✅ تم حذف {deleted_count} حساب بنجاح!**",
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

print("✅ تم تحميل بوت تعديل الصور بنجاح مع API محسن!")
