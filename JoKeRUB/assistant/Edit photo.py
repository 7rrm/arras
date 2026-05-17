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
from bs4 import BeautifulSoup

logging.getLogger().setLevel(logging.WARNING)

# إعدادات الملفات
os.makedirs("generated_images", exist_ok=True)
os.makedirs("temp_images", exist_ok=True)

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "ChatXBot"

# ========== دوال ChatX.ai (مثل الكود الأصلي تماماً) ==========
def get_fresh_tokens():
    """الحصول على توكنات جديدة من الموقع (مرة واحدة عند بدء التشغيل)"""
    url_main = "https://chatx.ai/ai-image"
    headers_main = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': "https://chatx.ai/",
        'accept-language': "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    session = requests.Session()
    resp_main = session.get(url_main, headers=headers_main, timeout=15)
    cookies = session.cookies.get_dict()
    soup = BeautifulSoup(resp_main.text, 'html.parser')
    meta_csrf = soup.find('meta', attrs={'name': 'csrf-token'})
    token = meta_csrf.get('content') if meta_csrf else None
    cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
    guest_token = cookies.get('chatx_guest_token', '')
    return token, cookie_str, guest_token

# الحصول على التوكنات مرة واحدة عند بدء التشغيل (مثل الكود الأصلي)
TOKEN, COOKIE_STR, GUEST_TOKEN = get_fresh_tokens()

def generate_user_id():
    """توليد معرف مستخدم عشوائي (مثل الكود الأصلي)"""
    user_id_base = "406994179"  # ثابت مثل الكود الأصلي
    new_last_three = str(random.randint(0, 999)).zfill(3)
    return user_id_base + new_last_three

def upload_image(image_path, token, cookie_str):
    """رفع صورة إلى السيرفر (مثل الكود الأصلي)"""
    if not os.path.exists(image_path):
        print(f"الملف غير موجود: {image_path}")
        return None
    
    file_name = os.path.basename(image_path)
    url = "https://chatx.ai/uploadImage"
    payload = {
        '_token': token,
        'user_id': '[object HTMLInputElement]',
        'chats_id': '[object HTMLInputElement]',
        'current_model': '[object HTMLInputElement]'
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua-mobile': "?1",
        'sec-ch-ua-platform': '"Android"',
        'origin': "https://chatx.ai",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://chatx.ai/gpt",
        'accept-language': "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': cookie_str
    }
    
    try:
        with open(image_path, 'rb') as f:
            files = [('images', (file_name, f, 'image/*'))]
            response = requests.post(url, data=payload, files=files, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            files_path = result.get('files')
            if isinstance(files_path, str):
                return files_path
            elif isinstance(files_path, list) and files_path:
                return files_path[0]
            else:
                print(f"رد غير متوقع: {result}")
                return None
        else:
            print(f"فشل الرفع: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None

def generate_image(prompt, token, cookie_str, images_param=None):
    """إنشاء صورة جديدة أو تعديلها (مثل الكود الأصلي)"""
    user_id = generate_user_id()
    
    url = "https://chatx.ai/generateImage"
    payload = {
        '_token': token,
        'user_id': user_id,
        'chats_id': "45762416",
        'prompt': prompt,
        'current_model': "gpt3",
        'images': images_param or "",
        'mask_image': "",
        'image_size': "auto",
        'image_quality': "auto",
        'image_type': "jpeg",
        'image_transparency': "auto",
        'gpt_image_model': "nano_2",
        'nano_aspect_ratio': "1:1"
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'x-csrf-token': token,
        'sec-ch-ua-mobile': "?1",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua-platform': '"Android"',
        'origin': "https://chatx.ai",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://chatx.ai/gpt",
        'accept-language': "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cookie': cookie_str
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=90)
        if response.status_code == 200:
            data = response.json()
            if data.get("response") and "image_url" in data:
                return data["image_url"]
    except Exception as e:
        print(f"Error generating image: {e}")
    
    return None

def download_image(image_url, prefix=""):
    """تحميل الصورة"""
    try:
        response = requests.get(image_url, stream=True, timeout=30)
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/{prefix}_{timestamp}.png"
            
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Error downloading image: {e}")
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
🎨 **بوت إنشاء وتعديل الصور باستخدام الذكاء الاصطناعي - aras.ai**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("‹ : إنشاء صورة جديدة 🎚 : ›", data="create_image", style="primary"), 
        Button.inline("‹ :🪞 تعديـل صـوره : ›", data="edit_image", style="primary"),
    ],
    [
        Button.url("‹ : 𝗌ᴏᴜʀᴄᴇ ᴀʀʀᴀ𝗌 : ›", "https://t.me/Lx5x5", style="danger")
    ]
]

# ========== تخزين الحالات الجارية ==========
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None
        self.photo_paths = []

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        session = user_sessions[user_id]
        for path in session.photo_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
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
    session.photo_paths = []
    
    await safe_edit(
        event,
        "**✍️ أرسل وصف الصورة التي تريد إنشاءها:**\n\n"
        "مثال: `قطة ترتدي نظارة شمسية`\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية"
    )

# ========== زر تعديل صورة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"edit_image")))
async def edit_image_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_photos'
    session.photo_paths = []
    
    await safe_edit(
        event,
        "**📤 أرسل الصور التي تريد تعديلها (من 1 إلى 14 صورة)**\n\n"
        "📌 **طريقة الاستخدام:**\n"
        "• أرسل الصور واحدة تلو الأخرى\n"
        "• **عند الانتهاء من إرسال الصور، اكتب وصف التعديل مباشرة**\n\n"
        "مثال: `حول هذه الصور إلى طراز كرتوني`\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية"
    )

# ========== معالجة الصور ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.media))
async def handle_photo_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photos':
        if len(session.photo_paths) >= 14:
            await event.respond("**⚠️ لقد وصلت للحد الأقصى (14 صورة)!\nالآن أرسل وصف التعديل مباشرة**")
            session.state = 'waiting_prompt_edit'
            return
        
        photo_path = await event.download_media(file="temp_images/")
        session.photo_paths.append(photo_path)
        
        remaining = 14 - len(session.photo_paths)
        await event.respond(f"**✅ تم استلام الصورة رقم {len(session.photo_paths)}**\n📸 متبقي: {remaining} صورة\n\n"
                           f"• أرسل المزيد من الصور (حتى 14)\n"
                           f"• **أو اكتب وصف التعديل الآن للبدء**")

# ========== معالجة النصوص ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and not x.media))
async def handle_text_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    text = event.text.strip()
    
    if text.startswith('/'):
        return
    
    # إنشاء صورة جديدة
    if session.state == 'waiting_prompt':
        if not text or len(text) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        await event.respond("**⏳ جاري إنشاء الصورة... انتظر قليلاً**")
        
        image_url = generate_image(text, TOKEN, COOKIE_STR)
        
        if image_url:
            filename = download_image(image_url, f"create_{user_id}")
            if filename:
                await bot.send_file(event.chat_id, filename, 
                                  caption=f"**✅ تم إنشاء الصورة بنجاح!**\n📝 **الوصف:** {text}")
                os.remove(filename)
            else:
                await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في إنشاء الصورة، حاول مرة أخرى**", buttons=keyboard)
        
        clear_user_session(user_id)
    
    # تحويل تلقائي من انتظار الصور إلى تعديل
    elif session.state == 'waiting_photos':
        if session.photo_paths:
            session.state = 'waiting_prompt_edit'
            await handle_text_message(event)
        else:
            await event.respond("**❌ لم ترسل أي صورة بعد!\nأرسل الصور أولاً ثم وصف التعديل**")
    
    # تعديل الصور
    elif session.state == 'waiting_prompt_edit':
        if not session.photo_paths:
            await event.respond("**❌ لا توجد صور للتعديل!**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        if not text or len(text) < 3:
            await event.respond("**❌ وصف التعديل قصير جداً**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        await event.respond(f"**⏳ جاري معالجة {len(session.photo_paths)} صورة...**\nقد يستغرق هذا بعض الوقت، انتظر قليلاً")
        
        # رفع الصور
        uploaded_urls = []
        total = len(session.photo_paths)
        
        for idx, img_path in enumerate(session.photo_paths, 1):
            await event.respond(f"**📤 جاري رفع الصورة {idx} من {total}...**")
            uploaded = upload_image(img_path, TOKEN, COOKIE_STR)
            if uploaded:
                uploaded_urls.append(uploaded)
            
            if os.path.exists(img_path):
                try:
                    os.remove(img_path)
                except:
                    pass
        
        if not uploaded_urls:
            await event.respond("**❌ فشل في رفع الصور، تأكد من صيغتها وحاول مرة أخرى**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        images_param = ','.join(uploaded_urls)
        
        await event.respond(f"**✅ تم رفع {len(uploaded_urls)} صورة بنجاح!**\n**🎨 جاري إنشاء الصورة المعدلة...**")
        
        image_url = generate_image(text, TOKEN, COOKIE_STR, images_param)
        
        if image_url:
            filename = download_image(image_url, f"edit_{user_id}")
            if filename:
                await bot.send_file(event.chat_id, filename, 
                                  caption=f"**✅ تم تعديل الصور بنجاح!**\n📝 **التعديل:** {text}\n🖼️ **عدد الصور الأصلية:** {len(uploaded_urls)}")
                os.remove(filename)
            else:
                await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في تعديل الصور، حاول مرة أخرى**", buttons=keyboard)
        
        clear_user_session(user_id)

print("✅ تم تحميل بوت ChatX.ai بنجاح!")
