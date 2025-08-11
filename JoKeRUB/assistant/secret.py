import json
import os
import re
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import UpdateInlineBotMessageRequest
from telethon.tl.types import InputBotInlineMessageID

from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    uzerid = gvarstatus("hmsa_id")
    ussr = int(uzerid) if uzerid.isdigit() else uzerid
    myid = Config.OWNER_ID
    
    try:
        zzz = await l313l.get_entity(ussr)
    except ValueError:
        zzz = await l313l(GetUsersRequest(ussr))
    
    user_id = int(uzerid)
    file_name = f"./JoKeRUB/{user_id}.txt"
    
    if os.path.exists(file_name):
        jsondata = json.load(open(file_name))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid, myid, zzz.id]
            
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
                
                # إذا كان المستخدم هو المستقبل (وليست المالك أو المساعد)
                if event.query.user_id == userid:
                    # نص الرسالة المعدل
                    new_text = (
                        f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                        f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                        f"⌔╎الهمسـة لـ {zzz.first_name}\n"
                        f"⌔╎تمت قراءة الهمسة ✅"
                    )
                    
                    # الأزرار الجديدة (زر واحد فقط)
                    new_buttons = [
                        [Button.switch_inline("اضغـط للـرد", query=f"secret {myid} \nهلو", same_peer=True)]
                    ]
                    
                    # تحديث الرسالة
                    try:
                        await event.client(
                            UpdateInlineBotMessageRequest(
                                peer=await event.get_input_chat(),
                                id=event.query.msg_id,
                                text=new_text,
                                buttons=new_buttons
                            )
                        )
                    except Exception as e:
                        LOGS.error(f"Error updating message: {e}")
            else:
                reply_pop_up_alert = "مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓"
        except KeyError:
            reply_pop_up_alert = "- عـذراً .. الهمسة ليست موجهة لك !!"
    else:
        reply_pop_up_alert = "- عـذراً .. هذه الرسـالة لم تعد موجـوده ."
    
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
