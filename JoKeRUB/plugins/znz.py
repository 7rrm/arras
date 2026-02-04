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
from telethon.tl.types import InputBotInlineResult, InputBotInlineMessageText

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
hss = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎الهمسـة لـ"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص)."
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎لـ أࢪسـال همسـه سـريـه الى"
ddd = "💌"
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
    
    query_user_id = event.query.user_id
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    
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
                zilzal += f"👤 {u.first_name}"
            user_list.append(u.id)
            zilzal += " "
        
        zilzal = zilzal[:-1]
        old_msg = os.path.join("./JoKeRUB", f"{query_user_id}.txt")
        
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
        
        # إنشاء النتيجة
        result = builder.article(
            title=f"📩 همسة سرية لـ {zilzal}",
            description="اضغط لفتح الهمسة",
            text=f'''📠 **ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه**
┄─┄─┄─┄┄─┄─┄─┄─┄┄
📍 **الهمسـة لـ** {zilzal}
👁️ **هو فقط من يستطيع رؤيتها**

🔓 **اضغط الزر بالأسفل لفتح الهمسة**''',
            buttons=[[Button.inline("🔓 فتح الهمسة", data=f"secret_{timestamp}")]],
            link_preview=False
        )
        
        await event.answer([result] if result else None)
    
    # معالجة أمر zelzal
    elif string == "zelzal":
        if not gvarstatus("hmsa_id"):
            return
        
        if username and username.startswith("@"):
            zelzal_display = username
        else:
            zelzal_display = f"👤 {full_name}"
        
        result = builder.article(
            title="📨 أرسل همسة سرية",
            description=f"إلى {zelzal_display}",
            text=f'''📠 **ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه**
┄─┄─┄─┄┄─┄─┄─┄─┄┄
📍 **لـ أرسال همسـه سـريـه الى** {zelzal_display}
💌 **اكتب رسالتك بعد الضغط على الزر**''',
            buttons=[[
                Button.switch_inline(
                    "💌 اضغـط هنـا للكتابة",
                    query=f"secret {user_id} ",
                    same_peer=True
                )
            ]],
            link_preview=False
        )
        
        await event.answer([result] if result else None)
