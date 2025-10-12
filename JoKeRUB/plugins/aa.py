from telethon.tl.functions.messages import SetChatWallPaperRequest
from telethon.tl.types import InputWallPaper, WallPaperSettings, InputDocument
import requests
import os

async def set_blurred_wallpaper_auto(client, peer):
    """
    تعيين الخلفية مع ضبابية تلقائياً لأي شخص يراسلك
    """
    try:
        # رابط الصورة الثابت
        wallpaper_url = "https://graph.org/file/eff529df26a96f563829a-f6422391f7f002cd3a.jpg"
        
        # تحميل الصورة من الرابط
        response = requests.get(wallpaper_url)
        if response.status_code != 200:
            print("❌ فشل في تحميل الصورة")
            return False
        
        # حفظ الصورة مؤقتاً
        temp_file = "temp_auto_wallpaper.jpg"
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        # رفع الصورة كملف
        uploaded_file = await client.upload_file(temp_file)
        
        # استخدام InputWallPaper مباشرة
        await client(SetChatWallPaperRequest(
            peer=peer,
            wallpaper=InputWallPaper(
                id=0,  # استخدام 0 للصور المرفوعة حديثاً
                access_hash=0
            ),
            settings=WallPaperSettings(
                blur=True,        # ✅ تفعيل الضبابية
                motion=False,
                background_color=0x000000,
                intensity=70      # ✅ شدة الضبابية
            )
        ))
        
        # حذف الملف المؤقت
        os.remove(temp_file)
        print("✅ تم تعيين الخلفية بنجاح")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تعيين الخلفية: {e}")
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
