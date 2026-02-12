import json
import math
import asyncio
import os
import random
import re
import time
import requests
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
ttt = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📨\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎لـ أࢪسـال همسـه سريـه الى**"
ddd = "💌"
bbb = None

# إيموجي ناري للتزيين
FIRE_EMOJI = "🔥"

# Copyright (C) 2023 Zilzalll . All Rights Reserved
@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
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
    
    # التحقق من الصلاحية
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        
        # قسم secret
        if query.startswith("secret "):
            try:
                user_list = []
                zilzal = ""
                query_text = query[7:]
                info_type = [hmm, ymm, fmm]
                
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
                new_msg = {str(timestamp): {"userid": user_list, "text": msg_text}}
                
                # استخدام REST API للأزرار الملونة - أخضر
                url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
                
                keyboard = {
                    "inline_keyboard": [
                        [
                            {
                                "text": f"✅ {info_type[2]} ✅",
                                "callback_data": f"{scc}_{timestamp}",
                                "style": "success"
                            }
                        ]
                    ]
                }
                
                inline_data = {
                    "inline_query_id": event.id,
                    "results": json.dumps([
                        {
                            "type": "article",
                            "id": str(timestamp),
                            "title": f"{hmm} {zilzal}",
                            "description": f"{dss}",
                            "input_message_content": {
                                "message_text": f"{hss} {zilzal} \n**{dss}**",
                                "parse_mode": "Markdown"
                            },
                            "reply_markup": keyboard
                        }
                    ]),
                    "cache_time": 0,
                    "is_personal": True
                }
                
                # إرسال الطلب - بدون استخدام event.answer
                requests.post(url, json=inline_data)
                
                if jsondata:
                    jsondata.update(new_msg)
                    json.dump(jsondata, open(old_msg, "w"))
                else:
                    json.dump(new_msg, open(old_msg, "w"))
                    
            except Exception as e:
                LOGS.error(f"خطأ في secret: {e}")
                # Fallback
                buttons = [[Button.inline(info_type[2], data=f"{scc}_{timestamp}")]]
                result = builder.article(
                    title=f"{hmm} {zilzal}",
                    description=f"{dss}",
                    text=f"{hss} {zilzal} \n**{dss}**",
                    buttons=buttons,
                    link_preview=False,
                )
                await event.answer([result] if result else None)
        
        # قسم zelzal
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                try:
                    # استخدام REST API للأزرار الملونة - أزرق
                    url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
                    
                    keyboard = {
                        "inline_keyboard": [
                            [
                                {
                                    "text": f"{FIRE_EMOJI} اضغـط لفتـح الهمسـة {FIRE_EMOJI}",
                                    "switch_inline_query": f"secret {gvarstatus('hmsa_id')} \nهلو",
                                    "style": "primary"
                                }
                            ]
                        ]
                    }
                    
                    inline_data = {
                        "inline_query_id": event.id,
                        "results": json.dumps([
                            {
                                "type": "article",
                                "id": "zelzal_1",
                                "title": f"{nmm}",
                                "description": f"{mnn}",
                                "input_message_content": {
                                    "message_text": f"{ttt} {zelzal} **{ddd}**",
                                    "parse_mode": "Markdown"
                                },
                                "reply_markup": keyboard
                            }
                        ]),
                        "cache_time": 0,
                        "is_personal": True
                    }
                    
                    # إرسال الطلب - بدون استخدام event.answer
                    requests.post(url, json=inline_data)
                    
                except Exception as e:
                    LOGS.error(f"خطأ في zelzal: {e}")
                    # Fallback
                    bbb = [[Button.switch_inline("اضغـط هنـا", query=("secret " + gvarstatus("hmsa_id") + " \nهلو"), same_peer=True)]]
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
            else:
                # إذا ما في hmsa_id
                await event.answer([])
        
        else:
            await event.answer([])
    else:
        await event.answer([])
