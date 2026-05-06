from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import re
from datetime import datetime
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from ..core import check_owner
from . import l313l

# =========================================================== #
# تعريف الـ mention
# =========================================================== #

USERID = l313l.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
mention = f"[{Config.ALIVE_NAME}](tg://user?id={USERID})"
hmention = f"<a href='tg://user?id={USERID}'>{Config.ALIVE_NAME}</a>"

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
    @check_owner  # ✅ أضف هذا للتحقق من الصلاحيات
    async def inline_bank_handler(event):
        builder = event.builder
        query = event.text
        
        # ✅ طباعة للتأكد من وصول الاستعلام
        print(f"استعلام مضمن: {query}")
        
        if query == "بنك" or query.startswith("بنك"):
            # حساب وقت الاستجابة
            start = datetime.now()
            await asyncio.sleep(0.1)
            end = datetime.now()
            ms = (end - start).microseconds / 1000
            
            caption = BANK_TEXT.format(ping=ms)
            
            buttons = [
                [Button.url(f"👤 {Config.ALIVE_NAME}", f"tg://user?id={USERID}", style="primary")],
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
            print("✅ تم إرسال نتيجة بنك")

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

    TG_BOT = Config.TG_BOT_USERNAME
    
    # ✅ طباعة للتأكد من اسم البوت
    print(f"اسم البوت: {TG_BOT}")
    
    response = await l313l.inline_query(TG_BOT, "بنك")
    
    # ✅ طباعة عدد النتائج
    print(f"عدد النتائج: {len(response) if response else 0}")
    
    if response and len(response) > 0:
        await response[0].click(event.chat_id)
        await event.delete()
    else:
        await event.edit("❌ لم يتم العثور على استعلام مضمن\nتأكد من تشغيل البوت بشكل صحيح")
