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

# النصوص الثابتة
scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "فتـح الهمسـه 🗳"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - **همسـة سـريـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎أضغـط الـزر بالأسفـل ⚓\n⌔╎لـ أࢪسـال همسـه سـريـه الى"
ddd = "💌"

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    query_user_id = event.query.user_id
    
    # الحصول على بيانات المستخدم الهدف
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    
    # إنشاء رابط المنشن
    zelzal = f"[{full_name}](tg://user?id={user_id})" if user_id and full_name else None
    
    # التحقق من صلاحيات المستخدم
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        malathid = Config.OWNER_ID
    elif query_user_id == user_id:
        malathid = user_id
    else:
        malathid = None

    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        # معالجة الأمر secret
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, event.text)
        
        if match2:
            query = event.text[7:]
            info_type = [hmm, ymm, fmm]
            
            # فصل المستخدمين عن النص
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            
            # بناء قائمة المستخدمين
            user_list = []
            zilzal = ""
            
            for user in users:
                usr = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else int(user)
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                
                # إضافة منشن للمستخدم
                zilzal += f"[{u.first_name}](tg://user?id={u.id}) "
                user_list.append(u.id)
            
            zilzal = zilzal.strip()
            
            # حفظ الرسالة
            timestamp = int(time.time() * 2)
            new_msg = {str(timestamp): {"userid": user_list, "text": query}}
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            
            try:
                jsondata = json.load(open(old_msg))
                jsondata.update(new_msg)
            except Exception:
                jsondata = new_msg
                
            with open(old_msg, "w") as f:
                json.dump(jsondata, f)
            
            # إنشاء زر الرد
            buttons = [
                [Button.inline(info_type[2], data=f"{scc}_{timestamp}")],
                [Button.switch_inline(bmm, query=f"secret {malathid} \nهلو", same_peer=True)]
            ]
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n**{dss}**",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
        
        # معالجة الأمر zelzal
        elif event.text.lower() == "zelzal":
            if user_id:
                bbb = [Button.switch_inline(
                    "اضغـط هنـا", 
                    query=f"secret {user_id} \nهلو", 
                    same_peer=True
                )]
                
                results = [builder.article(
                    title=nmm,
                    description=mnn,
                    text=f"**{ttt}** {zelzal} **{ddd}**",
                    buttons=bbb,
                    link_preview=False,
                )]
                
                await event.answer(results)
