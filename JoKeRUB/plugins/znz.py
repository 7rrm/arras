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
hss = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎لـ أࢪسـال همسـه سـريـه الى**"
ddd = "💌"
bbb = None

# 🎯 **إيموجيات بريميوم** 🎯
FIRE_EMOJI = "5368324170671202286"      # 🔥
HEART_EMOJI = "5316347681116269519"     # ❤️
LOCK_EMOJI = "5341741293349680948"      # 🔒
UNLOCK_EMOJI = "5341741293789691996"    # 🔓
CHECK_EMOJI = "5316347681116269520"     # ✅
MAIL_EMOJI = "5210763312597326700"      # 📨
STAR_EMOJI = "5316347681116269521"      # ⭐
ARROW_EMOJI = "5316347681116269522"     # ➡️
ZELZAL_EMOJI = "5368324170671202287"    # 🌪️

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
            
            # ✅ **زر مع إيموجي بريميوم + لون** ✅
            buttons = [[
                Button.inline(
                    f"{chr(8206)}‌‌ ",  # نص فارغ
                    data=f"{scc}_{timestamp}",
                    buttons=None,
                    **{
                        "text": "🔥 فتح الهمسة",
                        "icon_custom_emoji_id": FIRE_EMOJI,
                        "style": "primary"
                    }
                )
            ]]
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n**{dss}**",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                # ✅ **زر switch_inline مع إيموجي بريميوم** ✅
                switch_button = types.KeyboardButtonSwitchInline(
                    text="🔥 همسة سريـة",
                    query=f"secret {gvarstatus('hmsa_id')} \nهلو",
                    same_peer=True,
                    **{
                        "icon_custom_emoji_id": FIRE_EMOJI,
                        "style": "primary"
                    }
                )
                bbb = [[switch_button]]
            else:
                return
            
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=f"{ttt} {zelzal} **{ddd}**",
                    buttons=bbb,
                    link_preview=False,
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
            
            # ✅ **زر مع إيموجي بريميوم** ✅
            buttons = [[
                Button.inline(
                    f"{chr(8206)}‌‌ ",
                    data=f"{scc}_{timestamp}",
                    buttons=None,
                    **{
                        "text": "🔥 فتح الهمسة",
                        "icon_custom_emoji_id": FIRE_EMOJI,
                        "style": "primary"
                    }
                )
            ]]
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n{dss}",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                # ✅ **زر switch_inline مع إيموجي بريميوم** ✅
                switch_button = types.KeyboardButtonSwitchInline(
                    text="🔥 همسة سريـة",
                    query=f"secret {gvarstatus('hmsa_id')} \nهلو",
                    same_peer=True,
                    **{
                        "icon_custom_emoji_id": FIRE_EMOJI,
                        "style": "primary"
                    }
                )
                bbb = [[switch_button]]
            else:
                return
            
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=f"**{ttt}** {zelzal} **{ddd}**",
                    buttons=bbb,
                    link_preview=False,
                ),
            )
            await event.answer(results)
    else:
        return
