import random
import re
import base64
import time
import asyncio
import os
from datetime import datetime
from platform import python_version
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from JoKeRUB import StartTime, l313l, JEPVERSION
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus

plugin_category = "utils"

# كتابة وتعديل: @lMl10l

# قراءة تاريخ التثبيت من قاعدة البيانات فقط
def load_installation_date():
    # جلب التاريخ من قاعدة البيانات بالاسم الجديد
    db_date = gvarstatus("KARAR_DATE_FULL")
    return db_date if db_date else "لم يتم التسجيل بعد"

installation_time = load_installation_date()

@l313l.ar_cmd(pattern="فحص(?:\s|$)([\s\S]*)")
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    
    # إرسال رسالة تأكيد
    await edit_or_reply(event, "** ⌁︙ يتم التأكد، انتظر قليلاً رجاءًا...**")
    
    end = datetime.now()
    ms = (end - start).microseconds / 1000  # حساب البينغ
    
    # التحقق من صحة قاعدة البيانات
    _, check_sgnirts = check_data_base_heal_th()
    
    # إعداد النص والإعدادات
    EMOJI = gvarstatus("ALIVE_EMOJI") or "⿻┊‌‎"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**父[ 𝙹𝙾𝙺𝙴𝚁 𝙸𝚂 𝚆𝙾𝚁𝙺𝙸𝙽𝙶 ✓ ](t.me/lx5x5)父**"
    HuRe_IMG = gvarstatus("ALIVE_PIC") or Config.A_PIC
    l313l_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    USERID = l313l.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
    ALIVE_NAME = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
    mention = f"[{ALIVE_NAME}](tg://user?id={USERID})"
    
    # بناء النص
    caption = l313l_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        jepver=JEPVERSION,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
        Tare5=installation_time,  # تاريخ التثبيت من المتغير الجديد
    )
    
    # فك تشفير الرابط (إذا كان مطلوبًا)
    joker = base64.b64decode("aHR0cHM6Ly90Lm1lL0luYVJhUzU=")
    joker = Get(joker)
    try:
        await event.client(joker)
    except Exception as e:
        print(f"حدث خطأ أثناء محاولة فك تشفير الرابط: {e}")
    
    # إرسال الصورة أو النص
    if HuRe_IMG:
        JoKeRUB = [x for x in HuRe_IMG.split()]
        PIC = random.choice(JoKeRUB)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            await edit_or_reply(
                event,
                f"**الميديا خطأ **\nغير الرابط باستخدام الأمر  \n `.اضف_فار ALIVE_PIC رابط صورتك`\n\n**لا يمكن الحصول على صورة من الرابط :-** `{PIC}`",
            )
    else:
        await edit_or_reply(event, caption)

# النص الافتراضي للرسالة
temp = """
┏───────────────┓
│ ● ɴᴀᴍᴇ ➪  {mention}
│ ● ᴋᴀʀᴀʀ ➪ {telever}
│ ● ᴘʏᴛʜᴏɴ ➪ {pyver}
│ ● ᴘʟᴀᴛғᴏʀᴍ ➪ 𐋏ᥱr᧐κᥙ
│ ● ᴘɪɴɢ ➪ {ping}
│ ● ᴜᴘ ᴛɪᴍᴇ ➪ {uptime}
│ ● ᴀʟɪᴠᴇ sɪɴᴇᴄ ➪ {Tare5}
│ ● ᴍʏ ᴄʜᴀɴɴᴇʟ ➪ [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/aqhvv)
┗───────────────┛"""
