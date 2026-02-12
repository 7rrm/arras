
import json
import os
import re
import time
import random
from uuid import uuid4
import requests

from telethon.errors import QueryIdInvalidError
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
SECRET_EMOJI_ID = "5210763312597326700"   # 📨  (همسة)
CHECK_EMOJI_ID  = "5210740682414644888"   # ✅  (تم القراءة)
CLOCK_EMOJI_ID  = "5839380464116175529"   # 🕖  (وقت)
FIRE_EMOJI_ID   = "5368324170671202286"   # 🔥  (تزيين)

COMMAND_HANDLER = Config.COMMAND_HAND_LER

# --------------------------------------
#  🔐  التحقق من الصلاحية
# --------------------------------------
def is_authorized(user_id: int) -> bool:
    """الصلاحية لاستخدام الهمسات (المالك + السودو + الشخص المخزّن)"""
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

    # ❌  منع المستخدمين غير المصرّح لهم
    if not is_authorized(user_id):
        return

    # --------------------------------------
    #  1️⃣  عرض زر البداية (zelzal)
    # --------------------------------------
    if query == "zelzal":
        await answer_start_button(event)
        return

    # --------------------------------------
    #  2️⃣  إنشاء همسة جديدة (secret)
    # --------------------------------------
    if query.startswith("secret "):
        await create_secret(event, query)
        return

# --------------------------------------
#  🔹  دالة عرض زر البداية
# --------------------------------------
async def answer_start_button(event):
    """عند كتابة 'zelzal' في الإنلاين -> زر واحد يفتح الهمسة"""
    stored_id = gvarstatus("hmsa_id")
    stored_name = gvarstatus("hmsa_name")
    stored_user = gvarstatus("hmsa_user")

    if not stored_id:
        return

    # نص جميل مع إيموجي بريميوم
    text = f'''
<tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji> <b>همسة سريّة</b> <tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji>

<b>لـ</b> {stored_user or f'[{stored_name}](tg://user?id={stored_id})'}
<b>اضغط الزر بالأسفل لبدء الكتابة</b>
'''

    # زر Switch Inline (يوجه المستخدم لكتابة "secret @id نص")
    button = {
        "text": f"✍️ ابدأ الهمسة  {chr(65039)}",  # يمكنك إضافة إيموجي عادي هنا
        "switch_inline_query_current_chat": f"secret {stored_id} \n"
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
    """معالجة الأمر: secret @user1 @user2 | النص السري"""
    # قص كلمة "secret " من البداية
    query_body = query[7:]

    # فصل المستلمين عن النص باستخدام "|"
    if "|" in query_body:
        raw_users, secret_text = query_body.split("|", 1)
        raw_users = raw_users.strip()
        secret_text = secret_text.strip()
    else:
        # صيغة قديمة: user نص
        parts = query_body.split(" ", 1)
        if len(parts) < 2:
            return
        raw_users, secret_text = parts[0], parts[1]
        secret_text = secret_text.strip()

    # استخراج المعرفات (يدعم @username, id رقمي, منشن)
    user_pattern = re.compile(r"@\w+|\d+")
    user_matches = user_pattern.findall(raw_users)
    if not user_matches:
        return

    # تحويل المعرفات إلى كائنات مستخدمين وحفظ الأسماء
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

    # إنشاء معرف فريد للهمسة
    timestamp = int(time.time() * 1000)  # ملي ثانية
    secret_id = f"{timestamp}_{random.randint(100, 999)}"

    # حفظ الهمسة في ملف JSON (بنفس الطريقة القديمة)
    user_dir = "./JoKeRUB"
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, f"{user_list[0]}.txt")  # نستخدم أول مستلم كاسم ملف

    try:
        with open(file_path, "r") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {}

    db[secret_id] = {
        "userid": user_list,
        "text": secret_text,
        "sender_id": event.query.user_id,  # مهم لمعرفة المرسل
        "timestamp": timestamp
    }

    with open(file_path, "w") as f:
        json.dump(db, f, indent=4)

    # --------------------------------------
    #  💎  بناء النتيجة الإنلاين (الهمسة)
    # --------------------------------------
    # نص الهمسة مع إيموجي بريميوم
    message_text = f"""
<tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji> <b>همسة سريّة</b> <tg-emoji emoji-id="{SECRET_EMOJI_ID}">📨</tg-emoji>

<b>إلى:</b> {mention_str}
<b>المحتوى:</b> <code>{secret_text}</code>
——————————————————
<i>لا يمكن رؤيتها إلا من قبل المستلمين والمرسل</i>
"""

    # زر "فتح الهمسة" – يظهر للجميع لكن الضغط محكوم بالصلاحية
    open_button = {
        "text": f"🔓 فتح الهمسة  {chr(65039)}",
        "callback_data": f"secret_{secret_id}",
        "style": "primary",
        "icon_custom_emoji_id": SECRET_EMOJI_ID
    }

    # زر "رد سريع" (اختياري) – يظهر فقط للمرسل؟ لا، يمكن للجميع لكنه مفيد
    reply_button = {
        "text": f"💬 رد بهمسة",
        "switch_inline_query_current_chat": f"secret {event.query.user_id} \n",
        "style": "danger",
        "icon_custom_emoji_id": FIRE_EMOJI_ID
    }

    # يمكن إضافة أزرار إضافية حسب الرغبة
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
    """إرسال النتائج عبر طلب HTTP مباشر إلى Telegram Bot API"""
    url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
    payload = {
        "inline_query_id": inline_query_id,
        "results": json.dumps(results),
        "cache_time": 0,          # عدم التخزين المؤقت
        "is_personal": True       # نتائج خاصة بالمستخدم
    }
    try:
        resp = requests.post(url, json=payload, timeout=3)
        if resp.status_code != 200:
            LOGS.error(f"answerInlineQuery error: {resp.text}")
    except Exception as e:
        LOGS.error(f"answerInlineQuery exception: {e}")
