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
from telethon import Button, functions, events, types
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

LOGS = logging.getLogger(os.path.basename(__name__))

scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "فتـح الهمسـه 🗳"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **همسـة سـࢪيـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص).\nعبـر زدثــون"
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - همسـة سـࢪيـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎اضغـط الـزر بالاسفـل ⚓\n⌔╎لـ اࢪسـال همسـه سـࢪيـه الى"
ddd = "💌"
Zel_Uid = l313l.uid

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

async def user_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    username = zthon_user.username
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else None
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else "None"
    return user_id, full_name, username

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def secret_msg(event):
    if gvarstatus("ZThon_Vip") is None and event.sender_id not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot**")
    
    reply = await event.get_reply_message()
    if not reply and not event.pattern_match.group(1):
        return await edit_or_reply(event, "**⌔╎يجب الرد على الشخص أو كتابة معرفه**")
    
    try:
        user = await get_user_from_event(event)
        user_id = user.id
        full_name = user.first_name
    except Exception as e:
        return await edit_or_reply(event, f"**حدث خطأ: {str(e)}**")
    
    # إنشاء زر إنلاين يعمل مع اليوزر بوت
    button = [
        [
            Button.url(
                "اضغط هنا لإرسال الهمسة",
                f"https://t.me/{Config.TG_BOT_USERNAME}?start=hmsa_{user_id}"
            )
        ]
    ]
    
    # نص الرسالة
    msg_text = (
        f"**ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - همسـة سـࢪيـه**\n"
        f"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
        f"⌔╎اضغـط الـزر بالاسفـل ⚓\n"
        f"⌔╎لـ إرسال همسـه سـࢪيـه إلى {full_name}"
    )
    
    # إرسال الرسالة
    await event.client.send_message(
        event.chat_id,
        msg_text,
        buttons=button,
        reply_to=reply.id if reply else None
    )
    await event.delete()
