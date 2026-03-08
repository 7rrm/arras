
from JoKeRUB import bot, l313l
# By Source joker @ucriss
from telethon import events, functions, types, Button
from datetime import datetime, timedelta
from JoKeRUB.utils import admin_cmd
import asyncio
from ..Config import Config
import os
import re
import traceback
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
from telethon.tl.functions.channels import CreateChannelRequest as ccr
from telethon import Button, events
import aiohttp
import random
import json
import requests
import time
import logging

logging.getLogger().setLevel(logging.WARNING)

# ========== API ==========
# هنا تستخدم أي API تريد (قديم أو جديد)
API_BASE_URL = "https://viscodev.x10.mx/nano/nano-banana.php"  # أو nanabanana.ai

# إعدادات الملفات
os.makedirs("generated_images", exist_ok=True)

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "NanoBananaBot"

# ========== تخزين الحالات الجارية ==========
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None
        self.prompt = None
        self.image_path = None  # مسار الصورة المحلي
        self.image_url = None    # رابط الصورة (للتعديل بالرابط)

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        if user_sessions[user_id].image_path and os.path.exists(user_sessions[user_id].image_path):
            try:
                os.remove(user_sessions[user_id].image_path)
            except:
                pass
        del user_sessions[user_id]

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
    session = get_user_session(user_id)
    
    if session.state:
        clear_user_session(user_id)
        await event.respond("✅ تم إلغاء العملية", buttons=keyboard)
    else:
        await event.respond("⚠️ لا توجد عملية جارية", buttons=keyboard)

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
            await event.respond("❌ الوصف قصير جداً", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        waiting_msg = await event.respond("⏳ جاري إنشاء الصورة...")
        
        try:
            # استدعاء API الإنشاء
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
                    await waiting_msg.delete()
                    
                    # إرسال الصورة
                    await bot.send_file(
                        event.chat_id,
                        result['url'],
                        caption=f"✅ تم إنشاء الصورة بنجاح!\n\n📝 الوصف: {prompt}"
                    )
                    
                    # أزرار إضافية
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
    session.state = 'waiting_image'
    
    keyboard_edit = [
        [Button.inline("🔗 إرسال رابط", data="send_link")],
        [Button.inline("📸 إرسال صورة", data="send_photo")],
        [Button.inline("🔙 رجوع", data="back_to_menu")]
    ]
    
    await safe_edit(
        event,
        "اختر طريقة إرسال الصورة:",
        buttons=keyboard_edit
    )

# ========== اختيار طريقة الإرسال ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"send_link")))
async def send_link_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_link'
    
    await safe_edit(
        event,
        "🔗 أرسل رابط الصورة التي تريد تعديلها:\n\n"
        "مثال: `https://example.com/image.jpg`\n\n"
        "أو /cancel للإلغاء"
    )

@tgbot.on(events.CallbackQuery(data=re.compile(b"send_photo")))
async def send_photo_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_photo'
    
    await safe_edit(
        event,
        "📸 أرسل الصورة التي تريد تعديلها:\n\n"
        "أو /cancel للإلغاء"
    )

# ========== معالجة الرابط ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid))
async def handle_link_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    text = event.text
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_link':
        if text.startswith(('http://', 'https://')):
            session.image_url = text
            session.state = 'waiting_edit_prompt_link'
            await event.respond(
                "✏️ أرسل التعديل الذي تريده على الصورة:\n\n"
                "مثال: `حولها إلى لوحة زيتية`\n\n"
                "أو /cancel للإلغاء"
            )
        else:
            await event.respond("❌ الرجاء إرسال رابط صحيح يبدأ بـ http:// أو https://")

# ========== معالجة الصورة المرفوعة ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.media))
async def handle_photo_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photo':
        # تحميل الصورة محلياً
        photo_path = await event.download_media(file="temp_images/")
        session.image_path = photo_path
        session.state = 'waiting_edit_prompt_photo'
        
        await event.respond(
            "✅ تم استلام الصورة!\n\n"
            "✏️ أرسل التعديل الذي تريده:\n\n"
            "مثال: `اجعلها بالأبيض والأسود`\n\n"
            "أو /cancel للإلغاء"
        )

# ========== معالجة التعديل (لرابط) ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid))
async def handle_edit_link_prompt(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_edit_prompt_link' and session.image_url:
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("❌ الوصف قصير جداً", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        waiting_msg = await event.respond("⏳ جاري تعديل الصورة...")
        
        try:
            # استدعاء API التعديل بالرابط
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
                    await waiting_msg.delete()
                    
                    await bot.send_file(
                        event.chat_id,
                        result['url'],
                        caption=f"✅ تم تعديل الصورة بنجاح!\n\n✏️ التعديل: {prompt}"
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

# ========== معالجة التعديل (للصورة المرفوعة) ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid))
async def handle_edit_photo_prompt(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_edit_prompt_photo' and session.image_path:
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("❌ الوصف قصير جداً", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        waiting_msg = await event.respond("⏳ جاري تعديل الصورة...")
        
        try:
            # استدعاء API التعديل بمسار الصورة المحلي (نفس طريقة الكود الصغير)
            # API المفروض يدعم استقبال مسار الملف المحلي من تليجرام
            response = requests.get(
                API_BASE_URL,
                params={
                    'mode': 'edit',
                    'prompt': prompt,
                    'image': session.image_path  # نفس الطريقة: نرسل المسار المحلي
                },
                timeout=60
            )
            
            # تنظيف الملف المؤقت
            if os.path.exists(session.image_path):
                try:
                    os.remove(session.image_path)
                except:
                    pass
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    await waiting_msg.delete()
                    
                    await bot.send_file(
                        event.chat_id,
                        result['url'],
                        caption=f"✅ تم تعديل الصورة بنجاح!\n\n✏️ التعديل: {prompt}"
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
            # تنظيف في حالة الخطأ
            if os.path.exists(session.image_path):
                try:
                    os.remove(session.image_path)
                except:
                    pass
        
        clear_user_session(user_id)

print("✅ تم تحميل بوت الصور بنجاح مع دعم رفع الصور المباشر!")
