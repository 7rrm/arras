import json
import os
import re
import time
from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.users import GetUsersRequest

from . import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# تعريف النصوص الثابتة
WHISPER_DATA = {
    "secret": "secret",
    "title": "همسـة",
    "description": "⌔╎هو فقط من يستطيع ࢪؤيتهـا",
    "header": "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - **همسـة سـريـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**",
    "open_btn": "فتـح الهمسـه 🗳",
    "reply_btn": "اضغـط للـرد"
}

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    try:
        builder = event.builder
        query = event.text
        query_user_id = event.query.user_id
        
        # الحصول على بيانات المرسل إليه
        target_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
        target_name = gvarstatus("hmsa_name") or "المستلم"
        target_username = gvarstatus("hmsa_user") or ""
        
        # التحقق من الصلاحيات
        is_authorized = (query_user_id == Config.OWNER_ID or 
                        query_user_id in Config.SUDO_USERS or 
                        query_user_id == target_id)
        
        if not is_authorized:
            return
        
        # معالجة أمر الهمسة
        if query.startswith("secret "):
            parts = query.split(" ", 2)
            if len(parts) < 3:
                return
                
            recipients, message = parts[1], parts[2]
            
            # معالجة متعددة للمستلمين
            if "|" in recipients:
                recipients = recipients.replace(" |", "|").replace("| ", "|").split("|")
            else:
                recipients = [recipients]
            
            users_info = []
            user_ids = []
            
            for recipient in recipients:
                try:
                    user = await l313l.get_entity(recipient)
                    users_info.append(f"@{user.username}" if user.username else f"[{user.first_name}](tg://user?id={user.id})")
                    user_ids.append(user.id)
                except Exception as e:
                    LOGS.error(f"Error getting user: {e}")
                    continue
            
            if not users_info:
                return
                
            users_str = " ".join(users_info)
            
            # حفظ الهمسة
            timestamp = int(time.time() * 2)
            whisper_data = {
                "userid": user_ids,
                "text": message,
                "read": False,
                "timestamp": timestamp
            }
            
            # حفظ في ملف
            os.makedirs("./JoKeRUB", exist_ok=True)
            file_path = f"./JoKeRUB/{target_id}.txt"
            
            all_whispers = {}
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    all_whispers = json.load(f)
            
            all_whispers[str(timestamp)] = whisper_data
            
            with open(file_path, "w") as f:
                json.dump(all_whispers, f, indent=4)
            
            # إنشاء الأزرار
            buttons = [
                [Button.inline(WHISPER_DATA["open_btn"], data=f"secret_{timestamp}")],
                [Button.switch_inline(WHISPER_DATA["reply_btn"], query=f"secret {target_id} ", same_peer=True)]
            ]
            
            # إرسال النتيجة
            result = builder.article(
                title=f"{WHISPER_DATA['title']} {users_str}",
                description=WHISPER_DATA["description"],
                text=f"{WHISPER_DATA['header']} {users_str} \n**{WHISPER_DATA['description']}**",
                buttons=buttons,
                link_preview=False
            )
            
            await event.answer([result])
            
        elif query.lower() == "zelzal":
            if not target_id:
                return
                
            buttons = [[Button.switch_inline(WHISPER_DATA["reply_btn"], 
                      query=f"secret {target_id} ", same_peer=True)]]
            
            result = builder.article(
                title="همسـه سريـه",
                description="ارسـال همسـه سريـه لـ (شخـص/اشخـاص).",
                text=f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎أضغـط الـزر بالأسفـل ⚓\n⌔╎لـ أࢪسـال همسـه سـريـه الى {target_name} 💌",
                buttons=buttons,
                link_preview=False
            )
            
            await event.answer([result])
            
    except Exception as e:
        LOGS.error(f"Error in inline handler: {e}")
