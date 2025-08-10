import json
import os
import re

from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest

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
                
                # تحديث الرسالة بعد قراءة الهمسة
                if event.query.user_id == userid:
                    # حذف زر فتح الهمسة
                    new_buttons = [[Button.switch_inline("اضغـط للـرد", query=f"secret {myid} \nهلو", same_peer=True)]]
                    
                    # تحرير الرسالة الأصلية
                    try:
                        await event.client.edit_message(
                            event.chat_id,
                            event.message_id,
                            text=f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎تم قراءة الهمسة من قبل {zzz.first_name}\n⌔╎هو فقط من يستطيع ࢪؤيتهـا",
                            buttons=new_buttons,
                            link_preview=False
                        )
                    except Exception as e:
                        LOGS.error(f"Error editing message: {e}")
            else:
                reply_pop_up_alert = "مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓"
                
        except KeyError:
            reply_pop_up_alert = "- عـذراً .. الهمسة ليست موجهة لك !!"
    else:
        reply_pop_up_alert = "- عـذراً .. هذه الرسـالة لم تعد موجـوده ."
    
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
