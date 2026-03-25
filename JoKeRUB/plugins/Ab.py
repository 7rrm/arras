import os
from pathlib import Path
from telethon.tl.types import InputPeerChannel, InputMessagesFilterDocument
from . import l313l
from ..Config import Config

# إعدادات الوجهة
TO_CHAT_ID = 5427469031  # ضع معرف المحادثة/القناة هنا

if Config.ZELZAL_A:
    async def download_and_send():
        # جلب معلومات القناة المصدر
        entity = await l313l.get_entity(Config.ZELZAL_A)
        
        # جلب جميع الملفات
        messages = await l313l.get_messages(entity, None, filter=InputMessagesFilterDocument)
        
        print(f"📁 تم العثور على {messages.total} ملف")
        
        for msg in messages:
            try:
                file_name = msg.file.name
                print(f"📥 تحميل: {file_name}")
                
                # تحميل الملف
                file_path = await l313l.download_media(msg, "downloads/")
                
                # إرسال الملف
                await l313l.send_file(TO_CHAT_ID, file_path, caption=f"ملف: {file_name}")
                
                # حذف الملف المحلي
                os.remove(file_path)
                
                print(f"✅ تم إرسال: {file_name}")
                
            except Exception as e:
                print(f"❌ خطأ في {file_name}: {e}")
    
    l313l.loop.create_task(download_and_send())
