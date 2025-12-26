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
logging.getLogger().setLevel(logging.WARNING)  # ⬅️ نفس كود الاختراق

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

# ========== دوال إنشاء البريد ==========
async def create_email_account():
    email_url = "https://api.mail.tm"
    email_headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    
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
            
            return email, password, token
    except:
        return False, False, False

async def wait_for_verification_code(token, email):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
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
                            return matches[0]
                await asyncio.sleep(5)
            except:
                await asyncio.sleep(5)
    return None

# ========== دوال NanoBanana ==========
async def create_nanabanana_account():
    email, password, mail_token = await create_email_account()
    
    if not email or not mail_token:
        return None, None, None
    
    nana_headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
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
    
    verification_headers = {**nana_headers, 'Content-Type': "application/json", 'origin': "https://nanabanana.ai", 'referer': "https://nanabanana.ai/ar/ai-image", 'Cookie': f"__Host-authjs.csrf-token={csrf_cookie}"}
    
    for key, value in cookies_dict.items():
        if key != '__Host-authjs.csrf-token':
            verification_headers['Cookie'] += f"; {key}={value}"
    
    verification_payload = {"email": email}
    requests.post("https://nanabanana.ai/api/auth/email-verification", data=json.dumps(verification_payload), headers=verification_headers)
    
    code = await wait_for_verification_code(mail_token, email)
    
    if not code:
        return None, None, None
    
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
        return email, password, session_token
    else:
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

def get_or_create_account(user_id):
    accounts = load_accounts()
    user_accs = get_user_accounts(user_id)
    
    if user_accs:
        for acc in user_accs:
            if acc.get('use_count', 0) < 5:
                return acc
    
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

# ========== القائمة والأزرار ==========
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
# ========== الإنلاين (نسخة صحيحة) ==========
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        if query.startswith("صور") and event.query.user_id == bot.uid:
            buttons = Button.url(" اضغط هنا عزيزي ", f"https://t.me/{joker}?start=edit")
            result = builder.article(
                title="Aljoker 🤡",
                description="اضغط على الزر لعرض الأوامر.",
                text="**✧︙ قم بالضغط على زر ادناه لأستخدام امر اختراق عبر كود التيرمكس",
                buttons=buttons
            )
        await event.answer([result] if result else None)

# الأمر .تعديل_الصور
# أضف هذا الأمر الجديد
@bot.on(admin_cmd(outgoing=True, pattern="صور$"))
async def images_cmd(event):
    if event.fwd_from:
        return
    bot_username = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(bot_username, "صور")
    if response:
        await response[0].click(event.chat_id)
        await event.delete()
    else:
        await event.edit("❌ لم يتم العثور على نتائج الإنلاين")


# ========== الأمر الرئيسي (مثل /hack) ==========
@tgbot.on(events.NewMessage(pattern="/edit", func=lambda x: x.is_private))
async def start(event):
    if event.sender_id == bot.uid:
        async with bot.conversation(event.chat_id) as x:
            await x.send_message(f"{menu}", buttons=keyboard)
    

# ========== معالجة الأزرار ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"create_image")))
async def create_image_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**✍️ أرسل وصف الصورة التي تريد إنشاءها:**")
        prompt_msg = await x.get_response()
        prompt = prompt_msg.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            return
        
        await event.respond("**⏳ جاري إنشاء الصورة...**")
        
        account = get_or_create_account(event.sender_id)
        if not account:
            await event.respond("**❌ فشل في إنشاء أو استرجاع الحساب**", buttons=keyboard)
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

@tgbot.on(events.CallbackQuery(data=re.compile(b"edit_image")))
async def edit_image_handler(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("**📤 أرسل الصورة التي تريد تعديلها:**")
        photo_msg = await x.get_response()
        
        if not photo_msg.media:
            await event.respond("**❌ لم ترسل صورة**", buttons=keyboard)
            return
        
        # حفظ الصورة
        photo_path = await photo_msg.download_media(file="temp_images/")
        
        await x.send_message("**✍️ أرسل وصف التعديل المطلوب:**")
        prompt_msg = await x.get_response()
        prompt = prompt_msg.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            os.remove(photo_path)
            return
        
        await event.respond("**⏳ جاري معالجة الصورة...**")
        
        account = get_or_create_account(event.sender_id)
        if not account:
            await event.respond("**❌ فشل في إنشاء أو استرجاع الحساب**", buttons=keyboard)
            os.remove(photo_path)
            return
        
        # رفع الصورة
        uploaded_url = upload_image(photo_path)
        os.remove(photo_path)
        
        if not uploaded_url:
            await event.respond("**❌ فشل في رفع الصورة**", buttons=keyboard)
            return
        
        # إنشاء الصورة المعدلة
        task_id = create_or_edit_image(account['session_token'], prompt, [uploaded_url])
        
        if task_id:
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

@tgbot.on(events.CallbackQuery(data=re.compile(b"my_accounts")))
async def my_accounts_handler(event):
    accounts = get_user_accounts(event.sender_id)
    
    if not accounts:
        response = "**📭 لا توجد حسابات مرفوعة بعد.**"
    else:
        response = "**📋 حساباتك:**\n\n"
        for i, acc in enumerate(accounts, 1):
            response += f"**{i}. {acc['email']}**\n"
            response += f"   استخدامات: {acc.get('use_count', 0)}/5\n"
            response += f"   تاريخ: {acc.get('created_at', 'غير معروف')[:10]}\n\n"
    
    await event.edit(response, buttons=keyboard)

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
            f"📧 **{email}**\n"
            f"🔑 **{password}**\n\n"
            f"**تم الحفظ تلقائياً.**",
            buttons=keyboard
        )
    else:
        await event.edit("**❌ فشل في إنشاء الحساب**", buttons=keyboard)

print("✅ تم تحميل بوت تعديل الصور بنجاح!")
