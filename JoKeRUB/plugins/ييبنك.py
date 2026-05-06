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
hmention = f"<a href='tg://user?id={USERID}'>{Config.ALIVE_NAME}</a>"

# =========================================================== #
# أمر بنك (طريقة مباشرة - بدون استعلام مضمن)
# =========================================================== #

@l313l.ar_cmd(pattern="بنك$")
async def bank_cmd(event):
    # حساب وقت الاستجابة
    start = datetime.now()
    await asyncio.sleep(0.1)
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    
    caption = f"""**᯽︙ يتـم التـأكـد من البنك انتـظر قليلا رجاءا**

┏━━━━━━━┓
┃ ✦ {ms}
┃ ✦ {mention}
┗━━━━━━━┛"""
    
    buttons = [
        [Button.url(f"👤 {Config.ALIVE_NAME}", f"tg://user?id={USERID}", style="primary")],
    ]
    
    # حذف رسالة الأمر وإرسال الرد
    await event.delete()
    await event.client.send_message(
        event.chat_id,
        caption,
        buttons=buttons,
        parse_mode="Markdown",
        link_preview=False
    )
