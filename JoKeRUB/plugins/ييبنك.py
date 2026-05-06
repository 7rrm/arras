from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import random
from datetime import datetime
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from . import l313l

# =========================================================== #
# تعريف الـ mention
# =========================================================== #

USERID = l313l.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
mention = f"[{Config.ALIVE_NAME}](tg://user?id={USERID})"

# =========================================================== #
# نص بنك
# =========================================================== #

BANK_TEXT = f"""**᯽︙ يتـم التـأكـد من البنك انتـظر قليلا رجاءا**

┏━━━━━━━┓
┃ ✦ {{ping}}
┃ ✦ {mention}
┗━━━━━━━┛"""

# =========================================================== #
# أمر بنك (طريقة مباشرة)
# =========================================================== #

@l313l.ar_cmd(pattern="بنك$")
async def bank_cmd(event):
    # حساب وقت الاستجابة
    start = datetime.now()
    await asyncio.sleep(0.1)
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    
    caption = BANK_TEXT.format(ping=ms)
    
    # نفس أسلوب زر المطور والسورس
    buttons = [
        [Button.url(f"👤 {Config.ALIVE_NAME}", f"tg://user?id={USERID}", style="primary")],
    ]
    
    # حذف رسالة الأمر
    await event.delete()
    
    # إرسال الرد مع الأزرار
    await event.client.send_message(
        event.chat_id,
        caption,
        buttons=buttons,
        parse_mode="Markdown",
        link_preview=False
    )
