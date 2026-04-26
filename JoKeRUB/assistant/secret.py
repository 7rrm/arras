import json
import os
import re
from datetime import datetime
import asyncio

from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import EditMessageRequest
from telethon import Button
from telethon.utils import get_display_name

from JoKeRUB import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

async def update_message_async(event, new_text, buttons):
    """Update message without blocking"""
    try:
        await event.edit(new_text, buttons=buttons, parse_mode='html')
    except Exception as e:
        LOGS.error(f"Error editing message: {e}")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    uzerid = gvarstatus("hmsa_id")
    
    if not uzerid:
        await event.answer("❌ خطأ: لم يتم تحديد المستلم", cache_time=0, alert=True)
        return
    
    ussr = int(uzerid) if str(uzerid).isdigit() else uzerid
    myid = Config.OWNER_ID
    
    try:
        zzz = await l313l.get_entity(ussr)
    except ValueError:
        zzz = await l313l(GetUsersRequest(ussr))
    
    user_id = int(uzerid)
    file_name = f"./JoKeRUB/{user_id}.txt"
    
    if os.path.exists(file_name):
        try:
            jsondata = json.load(open(file_name))
            message = jsondata.get(f"{timestamp}")
            
            if not message:
                await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", cache_time=0, alert=True)
                return
                
            userid = message["userid"]
            sender_id = message.get("sender_id", myid)
            idlist = userid if isinstance(userid, list) else [userid]
            ids = idlist + [myid, zzz.id, sender_id]
            
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                
                # Show the whisper in popup
                await event.answer(encrypted_tcxt, cache_time=0, alert=True)
                
                # Only receiver can update read status
                if event.query.user_id in idlist and not message.get("read", False):
                    # Get current time
                    current_time = datetime.now()
                    time_str = current_time.strftime("%I:%M")
                    if time_str.startswith('0'):
                        time_str = time_str[1:]
                    
                    message["read"] = True
                    message["read_time"] = time_str
                    jsondata[f"{timestamp}"] = message
                    
                    # Save asynchronously
                    async def save_json():
                        with open(file_name, "w") as f:
                            json.dump(jsondata, f)
                    asyncio.create_task(save_json())
                    
                    # Create mention for receiver
                    try:
                        receiver = await l313l.get_entity(event.query.user_id)
                        receiver_name = f'<a href="tg://user?id={event.query.user_id}">{get_display_name(receiver)}</a>'
                    except:
                        receiver_name = "المستخدم"
                    
                    new_text = f'''\
<tg-emoji emoji-id="5933974679269151927">📨</tg-emoji> <b> تم قراءة الهمسـة </b>
<tg-emoji emoji-id="5933974679269151927">📨</tg-emoji><b>قــرأهـا</b> <tg-emoji emoji-id="5290004119178734919">📨</tg-emoji>{receiver_name}</b> <tg-emoji emoji-id="5287782852287557349">✅</tg-emoji>
<tg-emoji emoji-id="5933974679269151927">📨</tg-emoji><b>عَـند</b> <code>{time_str}</code> . </b> <tg-emoji emoji-id="5839380464116175529">🕖</tg-emoji>'''
                    
                    # Reply button
                    btn = [[Button.switch_inline("اضغـط للـرد", query=f"secret {sender_id} \nهلو", same_peer=True, style="primary")]]
                    
                    # Update message in background
                    asyncio.create_task(update_message_async(event, new_text, btn))
            else:
                await event.answer("آراس | عَـذراً عَـزيزي الهَمْسَة لَيْسَتْ لكَ .", cache_time=0, alert=True)
        except KeyError:
            await event.answer("- عـذراً .. الهمسة ليست موجهة لك !!", cache_time=0, alert=True)
        except Exception as e:
            LOGS.error(f"Error in callback: {e}")
            await event.answer("- حدث خطأ أثناء معالجة الهمسة", cache_time=0, alert=True)
    else:
        await event.answer("- عـذراً .. هذه الرسـالة لم تعد موجـوده .", cache_time=0, alert=True)
