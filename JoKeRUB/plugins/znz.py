# Zilzalll
# Copyright (C) 2023 Zilzalll . All Rights Reserved
#
# This file is a part of < https://github.com/Zilzalll/ZThon/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Zilzalll/ZThon/blob/main/LICENSE/>.
"""سـورس زدثــون ™
So تخمـط الملـف اهينك واطشك للناس خماط واوثق عليك
Copyright (C) 2023 Zilzalll . All Rights Reserved
Credit: https://github.com/Zilzalll/ZThon
Devloper: https://t.me/zzzzl1l - زلــزال الهيبــه"""
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
fmm = "فتـح الهمسـه 🗳"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **همسـة سـࢪيـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص).\nعبـر زدثــون"
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - همسـة سـࢪيـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎اضغـط الـزر بالاسفـل ⚓\n⌔╎لـ اࢪسـال همسـه سـࢪيـه الى"
ddd = "💌"
bbb = None
# Copyright (C) 2023 Zilzalll . All Rights Reserved

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    query_user_id = event.query.user_id
    
    # جلب بيانات المستهدف من المتغيرات
    user_id = int(gvarstatus("hmsa_id")) if gvarstatus("hmsa_id") else None
    full_name = gvarstatus("hmsa_name") if gvarstatus("hmsa_name") else None
    username = gvarstatus("hmsa_user") if gvarstatus("hmsa_user") else None
    
    # التحقق من الصلاحيات
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS or query_user_id == user_id:
        inf = re.compile(r"secret (\d+) (.+)")
        match = re.match(inf, query)
        
        if match:
            target_id, message = match.groups()
            target_id = int(target_id)
            
            # إنشاء ملف الهمسة إذا لم يكن موجوداً
            os.makedirs("./JoKeRUB", exist_ok=True)
            msg_file = f"./JoKeRUB/{target_id}.txt"
            
            # حفظ الهمسة
            timestamp = int(time.time())
            msg_data = {
                str(timestamp): {
                    "userid": [target_id],
                    "text": message,
                    "sender": query_user_id
                }
            }
            
            try:
                if os.path.exists(msg_file):
                    with open(msg_file, "r") as f:
                        existing = json.load(f)
                    existing.update(msg_data)
                    with open(msg_file, "w") as f:
                        json.dump(existing, f)
                else:
                    with open(msg_file, "w") as f:
                        json.dump(msg_data, f)
            except Exception as e:
                LOGS.error(f"Error saving secret message: {e}")
                return
            
            # إنشاء زر الفتح
            buttons = [
                [Button.inline(fmm, data=f"open_secret_{timestamp}")],
                [Button.switch_inline(bmm, query=f"secret {target_id} ", same_peer=True)]
            ]
            
            # إنشاء نتيجة الإنلاين
            result = builder.article(
                title=f"{hmm}",
                description=f"{dss}",
                text=f"{hss} {username or full_name or target_id}\n**{dss}**",
                buttons=buttons,
                link_preview=False
            )
            
            await event.answer([result] if result else None)

@l313l.tgbot.on(CallbackQuery(data=re.compile(r"open_secret_(\d+)")))
async def open_secret(event):
    timestamp = int(event.pattern_match.group(1))
    user_id = event.query.user_id
    
    # البحث عن الهمسة
    try:
        for file in os.listdir("./JoKeRUB"):
            if file.endswith(".txt"):
                with open(f"./JoKeRUB/{file}", "r") as f:
                    data = json.load(f)
                    if str(timestamp) in data:
                        msg = data[str(timestamp)]
                        if user_id in [msg["sender"]] + msg["userid"]:
                            await event.answer(msg["text"], alert=True)
                            return
                        else:
                            await event.answer("ليس لديك صلاحية رؤية هذه الهمسة!", alert=True)
                            return
    except Exception as e:
        LOGS.error(f"Error opening secret: {e}")
    
    await event.answer("الهمسة غير موجودة أو انتهت صلاحيتها!", alert=True)
