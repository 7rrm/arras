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
from telethon.tl.types import InputWebDocument

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
hmm = "همسـة لـ"
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

# Cache for whispers to avoid disk I/O delay
whisper_cache = {}

async def save_json_async(data, path):
    """Save JSON data asynchronously without blocking"""
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        LOGS.error(f"Error saving JSON: {e}")

async def get_users_parallel(users, client):
    """Get multiple users in parallel for speed"""
    tasks = []
    for user in users:
        usr = int(user) if str(user).isdigit() else user
        tasks.append(client.get_entity(usr))
    return await asyncio.gather(*tasks, return_exceptions=True)

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
                user_part, query = query.split(" ", 1)
                users = [user_part]
            
            # Get users in parallel for speed
            users_entities = await get_users_parallel(users, l313l)
            
            for u in users_entities:
                if isinstance(u, Exception):
                    continue
                if hasattr(u, 'username') and u.username:
                    zilzal += f"@{u.username}"
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id})"
                user_list.append(u.id)
                zilzal += " "
            zilzal = zilzal[:-1] if zilzal else ""
            
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {"userid": user_list, "text": query}
            }
            
            buttons = [[Button.inline(info_type[2], data=f"{scc}_{timestamp}", style="danger")]]
            thumb = InputWebDocument(
                url="https://graph.org/file/5c149c9217a0eba19983e-2fe63df9e99eed4541.jpg",
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            )
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n**{dss}**",
                buttons=buttons,
                link_preview=False,
                thumb=thumb,
            )
            await event.answer([result] if result else None)
            
            # Save asynchronously without blocking
            if jsondata:
                jsondata.update(new_msg)
                asyncio.create_task(save_json_async(jsondata, old_msg))
            else:
                asyncio.create_task(save_json_async(new_msg, old_msg))
                
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                bbb = [(Button.switch_inline("اضغـط هنـا", query=("secret " + str(gvarstatus("hmsa_id")) + " \nهلو"), same_peer=True, style="primary"))]
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
                user_part, query = query.split(" ", 1)
                users = [user_part]
            
            # Get users in parallel for speed
            users_entities = await get_users_parallel(users, l313l)
            
            for u in users_entities:
                if isinstance(u, Exception):
                    continue
                if hasattr(u, 'username') and u.username:
                    zilzal += f"@{u.username}"
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id})"
                user_list.append(u.id)
                zilzal += " "
            zilzal = zilzal[:-1] if zilzal else ""
            
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {"userid": user_list, "text": query}
            }
            
            buttons = [[Button.inline(info_type[2], data=f"{scc}_{timestamp}", style="danger")]]
            thumb = InputWebDocument(
                url="https://graph.org/file/5c149c9217a0eba19983e-2fe63df9e99eed4541.jpg",
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            )
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n**{dss}**",
                buttons=buttons,
                link_preview=False,
                thumb=thumb,
            )
            await event.answer([result] if result else None)
            
            # Save asynchronously without blocking
            if jsondata:
                jsondata.update(new_msg)
                asyncio.create_task(save_json_async(jsondata, old_msg))
            else:
                asyncio.create_task(save_json_async(new_msg, old_msg))
                
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                bbb = [(Button.switch_inline("اضغـط هنـا", query=("secret " + str(gvarstatus("hmsa_id")) + " \nهلو"), same_peer=True, style="primary"))]
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
