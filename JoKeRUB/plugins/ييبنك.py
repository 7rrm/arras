from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import re
from datetime import datetime
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from JoKeRUB.plugins import mention
from . import l313l

# =========================================================== #
# نص بنك
# =========================================================== #

BANK_TEXT = """**᯽︙ يتـم التـأكـد من البنك انتـظر قليلا رجاءا**

┏━━━━━━━┓
┃ ✦ {ping}
┃ ✦ {mention}
┗━━━━━━━┛"""

# =========================================================== #
# الاستعلام المضمن (بنك)
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_bank_handler(event):
        builder = event.builder
        query = event.text
        
        if query.startswith("بنك") and event.query.user_id == l313l.uid:
            # حساب وقت الاستجابة
            start = datetime.now()
            await asyncio.sleep(0.1)
            end = datetime.now()
            ms = (end - start).microseconds / 1000
            
            # جلب معلومات المستخدم الحالي
            user_id = event.query.user_id
            user = await l313l.get_entity(user_id)
            user_name = user.first_name
            
            caption = BANK_TEXT.format(ping=ms, mention=mention)
            
            # ✅ زر رابط لحساب المستخدم نفسه
            buttons = [
                [Button.url(f"👤 {user_name}", f"tg://user?id={user_id}", style="primary")],
            ]
            
            result = builder.article(
                title="🏦 بنك آراس",
                description=f"سرعة البنك: {ms}",
                text=caption,
                buttons=buttons,
                link_preview=False,
                parse_mode="Markdown",
            )
            
            await event.answer([result], cache_time=0)

# =========================================================== #
# أمر بنك
# =========================================================== #

@l313l.ar_cmd(pattern="بنك$")
async def bank_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "بنك")
    await response[0].click(event.chat_id)
    await event.delete()
