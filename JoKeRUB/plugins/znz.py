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

# المتغيرات
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
bbb = None

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
        zelzal = f"[{full_name}](tg://user?id={user_id})"
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        malathid = Config.OWNER_ID
    elif query_user_id == user_id:
        malathid = user_id
    else:
        malathid = None
    
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
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
                
                # استخدام منشن بدلاً من اليوزر
                zilzal += f"[{u.first_name}](tg://user?id={u.id}) "
                user_list.append(u.id)
            
            zilzal = zilzal[:-1]
            old_msg = os.path.join("./JoKeRUB", f"{user_id}.txt")
            
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {
                    "userid": user_list,
                    "text": query,
                    "read": False,
                    "sender_id": event.query.user_id
                }
            }
            
            text_message = (
                "ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه\n"
                "⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
                "⌔╎أضغـط الـزر بالأسفـل ⚓\n"
                f"⌔╎لـ أࢪسـال همسـه سـريـه الى {zilzal} {ddd}"
            )
            
            buttons = [
                [Button.inline(fmm, data=f"{scc}_{timestamp}")],
                [Button.switch_inline(bmm, query=f"secret {malathid} \nهلو", same_peer=True)]
            ]
            
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=text_message,
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
                bbb = [(Button.switch_inline("اضغـط هنـا", query=("secret " + gvarstatus("hmsa_id") + " \nهلو"), same_peer=True))]
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
