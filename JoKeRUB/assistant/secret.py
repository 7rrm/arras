import json
import os
import re
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import UpdateInlineBotMessageRequest
from telethon.tl.types import InputBotInlineMessageID
from telethon.errors import MessageNotModifiedError

from JoKeRUB import l313l
from ..Config import Config
from ..core.logger import logging
from ..sql_helper.globals import gvarstatus

LOGS = logging.getLogger(__name__)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    try:
        timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
        uzerid = gvarstatus("hmsa_id")
        if not uzerid:
            await event.answer("❌ خطأ في إعدادات الهمسة!", alert=True)
            return

        ussr = int(uzerid) if uzerid.isdigit() else uzerid
        myid = Config.OWNER_ID
        
        try:
            zzz = await l313l.get_entity(ussr)
        except ValueError:
            zzz = await l313l(GetUsersRequest(ussr))
        
        user_id = int(uzerid)
        file_name = f"./JoKeRUB/{user_id}.txt"
        
        if not os.path.exists(file_name):
            await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده.", alert=True)
            return

        with open(file_name) as f:
            jsondata = json.load(f)
            
        if f"{timestamp}" not in jsondata:
            await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", alert=True)
            return

        message = jsondata[f"{timestamp}"]
        userid = message["userid"]
        ids = [userid, myid, zzz.id]
        
        if event.query.user_id not in ids:
            await event.answer("مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓", alert=True)
            return

        encrypted_tcxt = message["text"]
        
        # إذا كان المستخدم هو المستقبل
        if event.query.user_id == userid:
            new_text = (
                f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                f"⌔╎الهمسـة لـ {getattr(zzz, 'first_name', 'المستخدم')}\n"
                f"⌔╎تمت قراءة الهمسة ✅\n\n"
                f"{encrypted_tcxt}"
            )
            
            new_buttons = [
                [Button.switch_inline("اضغـط للـرد", query=f"secret {myid} \nهلو", same_peer=True)]
            ]
            
            try:
                await event.client(
                    UpdateInlineBotMessageRequest(
                        peer=await event.get_input_chat(),
                        id=event.query.msg_id,
                        text=new_text,
                        buttons=new_buttons
                    )
                )
            except MessageNotModifiedError:
                pass
            except Exception as e:
                LOGS.error(f"Error updating message: {e}")

        await event.answer(encrypted_tcxt, alert=True)
        
    except Exception as e:
        LOGS.error(f"Error in secret callback: {e}")
        await event.answer("❌ حدث خطأ أثناء محاولة فتح الهمسة!", alert=True)
