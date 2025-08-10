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
                
                # إرسال تنبيه بالمحتوى أولاً
                await event.answer(encrypted_tcxt, alert=True)
                
                # ثم تحرير الرسالة الأصلية
                try:
                    await event.edit(
                        text=updated_text,
                        buttons=buttons
                    )
                except Exception as e:
                    print(f"Error editing message: {e}")
                    
            else:
                await event.answer("مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓", alert=True)
        except KeyError:
            await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", alert=True)
    else:
        await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده .", alert=True)
