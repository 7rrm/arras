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

EMOJI_SECRET = "5933974679269151927"   # 📨

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
        return user_object
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        user_obj = await event.client.get_entity(user)
        return user_obj

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def repozedub(event):
    try:
        zthon_user = await get_user_from_event(event)
        user_id = zthon_user.id
        username = f"@{zthon_user.username}" if zthon_user.username else f"[{zthon_user.first_name}](tg://user?id={user_id})"
        
        # حفظ بيانات المستلم
        delgvar("hmsa_id")
        delgvar("hmsa_name")
        delgvar("hmsa_user")
        addgvar("hmsa_id", user_id)
        addgvar("hmsa_name", zthon_user.first_name)
        addgvar("hmsa_user", username)
        
        # نص الرسالة
        text = f'''
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎لـ إرسال همسة سريّة إلى</b> {username} 💌
'''
        
        # ✅ زر واحد بسيط
        buttons = [[Button.switch_inline("✍️ اضغط لكتابة الهمسة 📨", query=f"secret {user_id} \n", same_peer=True)]]
        
        # ✅ إرسال
        await event.delete()
        await event.respond(text, buttons=buttons, parse_mode='html')
        
    except Exception as e:
        await event.edit(f"❌ خطأ: {str(e)}")
