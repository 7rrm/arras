import json
import os
import re
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest

from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_whisper_callback(event):
    try:
        timestamp = event.pattern_match.group(1).decode("UTF-8")
        target_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
        
        if not target_id:
            return await event.answer("⚠️ لم يتم تعيين مستلم للهمسة", alert=True)
        
        file_path = f"./JoKeRUB/{target_id}.txt"
        
        if not os.path.exists(file_path):
            return await event.answer("❌ ملف الهمسات غير موجود", alert=True)
        
        with open(file_path, "r+") as file:
            whispers = json.load(file)
            whisper_data = whispers.get(timestamp)
            
            if not whisper_data:
                return await event.answer("❌ الهمسة غير موجودة أو منتهية الصلاحية", alert=True)
            
            user_id = event.query.user_id
            authorized_users = [target_id, Config.OWNER_ID] + Config.SUDO_USERS
            
            if user_id not in authorized_users:
                return await event.answer("🚫 ليس لديك صلاحية لرؤية هذه الهمسة", alert=True)
            
            # عرض محتوى الهمسة
            await event.answer(whisper_data["text"], alert=True)
            
            # إذا كان المستخدم هو المرسل إليه الرئيسي ولم تقرأ بعد
            if user_id == target_id and not whisper_data.get("read", False):
                # تحديث حالة القراءة
                whisper_data["read"] = True
                whispers[timestamp] = whisper_data
                
                # تحديث الملف
                file.seek(0)
                json.dump(whispers, file, indent=4)
                file.truncate()
                
                # تحرير الرسالة الأصلية
                try:
                    target_user = await l313l.get_entity(target_id)
                    target_name = target_user.first_name
                    
                    new_text = (
                        f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                        f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                        f"⌔╎تم قراءة الهمسة من قبل {target_name}\n"
                        f"⌔╎هو فقط من يستطيع ࢪؤيتهـا"
                    )
                    
                    new_buttons = [
                        [Button.switch_inline("اضغـط للـرد", query=f"secret {target_id} ", same_peer=True)]
                    ]
                    
                    await event.edit(
                        text=new_text,
                        buttons=new_buttons,
                        link_preview=False
                    )
                except Exception as edit_error:
                    LOGS.error(f"فشل في تعديل الرسالة: {edit_error}")
                    
    except Exception as e:
        LOGS.error(f"خطأ في معالجة الهمسة: {e}")
        await event.answer("⚠️ حدث خطأ أثناء معالجة الهمسة", alert=True)
