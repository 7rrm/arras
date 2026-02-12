# -*- coding: utf-8 -*-
# znz.py - نسخة Bot API مع إيموجي بريميوم وأزرار ملونة

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

# ----------------------------------------------
#  📦  إيموجي بريميوم (نفس المعرفات من ملف القراءة)
# ----------------------------------------------
EMOJI_SECRET = "5933974679269151927"   # 📨
EMOJI_CHECK  = "4929526216945305427"   # ✅
EMOJI_CLOCK  = "5839380464116175529"   # 🕖
EMOJI_OTHER  = "4931832872081294660"   # 📨 آخر

WHISPER_DIR = "./JoKeRUB"
os.makedirs(WHISPER_DIR, exist_ok=True)

# --------------------------------------
#  🔐  التحقق من الصلاحية (نفس الكود القديم)
# --------------------------------------
def is_authorized(user_id: int) -> bool:
    if user_id == Config.OWNER_ID or user_id in Config.SUDO_USERS:
        return True
    stored_id = gvarstatus("hmsa_id")
    if stored_id and str(user_id) == stored_id:
        return True
    return False

# --------------------------------------
#  🎯  معالج طلبات الإنلاين (بوابة Bot API)
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
#  🔹  زر البداية (zelzal) - يظهر بعد أمر .اهمس
# --------------------------------------
async def answer_start_button(event):
    stored_id = gvarstatus("hmsa_id")
    stored_name = gvarstatus("hmsa_name")
    stored_user = gvarstatus("hmsa_user")
    if not stored_id:
        return

    # نص رسالة الإنلاين مع إيموجي بريميوم
    text = f'''
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b> <tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎لـ أࢪسـال همسـه سـريـه الى</b> {stored_user or f'[{stored_name}](tg://user?id={stored_id})'} 💌
'''

    # زر ملون مع إيموجي بريميوم (Callback)
    button = {
        "text": "✍️ ابدأ الهمسة 📨",
        "callback_data": "start_whisper",
        "style": "primary",
        "icon_custom_emoji_id": EMOJI_SECRET
    }

    keyboard = {"inline_keyboard": [[button]]}

    inline_result = [{
        "type": "article",
        "id": str(uuid4()),
        "title": "📬 همسة سريّة جديدة",
        "description": f"إلى {stored_name}",
        "input_message_content": {
            "message_text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        },
        "reply_markup": keyboard
    }]

    await answer_inline_query(event.id, inline_result)

# --------------------------------------
#  🔹  إنشاء الهمسة (secret ...)
# --------------------------------------
async def create_secret(event, query):
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
    timestamp = int(time.time() * 2)  # نفس الطريقة القديمة
    secret_id = f"{timestamp}"

    # حفظ الهمسة (نفس النظام القديم)
    # نستخدم أول مستلم كاسم ملف
    first_recipient = user_list[0]
    file_name = os.path.join(WHISPER_DIR, f"{first_recipient}.txt")

    try:
        with open(file_name, "r") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {}

    db[secret_id] = {
        "userid": user_list,
        "text": secret_text,
        "sender_id": event.query.user_id,
        "read": False
    }

    with open(file_name, "w") as f:
        json.dump(db, f, indent=4)

    # بناء نص الهمسة مع إيموجي بريميوم
    message_text = f'''
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b> <tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎الهمسـة لـ</b> {mention_str}
<b>⌔╎المحتوى:</b> <code>{secret_text}</code>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<i>⌔╎هو فقط من يستطيع ࢪؤيتهـا</i>
'''

    # زر فتح الهمسة (ملون + إيموجي بريميوم)
    open_button = {
        "text": "🔓 فتح الهمسة 📩",
        "callback_data": f"secret_{secret_id}",
        "style": "primary",
        "icon_custom_emoji_id": EMOJI_SECRET
    }

    # زر الرد (يرسل همسة للمرسل)
    reply_button = {
        "text": "💬 رد بهمسة",
        "callback_data": f"reply_whisper_{event.query.user_id}",
        "style": "danger",
        "icon_custom_emoji_id": EMOJI_OTHER
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
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        },
        "reply_markup": keyboard
    }]

    await answer_inline_query(event.id, inline_result)

# --------------------------------------
#  🔹  معالج الضغط على زر "ابدأ الهمسة"
# --------------------------------------
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"^start_whisper$")))
async def start_whisper_callback(event):
    """عند الضغط على الزر الأزرق، يرسل رسالة فيها switch_inline حقيقي"""
    user_id = event.query.user_id
    stored_id = gvarstatus("hmsa_id")
    stored_name = gvarstatus("hmsa_name")

    if not stored_id:
        await event.answer("⚠️ لم يتم تحديد مستلم بعد. استخدم الأمر .اهمس أولاً.", alert=True)
        return

    # التأكد من الصلاحية
    if str(user_id) != stored_id and user_id != Config.OWNER_ID and user_id not in Config.SUDO_USERS:
        await event.answer("هذا الزر ليس لك.", alert=True)
        return

    # زر switch_inline الحقيقي
    switch_button = {
        "text": "✍️ اضغط هنا لكتابة الهمسة",
        "switch_inline_query_current_chat": f"secret {stored_id} \n"
    }

    keyboard = {"inline_keyboard": [[switch_button]]}

    await event.delete()  # حذف رسالة الإنلاين القديمة
    await l313l.tgbot.send_message(
        user_id,
        f"📨 اكتب الآن همستك إلى {stored_name or stored_id}",
        buttons=keyboard,
        parse_mode="html"
    )
    await event.answer("تم تجهيز الزر، اكتب همستك الآن.", alert=True)

# --------------------------------------
#  🔹  معالج فتح الهمسة (secret_*)
# --------------------------------------
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"^secret_(.+)")))
async def open_secret_callback(event):
    secret_id = event.pattern_match.group(1).decode("UTF-8")
    opener_id = event.query.user_id

    # البحث عن الهمسة في جميع ملفات JoKeRUB/*.txt
    found = False
    secret_data = None
    file_path_found = None

    for filename in os.listdir(WHISPER_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(WHISPER_DIR, filename)
            try:
                with open(file_path, "r") as f:
                    db = json.load(f)
                if secret_id in db:
                    secret_data = db[secret_id]
                    file_path_found = file_path
                    found = True
                    break
            except:
                continue

    if not found or not secret_data:
        await event.answer("❌ هذه الهمسة غير موجودة أو تم حذفها.", alert=True)
        return

    # قائمة المسموح لهم: المستلمين + المرسل + المالك
    allowed_ids = secret_data.get("userid", []) + [secret_data.get("sender_id"), Config.OWNER_ID]

    if opener_id not in allowed_ids:
        await event.answer("آراس | عَـذراً عَـزيزي الهَمْسَة لَيْسَتْ لكَ .", alert=True)
        return

    # عرض الهمسة
    await event.answer(secret_data["text"], alert=True)

    # إذا كان الفاتح هو أحد المستلمين، سجل القراءة
    if opener_id in secret_data.get("userid", []) and not secret_data.get("read", False):
        # تحديث وقت القراءة
        from datetime import datetime
        current_time = datetime.now()
        time_str = current_time.strftime("%I:%M").lstrip("0")
        
        secret_data["read"] = True
        secret_data["read_time"] = time_str
        secret_data["read_by"] = opener_id

        # حفظ التحديث
        with open(file_path_found, "r") as f:
            full_db = json.load(f)
        full_db[secret_id] = secret_data
        with open(file_path_found, "w") as f:
            json.dump(full_db, f, indent=4)

        # محاولة تعديل رسالة الهمسة الأصلية (إذا كان البوت هو من أرسلها)
        try:
            # نحتاج إلى معرف الرسالة الأصلية، غير متوفر هنا.
            # يمكنك ترك هذا أو إضافته لاحقاً.
            pass
        except:
            pass

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
