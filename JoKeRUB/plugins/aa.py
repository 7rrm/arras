from telethon.tl.functions.messages import SetChatWallPaperRequest
from telethon.tl.types import InputWallPaper, WallPaperSettings, InputDocument
import requests
import os

async def set_blurred_wallpaper_auto(client, peer):
    """
    طريقة بديلة لتعيين الخلفية
    """
    try:
        wallpaper_url = "https://graph.org/file/eff529df26a96f563829a-f6422391f7f002cd3a.jpg"
        
        # تحميل الصورة
        response = requests.get(wallpaper_url)
        if response.status_code != 200:
            return False
        
        # حفظ مؤقت
        temp_file = "temp_wall.jpg"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # محاولة برفع الصورة كملف وسائط أولاً
        message = await client.send_file(peer, temp_file)
        
        # ثم استخدام SetChatWallPaperRequest
        await client(SetChatWallPaperRequest(
            peer=peer,
            wallpaper=InputWallPaper(
                id=0,
                access_hash=0
            ),
            settings=WallPaperSettings(
                blur=True,
                motion=False,
                background_color=0x000000,
                intensity=70
            )
        ))
        
        # حذف الرسالة المؤقتة والملف
        await message.delete()
        os.remove(temp_file)
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False


@l313l.on(events.NewMessage(incoming=True))
async def auto_wallpaper_on_private_message(event):
    """
    تعيين خلفية تلقائية مع ضبابية عند استقبال رسالة خاصة
    """
    # التحقق من أن المرسل ليس البوت نفسه
    if event.sender_id == (await event.client.get_me()).id:
        return
    
    # التحقق من أن الرسالة في دردشة خاصة
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
