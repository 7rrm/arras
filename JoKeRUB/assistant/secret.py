import json
import os
import re
from telethon import Button, events
from telethon.tl.functions.users import GetUsersRequest
from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    # الحصول على البيانات الأساسية
    timestamp = event.pattern_match.group(1).decode("UTF-8")
    uzerid = gvarstatus("hmsa_id")
    ussr = int(uzerid) if uzerid.isdigit() else uzerid
    myid = Config.OWNER_ID
    
    try:
        target_user = await l313l.get_entity(ussr)
    except ValueError:
        target_user = await l313l(GetUsersRequest(ussr))
    
    user_id = int(uzerid)
    file_name = f"./JoKeRUB/{user_id}.txt"
    
    if not os.path.exists(file_name):
        return await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده.", cache_time=0, alert=True)
    
    try:
        with open(file_name, "r+") as file:
            jsondata = json.load(file)
            message_data = jsondata.get(timestamp)
            
            if not message_data:
                return await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", cache_time=0, alert=True)
                
            userid = message_data["userid"]
            ids = [userid, myid, target_user.id]
            
            if event.query.user_id not in ids:
                return await event.answer("مطـي الهمسـه مـو الك 🧑🏻‍🦯🦓", cache_time=0, alert=True)
            
            # عرض محتوى الهمسة
            await event.answer(message_data["text"], cache_time=0, alert=True)
            
            # إذا كان المستخدم هو المرسل إليه ولم تقرأ بعد
            if event.query.user_id == userid and not message_data.get("read", False):
                # تحديث حالة القراءة
                message_data["read"] = True
                jsondata[timestamp] = message_data
                file.seek(0)
                json.dump(jsondata, file, indent=4)
                file.truncate()
                
                # تحرير الرسالة الأصلية
                new_text = (
                    f"ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه 📠\n"
                    f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                    f"⌔╎تم قراءة الهمسة من قبل {target_user.first_name}\n"
                    f"⌔╎هو فقط من يستطيع ࢪؤيتهـا"
                )
                
                new_buttons = [
                    [Button.switch_inline("اضغـط للـرد", query=f"secret {myid} \nهلو", same_peer=True)]
                ]
                
                try:
                    await event.client.edit_message(
                        event.chat_id,
                        event.message_id,
                        text=new_text,
                        buttons=new_buttons,
                        link_preview=False
                    )
                except Exception as e:
                    LOGS.error(f"فشل في تعديل الرسالة: {e}")

    except Exception as e:
        LOGS.error(f"حدث خطأ: {e}")
        await event.answer("- حدث خطأ أثناء معالجة الهمسة", cache_time=0, alert=True)
