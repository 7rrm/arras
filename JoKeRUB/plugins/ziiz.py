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
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText

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
fmm = "• فتـح الهمسـه •"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n<b>⌔╎الهمسـة لـ</b>"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽 - همسـة سـريـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎اضغـط الـزر بالاسفـل ⚓\n⌔╎لـ اࢪسـال همسـه سـࢪيـه الى"
ddd = "<tg-emoji emoji-id='5210763312597326700'>💌</tg-emoji>"
Zel_Uid = l313l.uid

# معرف الإيموجي البريميوم
PREMIUM_EMOJI_ID = "5210763312597326700"

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

async def zzz_info(zthon_user, event): #Write Code By Zelzal T.me/zzzzl1l
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
async def repozedub(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>⛔</tg-emoji> <b>عـذࢪاً .. ؏ـزيـزي\nهــذا الامــر ليــس مجــانــي📵.</b>", parse_mode='html')
    
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return await edit_or_reply(event, f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>⚠️</tg-emoji> <b>يجب الرد على شخص أو كتابة معرفه</b>", parse_mode='html')
    
    zthon_user = await get_user_from_event(event)
    try:
        user_id, full_name, username = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError):
        return await edit_or_reply(event, f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>❌</tg-emoji> <b>لم أستطع العثور على المستخدم</b>", parse_mode='html')
    
    delgvar("hmsa_id")
    delgvar("hmsa_name")
    delgvar("hmsa_user")
    addgvar("hmsa_id", user_id)
    addgvar("hmsa_name", full_name)
    addgvar("hmsa_user", username)
    
    # إنشاء رابط المستخدم
    if username and username != "@None":
        zelzal = username
    else:
        zelzal = f'📌 {full_name}'
    
    # إنشاء رسالة HTML مع إيموجي بريميوم
    message_text = f'''<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>لـ أࢪسـال همسـه سـريـه الى</b> {zelzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">💌</tg-emoji>'''

    # إرسال الرسالة مع الزر باستخدام event.reply بدلاً من edit_or_reply
    await event.reply(
        message_text,
        buttons=[
            [Button.switch_inline(
                f"💌 اضـغـط هنـا لإرسـال هـمسـة",
                query=f"secret {user_id} ",
                same_peer=True
            )]
        ],
        parse_mode='html'
    )
    
    # حذف رسالة الأمر الأصلية
    await event.delete()
