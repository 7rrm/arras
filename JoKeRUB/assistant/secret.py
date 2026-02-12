# -*- coding: utf-8 -*-
# قراءه الهمسه.py - معالج أزرار إرسال الهمسة وفتحها

import json
import os
import re
from datetime import datetime

from telethon import Button
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from JoKeRUB import l313l
from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# ----------------------------------------------
#  إيموجي بريميوم
# ----------------------------------------------
EMOJI_SECRET = "5933974679269151927"   # 📨
EMOJI_CHECK  = "4929526216945305427"   # ✅
EMOJI_CLOCK  = "5839380464116175529"   # 🕖
EMOJI_OTHER  = "4931832872081294660"   # 📨 آخر

WHISPER_DIR = "./JoKeRUB"
WHISPERS_FILE = os.path.join(WHISPER_DIR, "whispers.json")

# ----------------------------------------------
#  دالة تحميل قاعدة بيانات الهمسات
# ----------------------------------------------
def load_whispers():
    try:
        with open(WHISPERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_whispers(data):
    with open(WHISPERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ----------------------------------------------
#  1. زر "إرسال الهمسة عبر البوت"
# ----------------------------------------------
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"^sendwhisper_(.+)")))
async def send_whisper_callback(event):
    secret_id = event.pattern_match.group(1).decode("UTF-8")
    db = load_whispers()
    secret_data = db.get(secret_id)

    if not secret_data:
        await event.answer("❌ هذه الهمسة غير موجودة أو انتهت صلاحيتها.", alert=True)
        return

    # التحقق: فقط الشخص الذي أنشأ الهمسة يمكنه إرسالها
    if event.query.user_id != secret_data["sender_id"] and event.query.user_id not in [Config.OWNER_ID] + Config.SUDO_USERS:
        await event.answer("أنت لست منشئ هذه الهمسة.", alert=True)
        return

    # 1️⃣ إرسال رسالة "جاري التحميل..."
    whisper_msg = await event.reply(
        "⏱️ <b>Generating whisper message...</b>",
        parse_mode="html"
    )

    # 2️⃣ تحضير نص الهمسة الكامل
    recipients = secret_data["userid"]
    mention_str = ""
    for uid in recipients:
        try:
            user = await l313l.get_entity(uid)
            if user.username:
                mention_str += f"@{user.username} "
            else:
                mention_str += f"[{user.first_name}](tg://user?id={uid}) "
        except:
            mention_str += f"[مستخدم](tg://user?id={uid}) "

    text = f'''
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>ᯓ 𝖺𝖱𝖺𝖲 𝖶𝗁𝗂𝗌𝗉 - همسـة سـريـه</b>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<b>⌔╎الهمسـة لـ</b> {mention_str.strip()}
<b>⌔╎المحتوى:</b> <code>{secret_data['text']}</code>
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
<i>⌔╎هو فقط من يستطيع ࢪؤيتهـا</i>
'''

    # زر فتح الهمسة
    open_button = Button.inline("🔓 فتح الهمسة 📩", data=f"openwhisper_{secret_id}")

    # 3️⃣ تعديل الرسالة إلى الهمسة الحقيقية
    await whisper_msg.edit(text, buttons=open_button, parse_mode="html")

    # 4️⃣ حفظ chat_id و message_id لاستخدامها لاحقاً (اختياري)
    secret_data["chat_id"] = whisper_msg.chat_id
    secret_data["message_id"] = whisper_msg.id
    db[secret_id] = secret_data
    save_whispers(db)

    # 5️⃣ حذف رسالة المستخدم التي تحتوي على زر الإرسال (اختياري)
    try:
        await event.delete()
    except:
        pass

    await event.answer("✅ تم إرسال الهمسة.", alert=True)

# ----------------------------------------------
#  2. زر "فتح الهمسة"
# ----------------------------------------------
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"^openwhisper_(.+)")))
async def open_whisper_callback(event):
    secret_id = event.pattern_match.group(1).decode("UTF-8")
    db = load_whispers()
    secret_data = db.get(secret_id)

    if not secret_data:
        await event.answer("❌ هذه الهمسة غير موجودة أو تم حذفها.", alert=True)
        return

    opener_id = event.query.user_id
    allowed_ids = secret_data["userid"] + [secret_data["sender_id"], Config.OWNER_ID]

    if opener_id not in allowed_ids:
        await event.answer("آراس | عَـذراً عَـزيزي الهَمْسَة لَيْسَتْ لكَ .", alert=True)
        return

    # عرض الهمسة
    await event.answer(secret_data["text"], alert=True)

    # إذا كان الفاتح هو أحد المستلمين ولم يسبق القراءة
    if opener_id in secret_data["userid"] and not secret_data.get("read", False):
        # تسجيل وقت القراءة
        now = datetime.now()
        time_str = now.strftime("%I:%M").lstrip("0")

        secret_data["read"] = True
        secret_data["read_time"] = time_str
        secret_data["read_by"] = opener_id
        db[secret_id] = secret_data
        save_whispers(db)

        # تجهيز اسم القارئ
        try:
            reader = await l313l.get_entity(opener_id)
            reader_name = f'<a href="tg://user?id={opener_id}">{get_display_name(reader)}</a>'
        except:
            reader_name = "المستخدم"

        # نص التعديل بعد القراءة
        new_text = f"""
<tg-emoji emoji-id="{EMOJI_SECRET}">📨</tg-emoji> <b>تم قراءة الهمسـة</b> <tg-emoji emoji-id="{EMOJI_CHECK}">✅</tg-emoji>
<b>قـرأهـا</b> {reader_name}
<b>عَـند</b> <code>{time_str}</code> <tg-emoji emoji-id="{EMOJI_CLOCK}">🕖</tg-emoji>
"""

        # زر الرد (همسة للمرسل)
        reply_button = Button.switch_inline(
            "💬 رد بهمسة",
            query=f"secret {secret_data['sender_id']} \n",
            same_peer=True
        )

        # تعديل رسالة الهمسة الأصلية
        try:
            await event.edit(new_text, buttons=reply_button, parse_mode="html")
        except Exception as e:
            LOGS.error(f"فشل تعديل الرسالة: {e}")
