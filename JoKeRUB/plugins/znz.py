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

scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "• فتـح الهمسـه •"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n<b>⌔╎الهمسـة لـ</b>"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n<b>⌔╎لـ أࢪسـال همسـه سـريـه الى</b>"
ddd = "<tg-emoji emoji-id='5210763312597326700'>💌</tg-emoji>"
bbb = None

# معرف الإيموجي البريميوم
PREMIUM_EMOJI_ID = "5210763312597326700"

# Copyright (C) 2023 Zilzalll . All Rights Reserved
@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    zelzal = None
    if gvarstatus("hmsa_user"):
        if username.startswith("@"):
            zelzal = gvarstatus("hmsa_user")
        else:
            zelzal = f'<a href="tg://user?id={user_id}">{full_name}</a>'
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:  # Code by T.me/zzzzl1l
        malathid = Config.OWNER_ID
    elif query_user_id == user_id: #or query_user_id == int(user_id):
        malathid = user_id
    else:
        malathid = None
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:  # Code by T.me/zzzzl1l
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            info_type = [hmm, ymm, fmm]
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
                    zilzal += f'<a href="tg://user?id={u.id}">{u.first_name}</a>'
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
            }  # Code by T.me/zzzzl1l
            
            # زر فتح الهمسة مع إيموجي بريميوم
            button_text = f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>🔓</tg-emoji> فتح الهمسة"
            buttons = [[Button.inline(button_text, data=f"{scc}_{timestamp}")]]
            
            # نص النتيجة مع إيموجي بريميوم
            result_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>الهمسـة لـ</b> {zilzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">👁️</tg-emoji> <b>هو فقط من يستطيع رؤيتها</b>'''
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=result_text,
                buttons=buttons,
                link_preview=False,
                parse_mode='html'
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                bbb = [(Button.switch_inline(f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>💌</tg-emoji> اضغـط هنـا", query=("secret " + gvarstatus("hmsa_id") + " \nهلو"), same_peer=True))]
            else:
                return
            
            # نص النتيجة للهمسة
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>لـ أࢪسـال همسـه سـريـه الى</b> {zelzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">💌</tg-emoji>''',
                    buttons=bbb,
                    link_preview=False,
                    parse_mode='html'
                ),
            )
            await event.answer(results)
    elif query_user_id == user_id:  # Code by T.me/zzzzl1l
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            info_type = [hmm, ymm, fmm]
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
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
                    zilzal += f'<a href="tg://user?id={u.id}">{u.first_name}</a>'
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
            }  # Code by T.me/zzzzl1l
            
            # زر فتح الهمسة مع إيموجي بريميوم
            button_text = f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>🔓</tg-emoji> فتح الهمسة"
            buttons = [[Button.inline(button_text, data=f"{scc}_{timestamp}")]]
            
            # نص النتيجة مع إيموجي بريميوم
            result_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>الهمسـة لـ</b> {zilzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">👁️</tg-emoji> <b>هو فقط من يستطيع رؤيتها</b>'''
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=result_text,
                buttons=buttons,
                link_preview=False,
                parse_mode='html'
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                bbb = [(Button.switch_inline(f"<tg-emoji emoji-id='{PREMIUM_EMOJI_ID}'>💌</tg-emoji> اضغـط هنـا", query=("secret " + gvarstatus("hmsa_id") + " \nهلو"), same_peer=True))]
            else:
                return
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📠</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">⋆</tg-emoji>┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">📍</tg-emoji> <b>لـ أࢪسـال همسـه سـريـه الى</b> {zelzal}
<tg-emoji emoji-id="{PREMIUM_EMOJI_ID}">💌</tg-emoji>''',
                    buttons=bbb,
                    link_preview=False,
                    parse_mode='html'
                ),
            )
            await event.answer(results)
    else:
        return
