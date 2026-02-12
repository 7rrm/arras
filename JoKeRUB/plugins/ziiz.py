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

# 📨 إيموجي بريميوم
EMOJI_SECRET = "5933974679269151927"   # 📨
EMOJI_FIRE = "5368324170671202286"     # 🔥

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

    # 📝 نص الرسالة مع إيموجي بريميوم
    text = f'''
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎لـ إرسال همسة سريّة إلى</b> {username or full_name} 💌
'''

    # 🎨 الأزرار الملونة مع إيموجي بريميوم (مثل كود السورس تماماً)
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "✍️ اضغط لكتابة الهمسة 📨",
                    "switch_inline_query_current_chat": f"secret {user_id} \n",
                    "style": "primary",                    # 🔵 أزرق
                    "icon_custom_emoji_id": EMOJI_SECRET   # 📨 داخل الزر
                }
            ],
            [
                {
                    "text": "🔥 همسة سريعة",
                    "switch_inline_query_current_chat": f"secret {user_id} \nمرحبا",
                    "style": "success",                    # 🟢 أخضر
                    "icon_custom_emoji_id": EMOJI_FIRE     # 🔥 داخل الزر
                }
            ]
        ]
    }

    # ✨ إرسال الرسالة عبر Bot API (مثل كود السورس)
    bot_token = Config.TG_BOT_TOKEN
    chat_id = event.chat_id
    
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    send_data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(keyboard),
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(send_url, json=send_data)
        if response.status_code == 200:
            await event.delete()  # حذف الأمر
            LOGS.info(f"✅ تم إرسال همسة إلى {username or full_name}")
        else:
            await event.edit("❌ حدث خطأ في الإرسال")
            LOGS.error(f"❌ خطأ: {response.text}")
    except Exception as e:
        await event.edit("❌ حدث خطأ، حاول مرة أخرى")
        LOGS.error(f"❌ خطأ: {e}")
