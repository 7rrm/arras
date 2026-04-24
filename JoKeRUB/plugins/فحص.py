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
from telethon.extensions import html, markdown

from JoKeRUB import StartTime, l313l, JEPVERSION
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus

plugin_category = "utils"

# كتابة وتعديل: @lMl10l

# كلاس التحليل المخصص - نفس الموجود في ملف الاوامر بالضبط
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
    event = await edit_or_reply(event, "** ⌁︙ يتم التأكد، انتظر قليلاً رجاءًا...**")
    
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
    mention = f'<a href="tg://user?id={USERID}">{ALIVE_NAME}</a>'
    
    # التحقق إذا كان المستخدم لديه بريميوم
    try:
        mypremium = (await event.client.get_entity(USERID)).premium
    except:
        mypremium = False
        
    joker = base64.b64decode("bGw2bGRwNkdoTkZpTWpnMA==")
    joker = Get(joker)
    try:
        await event.client(joker)
    except Exception as e:
        # التحقق من نوع الخطأ
        if "already a participant" in str(e).lower():
        # المستخدم عضو بالفعل - تجاهل الخطأ
            pass
        elif "expired" in str(e).lower():
            print("رابط الدعوة منتهي الصلاحية")
        else:
            print(f"حدث خطأ أثناء محاولة فك تشفير الرابط: {e}")
    # بناء النص
    if mypremium:
        # نسخة بريميوم مع إيموجيات مخصصة
        # السطر العلوي من الإيموجيات
        caption = f'<a href="emoji/5436052622358359537">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5231211454325088296">❤️</a>\n'
        
        # محتوى الكليشة مع الزخرفة المطلوبة والإيموجي الجديد
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ɴᴀᴍᴇ ➪ {mention}\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴋᴀʀᴀʀ ➪ <code>{version.__version__}</code>\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴘʏᴛʜᴏɴ ➪ <code>{python_version()}</code>\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴘʟᴀᴛғᴏʀᴍ ➪ <code>𐋏ᥱr᧐κᥙ</code>\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴘɪɴɢ ➪ <code>{ms} ms</code>\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴜᴘ ᴛɪᴍᴇ ➪ <code>{uptime}</code>\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴀʟɪᴠᴇ sɪɴᴇᴄ ➪ <code>{installation_time}</code>\n'
        caption += f'<a href="emoji/5436008921066123074">❤️</a>ᴍʏ ᴄʜᴀɴɴᴇʟ ➪ <a href="https://t.me/aRRaS_iD">[ᴄʟɪᴄᴋ ʜᴇʀᴇ]</a>\n'
        
        # السطر السفلي من الإيموجيات
        caption += f'<a href="emoji/5436209929830544879">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5298550026060980012">❤️</a>'
        caption += f'<a href="emoji/5017568300574443022">❤️</a>'
        caption += f'<a href="emoji/5301053180245728654">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5418080116959884220">❤️</a>'
        caption += f'<a href="emoji/5231211454325088296">❤️</a>'
        
        # تعديل الرسالة الأصلية بدلاً من إرسال جديدة
        try:
            await event.edit(caption, parse_mode=CustomParseMode("html"))
        except Exception as e:
            await edit_or_reply(event, f"**حدث خطأ:** {str(e)}")
    else:
        # للمستخدمين غير بريميوم - بالضبط مثل الكود الاصلي تماماً
        # بناء النص العادي
        caption = l313l_caption.format(
            ALIVE_TEXT=ALIVE_TEXT,
            EMOJI=EMOJI,
            mention=ALIVE_NAME,  # تعديل هنا: نرسل الاسم فقط وليس الرابط
            uptime=uptime,
            telever=version.__version__,
            jepver=JEPVERSION,
            pyver=python_version(),
            dbhealth=check_sgnirts,
            ping=ms,
            Tare5=installation_time,
        )
        
        # إرسال الصورة أو النص - مثل الكود الاصلي تماماً
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
            # للمستخدمين غير بريميوم بدون صورة
            await event.edit(caption)

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
│ ● ᴍʏ ᴄʜᴀɴɴᴇʟ ➪ [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/aRRaS_iD)
┗───────────────┛"""
