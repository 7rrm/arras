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
               await event.reply("**ح͟ا͟ظ͟ر͟ م͟ط͟و͟ر͟ي͟ ،͟ ل͟ق͟د͟ ت͟م͟ ح͟ظ͟ر͟ه͟ م͟ن͟ ا͟س͟ت͟خ͟د͟ا͟م͟ ا͟ل͟س͟و͟ر͟س͟**")
               addgvar("blockedfrom", "yes")
           elif event.message.message == "الغاء الحظر من السورس":
               await event.reply("**حاظر مطوري، لقد الغيت الحظر**")
               delgvar("blockedfrom")
                

