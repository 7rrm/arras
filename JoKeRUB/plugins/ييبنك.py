from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
from datetime import datetime
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from JoKeRUB.plugins import mention
from . import l313l

# =========================================================== #
# نص بنك
# =========================================================== #

BANK_TEXT = f"""**᯽︙ يتـم التـأكـد من البنك انتـظر قليلا رجاءا**

┏━━━━━━━┓
┃ ✦ {{ping}}
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
            
            caption = BANK_TEXT.format(ping=ms)
            
            # ✅ نفس أسلوب المطور
            buttons = [
                [Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5", style="primary")],
            ]
            
            await event.answer(
                [await builder.article(
                    title="🏦 بنك آراس",
                    description=f"سرعة البنك: {ms}",
                    text=caption,
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )

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
