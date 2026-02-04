import json
import math
import asyncio
import os
import random
import re
import time
from pathlib import Path
from uuid import uuid4

from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.types import InputBotInlineMessageText

from . import l313l
from ..Config import Config
from ..helpers import reply_id
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging
from ..helpers.utils import _format
from . import mention

LOGS = logging.getLogger(__name__)

# Copyright (C) 2023 Zilzalll . All Rights Reserved
@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    query = event.text
    string = query.lower()
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    zelzal = None
    
    if gvarstatus("hmsa_user"):
        if username.startswith("@"):
            zelzal = gvarstatus("hmsa_user")
        else:
            zelzal = f"[{full_name}](tg://user?id={user_id})"
    
    # للمطورين والمستخدم المسجل
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            
            for user in users:
                usr = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else int(user)
                try:
                    u = await l313l.get_entity(usr)
                except ValueError:
                    u = await l313l(GetUsersRequest(usr))
                
                if u.username:
                    zilzal += f"@{u.username}"
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id})"
                user_list.append(u.id)
                zilzal += " "
            
            zilzal = zilzal[:-1]
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {"userid": user_list, "text": query}
            }
            
            # نص الهمسة بنفس نمط البوت مع إيموجي بريميوم
            text_content = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="5210740682414644888">⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</tg-emoji>
<b>⌔╎الهمسـة لـ</b> {zilzal}
<b>⌔╎هو فقط من يستطيع ࢪؤيتهـا</b>'''
            
            # زر فتح الهمسة
            btn = [[Button.inline("<tg-emoji emoji-id=\"5258215850745275216\">🔓</tg-emoji> فتـح الهمسـه", data=f"secret_{timestamp}")]]
            
            # استخدم InputBotInlineMessageText بدلاً من builder.article
            result = builder.article(
                title=f"همسـة {zilzal}",
                description="همسـة سريـه",
                text=text_content,
                buttons=btn,
                link_preview=False,
                # جرب بدون parse_mode
            )
            
            await event.answer([result] if result else None)
            
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                # زر الإرسال
                btn = [[Button.switch_inline("<tg-emoji emoji-id=\"5210763312597326700\">📨</tg-emoji> اضغـط لـ أࢪسـال همسـه", query=("secret " + gvarstatus("hmsa_id") + " \nهلو"), same_peer=True)]]
            else:
                return
            
            # نص زر الهمسة
            text_content = f'''\
<tg-emoji emoji-id="5210763312597326700">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="5210740682414644888">⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</tg-emoji>
<b>⌔╎لـ أࢪسـال همسـه سـريـه الى</b> {zelzal} <tg-emoji emoji-id="5377453360531279468">💌</tg-emoji>'''
            
            result = builder.article(
                title="همسـه سريـه",
                description="أرسـال همسـه سريـه",
                text=text_content,
                buttons=btn,
                link_preview=False,
                # جرب بدون parse_mode
            )
            
            await event.answer([result])
    
    else:
        return
