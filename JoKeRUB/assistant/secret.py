
import json
import os
import re

from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon import Button

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
            # دعم الحالات لو userid قائمة أو رقم
            idlist = userid if isinstance(userid, list) else [userid]
            ids = idlist + [myid, zzz.id]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                # --- تبديل الرسالة الحالية بالنص الجديد ----
                new_text = (
                    "تم قراءه الهمسه ✓\n\n"
                    "💬: " + encrypted_tcxt
                )
                # فقط زر الرد كما تريد
                btn = [[Button.switch_inline("اضغـط للـرد", query=f"secret {user_id} \nهلو", same_peer=True)]]
                try:
                    await event.edit(new_text, buttons=btn, link_preview=False)
                    # اختياريًا تظهر أيضاً رسالة popup لصاحبها
                    await event.answer("تم عرض الهمسة بنجاح ✅", cache_time=0, alert=True)
                except Exception:
                    # إذا الرسالة غير قابلة للتعديل (inline history فارغ)، رد popup فقط
                    await event.answer(encrypted_tcxt, cache_time=0, alert=True)
            else:
                await event.answer("مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓", cache_time=0, alert=True)
        except KeyError:
            await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", cache_time=0, alert=True)
    else:
        await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده .", cache_time=0, alert=True)
