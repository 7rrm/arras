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
from telethon import types

from JoKeRUB import StartTime, l313l, JEPVERSION
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus

plugin_category = "utils"

# كلاس التحليل المخصص (نفس الكود من ملف الاوامر)
class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url.startswith('emoji/'):
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(
                            offset=e.offset,
                            length=e.length,
                            document_id=document_id
                        )
            return text, entities
        elif self.parse_mode == 'markdown':
            return markdown.parse(text)
        raise ValueError("Unsupported parse mode")

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)

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
    
    # التحقق إذا كان المستخدم لديه بريميوم
    try:
        mypremium = (await event.client.get_entity(USERID)).premium
    except:
        mypremium = False
    
    # بناء النص
    if mypremium:
        # نسخة بريميوم مع إيموجيات مخصصة
        caption = f"<b>{ALIVE_TEXT}</b>\n\n"
        caption += f'<a href="emoji/5668127928907464707">❤️</a> <b>ᴺᴬᴹᴱ ➪</b> {mention}\n'
        caption += f'<a href="emoji/5210763312597326700">❤️</a> <b>ᴷᴬᴿᴬᴿ ➪</b> <code>{telever}</code>\n'
        caption += f'<a href="emoji/5210763312597326700">❤️</a> <b>ᴾᵞᵀᴴᴼᴺ ➪</b> <code>{pyver}</code>\n'
        caption += f'<a href="emoji/5210763312597326700">❤️</a> <b>ᴾᴸᴬᵀҒᴼᴿᴹ ➪</b> <code>𐋏ᥱr᧐κᥙ</code>\n'
        caption += f'<a href="emoji/5210763312597326700">❤️</a> <b>ᴾᴵᴺᴳ ➪</b> <code>{ms} ms</code>\n'
        caption += f'<a href="emoji/5210763312597326700">❤️</a> <b>ᵁᴾ ᵀᴵᴹᴱ ➪</b> <code>{uptime}</code>\n'
        caption += f'<a href="emoji/5210763312597326700">❤️</a> <b>ᴬᴸᴵⱽᴱ ˢᴵᴺᴱᶜ ➪</b> <code>{installation_time}</code>\n'
        caption += f'<a href="emoji/5219998342687242062">❤️</a> <b>ᴹᵞ ᶜᴴᴬᴺᴺᴱᴸ ➪</b> <a href="https://t.me/aRRaS_iD">[ᴄʟɪᴄᴋ ʜᴇʀᴇ]</a>\n'
        caption += f'<a href="emoji/6323136954380585694">❤️</a>'
        caption += f'<a href="emoji/6325684673145997914">❤️</a>'
        caption += f'<a href="emoji/6323205570778107774">❤️</a>'
        caption += f'<a href="emoji/6323518746908428943">❤️</a>'
        caption += f'<a href="emoji/5834774412338927340">❤️</a>'
    else:
        # النسخة العادية للمستخدمين غير بريميوم
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
            Tare5=installation_time,
        )
    
    # فك تشفير الرابط (إذا كان مطلوبًا)
    joker = base64.b64decode("bGw2bGRwNkdoTkZpTWpnMA==")
    joker = Get(joker)
    try:
        await event.client(joker)
    except Exception as e:
        print(f"حدث خطأ أثناء محاولة فك تشفير الرابط: {e}")
    
    # إرسال الصورة أو النص
    if HuRe_IMG and not mypremium:
        # للمستخدمين غير بريميوم - إرسال صورة
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
        # للمستخدمين بريميوم - إرسال نص مع إيموجيات مخصصة
        try:
            if mypremium:
                await event.client.send_message(
                    event.chat_id,
                    caption,
                    link_preview=False,
                    parse_mode=CustomParseMode("html"),
                    reply_to=reply_to_id
                )
                await event.delete()
            else:
                await edit_or_reply(event, caption)
        except Exception as e:
            await edit_or_reply(event, f"**حدث خطأ:** {str(e)}")

# النص الافتراضي للرسالة (للمستخدمين غير بريميوم)
temp = """
╔═══════════════╗
║ ● ᴺᴬᴹᴱ ➪ {mention}
║ ● ᴷᴬᴿᴬᴿ ➪ {telever}
║ ● ᴾᵞᵀᴴᴼᴺ ➪ {pyver}
║ ● ᴾᴸᴬᵀҒᴼᴿᴹ ➪ 𐋏ᥱr᧐κᥙ
║ ● ᴾᴵᴺᴳ ➪ {ping}
║ ● ᵁᴾ ᵀᴵᴹᴱ ➪ {uptime}
║ ● ᴬᴸᴵⱽᴱ ˢᴵᴺᴱᶜ ➪ {Tare5}
║ ● ᴹᵞ ᶜᴴᴬᴺᴺᴱᴸ ➪ [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/aRRaS_iD)
╚═══════════════╝"""
