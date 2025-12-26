
import asyncio
import aiohttp
import random
import json
import requests
import re
import time
import os
from datetime import datetime
from telethon import Button, events
from .. import bot, l313l
from ..utils import admin_cmd
from ..Config import Config
import telethon

# إعدادات الملفات
accounts_file = "accounts/accounts_data.json"
os.makedirs("accounts", exist_ok=True)

# إعدادات البوت
BOT_USERNAME = Config.TG_BOT_USERNAME  # ضع يوزر بوتك هنا

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
    user_accs = [acc for acc in accounts if acc.get('user_id') == user_id]
    return user_accs

# ========== دوال إنشاء البريد ==========
async def create_email_account():
    email_url = "https://api.mail.tm"
    email_headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        async with aiohttp.ClientSession(headers=email_headers) as session:
            domains_resp = await session.get(f"{email_url}/domains")
            domains_data = await domains_resp.json()
            domain = domains_data["hydra:member"][0]["domain"]
            
            username = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(12))
            email = f"{username}@{domain}"
            password = f"Pass{random.randint(1000, 9999)}!"
            
            payload = {"address": email, "password": password}
            await session.post(f"{email_url}/accounts", json=payload)
            
            token_resp = await session.post(f"{email_url}/token", json=payload)
            token_data = await token_resp.json()
            token = token_data.get("token")
            
            print(f"✓ تم إنشاء البريد: {email}")
            return email, password, token
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء البريد: {e}")
        return False, False, False

async def wait_for_verification_code(token, email):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Authorization": f"Bearer {token}"
    }
    
    timeout = 300
    start_time = time.time()
    
    async with aiohttp.ClientSession(headers=headers) as session:
        while time.time() - start_time < timeout:
            try:
                messages_resp = await session.get("https://api.mail.tm/messages")
                inbox = await messages_resp.json()
                messages = inbox.get("hydra:member", [])
                
                for msg in messages:
                    sender = msg.get('from', {}).get('address', '')
                    if 'nanabanana.ai' in sender:
                        msg_id = msg["id"]
                        msg_resp = await session.get(f"https://api.mail.tm/messages/{msg_id}")
                        full_msg = await msg_resp.json()
                        text_content = full_msg.get('text', '')
                        matches = re.findall(r'\b\d{6}\b', text_content)
                        if matches:
                            code = matches[0]
                            print(f"✅ تم استقبال رمز التحقق: {code}")
                            return code
                
                await asyncio.sleep(5)
            except Exception as e:
                print(f"⚠ خطأ في التحقق من البريد: {e}")
                await asyncio.sleep(5)
    
    print("❌ انتهى وقت الانتظار ولم يتم استقبال الرمز")
    return None

# ========== دوال NanoBanana ==========
async def create_nanabanana_account():
    print("\n" + "="*50)
    print("🆕 إنشاء حساب جديد في NanoBanana")
    print("="*50)
    
    email, password, mail_token = await create_email_account()
    
    if not email or not mail_token:
        print("❌ فشل في إنشاء البريد الإلكتروني")
        return None, None, None
    
    nana_headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    print("🔄 جاري الحصول على رمز CSRF...")
    csrf_response = requests.get("https://nanabanana.ai/api/auth/csrf", headers=nana_headers)
    csrf_token = None
    csrf_cookie = None
    
    if csrf_response.text:
        try:
            csrf_data = json.loads(csrf_response.text)
            csrf_token = csrf_data.get("csrfToken")
            print(f"✅ CSRF Token: {csrf_token[:20]}...")
        except:
            pass
    
    if '__Host-authjs.csrf-token' in csrf_response.cookies:
        csrf_cookie = csrf_response.cookies.get('__Host-authjs.csrf-token')
        print(f"✅ CSRF Cookie: {csrf_cookie[:30]}...")
    
    cookies_dict = csrf_response.cookies.get_dict()
    
    print("📤 طلب إرسال رمز التحقق...")
    verification_headers = {**nana_headers, 'Content-Type': "application/json", 'origin': "https://nanabanana.ai", 'referer': "https://nanabanana.ai/ar/ai-image", 'Cookie': f"__Host-authjs.csrf-token={csrf_cookie}"}
    
    for key, value in cookies_dict.items():
        if key != '__Host-authjs.csrf-token':
            verification_headers['Cookie'] += f"; {key}={value}"
    
    verification_payload = {"email": email}
    verification_response = requests.post("https://nanabanana.ai/api/auth/email-verification", data=json.dumps(verification_payload), headers=verification_headers)
    print("✅ تم إرسال طلب التحقق")
    
    code = await wait_for_verification_code(mail_token, email)
    
    if not code:
        print("❌ لم يتم استقبال رمز التحقق")
        return None, None, None
    
    print("🔐 جاري إكمال عملية التسجيل...")
    callback_headers = {**nana_headers, 'x-auth-return-redirect': "1", 'origin': "https://nanabanana.ai", 'referer': "https://nanabanana.ai/ar/ai-image", 'Cookie': f"__Host-authjs.csrf-token={csrf_cookie}"}
    
    for key, value in cookies_dict.items():
        if key != '__Host-authjs.csrf-token':
            callback_headers['Cookie'] += f"; {key}={value}"
    
    callback_payload = {'email': email, 'code': code, 'redirect': "false", 'csrfToken': csrf_token, 'callbackUrl': "https://nanabanana.ai/ar/ai-image"}
    final_response = requests.post("https://nanabanana.ai/api/auth/callback/email-verification", data=callback_payload, headers=callback_headers)
    
    final_cookies = final_response.cookies.get_dict()
    session_token = None
    if '__Secure-authjs.session-token' in final_cookies:
        session_token = final_cookies['__Secure-authjs.session-token']
    
    if session_token:
        print("\n✅ تم إنشاء الحساب بنجاح!")
        print(f"📧 البريد: {email}")
        print(f"🔑 كلمة المرور: {password}")
        print(f"🍪 Session Token: {session_token[:50]}...")
        return email, password, session_token
    else:
        print("❌ فشل في استخراج التوكن من الكوكيز")
        return None, None, None

def upload_image(image_path):
    url = "https://nanabanana.ai/api/upload"
    try:
        if not os.path.exists(image_path):
            print(f"❌ خطأ: الملف '{image_path}' غير موجود.")
            return None
        
        with open(image_path, 'rb') as f:
            file_content = f.read()
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'sec-ch-ua-platform': "\"Android\"",
            'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            'sec-ch-ua-mobile': "?1",
            'origin': "https://nanabanana.ai",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://nanabanana.ai/ar/ai-image",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            'priority': "u=1, i"
        }
        
        files = [('file', (os.path.basename(image_path), file_content, 'image/jpeg'))]
        response = requests.post(url, files=files, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("url")
            print(f"✅ تم رفع الصورة بنجاح")
            return image_url
        else:
            print(f"❌ فشل رفع الصورة: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ خطأ أثناء رفع الصورة: {e}")
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
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://nanabanana.ai",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://nanabanana.ai/ar/ai-image",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i",
        'Cookie': cookie_string
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        task_id = data.get("task_id")
        if task_id:
            mode = "تعديل صورة" if image_urls else "إنشاء صورة جديدة"
            print(f"✅ تم بدء {mode} بنجاح")
            print(f"📝 رقم المهمة: {task_id}")
            return task_id
        else:
            print("❌ لم يتم الحصول على رقم المهمة")
            return None
    else:
        print(f"❌ فشل في طلب إنشاء الصورة: {response.status_code}")
        return None

def check_status(task_id, session_token, max_attempts=40, delay=5):
    url = "https://nanabanana.ai/api/image-generation-nano-banana/status"
    cookie_string = f"__Secure-authjs.session-token={session_token}; __Secure-authjs.callback-url=https%3A%2F%2Fnanabanana.ai%2Far%2Fai-image"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://nanabanana.ai",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://nanabanana.ai/ar/ai-image",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        'priority': "u=1, i",
        'Cookie': cookie_string
    }
    
    for attempt in range(max_attempts):
        print(f"⌛ المحاولة {attempt + 1}/{max_attempts}...")
        payload = {"taskId": task_id}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "generations" in data and len(data["generations"]) > 0:
                generation = data["generations"][0]
                status = generation.get("status", "unknown")
                if status == "succeed":
                    print("🎉 تم إنشاء الصورة بنجاح!")
                    image_url = generation.get("url", "")
                    if image_url:
                        print(f"🔗 رابط الصورة: {image_url}")
                        return image_url
                    else:
                        print("⚠ رابط الصورة غير متوفر")
                        return None
                elif status == "failed":
                    print("❌ فشل إنشاء الصورة")
                    return None
                elif status == "waiting":
                    print("⏳ جاري الانتظار في قائمة الانتظار...")
                    time.sleep(delay)
                elif status == "processing":
                    print("🔄 جاري معالجة الصورة...")
                    time.sleep(delay)
                else:
                    print(f"❓ حالة غير معروفة: {status}")
                    time.sleep(delay)
            else:
                print("⚠ لا توجد بيانات في الاستجابة")
                time.sleep(delay)
        else:
            print(f"⚠ خطأ في التحقق: {response.status_code}")
            time.sleep(delay)
    
    print("⏰ انتهت المحاولات دون نجاح")
    return None

def download_image(image_url, task_id, account_email):
    try:
        print("📥 جاري تحميل الصورة...")
        response = requests.get(image_url, stream=True)
        
        if response.status_code == 200:
            os.makedirs("generated_images", exist_ok=True)
            safe_email = account_email.replace("@", "_").replace(".", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/image_{safe_email}_{timestamp}.png"
            
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            
            print(f"✅ تم حفظ الصورة بنجاح: {filename}")
            return filename
        else:
            print(f"❌ فشل تحميل الصورة: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ خطأ أثناء التحميل: {e}")
        return None

def get_or_create_account(user_id):
    accounts = load_accounts()
    user_accs = [acc for acc in accounts if acc.get('user_id') == user_id]
    
    if user_accs:
        for acc in user_accs:
            if acc.get('use_count', 0) < 5:
                return acc
        for acc in user_accs:
            accounts.remove(acc)
        save_accounts(accounts)
    
    async def create_and_save():
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
        return None
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(create_and_save())
    loop.close()
    return result

# ========== تعريف الأوامر ==========
@bot.on(admin_cmd(pattern="تعديل_الصور$"))
async def image_edit_command(event):
    """عند كتابة .تعديل_الصور يرسل إلى البوت الخاص بك"""
    await event.edit("**جاري إرسال طلب تعديل الصور إلى البوت...**")
    
    # إرسال الأمر /edit إلى البوت الخاص بك
    async with bot.conversation(BOT_USERNAME) as conv:
        await conv.send_message("/edit")
        await event.edit("**✅ تم إرسال الأمر إلى البوت. راجع محادثتك مع البوت.**")

@bot.on(admin_cmd(pattern="حساباتي$"))
async def my_accounts_command(event):
    """عرض حسابات المستخدم"""
    user_id = event.sender_id
    accounts = get_user_accounts(user_id)
    
    if not accounts:
        await event.edit("**📭 لا توجد حسابات مرفوعة بعد.**")
        return
    
    response = "**📋 حساباتك:\n\n**"
    for i, acc in enumerate(accounts, 1):
        response += f"**{i}. {acc['email']}**\n"
        response += f"   عدد الاستخدامات: {acc.get('use_count', 0)}/5\n"
        response += f"   تاريخ الإنشاء: {acc.get('created_at', 'غير معروف')[:10]}\n"
        response += "   ───────────────\n"
    
    await event.edit(response)

@bot.on(admin_cmd(pattern="إنشاء_حساب$"))
async def create_account_command(event):
    """إنشاء حساب جديد"""
    await event.edit("**⏳ جاري إنشاء حساب جديد...**")
    
    async def create_account():
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
            await event.edit(f"**✅ تم إنشاء حساب جديد بنجاح!\n📧 {email}\n🔑 {password}**")
        else:
            await event.edit("**❌ فشل في إنشاء الحساب. الرجاء المحاولة لاحقًا.**")
    
    await create_account()

@bot.on(admin_cmd(pattern="إنشاء_صورة (.*)"))
async def create_image_command(event):
    """إنشاء صورة جديدة"""
    prompt = event.pattern_match.group(1)
    if not prompt or len(prompt.strip()) < 3:
        await event.edit("**❌ الوصف قصير جدًا. الرجاء إدخال وصف مفصل.**")
        return
    
    await event.edit("**⏳ جاري إنشاء حساب واستخراج التوكن...**")
    
    account = get_or_create_account(event.sender_id)
    if not account:
        await event.edit("**❌ فشل في إنشاء أو استرجاع الحساب.**")
        return
    
    # تحديث عدد الاستخدامات
    accounts = load_accounts()
    for acc in accounts:
        if acc.get('session_token') == account['session_token']:
            acc['use_count'] = acc.get('use_count', 0) + 1
            save_accounts(accounts)
            break
    
    await event.edit(f"**✅ تم استخدام الحساب: {account['email']}\n📊 عدد الاستخدامات: {account.get('use_count', 0)}/5\n\n⏳ جاري إنشاء الصورة...**")
    
    try:
        task_id = create_or_edit_image(account['session_token'], prompt)
        if task_id:
            await event.edit(f"**✅ تم بدء إنشاء الصورة\n📝 رقم المهمة: {task_id}**")
            
            # التحقق من حالة الصورة
            image_url = check_status(task_id, account['session_token'])
            if image_url:
                filename = download_image(image_url, task_id, account['email'])
                if filename:
                    await event.reply(file=filename, caption=f"**✅ تم إنشاء الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                else:
                    await event.edit("**❌ فشل في حفظ الصورة.**")
            else:
                await event.edit("**❌ فشل في إنشاء الصورة.**")
        else:
            await event.edit("**❌ فشل في بدء عملية إنشاء الصورة.**")
    except Exception as e:
        await event.edit(f"**❌ حدث خطأ: {str(e)}**")

@bot.on(admin_cmd(pattern="تعديل_الصورة$"))
async def edit_image_command(event):
    """تعديل صورة"""
    await event.edit("**📤 الرجاء إرسال الصورة التي تريد تعديلها:**")
    
    try:
        response = await event.wait_event(events.NewMessage(from_users=event.sender_id))
        if not response.media:
            await event.edit("**❌ لم يتم إرسال صورة.**")
            return
        
        # حفظ الصورة مؤقتاً
        photo = await response.download_media()
        
        await event.edit("**✍️ الرجاء إرسال وصف التعديل المطلوب:**")
        response2 = await event.wait_event(events.NewMessage(from_users=event.sender_id))
        prompt = response2.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.edit("**❌ الوصف قصير جدًا.**")
            os.remove(photo)
            return
        
        await event.edit("**⏳ جاري معالجة الصورة...**")
        
        account = get_or_create_account(event.sender_id)
        if not account:
            await event.edit("**❌ فشل في إنشاء أو استرجاع الحساب.**")
            os.remove(photo)
            return
        
        # رفع الصورة
        uploaded_url = upload_image(photo)
        os.remove(photo)
        
        if not uploaded_url:
            await event.edit("**❌ فشل في رفع الصورة.**")
            return
        
        # إنشاء الصورة المعدلة
        task_id = create_or_edit_image(account['session_token'], prompt, [uploaded_url])
        
        if task_id:
            await event.edit(f"**✅ تم بدء تعديل الصورة\n📝 رقم المهمة: {task_id}**")
            
            # التحقق من حالة الصورة
            image_url = check_status(task_id, account['session_token'])
            if image_url:
                filename = download_image(image_url, task_id, account['email'])
                if filename:
                    await event.reply(file=filename, caption=f"**✅ تم تعديل الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                else:
                    await event.edit("**❌ فشل في حفظ الصورة.**")
            else:
                await event.edit("**❌ فشل في تعديل الصورة.**")
        else:
            await event.edit("**❌ فشل في بدء عملية التعديل.**")
            
    except Exception as e:
        await event.edit(f"**❌ حدث خطأ: {str(e)}**")

# ========== معالج الأزرار (مثل الكود الثالث) ==========
@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """عند بدء المحادثة مع البوت"""
    buttons = [
        [Button.inline("🖼️ إنشاء صورة جديدة", data="create_new")],
        [Button.inline("✏️ تعديل صورة", data="edit_image")],
        [Button.inline("📋 حساباتي", data="my_accounts")],
        [Button.inline("🆕 إنشاء حساب جديد", data="create_account")],
        [Button.url("📢 قناة البوت", "https://t.me/your_channel")]
    ]
    
    await event.reply(
        "**🎨 مرحبًا بك في بوت إنشاء وتعديل الصور باستخدام NanoBanana AI!**\n\n"
        "**اختر أحد الخيارات:**",
        buttons=buttons
    )

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    """معالجة النقر على الأزرار"""
    data = event.data.decode('utf-8')
    user_id = event.sender_id
    
    if data == "create_new":
        await event.edit(
            "**🖼️ إنشاء صورة جديدة**\n\n"
            "**أرسل وصف الصورة المطلوبة:**",
            buttons=[Button.inline("🔙 رجوع", data="back_to_menu")]
        )
        # هنا يمكنك إضافة منطق لاستلام الوصف
        
    elif data == "edit_image":
        await event.edit(
            "**✏️ تعديل صورة**\n\n"
            "**أرسل الصورة التي تريد تعديلها:**",
            buttons=[Button.inline("🔙 رجوع", data="back_to_menu")]
        )
        # هنا يمكنك إضافة منطق لاستلام الصورة
        
    elif data == "my_accounts":
        accounts = get_user_accounts(user_id)
        
        if not accounts:
            text = "**📭 لا توجد حسابات مرفوعة بعد.**"
        else:
            text = "**📋 حساباتك:\n\n**"
            for i, acc in enumerate(accounts, 1):
                text += f"**{i}. {acc['email']}**\n"
                text += f"   استخدامات: {acc.get('use_count', 0)}/5\n\n"
        
        await event.edit(
            text,
            buttons=[Button.inline("🔙 رجوع", data="back_to_menu")]
        )
        
    elif data == "create_account":
        await event.edit("**⏳ جاري إنشاء حساب جديد...**")
        
        email, password, session_token = await create_nanabanana_account()
        if session_token:
            accounts = load_accounts()
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
            
            await event.edit(
                f"**✅ تم إنشاء حساب جديد!\n\n"
                f"📧 **{email}**\n"
                f"🔑 **{password}**\n\n"
                f"**تم الحفظ تلقائيًا.**",
                buttons=[Button.inline("🔙 رجوع", data="back_to_menu")]
            )
        else:
            await event.edit(
                "**❌ فشل في إنشاء الحساب.**",
                buttons=[Button.inline("🔙 رجوع", data="back_to_menu")]
            )
            
    elif data == "back_to_menu":
        buttons = [
            [Button.inline("🖼️ إنشاء صورة جديدة", data="create_new")],
            [Button.inline("✏️ تعديل صورة", data="edit_image")],
            [Button.inline("📋 حساباتي", data="my_accounts")],
            [Button.inline("🆕 إنشاء حساب جديد", data="create_account")],
            [Button.url("📢 قناة البوت", "https://t.me/your_channel")]
        ]
        
        await event.edit(
            "**🎨 مرحبًا بك في بوت إنشاء وتعديل الصور باستخدام NanoBanana AI!**\n\n"
            "**اختر أحد الخيارات:**",
            buttons=buttons
        )

# ========== كود للتواصل مع البوت الخاص ==========
async def send_to_my_bot(message):
    """إرسال رسالة إلى البوت الخاص"""
    try:
        async with telethon.TelegramClient('session_name', Config.APP_ID, Config.API_HASH) as client:
            await client.send_message(BOT_USERNAME, message)
            return True
    except:
        return False

@bot.on(admin_cmd(pattern="تواصل$"))
async def contact_bot(event):
    """اختبار التواصل مع البوت الخاص"""
    success = await send_to_my_bot("مرحباً من البوت الرئيسي!")
    if success:
        await event.edit("**✅ تم إرسال الرسالة إلى البوت الخاص**")
    else:
        await event.edit("**❌ فشل في التواصل مع البوت الخاص**")

print("✅ تم تحميل موديول تعديل الصور بنجاح!")
