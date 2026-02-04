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

from . import l313l
from ..Config import Config
from ..helpers import reply_id
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging
from ..helpers.utils import _format
from . import mention

LOGS = logging.getLogger(__name__)
tr = Config.COMMAND_HAND_LER

# معرف الإيموجي البريميوم
PREMIUM_EMOJI_ID = "5210763312597326700"

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
    
    # إنشاء نص zelzal
    zelzal = None
    if gvarstatus("hmsa_user"):
        if username and username.startswith("@"):
            zelzal = username
        else:
            zelzal = f"[{full_name}](tg://user?id={user_id})"
    
    # التحقق من الصلاحيات
    allowed = False
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        allowed = True
    elif query_user_id == user_id:
        allowed = True
    
    if not allowed:
        return
    
    # معالجة أمر secret
    inf = re.compile("secret (.*) (.*)")
    match2 = re.findall(inf, query)
    
    if match2:
        user_list = []
        zilzal = ""
        query_text = query[7:]  # إزالة "secret "
        
        if "|" in query_text:
            iris, msg_text = query_text.replace(" |", "|").replace("| ", "|").split("|")
            users = iris.split(" ")
        else:
            user, msg_text = query_text.split(" ", 1)
            users = [user]
        
        for user in users:
            usr = int(user) if user.isdigit() else user
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
            str(timestamp): {"userid": user_list, "text": msg_text, "sender_id": query_user_id}
        }
        
        # حفظ البيانات
        if jsondata:
            jsondata.update(new_msg)
            json.dump(jsondata, open(old_msg, "w"))
        else:
            json.dump(new_msg, open(old_msg, "w"))
        
        # نص النتيجة مع إيموجي بريميوم
        result_text = f'''<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>الهمسـة لـ</b> {zilzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">👁️</tg-emoji> <b>هو فقط من يستطيع رؤيتها</b>'''
        
        # زر فتح الهمسة مع إيموجي بريميوم
        button_text = f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>🔓</tg-emoji> فتح الهمسة"
        buttons = [[Button.inline(button_text, data=f"secret_{timestamp}")]]
        
        result = builder.article(
            title=f"همسة سرية لـ {zilzal}",
            description="اضغط لفتح الهمسة السرية",
            text=result_text,
            buttons=buttons,
            link_preview=False
        )
        
        await event.answer([result] if result else None)
    
    # معالجة أمر zelzal
    elif string == "zelzal":
        if not gvarstatus("hmsa_id"):
            return
        
        # زر الإرسال مع إيموجي بريميوم
        button_text = f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>💌</tg-emoji> اضغـط هنـا"
        buttons = [[Button.switch_inline(button_text, query=("secret " + gvarstatus("hmsa_id") + " "), same_peer=True)]]
        
        # نص النتيجة مع إيموجي بريميوم
        result_text = f'''<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>لـ أࢪسـال همسـه سـريـه الى</b> {zelzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">💌</tg-emoji>'''
        
        result = builder.article(
            title="همسة سرية",
            description="أرسل همسة سرية",
            text=result_text,
            buttons=buttons,
            link_preview=False
        )
        
        await event.answer([result] if result else None)
