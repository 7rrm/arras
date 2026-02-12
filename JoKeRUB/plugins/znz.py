# -*- coding: utf-8 -*-
# znz.py - إنشاء زر "إرسال عبر البوت" عند كتابة secret في الإنلاين

import json
import os
import re
import time
import random
from uuid import uuid4

from telethon.events import InlineQuery
from telethon.tl.functions.users import GetUsersRequest

from . import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# ----------------------------------------------
#  إيموجي بريميوم (نفس المعرفات)
# ----------------------------------------------
EMOJI_SECRET = "5933974679269151927"   # 📨
WHISPER_DIR = "./JoKeRUB"
os.makedirs(WHISPER_DIR, exist_ok=True)
WHISPERS_FILE = os.path.join(WHISPER_DIR, "whispers.json")

# ----------------------------------------------
#  التحقق من الصلاحية
# ----------------------------------------------
def is_authorized(user_id: int) -> bool:
    if user_id == Config.OWNER_ID or user_id in Config.SUDO_USERS:
        return True
    stored_id = gvarstatus("hmsa_id")
    if stored_id and str(user_id) == stored_id:
        return True
    return False

# ----------------------------------------------
#  معالج طلبات الإنلاين
# ----------------------------------------------
@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    query = event.text.strip()
    user_id = event.query.user_id

    if not is_authorized(user_id):
        return

    if query.startswith("secret "):
        await create_inline_result(event, query)

# ----------------------------------------------
#  إنشاء نتيجة الإنلاين (زر إرسال عبر البوت)
# ----------------------------------------------
async def create_inline_result(event, query):
    query_body = query[7:]

    # فصل المستلمين عن النص
    if "|" in query_body:
        raw_users, secret_text = query_body.split("|", 1)
        raw_users = raw_users.strip()
        secret_text = secret_text.strip()
    else:
        parts = query_body.split(" ", 1)
        if len(parts) < 2:
            return
        raw_users, secret_text = parts[0], parts[1]
        secret_text = secret_text.strip()

    # استخراج المعرفات
    user_matches = re.findall(r"@\w+|\d+", raw_users)
    if not user_matches:
        return

    user_list = []
    mention_str = ""

    for identifier in user_matches:
        try:
            if identifier.isdigit():
                entity = await l313l.get_entity(int(identifier))
            else:
                entity = await l313l.get_entity(identifier)

            uid = entity.id
            user_list.append(uid)

            if entity.username:
                mention_str += f"@{entity.username} "
            else:
                name = entity.first_name or "المستخدم"
                mention_str += f"[{name}](tg://user?id={uid}) "
        except Exception as e:
            LOGS.debug(f"خطأ في جلب المستخدم {identifier}: {e}")
            continue

    mention_str = mention_str.strip()
    if not mention_str:
        return

    # معرف فريد للهمسة
    secret_id = f"{int(time.time() * 1000)}_{random.randint(100, 999)}"

    # حفظ البيانات في ملف JSON الموحد
    try:
        with open(WHISPERS_FILE, "r") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {}

    db[secret_id] = {
        "userid": user_list,
        "text": secret_text,
        "sender_id": event.query.user_id,
        "read": False,
        "chat_id": None,      # سيتم ملؤها لاحقاً عند الإرسال
        "message_id": None
    }

    with open(WHISPERS_FILE, "w") as f:
        json.dump(db, f, indent=4)

    # بناء زر الإرسال عبر البوت
    send_button = {
        "text": "📤 إرسال الهمسة عبر البوت",
        "callback_data": f"sendwhisper_{secret_id}"
    }

    # نص النتيجة
    text = f"""
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>همسة سريّة</b>
<b>إلى:</b> {mention_str}
<b>النص:</b> <code>{secret_text[:30]}{'...' if len(secret_text) > 30 else ''}</code>

⬆️ اضغط الزر لإرسال الهمسة عبر البوت
"""

    keyboard = {"inline_keyboard": [[send_button]]}

    # إنشاء نتيجة الإنلاين
    result = {
        "type": "article",
        "id": str(uuid4()),
        "title": f"🔐 همسة إلى {user_list[0]}",
        "description": secret_text[:50],
        "input_message_content": {
            "message_text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        },
        "reply_markup": keyboard
    }

    # إرسال النتيجة عبر API الخاص بـ Telethon (event.answer)
    await event.answer([result] if result else None, cache_time=0)
