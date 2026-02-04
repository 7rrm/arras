import json
import os
import re
from datetime import datetime

from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import EditMessageRequest
from telethon import Button
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
            sender_id = message.get("sender_id", myid)
            idlist = userid if isinstance(userid, list) else [userid]
            ids = idlist + [myid, zzz.id, sender_id]
            
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                
                # عرض الهمسة في رسالة منبثقة للجميع
                await event.answer(encrypted_tcxt, cache_time=0, alert=True)
                
                # فقط المستقبل يمكنه تحديث حالة القراءة
                if event.query.user_id in idlist and not message.get("read", False):
                    # الحصول على الوقت الحالي
                    current_time = datetime.now()
                    # تنسيق الوقت
                    time_str = current_time.strftime("%I:%M")
                    # إزالة الصفر البادئ إذا كان الساعة أقل من 10
                    if time_str.startswith('0'):
                        time_str = time_str[1:]
                    
                    message["read"] = True
                    message["read_time"] = time_str
                    jsondata[f"{timestamp}"] = message
                    json.dump(jsondata, open(file_name, "w"))
                    
                    # إنشاء منشن للمستقبل (الذي ضغط على الزر)
                    try:
                        receiver = await l313l.get_entity(event.query.user_id)
                        receiver_name = f'<a href="tg://user?id={event.query.user_id}">{get_display_name(receiver)}</a>'
                    except:
                        receiver_name = "المستخدم"
                    
                    # تحرير الرسالة الأصلية مع إضافة الوقت والإيموجي البريميوم
                    # معرف الإيموجي البريميوم
                    PREMIUM_EMOJI_ID = "5210763312597326700"
                    
                    new_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📨</tg-emoji> <b>تم قراءة الهمسـة</b> <tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">✅</tg-emoji>
<b>قـرأهـا</b> {receiver_name}
<b>عَـند</b> <code>{time_str}</code>'''
                    
                    # زر الرد يرسل همسة للمرسل الأصلي
                    btn = [[Button.switch_inline("<tg-emoji emoji-id='5210763312597326700'>💌</tg-emoji> اضغـط للـرد", query=f"secret {sender_id} \nهلو", same_peer=True)]]
                    
                    try:
                        await event.edit(new_text, buttons=btn, parse_mode='html')
                    except Exception as e:
                        LOGS.error(f"Error editing message: {e}")
                
            else:
                await event.answer("<tg-emoji emoji-id='5210763312597326700'>⛔</tg-emoji> آراس | عَـذراً عَـزيزي الهَمْسَة لَيْسَتْ لكَ .", cache_time=0, alert=True)
        except KeyError:
            await event.answer("<tg-emoji emoji-id='5210763312597326700'>⚠️</tg-emoji> عـذراً .. الهمسة ليست موجهة لك !!", cache_time=0, alert=True)
    else:
        await event.answer("<tg-emoji emoji-id='5210763312597326700'>❌</tg-emoji> عـذراً .. هذه الرسـالة لم تعد موجـوده .", cache_time=0, alert=True)
