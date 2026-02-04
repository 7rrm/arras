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

LOGS = logging.getLogger(os.path.basename(__name__))

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
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵.**")
    
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎يرجـى الـرد على شخـص او كتـابة معـرفه/ايـدي الشـخص**")
    
    zthon_user = await get_user_from_event(event)
    if not zthon_user:
        return await edit_or_reply(event, "**⎉╎لم أستطـع العثـور على المستخـدم**")
    
    try:
        user_id, full_name, username = await zzz_info(zthon_user, event)
    except (AttributeError, TypeError) as e:
        LOGS.error(f"Error getting user info: {e}")
        return await edit_or_reply(event, "**⎉╎خطـأ في جلب معلومـات المستخـدم**")
    
    delgvar("hmsa_id")
    delgvar("hmsa_name")
    delgvar("hmsa_user")
    addgvar("hmsa_id", user_id)
    addgvar("hmsa_name", full_name)
    addgvar("hmsa_user", username)
    
    try:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "zelzal")
        if response and len(response) > 0:
            await response[0].click(event.chat_id, reply_to=event.reply_to_msg_id)
            await event.delete()
        else:
            await edit_or_reply(event, "**⎉╎خطـأ في إنشـاء الهمسـة. يـرجى المحاولـة لاحقـاً**")
    except Exception as e:
        LOGS.error(f"Error in repozedub: {e}")
        await edit_or_reply(event, f"**⎉╎خطـأ: {str(e)}**")
