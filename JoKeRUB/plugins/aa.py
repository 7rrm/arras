from telethon.tl.functions.messages import SetChatWallPaperRequest
from telethon.tl.types import InputWallPaper, WallPaperSettings
from telethon.tl.types import InputDocument, DocumentAttributeFilename
import requests
import os

async def set_blurred_wallpaper_auto(client, peer):
    """
    إصفح مبسط باستخدام خلفية افتراضية من التيليجرام
    """
    try:
        # استخدام خلفية افتراضية من التيليجرام مع ضبابية
        await client(SetChatWallPaperRequest(
            peer=peer,
            wallpaper=InputWallPaper(
                id=123456789,  # ID خلفية افتراضية
                access_hash=123456789
            ),
            settings=WallPaperSettings(
                blur=True,
                motion=False,
                background_color=0x1E1E1E,  # لون رمادي غامق
                intensity=60
            )
        ))
        
        print("✅ تم تعيين الخلفية الضبابية بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        
        # محاولة بديلة باستخدام لون خلفية فقط
        try:
            await client(SetChatWallPaperRequest(
                peer=peer,
                wallpaper=InputWallPaper(
                    id=0,
                    access_hash=0
                ),
                settings=WallPaperSettings(
                    blur=False,
                    motion=False,
                    background_color=0x1E1E1E,  # لون خلفية
                    intensity=0
                )
            ))
            return True
        except:
            return False

@l313l.on(events.NewMessage(incoming=True))
async def auto_wallpaper_on_private_message(event):
    """
    تعيين خلفية تلقائية مع ضبابية عند استقبال رسالة خاصة
    """
    if event.sender_id == (await event.client.get_me()).id:
        return
    
    if event.is_private:
        try:
            print(f"🔄 محاولة تعيين خلفية لـ {event.sender_id}")
            success = await set_blurred_wallpaper_auto(
                event.client, 
                await event.get_input_chat()
            )
            
            if success:
                print(f"✅ تم تعيين خلفية ضبابية لـ {event.sender_id}")
            else:
                print(f"❌ فشل تعيين خلفية لـ {event.sender_id}")
                
        except Exception as e:
            print(f"❌ خطأ في الخلفية التلقائية: {e}")
