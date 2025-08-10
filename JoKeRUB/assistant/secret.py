import json
import os
import re
from datetime import datetime

from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import InputWebDocument
from telethon.utils import get_display_name

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
                # إذا كان المستخدم مسموحًا له برؤية الهمسة
                encrypted_tcxt = message["text"]
                
                # الحصول على معلومات المستخدم الذي فتح الهمسة
                viewer = await event.get_sender()
                viewer_name = get_display_name(viewer)
                current_time = datetime.now().strftime("%I:%M %p")
                
                # تحديث الرسالة لتعكس أن الهمسة تم قراءتها
                updated_text = (
                    f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                    f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                    f"⌔╎الهمسـة لـ {zzz.first_name}\n"
                    f"⌔╎تم قراءة الهمسة من قبل {viewer_name}\n"
                    f"⌔╎الوقت: {current_time}"
                )
                
                # تحديث الزر لإظهار زر الرد فقط
                buttons = [
                    [Button.switch_inline("اضغط للرد", query=f"secret {user_id} \nرد على الهمسة", same_peer=True)]
                ]
                
                # تحرير الرسالة الأصلية لتظهر التحديثات
                try:
                    await event.edit(
                        text=updated_text,
                        buttons=buttons
                    )
                except:
                    pass
                    
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓"
        except KeyError:
            reply_pop_up_alert = "- عـذراً .. الهمسة ليست موجهة لك !!"
    else:
        reply_pop_up_alert = "- عـذراً .. هذه الرسـالة لم تعد موجـوده ."
    
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
