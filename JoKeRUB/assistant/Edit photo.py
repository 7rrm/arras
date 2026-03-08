from JoKeRUB import bot, l313l
from telethon import events, Button
from datetime import datetime
from JoKeRUB.utils import admin_cmd
from ..Config import Config
import os, re, requests, json, time, asyncio
import logging

logging.getLogger().setLevel(logging.WARNING)

# ========== API القديم ==========
API_BASE_URL = "https://viscodev.x10.mx/nano/nano-banana.php"

# مفتاح ImgBB
IMGBB_KEY = "fdc56ddf64d2f3d3294433761930349f"

# إعدادات الملفات
os.makedirs("temp_images", exist_ok=True)

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "NanoBananaBot"

# ========== تخزين الحالات الجارية ==========
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None
        self.prompt = None
        self.image_url = None
        self.message_id = None

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]

async def safe_edit(event, text, buttons=None):
    """تعديل الرسالة بأمان"""
    try:
        if buttons:
            await event.edit(text, buttons=buttons)
        else:
            await event.edit(text)
    except:
        try:
            if buttons:
                await event.respond(text, buttons=buttons)
            else:
                await event.respond(text)
        except:
            pass

async def safe_delete(msg):
    """حذف الرسالة بأمان"""
    try:
        await msg.delete()
    except:
        pass

# ========== دالة رفع الصور لـ ImgBB ==========
def upload_to_imgbb(image_path):
    """رفع الصورة إلى ImgBB"""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                data={'key': IMGBB_KEY},
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data['data']['url']
    except:
        pass
    return None

# ========== القائمة والأزرار ==========
menu = '''
🎨 **بوت إنشاء وتعديل الصور**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("🎨 إنشاء صورة", data="create_image"), 
        Button.inline("✏️ تعديل صورة", data="edit_image"),
    ],
    [
        Button.url("المـطور", "https://t.me/Lx5x5")
    ]
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
                title="🎨 بوت الصور",
                description="اضغط للدخول إلى بوت الصور",
                text="**🎨 قم بالضغط على الزر لبدء الاستخدام**",
                buttons=buttons
            )
        await event.answer([result] if result else None)

# الأمر .صور
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
    clear_user_session(user_id)
    await event.respond("✅ تم إلغاء العملية", buttons=keyboard)

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
        "✍️ أرسل وصف الصورة التي تريد إنشاءها:\n\n"
        "مثال: `منظر طبيعي مع جبال`\n\n"
        "أو /cancel للإلغاء"
    )

# ========== معالجة الإنشاء ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid))
async def handle_create_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt':
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("❌ الوصف قصير جداً", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        waiting_msg = await event.respond("⏳ جاري إنشاء الصورة...")
        session.message_id = waiting_msg.id
        
        try:
            response = requests.get(
                API_BASE_URL,
                params={
                    'mode': 'create',
                    'prompt': prompt
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    await safe_delete(waiting_msg)
                    
                    await bot.send_file(
                        event.chat_id,
                        result['url'],
                        caption=f"✅ تم إنشاء الصورة بنجاح!"
                    )
                    
                    after_buttons = [
                        [Button.inline("🔄 إنشاء مرة أخرى", data="create_image")],
                        [Button.inline("✏️ تعديل صورة", data="edit_image")],
                        [Button.inline("🏠 القائمة الرئيسية", data="back_to_menu")]
                    ]
                    await event.respond("ماذا تريد أن تفعل الآن؟", buttons=after_buttons)
                else:
                    await waiting_msg.edit("❌ فشل في إنشاء الصورة")
            else:
                await waiting_msg.edit(f"❌ خطأ في الاتصال: {response.status_code}")
        
        except Exception as e:
            await waiting_msg.edit(f"❌ حدث خطأ: {str(e)}")
        
        clear_user_session(user_id)

# ========== زر تعديل صورة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"edit_image")))
async def edit_image_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_photo'
    
    await safe_edit(
        event,
        "📸 أرسل الصورة التي تريد تعديلها:\n\n"
        "أو /cancel للإلغاء"
    )

# ========== معالجة استقبال الصورة ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.media))
async def handle_photo_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photo':
        if event.photo:
            photo_path = await event.download_media(file="temp_images/")
            imgbb_url = upload_to_imgbb(photo_path)
            
            if os.path.exists(photo_path):
                os.remove(photo_path)
            
            if imgbb_url:
                session.image_url = imgbb_url
                session.state = 'waiting_prompt_edit'
                
                await event.respond(
                    "✅ تم استلام ورفع الصورة بنجاح!\n\n"
                    "✏️ أرسل التعديل الذي تريده:\n\n"
                    "مثال: `حولها إلى لوحة زيتية`\n\n"
                    "أو /cancel للإلغاء"
                )
            else:
                await event.respond("❌ فشل في رفع الصورة. حاول مرة أخرى")
        else:
            await event.respond("❌ الرجاء إرسال صورة فقط")

# ========== معالجة التعديل ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and not x.media))
async def handle_edit_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt_edit' and session.image_url:
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("❌ الوصف قصير جداً", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        waiting_msg = await event.respond("⏳ جاري تعديل الصورة...")
        session.message_id = waiting_msg.id
        
        try:
            response = requests.get(
                API_BASE_URL,
                params={
                    'mode': 'edit',
                    'prompt': prompt,
                    'image': session.image_url
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    await safe_delete(waiting_msg)
                    
                    await bot.send_file(
                        event.chat_id,
                        result['url'],
                        caption=f"✅ تم تعديل الصورة بنجاح!"
                    )
                    
                    after_buttons = [
                        [Button.inline("🔄 تعديل صورة أخرى", data="edit_image")],
                        [Button.inline("🎨 إنشاء صورة", data="create_image")],
                        [Button.inline("🏠 القائمة الرئيسية", data="back_to_menu")]
                    ]
                    await event.respond("ماذا تريد أن تفعل الآن؟", buttons=after_buttons)
                else:
                    await waiting_msg.edit("❌ فشل في تعديل الصورة")
            else:
                await waiting_msg.edit(f"❌ خطأ في الاتصال: {response.status_code}")
        
        except Exception as e:
            await waiting_msg.edit(f"❌ حدث خطأ: {str(e)}")
        
        clear_user_session(user_id)

print("✅ تم تحميل بوت الصور بنجاح!")
