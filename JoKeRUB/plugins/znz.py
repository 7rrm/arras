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
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ddd = "💌"
bbb = None

# 🎯 إيموجيات بريميوم للنصوص
PREMIUM_EMOJIS = {
    "mail": "5210763312597326700",      # 📨
    "check": "5210740682414644888",     # ✅
    "check_green": "5843826335088120045", # ✅ أخضر
    "clock": "5839380464116175529",     # 🕖
    "fire": "5368324170671202286",      # 🔥
    "heart": "5316347681116269519",     # ❤️
    "lock": "5341741293349680948",      # 🔒
    "unlock": "5341741293789691996",    # 🔓
    "star": "5316347681116269521",      # ⭐
    "arrow": "5316347681116269522",     # ➡️
    "zilzal": "5368324170671202287",    # 🌪️
    "speech": "5210763312597326701",    # 💬
    "robot": "5210763312597326702",     # 🤖
    "crown": "5316347681116269523",     # 👑
    "gem": "5316347681116269524",       # 💎
}

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
            zelzal = f"[{full_name}](tg://user?id={user_id})"
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        malathid = Config.OWNER_ID
    elif query_user_id == user_id:
        malathid = user_id
    else:
        malathid = None
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
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
            
            # ✅ زر عادي
            buttons = [[Button.inline(info_type[2], data=f"{scc}_{timestamp}")]]
            
            # ✅ نص مع إيموجي بريميوم مثل ملف sii
            hmsa_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJIS['mail']}">📨</tg-emoji> <b> الهمسة السريـة </b> <tg-emoji emoji-id="{PREMIUM_EMOJIS['lock']}">🔒</tg-emoji>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['arrow']}">➡️</tg-emoji> <b>إلى:</b> {zilzal}

<tg-emoji emoji-id="{PREMIUM_EMOJIS['speech']}">💬</tg-emoji> <b>الرسالة:</b> <i>"{query[:50]}{'...' if len(query) > 50 else ''}"</i>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['fire']}">🔥</tg-emoji> <b>فقط المستقبل يمكنه فتحها</b> <tg-emoji emoji-id="{PREMIUM_EMOJIS['check']}">✅</tg-emoji>'''
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=hmsa_text,
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
                # ✅ زر switch_inline عادي
                bbb = [[
                    Button.switch_inline(
                        "🔥 همسة سريـة",
                        query=f"secret {gvarstatus('hmsa_id')} \nهلو",
                        same_peer=True
                    )
                ]]
                
                # ✅ نص مع إيموجي بريميوم مثل ملف sii
                zelzal_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJIS['crown']}">👑</tg-emoji> <b> آراس ويسبر - همسة سريـة </b> <tg-emoji emoji-id="{PREMIUM_EMOJIS['gem']}">💎</tg-emoji>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['zilzal']}">🌪️</tg-emoji> <b>مرحباً بك في نظام الهمسات السرية</b>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['arrow']}">➡️</tg-emoji> <b>الهمسة موجهة إلى:</b> {zelzal}

<tg-emoji emoji-id="{PREMIUM_EMOJIS['fire']}">🔥</tg-emoji> <b>اضغط الزر بالأسفل لإرسال همسة</b>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['lock']}">🔒</tg-emoji> <i>همسة خاصة - لا يراها إلا المستقبل</i>'''
            else:
                return
            
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=zelzal_text,
                    buttons=bbb,
                    link_preview=False,
                    parse_mode='html'
                ),
            )
            await event.answer(results)
    
    elif query_user_id == user_id:
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
            
            # ✅ زر عادي
            buttons = [[Button.inline(info_type[2], data=f"{scc}_{timestamp}")]]
            
            # ✅ نص مع إيموجي بريميوم
            hmsa_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJIS['mail']}">📨</tg-emoji> <b> الهمسة السريـة </b> <tg-emoji emoji-id="{PREMIUM_EMOJIS['lock']}">🔒</tg-emoji>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['arrow']}">➡️</tg-emoji> <b>إلى:</b> {zilzal}

<tg-emoji emoji-id="{PREMIUM_EMOJIS['speech']}">💬</tg-emoji> <b>الرسالة:</b> <i>"{query[:50]}{'...' if len(query) > 50 else ''}"</i>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['fire']}">🔥</tg-emoji> <b>فقط المستقبل يمكنه فتحها</b> <tg-emoji emoji-id="{PREMIUM_EMOJIS['check']}">✅</tg-emoji>'''
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=hmsa_text,
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
                # ✅ زر switch_inline عادي
                bbb = [[
                    Button.switch_inline(
                        "🔥 همسة سريـة",
                        query=f"secret {gvarstatus('hmsa_id')} \nهلو",
                        same_peer=True
                    )
                ]]
                
                # ✅ نص مع إيموجي بريميوم
                zelzal_text = f'''\
<tg-emoji emoji-id="{PREMIUM_EMOJIS['crown']}">👑</tg-emoji> <b> آراس ويسبر - همسة سريـة </b> <tg-emoji emoji-id="{PREMIUM_EMOJIS['gem']}">💎</tg-emoji>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['zilzal']}">🌪️</tg-emoji> <b>مرحباً بك في نظام الهمسات السرية</b>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['arrow']}">➡️</tg-emoji> <b>الهمسة موجهة إلى:</b> {zelzal}

<tg-emoji emoji-id="{PREMIUM_EMOJIS['fire']}">🔥</tg-emoji> <b>اضغط الزر بالأسفل لإرسال همسة</b>

<tg-emoji emoji-id="{PREMIUM_EMOJIS['lock']}">🔒</tg-emoji> <i>همسة خاصة - لا يراها إلا المستقبل</i>'''
            else:
                return
            
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=zelzal_text,
                    buttons=bbb,
                    link_preview=False,
                    parse_mode='html'
                ),
            )
            await event.answer(results)
    else:
        return
