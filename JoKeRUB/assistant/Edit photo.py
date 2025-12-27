
from JoKeRUB import bot, l313l
#By Source joker @ucriss
from telethon import events, functions, types, Button
from datetime import timedelta
from JoKeRUB.utils import admin_cmd
import asyncio
from ..Config import Config
import os, asyncio, re
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
    user_accounts = [acc for acc in accounts if acc.get('user_id') == user_id]
    
    # حذف الحسابات التي وصلت 5/5 تلقائياً عند الطلب
    accounts_to_keep = []
    for acc in user_accounts:
        if acc.get('use_count', 0) < 5:
            accounts_to_keep.append(acc)
    
    # إذا وجدنا حسابات تم حذفها، نحدث الملف
    if len(accounts_to_keep) != len(user_accounts):
        all_accounts = load_accounts()
        updated_accounts = []
        for acc in all_accounts:
            if acc.get('user_id') != user_id or acc.get('use_count', 0) < 5:
                updated_accounts.append(acc)
        save_accounts(updated_accounts)
    
    return accounts_to_keep

# ========== دوال إنشاء البريد ==========
async def create_email_account():
    email_url = "https://api.mail.tm"
    email_headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    
    try:
        async with aiohttp.ClientSession(headers=email_headers) as session:
            # الحصول على نطاق
            domains_resp = await session.get(f"{email_url}/domains")
            if domains_resp.status != 200:
                return None, None, None
                
            domains_data = await domains_resp.json()
            if not domains_data.get("hydra:member"):
                return None, None, None
                
            domain = domains_data["hydra:member"][0]["domain"]
            
            # إنشاء بريد عشوائي
            username = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(12))
            email = f"{username}@{domain}"
            password = f"Pass{random.randint(1000, 9999)}!"
            
            # إنشاء الحساب
            payload = {"address": email, "password": password}
            account_resp = await session.post(f"{email_url}/accounts", json=payload)
            if account_resp.status != 201:
                return None, None, None
            
            # الحصول على التوكن
            token_resp = await session.post(f"{email_url}/token", json=payload)
            if token_resp.status != 200:
                return None, None, None
                
            token_data = await token_resp.json()
            token = token_data.get("token")
            
            return email, password, token
    except Exception as e:
        print(f"خطأ في إنشاء البريد: {e}")
        return None, None, None

async def wait_for_verification_code(token, email):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Authorization": f"Bearer {token}"
    }
    
    timeout = 180  # 3 دقائق فقط
    start_time = time.time()
    
    async with aiohttp.ClientSession(headers=headers) as session:
        while time.time() - start_time < timeout:
            try:
                messages_resp = await session.get("https://api.mail.tm/messages")
                if messages_resp.status != 200:
                    await asyncio.sleep(5)
                    continue
                    
                inbox = await messages_resp.json()
                messages = inbox.get("hydra:member", [])
                
                for msg in messages:
                    sender = msg.get('from', {}).get('address', '')
                    if 'nanabanana.ai' in sender:
                        msg_id = msg["id"]
                        msg_resp = await session.get(f"https://api.mail.tm/messages/{msg_id}")
                        if msg_resp.status == 200:
                            full_msg = await msg_resp.json()
                            text_content = full_msg.get('text', '')
                            matches = re.findall(r'\b\d{6}\b', text_content)
                            if matches:
                                return matches[0]
                await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)
    return None

# ========== دوال NanoBanana ==========
async def create_nanabanana_account():
    # محاولة 3 مرات
    for attempt in range(3):
        email, password, mail_token = await create_email_account()
        
        if not email or not mail_token:
            await asyncio.sleep(2)
            continue
        
        nana_headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        
        try:
            csrf_response = requests.get("https://nanabanana.ai/api/auth/csrf", headers=nana_headers, timeout=10)
            if csrf_response.status_code != 200:
                continue
                
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
            
            verification_headers = nana_headers.copy()
            verification_headers.update({
                'Content-Type': "application/json",
                'origin': "https://nanabanana.ai",
                'referer': "https://nanabanana.ai/ar/ai-image"
            })
            
            # بناء الكوكيز
            cookie_str = ""
            if csrf_cookie:
                cookie_str += f"__Host-authjs.csrf-token={csrf_cookie}; "
            for key, value in cookies_dict.items():
                if key != '__Host-authjs.csrf-token':
                    cookie_str += f"{key}={value}; "
            
            verification_headers['Cookie'] = cookie_str.strip()
            
            # طلب كود التحقق
            verification_payload = {"email": email}
            verify_resp = requests.post(
                "https://nanabanana.ai/api/auth/email-verification",
                data=json.dumps(verification_payload),
                headers=verification_headers,
                timeout=10
            )
            
            if verify_resp.status_code != 200:
                continue
            
            # انتظار الكود
            code = await wait_for_verification_code(mail_token, email)
            
            if not code:
                continue
            
            # تأكيد التسجيل
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
                headers=verification_headers,
                timeout=10
            )
            
            final_cookies = final_response.cookies.get_dict()
            session_token = final_cookies.get('__Secure-authjs.session-token')
            
            if session_token:
                return email, password, session_token
                
        except Exception as e:
            print(f"المحاولة {attempt+1} فشلت: {e}")
            await asyncio.sleep(2)
    
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
        response = requests.post(url, files=files, headers=headers, timeout=30)
        
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
    
    cookie_string = f"__Secure-authjs.session-token={session_token}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'Cookie': cookie_string
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get("task_id")
            return task_id
        else:
            return None
    except:
        return None

def check_status(task_id, session_token, max_attempts=30, delay=3):
    url = "https://nanabanana.ai/api/image-generation-nano-banana/status"
    cookie_string = f"__Secure-authjs.session-token={session_token}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'Content-Type': "application/json",
        'Cookie': cookie_string
    }
    
    for attempt in range(max_attempts):
        try:
            payload = {"taskId": task_id}
            response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
            
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
        except:
            time.sleep(delay)
    return None

def download_image(image_url, account_email):
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
        else:
            return None
    except:
        return None

# ========== القائمة والأزرار ==========
menu = '''
🎨 **بوت إنشاء وتعديل الصور باستخدام الذكاء الاصطناعي**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("🖼️ إنشاء صورة جديدة", data="create_image"), 
        Button.inline("✏️ تعديل صورة", data="edit_image"),
    ],
    [
        Button.inline("📋 حساباتي", data="my_accounts"),
        Button.inline("🆕 إنشاء حساب جديد", data="new_account"),
    ],
    [
        Button.url("المـطور", "https://t.me/Lx5x5")
    ]
]

back_keyboard = [
    [Button.inline("🔙 رجوع للقائمة", data="back_to_menu")]
]

delete_keyboard = [
    [Button.inline("🗑️ حذف جميع الحسابات", data="delete_all_accounts")],
    [Button.inline("🔙 رجوع", data="back_to_menu")]
]

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
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"{menu}", buttons=keyboard)

# ========== زر الرجوع ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"back_to_menu")))
async def back_to_menu_handler(event):
    try:
        await event.edit(menu, buttons=keyboard)
    except:
        await event.respond(menu, buttons=keyboard)

# ========== إنشاء صورة جديدة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"create_image")))
async def create_image_handler(event):
    try:
        # إرسال رسالة الطلب
        await event.respond("**✍️ أرسل وصف الصورة التي تريد إنشاءها:**")
        
        # انتظار الرد
        prompt_msg = await event.get_response()
        prompt = prompt_msg.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            return
        
        await event.respond("**⏳ جاري إنشاء حساب وصورة... قد يستغرق دقيقة**")
        
        # إنشاء حساب جديد
        email, password, session_token = await create_nanabanana_account()
        
        if not session_token:
            await event.respond("**❌ فشل في إنشاء الحساب، حاول لاحقاً**", buttons=keyboard)
            return
        
        # حفظ الحساب
        accounts = load_accounts()
        new_account = {
            'user_id': event.sender_id,
            'email': email,
            'password': password,
            'session_token': session_token,
            'use_count': 1,
            'created_at': datetime.now().isoformat()
        }
        accounts.append(new_account)
        save_accounts(accounts)
        
        # إنشاء الصورة
        task_id = create_or_edit_image(session_token, prompt)
        
        if not task_id:
            await event.respond("**❌ فشل في بدء إنشاء الصورة**", buttons=keyboard)
            return
        
        await event.respond(f"**✅ تم بدء إنشاء الصورة\n📝 رقم المهمة: {task_id[:10]}...**")
        
        # متابعة الحالة
        image_url = check_status(task_id, session_token)
        
        if image_url:
            filename = download_image(image_url, email)
            if filename:
                try:
                    await bot.send_file(
                        event.chat_id, 
                        filename,
                        caption=f"**✅ تم إنشاء الصورة بنجاح!\n📧 الحساب: {email}\n⚡ استخدامات: 1/5**"
                    )
                    os.remove(filename)
                except:
                    await event.respond("**✅ تم إنشاء الصورة لكن حدث خطأ في الإرسال**", buttons=keyboard)
            else:
                await event.respond("**✅ تم إنشاء الصورة لكن فشل التنزيل**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في إنشاء الصورة**", buttons=keyboard)
            
    except asyncio.TimeoutError:
        await event.respond("**⏰ انتهى وقت الانتظار**", buttons=keyboard)
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ غير متوقع**", buttons=keyboard)
        print(f"خطأ في create_image_handler: {e}")

# ========== تعديل صورة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"edit_image")))
async def edit_image_handler(event):
    try:
        await event.respond("**📤 أرسل الصورة التي تريد تعديلها:**")
        photo_msg = await event.get_response()
        
        if not photo_msg.media:
            await event.respond("**❌ لم ترسل صورة**", buttons=keyboard)
            return
        
        # حفظ الصورة
        photo_path = await photo_msg.download_media(file="temp_images/")
        
        await event.respond("**✍️ أرسل وصف التعديل المطلوب:**")
        prompt_msg = await event.get_response()
        prompt = prompt_msg.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            if os.path.exists(photo_path):
                os.remove(photo_path)
            return
        
        await event.respond("**⏳ جاري معالجة الصورة...**")
        
        # إنشاء حساب جديد للتعديل
        email, password, session_token = await create_nanabanana_account()
        
        if not session_token:
            await event.respond("**❌ فشل في إنشاء الحساب**", buttons=keyboard)
            if os.path.exists(photo_path):
                os.remove(photo_path)
            return
        
        # حفظ الحساب
        accounts = load_accounts()
        new_account = {
            'user_id': event.sender_id,
            'email': email,
            'password': password,
            'session_token': session_token,
            'use_count': 1,
            'created_at': datetime.now().isoformat()
        }
        accounts.append(new_account)
        save_accounts(accounts)
        
        # رفع الصورة
        uploaded_url = upload_image(photo_path)
        if os.path.exists(photo_path):
            os.remove(photo_path)
        
        if not uploaded_url:
            await event.respond("**❌ فشل في رفع الصورة**", buttons=keyboard)
            return
        
        # تعديل الصورة
        task_id = create_or_edit_image(session_token, prompt, [uploaded_url])
        
        if not task_id:
            await event.respond("**❌ فشل في بدء التعديل**", buttons=keyboard)
            return
        
        await event.respond(f"**✅ تم بدء تعديل الصورة\n📝 رقم المهمة: {task_id[:10]}...**")
        
        # متابعة الحالة
        image_url = check_status(task_id, session_token)
        
        if image_url:
            filename = download_image(image_url, email)
            if filename:
                try:
                    await bot.send_file(
                        event.chat_id,
                        filename,
                        caption=f"**✅ تم تعديل الصورة بنجاح!\n📧 الحساب: {email}\n⚡ استخدامات: 1/5**"
                    )
                    os.remove(filename)
                except:
                    await event.respond("**✅ تم التعديل لكن حدث خطأ في الإرسال**", buttons=keyboard)
            else:
                await event.respond("**✅ تم التعديل لكن فشل التنزيل**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في تعديل الصورة**", buttons=keyboard)
            
    except asyncio.TimeoutError:
        await event.respond("**⏰ انتهى وقت الانتظار**", buttons=keyboard)
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ غير متوقع**", buttons=keyboard)
        print(f"خطأ في edit_image_handler: {e}")

# ========== حساباتي (مع زر الحذف) ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"my_accounts")))
async def my_accounts_handler(event):
    accounts = get_user_accounts(event.sender_id)
    
    if not accounts:
        response = "**📭 لا توجد حسابات نشطة.\n\n**"
        response += "الحسابات التي تصل إلى 5 استخدامات تحذف تلقائياً."
        await event.edit(response, buttons=back_keyboard)
        return
    
    response = "**📋 حساباتك النشطة:**\n\n"
    for i, acc in enumerate(accounts, 1):
        use_count = acc.get('use_count', 0)
        response += f"{i}. **{acc['email']}**\n"
        response += f"   استخدامات: {use_count}/5\n"
        created_date = acc.get('created_at', 'غير معروف')
        if len(created_date) > 10:
            response += f"   تاريخ: {created_date[:10]}\n\n"
        else:
            response += f"   تاريخ: {created_date}\n\n"
    
    response += f"**📊 الإجمالي: {len(accounts)} حساب نشط**\n"
    response += "الحسابات التي تصل إلى 5 استخدامات تحذف تلقائياً."
    
    await event.edit(response, buttons=delete_keyboard)

# ========== حذف جميع الحسابات ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"delete_all_accounts")))
async def delete_all_accounts_handler(event):
    accounts = load_accounts()
    original_count = len(accounts)
    
    # حساب عدد الحسابات قبل الحذف
    user_accounts_before = [acc for acc in accounts if acc.get('user_id') == event.sender_id]
    
    # حذف حسابات هذا المستخدم فقط
    accounts = [acc for acc in accounts if acc.get('user_id') != event.sender_id]
    
    deleted_count = len(user_accounts_before)
    save_accounts(accounts)
    
    if deleted_count > 0:
        response = f"✅ تم حذف **{deleted_count}** حساب بنجاح.\n\n"
    else:
        response = "⚠️ لم يكن لديك أي حسابات لحذفها.\n\n"
    
    response += "يمكنك إنشاء حسابات جديدة من القائمة الرئيسية."
    
    await event.edit(response, buttons=back_keyboard)

# ========== إنشاء حساب جديد ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"new_account")))
async def new_account_handler(event):
    await event.edit("**⏳ جاري إنشاء حساب جديد...**")
    
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
        
        await event.edit(
            f"**✅ تم إنشاء حساب جديد!\n\n"
            f"📧 البريد: `{email}`\n"
            f"🔑 كلمة المرور: `{password}`\n\n"
            f"**تم حفظه تلقائياً في حساباتك.**\n"
            f"الحد الأقصى: 5 استخدامات لكل حساب.",
            buttons=back_keyboard
        )
    else:
        await event.edit(
            "**❌ فشل في إنشاء الحساب**\n\n"
            "الأسباب المحتملة:\n"
            "1. انتهت محاولات البريد المؤقت\n"
            "2. موقع NanoBanana غير متاح\n"
            "3. حظر مؤقت للعنوان IP\n\n"
            "حاول مرة أخرى بعد قليل.",
            buttons=back_keyboard
        )

print("✅ تم تحميل بوت تعديل الصور بنجاح مع الإصلاحات!")
