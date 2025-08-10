import json
import os
import re
from datetime import datetime
from telethon import events, Button
from telethon.tl.functions.users import GetUsersRequest
from telethon.utils import get_display_name

@l313l.tgbot.on(events.CallbackQuery(data=re.compile(b"secret_(.*)")))
async def secret_open_handler(event):
    # بيانات الهمسة
    timestamp = event.pattern_match.group(1).decode("UTF-8")
    sender_id = int(gvarstatus("hmsa_id"))
    
    # مسار ملف الهمسة
    secret_file = f"./JoKeRUB/{sender_id}.txt"
    
    if not os.path.exists(secret_file):
        return await event.answer("❌ هذه الهمسة لم تعد موجودة", alert=True)
    
    try:
        with open(secret_file, 'r') as f:
            secrets = json.load(f)
        
        secret_data = secrets.get(timestamp)
        if not secret_data:
            return await event.answer("❌ هذه الهمسة منتهية الصلاحية", alert=True)
        
        # التحقق من الصلاحيات
        allowed_users = [
            sender_id,  # المرسل
            Config.OWNER_ID,  # المطور
            *secret_data['userid']  # المستقبل/المستقبلين
        ]
        
        if event.query.user_id not in allowed_users:
            return await event.answer("🚫 ليس لديك صلاحية رؤية هذه الهمسة", alert=True)
        
        # عرض المحتوى للمستخدم
        await event.answer(secret_data['text'], alert=True)
        
        # إذا كان المستخدم هو المستقبل، نحدث الواجهة
        if event.query.user_id in secret_data['userid']:
            viewer = await event.get_sender()
            viewer_name = get_display_name(viewer)
            time_read = datetime.now().strftime("%I:%M %p")
            
            new_text = (
                f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                f"⌔╎الهمسـة لـ {viewer_name}\n"
                f"⌔╎تم القراءة في: {time_read}"
            )
            
            new_buttons = [
                [Button.switch_inline(
                    "↪️ اضغط للرد", 
                    query=f"secret {sender_id} \nرد على الهمسة", 
                    same_peer=True
                )]
            ]
            
            try:
                await event.edit(
                    text=new_text,
                    buttons=new_buttons
                )
            except Exception as e:
                print(f"Error updating message: {e}")
                
    except Exception as e:
        print(f"Secret error: {e}")
        await event.answer("⚠️ حدث خطأ في عرض الهمسة", alert=True)
