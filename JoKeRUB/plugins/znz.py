# -*- coding: utf-8 -*-
import json
import os
import re
import time
import random
from uuid import uuid4
import requests

from telethon.events import InlineQuery
from telethon.tl.functions.users import GetUsersRequest

from . import l313l
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# --------------------------------------
#  📦  إعدادات ثابتة
# --------------------------------------
SECRET_EMOJI_ID = "5210763312597326700"   # 📨
CHECK_EMOJI_ID  = "5210740682414644888"   # ✅
CLOCK_EMOJI_ID  = "5839380464116175529"   # 🕖
FIRE_EMOJI_ID   = "5368324170671202286"   # 🔥

# --------------------------------------
#  🔐  التحقق من الصلاحية
# --------------------------------------
def is_authorized(user_id: int) -> bool:
    if user_id == Config.OWNER_ID or user_id in Config.SUDO_USERS:
        return True
    stored_id = gvarstatus("hmsa_id")
    if stored_id and str(user_id) == stored_id:
        return True
    return False

# --------------------------------------
#  🎯  معالج طلبات الإنلاين
# --------------------------------------
@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    query = event.text.strip()
    user_id = event.query.user_id

    if not is_authorized(user_id):
        return

    if query == "zelzal":
        await answer_start_button(event)
        return

    if query.startswith("secret "):
        await create_secret(event, query)
        return

# --------------------------------------
#  🔹  دالة عرض زر البداية (بشكل ملون + أيقونة)
# --------------------------------------
async def answer_start_button(event):
    stored_id = gvarstatus("hmsa_id")
    stored_name = gvarstatus("hmsa_name")
    stored_user = gvarstatus("hmsa_user")
    if not stored_id:
        return

    # نص الهمسة مع إيموجي بريميوم
    text = f'''
<tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji> <b>همسة سريّة</b> <tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji>

<b>لـ</b> {stored_user or f'[{stored_name}](tg://user?id={stored_id})'}
<b>اضغط الزر بالأسفل لبدء الكتابة</b>
'''

    # الزر الملون مع أيقونة – هذا زر callback، عند الضغط يرسل البوت رسالة فيها switch_inline
    button = {
        "text": f"✍️ ابدأ الهمسة  🔐",
        "callback_data": "start_whisper",   # سيتم معالجته في ملف آخر (مثلاً قراءة الهمسة)
        "style": "primary",                 # لون أزرق
        "icon_custom_emoji_id": SECRET_EMOJI_ID
    }

    keyboard = {"inline_keyboard": [[button]]}

    inline_result = [{
        "type": "article",
        "id": str(uuid4()),
        "title": "📬  همسة سريّة جديدة",
        "description": f"إلى {stored_name}",
        "input_message_content": {
            "message_text": text,
            "parse_mode": "HTML"
        },
        "reply_markup": keyboard
    }]

    await answer_inline_query(event.id, inline_result)

# --------------------------------------
#  🔹  دالة إنشاء الهمسة (secret ...)
# --------------------------------------
async def create_secret(event, query):
    query_body = query[7:]

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

    user_pattern = re.compile(r"@\w+|\d+")
    user_matches = user_pattern.findall(raw_users)
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

    # معرف فريد
    timestamp = int(time.time() * 1000)
    secret_id = f"{timestamp}_{random.randint(100, 999)}"

    # حفظ الهمسة
    user_dir = "./JoKeRUB"
    os.makedirs(user_dir, exist_ok=True)
    # نستخدم أول مستلم كاسم ملف، أو يمكن استخدام معرف فريد
    file_path = os.path.join(user_dir, f"whispers_{user_list[0]}.json")

    try:
        with open(file_path, "r") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {}

    db[secret_id] = {
        "userid": user_list,
        "text": secret_text,
        "sender_id": event.query.user_id,
        "timestamp": timestamp
    }

    with open(file_path, "w") as f:
        json.dump(db, f, indent=4)

    # --------------------------------------
    #  💎  بناء الهمسة نفسها (زر ملون مع أيقونة)
    # --------------------------------------
    message_text = f"""
<tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji> <b>همسة سريّة</b> <tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji>

<b>إلى:</b> {mention_str}
<b>المحتوى:</b> <code>{secret_text}</code>
——————————————————
<i>لا يمكن رؤيتها إلا من قبل المستلمين والمرسل</i>
"""

    # زر فتح الهمسة – ملون وبه أيقونة
    open_button = {
        "text": f"🔓 فتح الهمسة  📩",
        "callback_data": f"secret_{secret_id}",
        "style": "primary",
        "icon_custom_emoji_id": SECRET_EMOJI_ID
    }

    # زر رد سريع – ملون وبه أيقونة
    reply_button = {
        "text": f"💬 رد بهمسة",
        "callback_data": f"reply_whisper_{event.query.user_id}",
        "style": "danger",
        "icon_custom_emoji_id": FIRE_EMOJI_ID
    }

    keyboard = {
        "inline_keyboard": [
            [open_button],
            [reply_button]
        ]
    }

    inline_result = [{
        "type": "article",
        "id": str(uuid4()),
        "title": f"🔐 همسة إلى {user_list[0]}",
        "description": secret_text[:30] + ("..." if len(secret_text) > 30 else ""),
        "input_message_content": {
            "message_text": message_text,
            "parse_mode": "HTML"
        },
        "reply_markup": keyboard
    }]

    await answer_inline_query(event.id, inline_result)

# --------------------------------------
#  🔹  دالة الإرسال إلى Bot API
# --------------------------------------
async def answer_inline_query(inline_query_id: int, results: list):
    url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
    payload = {
        "inline_query_id": inline_query_id,
        "results": json.dumps(results),
        "cache_time": 0,
        "is_personal": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=3)
        if resp.status_code != 200:
            LOGS.error(f"answerInlineQuery error: {resp.text}")
    except Exception as e:
        LOGS.error(f"answerInlineQuery exception: {e}")
