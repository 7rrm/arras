import json
import os
import re
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import EditMessageRequest
from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

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
    
    if not os.path.exists(file_name):
        return await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده .", cache_time=0, alert=True)

    try:
        with open(file_name) as f:
            jsondata = json.load(f)
    except Exception as e:
        LOGS.error(f"Error loading JSON file: {e}")
        return await event.answer("- حدث خطأ في تحميل البيانات", cache_time=0, alert=True)

    try:
        message = jsondata[f"{timestamp}"]
        userid = message["userid"]
        ids = [userid, myid, zzz.id]
        
        if event.query.user_id not in ids:
            return await event.answer("مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓", cache_time=0, alert=True)
            
        encrypted_tcxt = message["text"]
        
        # إذا كان المستخدم هو المرسل إليه
        if event.query.user_id == userid:
            try:
                # تحديث الرسالة الأصلية
                new_text = (
                    f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                    f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                    f"⌔╎تم قراءة الهمسة من قبل {zzz.first_name}\n"
                    f"⌔╎المحتوى: {encrypted_tcxt}"
                )
                
                buttons = [[Button.switch_inline("اضغط للرد", query=f"secret {myid} \nهلو", same_peer=True)]]
                
                await event.client(EditMessageRequest(
                    peer=await event.get_input_chat(),
                    id=event.query.msg_id,
                    message=new_text,
                    buttons=buttons
                ))
            except Exception as e:
                LOGS.error(f"Error editing message: {e}")
                return await event.answer(encrypted_tcxt, cache_time=0, alert=True)
        
        await event.answer(encrypted_tcxt, cache_time=0, alert=True)
        
    except KeyError:
        await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", cache_time=0, alert=True)
