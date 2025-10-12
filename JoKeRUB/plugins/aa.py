import os
import requests
from telethon.tl.functions.messages import SetChatWallPaperRequest
from telethon.tl.types import InputWallPaper, InputWallPaperSlug, WallPaperSettings
from telethon import events

# رابط الصورة التي تريد استخدامها كخلفية
WALLPAPER_URL = "https://graph.org/file/eff529df26a96f563829a-f6422391f7f002cd3a.jpg"
WALLPAPER_PATH = "chat_wallpaper.jpg"

async def download_wallpaper():
    """تحميل الصورة من الرابط"""
    try:
        response = requests.get(WALLPAPER_URL, stream=True)
        if response.status_code == 200:
            with open(WALLPAPER_PATH, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"خطأ في تحميل الصورة: {e}")
    return False

@l313l.on(events.NewMessage(incoming=True))
async def auto_set_wallpaper(event):
    """تغيير خلفية المحادثة تلقائياً عند استقبال رسالة جديدة"""
    
    # التأكد من أن الرسالة من مستخدم وليست من قناة أو مجموعة
    if not event.is_private:
        return
    
    # تجنب الرد على الرسائل من البوت نفسه
    if event.sender_id == (await event.client.get_me()).id:
        return
    
    try:
        # تحميل الصورة إذا لم تكن موجودة
        if not os.path.exists(WALLPAPER_PATH):
            success = await download_wallpaper()
            if not success:
                return
        
        # الحصول على كيان المحادثة
        chat = await event.get_chat()
        
        # رفع الصورة كملف
        uploaded_file = await event.client.upload_file(WALLPAPER_PATH)
        
        # إعدادات الخلفية
        wallpaper_settings = WallPaperSettings(
            blur=False,  # إزالة التشويش إذا كنت تريده
            motion=False,
            background_color=0,
            intensity=0,
            second_background_color=0,
            third_background_color=0,
            fourth_background_color=0,
        )
        
        # طلب تغيير خلفية المحادثة
        await event.client(SetChatWallPaperRequest(
            peer=chat,
            wallpaper=InputWallPaper(
                id=0,
                access_hash=0,
                slug="custom_wallpaper"
            ),
            settings=wallpaper_settings,
            file=uploaded_file
        ))
        
        # طباعة رسالة تأكيد (اختياري)
        print(f"✓ تم تغيير خلفية المحادثة مع {chat.first_name if chat.first_name else 'مستخدم'}")
        
    except Exception as e:
        print(f"خطأ في تعيين الخلفية: {e}")

# أمر يدوي لتغيير الخلفية
@l313l.ar_cmd(pattern="خلفية(?:\s|$)([\s\S]*)")
async def set_wallpaper_manual(event):
    """أمر يدوي لتغيير خلفية المحادثة الحالية"""
    try:
        # تحميل الصورة إذا لم تكن موجودة
        if not os.path.exists(WALLPAPER_PATH):
            success = await download_wallpaper()
            if not success:
                await edit_or_reply(event, "**❌ فشل في تحميل الصورة**")
                return
        
        chat = await event.get_chat()
        uploaded_file = await event.client.upload_file(WALLPAPER_PATH)
        
        wallpaper_settings = WallPaperSettings(
            blur=False,
            motion=False,
            background_color=0,
            intensity=0,
            second_background_color=0,
            third_background_color=0,
            fourth_background_color=0,
        )
        
        await event.client(SetChatWallPaperRequest(
            peer=chat,
            wallpaper=InputWallPaper(
                id=0,
                access_hash=0,
                slug="custom_wallpaper"
            ),
            settings=wallpaper_settings,
            file=uploaded_file
        ))
        
        await edit_or_reply(event, "**✓ تم تغيير خلفية المحادثة بنجاح**")
        
    except Exception as e:
        await edit_or_reply(event, f"**❌ خطأ في تعيين الخلفية:** `{str(e)}`")

# أمر لتعطيل/تفعيل الميزة
@l313l.ar_cmd(pattern="(تفعيل الخلفية|تعطيل الخلفية)")
async def toggle_auto_wallpaper(event):
    """تفعيل أو تعطيل تغيير الخلفية التلقائي"""
    command = event.pattern_match.group(1)
    
    if command == "تفعيل الخلفية":
        addgvar("auto_wallpaper", "on")
        await edit_or_reply(event, "**✓ تم تفعيل تغيير الخلفية التلقائي**")
    else:
        delgvar("auto_wallpaper")
        await edit_or_reply(event, "**✓ تم تعطيل تغيير الخلفية التلقائي**")

# تحديث الدالة الرئيسية للتحقق من التفعيل
@l313l.on(events.NewMessage(incoming=True))
async def auto_set_wallpaper(event):
    """تغيير خلفية المحادثة تلقائياً مع التحقق من التفعيل"""
    
    # التحقق من تفعيل الميزة
    if not gvarstatus("auto_wallpaper"):
        return
    
    # التأكد من أن الرسالة من مستخدم وليست من قناة أو مجموعة
    if not event.is_private:
        return
    
    # تجنب الرد على الرسائل من البوت نفسه
    if event.sender_id == (await event.client.get_me()).id:
        return
    
    try:
        # تحميل الصورة إذا لم تكن موجودة
        if not os.path.exists(WALLPAPER_PATH):
            success = await download_wallpaper()
            if not success:
                return
        
        # الحصول على كيان المحادثة
        chat = await event.get_chat()
        
        # رفع الصورة كملف
        uploaded_file = await event.client.upload_file(WALLPAPER_PATH)
        
        # إعدادات الخلفية
        wallpaper_settings = WallPaperSettings(
            blur=False,
            motion=False,
            background_color=0,
            intensity=0,
            second_background_color=0,
            third_background_color=0,
            fourth_background_color=0,
        )
        
        # طلب تغيير خلفية المحادثة
        await event.client(SetChatWallPaperRequest(
            peer=chat,
            wallpaper=InputWallPaper(
                id=0,
                access_hash=0,
                slug="custom_wallpaper"
            ),
            settings=wallpaper_settings,
            file=uploaded_file
        ))
        
    except Exception as e:
        print(f"خطأ في تعيين الخلفية: {e}")
