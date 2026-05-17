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

# ========== دوال ChatX.ai ==========
class ChatXAPI:
    def __init__(self):
        self.base_url = "https://chatx.ai"
        self.session = requests.Session()
        self.token = None
        self.cookie_str = None
        self.guest_token = None
        
    def get_fresh_tokens(self):
        """الحصول على توكنات جديدة من الموقع"""
        try:
            url_main = f"{self.base_url}/ai-image"
            headers_main = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': "?1",
                'sec-ch-ua-platform': '"Android"',
                'upgrade-insecure-requests': "1",
                'referer': "https://chatx.ai/",
                'accept-language': "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            }
            
            response = self.session.get(url_main, headers=headers_main, timeout=15)
            cookies = self.session.cookies.get_dict()
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_csrf = soup.find('meta', attrs={'name': 'csrf-token'})
            
            if meta_csrf:
                self.token = meta_csrf.get('content')
            
            self.cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            self.guest_token = cookies.get('chatx_guest_token', '')
            
            return self.token is not None
            
        except Exception as e:
            print(f"Error getting tokens: {e}")
            return False
    
    def generate_user_id(self):
        """توليد معرف مستخدم عشوائي"""
        base_id = self.guest_token[:-3] if len(self.guest_token) >= 3 else "406994179"
        new_last_three = str(random.randint(0, 999)).zfill(3)
        return base_id + new_last_three
    
    def upload_image(self, image_path):
        """رفع صورة إلى السيرفر"""
        if not os.path.exists(image_path):
            return None
        
        if not self.token:
            self.get_fresh_tokens()
        
        url = f"{self.base_url}/uploadImage"
        file_name = os.path.basename(image_path)
        
        payload = {
            '_token': self.token,
            'user_id': '[object HTMLInputElement]',
            'chats_id': '[object HTMLInputElement]',
            'current_model': '[object HTMLInputElement]'
        }
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'x-csrf-token': self.token,
            'x-requested-with': "XMLHttpRequest",
            'origin': "https://chatx.ai",
            'referer': "https://chatx.ai/gpt",
            'accept-language': "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cookie': self.cookie_str
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
        except Exception as e:
            print(f"Error uploading image: {e}")
        
        return None
    
    def generate_image(self, prompt, image_urls=None):
        """إنشاء صورة جديدة أو تعديلها"""
        if not self.token:
            self.get_fresh_tokens()
        
        user_id = self.generate_user_id()
        
        url = f"{self.base_url}/generateImage"
        
        payload = {
            '_token': self.token,
            'user_id': user_id,
            'chats_id': "45762416",
            'prompt': prompt,
            'current_model': "gpt3",
            'images': image_urls or "",
            'mask_image': "",
            'image_size': "auto",
            'image_quality': "auto",
            'image_type': "jpeg",
            'image_transparency': "auto",
            'gpt_image_model': "nano_2",
            'nano_aspect_ratio': "1:1"
        }
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'x-csrf-token': self.token,
            'x-requested-with': "XMLHttpRequest",
            'origin': "https://chatx.ai",
            'referer': "https://chatx.ai/gpt",
            'accept-language': "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cookie': self.cookie_str
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
🎨 **بوت إنشاء وتعديل الصور باستخدام الذكاء الاصطناعي - ChatX.ai**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("‹ : إنشاء صورة جديدة 🎚 : ›", data="create_image"), 
        Button.inline("‹ :🪞 تعديل صوره : ›", data="edit_image"),
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
        self.photo_paths = []  # قائمة بمسارات الصور المرفوعة

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        session = user_sessions[user_id]
        # تنظيف الملفات المؤقتة
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
    
    await safe_edit(
        event,
        "**✍️ أرسل وصف الصورة التي تريد إنشاءها:**\n\n"
        "مثال: `قطة ترتدي نظارة شمسية`\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية"
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
        
        await event.respond("**⏳ جاري إنشاء الصورة... انتظر قليلاً**")
        
        # إنشاء API
        api = ChatXAPI()
        
        # إنشاء الصورة
        image_url = api.generate_image(prompt)
        
        if image_url:
            filename = download_image(image_url, f"create_{user_id}")
            if filename:
                await bot.send_file(event.chat_id, filename, 
                                  caption=f"**✅ تم إنشاء الصورة بنجاح!**\n📝 **الوصف:** {prompt}")
                os.remove(filename)
            else:
                await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في إنشاء الصورة، حاول مرة أخرى**", buttons=keyboard)
        
        clear_user_session(user_id)

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
        "• سيتم إعلامك بعدد الصور المستلمة\n"
        "• عندما تنتهي من إرسال الصور، أرسل كلمة `done`\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية"
    )

# ========== معالجة الصور ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.media))
async def handle_photo_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photos':
        if len(session.photo_paths) >= 14:
            await event.respond("**⚠️ لقد وصلت للحد الأقصى (14 صورة)!\nأرسل `done` للانتقال إلى الوصف**")
            return
        
        photo_path = await event.download_media(file="temp_images/")
        session.photo_paths.append(photo_path)
        
        remaining = 14 - len(session.photo_paths)
        await event.respond(f"**✅ تم استلام الصورة رقم {len(session.photo_paths)}**\n"
                           f"📸 متبقي: {remaining} صورة\n\n"
                           "أرسل `done` عند الانتهاء من إرسال الصور")

# ========== إنهاء استلام الصور ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.text and x.text.lower() == "done"))
async def handle_done_photos(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photos':
        if not session.photo_paths:
            await event.respond("**❌ لم ترسل أي صورة بعد!\nأرسل الصور أولاً ثم `done`**")
            return
        
        session.state = 'waiting_prompt_edit'
        await event.respond(f"**✅ تم استلام {len(session.photo_paths)} صورة بنجاح!**\n\n"
                           "**✍️ الآن أرسل وصف التعديل المطلوب:**\n\n"
                           "مثال: `حول هذه الصور إلى طراز كرتوني`\n"
                           "أو: `أضف خلفية شاطئ بحر إلى هذه الصور`\n\n"
                           "يمكنك إرسال `/cancel` لإلغاء العملية")

# ========== معالجة وصف التعديل ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and not x.media))
async def handle_edit_prompt_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/') or event.text.lower() == 'done':
        return
    
    if session.state == 'waiting_prompt_edit' and session.photo_paths:
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        await event.respond(f"**⏳ جاري معالجة {len(session.photo_paths)} صورة...**\n"
                           "قد يستغرق هذا بعض الوقت، انتظر قليلاً")
        
        # إنشاء API
        api = ChatXAPI()
        
        if not api.get_fresh_tokens():
            await event.respond("**❌ فشل في الاتصال بالموقع**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # رفع الصور أولاً
        uploaded_urls = []
        total = len(session.photo_paths)
        
        for idx, img_path in enumerate(session.photo_paths, 1):
            await event.respond(f"**📤 جاري رفع الصورة {idx} من {total}...**")
            uploaded = api.upload_image(img_path)
            if uploaded:
                uploaded_urls.append(uploaded)
            
            # تنظيف الملف المؤقت
            if os.path.exists(img_path):
                try:
                    os.remove(img_path)
                except:
                    pass
        
        if not uploaded_urls:
            await event.respond("**❌ فشل في رفع الصور، تأكد من صيغتها وحاول مرة أخرى**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # دمج روابط الصور
        images_param = ','.join(uploaded_urls)
        
        await event.respond(f"**✅ تم رفع {len(uploaded_urls)} صورة بنجاح!**\n"
                           "**🎨 جاري إنشاء الصورة المعدلة...**")
        
        # إنشاء الصورة المعدلة
        image_url = api.generate_image(prompt, images_param)
        
        if image_url:
            filename = download_image(image_url, f"edit_{user_id}")
            if filename:
                await bot.send_file(event.chat_id, filename, 
                                  caption=f"**✅ تم تعديل الصور بنجاح!**\n"
                                         f"📝 **التعديل:** {prompt}\n"
                                         f"🖼️ **عدد الصور الأصلية:** {len(uploaded_urls)}")
                os.remove(filename)
            else:
                await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في تعديل الصور، حاول مرة أخرى**", buttons=keyboard)
        
        clear_user_session(user_id)

print("✅ تم تحميل بوت ChatX.ai بنجاح!")
