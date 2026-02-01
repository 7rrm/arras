
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

# ========== دوال البريد المؤقت ==========
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
        """انتظار كود التحقق"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.get_messages(email)
            
            for message in messages:
                body_text = message.get('body_text', '')
                body_html = message.get('body_html', '')
                
                text_content = body_text + body_html
                
                # البحث عن كود 6 أرقام
                matches = re.findall(r'\b\d{6}\b', text_content)
                if matches:
                    return matches[0]
                
                # البحث عن رابط التحقق
                links = re.findall(r'https://nanabanana\.ai/api/auth/callback/email\?[^\s"\']+', text_content)
                if links:
                    match = re.search(r'code=(\d{6})', links[0])
                    if match:
                        return match.group(1)
            
            time.sleep(5)
        
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
    accounts = load_accounts()
    user_accs_before = len(get_user_accounts(user_id))
    
    remaining_accounts = [acc for acc in accounts if acc.get('user_id') != user_id]
    save_accounts(remaining_accounts)
    return user_accs_before

def delete_expired_accounts(user_id=None):
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

# ========== نانو بانانا مع متصفح حقيقي ==========
class NanoBananaBrowser:
    """استخدام متصفح حقيقي لتجاوز Cloudflare"""
    
    def __init__(self):
        self.base_url = "https://nanabanana.ai"
        self.use_playwright = False
        
        # حاول استيراد Playwright
        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright
            self.use_playwright = True
            print("✅ Playwright جاهز للاستخدام")
        except ImportError:
            print("⚠️ Playwright غير مثبت، استخدم: pip install playwright")
            print("⚠️ ثم: playwright install chromium")
    
    def create_account_with_browser(self, email):
        """إنشاء حساب باستخدام متصفح حقيقي"""
        if not self.use_playwright:
            print("❌ Playwright غير مثبت")
            return None, None
        
        print(f"🌐 فتح متصفح لإنشاء حساب: {email}")
        
        try:
            with self.playwright() as p:
                # تشغيل متصفح Chrome (headless)
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    locale='ar-EG'
                )
                page = context.new_page()
                
                # 1. زيارة الموقع
                page.goto(f"{self.base_url}/ar/ai-image", wait_until='networkidle')
                time.sleep(2)
                
                # 2. النقر على تسجيل الدخول
                try:
                    page.click("text=تسجيل الدخول", timeout=5000)
                except:
                    # قد يكون الزر بلغة أخرى
                    page.click("text=Sign in", timeout=5000)
                
                time.sleep(2)
                
                # 3. اختيار البريد الإلكتروني
                try:
                    page.click("text=البريد الإلكتروني", timeout=5000)
                except:
                    page.click("text=Email", timeout=5000)
                
                time.sleep(1)
                
                # 4. إدخال البريد
                email_input = page.locator('input[type="email"]')
                email_input.fill(email)
                time.sleep(1)
                
                # 5. النقر على زر الإرسال
                submit_button = page.locator('button[type="submit"]')
                submit_button.click()
                
                # 6. انتظار إرسال البريد
                print(f"📨 انتظار إرسال البريد...")
                time.sleep(5)
                
                # 7. الحصول على حالة الصفحة
                page_content = page.content()
                
                # 8. التحقق من نجاح العملية
                if "تم إرسال" in page_content or "sent" in page_content.lower():
                    print("✅ تم إرسال طلب التحقق بنجاح")
                    
                    # 9. الحصول على الكوكيز
                    cookies = context.cookies()
                    session_token = None
                    
                    for cookie in cookies:
                        if 'session' in cookie['name'].lower() or 'authjs' in cookie['name'].lower():
                            session_token = cookie['value']
                            break
                    
                    # 10. إغلاق المتصفح
                    browser.close()
                    
                    return session_token
                
                else:
                    print(f"❌ لم يظهر تأكيد الإرسال")
                    print(f"📄 محتوى الصفحة: {page_content[:500]}")
                    browser.close()
                    return None
                    
        except Exception as e:
            print(f"❌ خطأ في المتصفح: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_account_manual(self, email):
        """إنشاء حساب باستخدام طريقة يدوية"""
        print(f"🔧 محاولة إنشاء حساب يدوياً: {email}")
        
        try:
            # جلسة requests تحاكي المتصفح
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'ar,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
            })
            
            # 1. زيارة الصفحة الرئيسية
            print("🌐 زيارة الصفحة الرئيسية...")
            response = session.get(f"{self.base_url}/ar/ai-image", timeout=10)
            
            # 2. استخراج CSRF token من HTML
            csrf_token = None
            csrf_patterns = [
                r'name="csrfToken" value="([^"]+)"',
                r'"csrfToken":"([^"]+)"',
                r'csrfToken["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in csrf_patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    csrf_token = matches[0]
                    print(f"✅ وجدت CSRF: {csrf_token[:50]}...")
                    break
            
            # 3. البحث عن رابط API
            api_url = f"{self.base_url}/api/auth/signin/email"
            
            # 4. إرسال طلب التسجيل
            print(f"📨 إرسال طلب تسجيل...")
            payload = {
                'email': email,
                'callbackUrl': f"{self.base_url}/ar/ai-image",
                'redirect': 'false',
                'csrfToken': csrf_token,
                'json': 'true'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': self.base_url,
                'Referer': f"{self.base_url}/ar/ai-image",
            }
            
            response = session.post(api_url, data=payload, headers=headers, timeout=15)
            
            print(f"📊 الاستجابة: {response.status_code}")
            print(f"📝 النص: {response.text[:200]}")
            
            if response.status_code in [200, 201]:
                print("✅ تم إرسال طلب التحقق")
                return "manual_session_token"
            else:
                print("❌ فشل إرسال الطلب")
                return None
                
        except Exception as e:
            print(f"❌ خطأ في الطريقة اليدوية: {e}")
            return None

# ========== دوال مساعدة ==========
async def create_nanabanana_account():
    """إنشاء حساب جديد باستخدام الطريقة المناسبة"""
    print("\n" + "="*60)
    print("🚀 محاولة إنشاء حساب جديد")
    print("="*60)
    
    # 1. إنشاء بريد مؤقت
    temp_mail = TempMail()
    email = temp_mail.create_email()
    
    if not email:
        print("❌ فشل إنشاء بريد")
        return None, None, None
    
    print(f"✅ البريد: {email}")
    
    # 2. محاولة الطريقة الأولى: المتصفح الحقيقي
    browser = NanoBananaBrowser()
    
    if browser.use_playwright:
        print("\n🖥️ جرب طريقة المتصفح الحقيقي...")
        session_token = browser.create_account_with_browser(email)
    else:
        print("\n🔧 جرب الطريقة اليدوية...")
        session_token = browser.create_account_manual(email)
    
    if not session_token:
        print("❌ فشل إنشاء الحساب")
        return None, None, None
    
    print(f"\n✅ تم إنشاء الحساب بنجاح!")
    print(f"🔑 Session Token: {session_token[:50]}...")
    
    print("="*60)
    print("🎉 اكتملت العملية!")
    print("="*60)
    
    return email, "temp_mail_password", session_token

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
    deleted_expired = delete_expired_accounts(user_id)
    if deleted_expired > 0:
        print(f"🗑️ تم حذف {deleted_expired} حساب منتهي")
    
    accounts = get_user_accounts(user_id)
    
    for acc in accounts:
        if acc.get('use_count', 0) < 5:
            return acc
    
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
        print(f"🎨 جاري إنشاء صورة: {prompt}")
        
        # استخدم API مباشرة
        import requests
        
        url = "https://nanabanana.ai/api/image-generation-nano-banana/create"
        cookie_string = f"__Secure-authjs.session-token={account['session_token']}"
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
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
        
        try:
            response = requests.post(url, 
                                   data=json.dumps(payload), 
                                   headers=headers, 
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                task_id = data.get("task_id")
                
                if task_id:
                    await event.respond(f"**✅ تم بدء إنشاء الصورة\n📝 رقم المهمة: {task_id}**")
                    
                    # التحقق من الحالة
                    status_url = "https://nanabanana.ai/api/image-generation-nano-banana/status"
                    for attempt in range(40):
                        time.sleep(5)
                        
                        status_response = requests.post(status_url, 
                                                      data=json.dumps({"taskId": task_id}), 
                                                      headers=headers, 
                                                      timeout=30)
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            if "generations" in status_data and status_data["generations"]:
                                generation = status_data["generations"][0]
                                if generation.get("status") == "succeed":
                                    image_url = generation.get("url")
                                    
                                    if image_url:
                                        filename = download_image(image_url, account['email'])
                                        if filename:
                                            await bot.send_file(event.chat_id, filename, 
                                                              caption=f"**✅ تم إنشاء الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                                            os.remove(filename)
                                        else:
                                            await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
                                    else:
                                        await event.respond("**❌ لا يوجد رابط للصورة**", buttons=keyboard)
                                    break
                                elif generation.get("status") == "failed":
                                    await event.respond("**❌ فشل في إنشاء الصورة**", buttons=keyboard)
                                    break
                    
                    else:
                        await event.respond("**⏰ انتهى وقت الانتظار**", buttons=keyboard)
                else:
                    await event.respond("**❌ لم يتم إنشاء المهمة**", buttons=keyboard)
            else:
                await event.respond("**❌ فشل في بدء العملية**", buttons=keyboard)
                
        except Exception as e:
            await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)
        
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
        try:
            upload_url = "https://nanabanana.ai/api/upload"
            
            with open(session.photo_path, 'rb') as f:
                files = {'file': (os.path.basename(session.photo_path), f, 'image/jpeg')}
                upload_response = requests.post(upload_url, files=files, timeout=30)
            
            if upload_response.status_code == 200:
                upload_data = upload_response.json()
                uploaded_url = upload_data.get("url")
                
                if uploaded_url:
                    # إنشاء الصورة المعدلة
                    create_url = "https://nanabanana.ai/api/image-generation-nano-banana/create"
                    cookie_string = f"__Secure-authjs.session-token={account['session_token']}"
                    
                    headers = {
                        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
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
                        "is_public": False,
                        "image_urls": [uploaded_url]
                    }
                    
                    response = requests.post(create_url, 
                                           data=json.dumps(payload), 
                                           headers=headers, 
                                           timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        task_id = data.get("task_id")
                        
                        if task_id:
                            await event.respond(f"**✅ تم بدء تعديل الصورة\n📝 رقم المهمة: {task_id}**")
                            
                            # التحقق من الحالة
                            status_url = "https://nanabanana.ai/api/image-generation-nano-banana/status"
                            for attempt in range(40):
                                time.sleep(5)
                                
                                status_response = requests.post(status_url, 
                                                              data=json.dumps({"taskId": task_id}), 
                                                              headers=headers, 
                                                              timeout=30)
                                
                                if status_response.status_code == 200:
                                    status_data = status_response.json()
                                    if "generations" in status_data and status_data["generations"]:
                                        generation = status_data["generations"][0]
                                        if generation.get("status") == "succeed":
                                            image_url = generation.get("url")
                                            
                                            if image_url:
                                                filename = download_image(image_url, account['email'])
                                                if filename:
                                                    await bot.send_file(event.chat_id, filename, 
                                                                      caption=f"**✅ تم تعديل الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                                                    os.remove(filename)
                                                else:
                                                    await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
                                            else:
                                                await event.respond("**❌ لا يوجد رابط للصورة**", buttons=keyboard)
                                            break
                                        elif generation.get("status") == "failed":
                                            await event.respond("**❌ فشل في تعديل الصورة**", buttons=keyboard)
                                            break
                            
                            else:
                                await event.respond("**⏰ انتهى وقت الانتظار**", buttons=keyboard)
                        else:
                            await event.respond("**❌ لم يتم إنشاء المهمة**", buttons=keyboard)
                    else:
                        await event.respond("**❌ فشل في بدء العملية**", buttons=keyboard)
                else:
                    await event.respond("**❌ فشل في رفع الصورة**", buttons=keyboard)
            else:
                await event.respond("**❌ فشل في رفع الصورة**", buttons=keyboard)
                
        except Exception as e:
            await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)
        
        # تنظيف الملف المؤقت
        if os.path.exists(session.photo_path):
            try:
                os.remove(session.photo_path)
            except:
                pass
        
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

print("✅ تم تحميل بوت تعديل الصور بنجاح!")
print("🖥️ يستخدم Playwright لتجاوز Cloudflare")

# نصيحة التثبيت
print("\n⚠️ **للتثبيت إذا لزم:**")
print("1. pip install playwright")
print("2. playwright install chromium")
print("3. تأكد من وجود Chrome/Chromium على السيرفر")
