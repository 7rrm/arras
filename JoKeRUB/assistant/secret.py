import json
import os
import re
from datetime import datetime
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.messages import EditMessageRequest
from telethon.tl.functions.users import GetUsersRequest
from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"secret_(.*)")))
async def on_whisper_callback(event):
    try:
        timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
        whisper_owner = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
        
        if not whisper_owner:
            return await event.answer("❌ هذه الهمسة لم تعد متاحة", alert=True)

        # جلب بيانات المرسل إليه
        try:
            receiver = await event.client.get_entity(whisper_owner)
        except Exception as e:
            LOGS.error(f"Error getting receiver: {e}")
            return await event.answer("❌ خطأ في جلب بيانات المستخدم", alert=True)

        file_name = f"./JoKeRUB/{whisper_owner}.txt"
        if not os.path.exists(file_name):
            return await event.answer("❌ هذه الهمسة انتهت صلاحيتها", alert=True)

        with open(file_name, 'r') as f:
            jsondata = json.load(f)

        if str(timestamp) not in jsondata:
            return await event.answer("❌ هذه الهمسة لم تعد موجودة", alert=True)

        whisper_data = jsondata[str(timestamp)]
        allowed_users = [whisper_data["userid"], Config.OWNER_ID, receiver.id]
        
        if event.query.user_id not in allowed_users:
            return await event.answer("🔒 هذه الهمسة ليست لك!", alert=True)

        # عرض المحتوى للمستخدم
        await event.answer(whisper_data["text"], alert=True)

        # إذا كان المستخدم هو المرسل إليه (وليست للمالك أو السودو)
        if event.query.user_id == whisper_data["userid"] and event.query.user_id not in [Config.OWNER_ID] + Config.SUDO_USERS:
            # نص الرسالة بعد القراءة
            read_text = (
                f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                f"✅ تم قراءة الهمسة من قبل: {receiver.first_name}\n"
                f"⏰ في: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"✉️ المحتوى: {whisper_data['text']}"
            )
            
            # الأزرار الجديدة (زر الرد فقط)
            new_buttons = [
                [Button.switch_inline("↩️ رد على الهمسة", query=f"secret {whisper_owner} \nرد: ", same_peer=True)]
            ]
            
            try:
                await event.client(EditMessageRequest(
                    peer=await event.get_input_chat(),
                    id=event.query.msg_id,
                    message=read_text,
                    buttons=new_buttons
                ))
            except Exception as e:
                LOGS.error(f"Error editing message: {e}")
                # محاولة بدون أزرار إذا فشلت
                try:
                    await event.client(EditMessageRequest(
                        peer=await event.get_input_chat(),
                        id=event.query.msg_id,
                        message=read_text
                    ))
                except Exception as e2:
                    LOGS.error(f"Error in simple edit: {e2}")

    except Exception as main_error:
        LOGS.error(f"Error in whisper callback: {main_error}")
        await event.answer("⚠
