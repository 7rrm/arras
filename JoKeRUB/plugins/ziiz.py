import json
import math
import os
import aiohttp
import requests
import random
import re
import time
from uuid import uuid4
import sys
import asyncio
from validators.url import url
from subprocess import run as runapp
from datetime import datetime
from pySmartDL import SmartDL
from pathlib import Path
from platform import python_version
from telethon import Button, functions, events, types, custom
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.utils import get_display_name
from telethon.tl.types import InputMessagesFilterDocument
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import BotInlineResult, InputBotInlineMessageMediaAuto, DocumentAttributeImageSize, InputWebDocument, InputBotInlineResult
from telethon.tl.functions.messages import SetInlineBotResultsRequest

from . import l313l
from ..Config import Config
from ..helpers.functions import rand_key
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import reply_id, _format
from . import media_type, progress
from ..utils import Zed_Dev, load_module, remove_plugin
from ..sql_helper.global_collection import add_to_collectionlist, del_keyword_collectionlist, get_collectionlist_items
from . import SUDO_LIST, edit_delete, edit_or_reply, reply_id, BOTLOG, BOTLOG_CHATID, HEROKU_APP, mention



LOGS = logging.getLogger(__name__)

# 📨 ايموجي بريميوم - نفس كود القراءة!
EMOJI_SECRET = "5933974679269151927"   # 📨
EMOJI_CHECK = "4929526216945305427"    # ✅
EMOJI_CLOCK = "5839380464116175529"    # 🕖

WHISPER_DIR = "./JoKeRUB"
os.makedirs(WHISPER_DIR, exist_ok=True)

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

async def zzz_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    username = zthon_user.username
    first_name = first_name.replace("\u2060", "") if first_name else None
    full_name = full_name or first_name
    username = "@{}".format(username) if username else "None"
    return user_id, full_name, username

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def repozedub(event):
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return

    zthon_user = await get_user_from_event(event)
    try:
        user_id, full_name, username = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError):
        return

    # حفظ بيانات المستلم
    delgvar("hmsa_id")
    delgvar("hmsa_name")
    delgvar("hmsa_user")
    addgvar("hmsa_id", user_id)
    addgvar("hmsa_name", full_name)
    addgvar("hmsa_user", username)

    # ✅ 1. حسابك يرسل رسالة "جاري الإنشاء..."
    whisper_msg = await event.edit("⏱️ **جاري إنشاء الهمسة...**")

    # معرف فريد للهمسة
    secret_id = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"

    # حفظ الهمسة (بدون نص - سنضيفه لاحقاً)
    file_name = os.path.join(WHISPER_DIR, f"{user_id}.txt")
    try:
        with open(file_name, "r") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {}

    db[secret_id] = {
        "userid": [user_id],
        "text": None,  # سنضيف النص لاحقاً
        "sender_id": event.sender_id,
        "read": False,
        "chat_id": event.chat_id,
        "message_id": whisper_msg.id
    }

    with open(file_name, "w") as f:
        json.dump(db, f, indent=4)

    # ✅ 2. نص الهمسة مع إيموجي بريميوم (مثل كود القراءة!)
    text = f'''
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎الهمسـة لـ</b> {username or f'[{full_name}](tg://user?id={user_id})'}
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<i>⌔╎اكتب الهمسة الآن بالرد على هذه الرسالة</i>
'''

    # ✅ 3. زر لكتابة الهمسة (رد)
    buttons = [
        [Button.switch_inline(
            "✍️ اضغط لكتابة الهمسة 📨",
            query=f"whisper_{secret_id} \n",
            same_peer=True
        )]
    ]

    # ✅ 4. تعديل الرسالة إلى الهمسة النهائية!
    await whisper_msg.edit(text, buttons=buttons, parse_mode='html')
