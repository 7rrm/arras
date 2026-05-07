from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import random
from datetime import datetime
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from JoKeRUB.plugins import mention
from . import l313l

# =========================================================== #
# تعريف الـ mention و USERID
# =========================================================== #

USERID = l313l.uid if Config.OWNER_ID == 0 else Config.OWNER_ID

# الكليشة مباشرة (بدون استدعاء)
ROZ = f"""╭───────• 𝗔𝗥𝗔𝗦 •───────╮
│ **● ʙᴏᴛ sᴛᴀᴛᴜs: ʀᴜɴɴɪɴɢ ✅**
├──────────────────────
│ **● ᴘʟᴀᴛғᴏʀᴍ ᴅᴇᴛᴀɪʟs:**
│ • ᴛᴇʟᴇᴛʜᴏɴ: `1.23.0`
│ • sᴏᴜʀᴄᴇ: `4.0.1`
│ • ʙᴏᴛ: `{Config.TG_BOT_USERNAME}`
│ • ᴘʏᴛʜᴏɴ: `3.9.10`
│ • ᴜsᴇʀ: {mention}
╰──────────────────────╯"""

# كليشة المطور
DEV_TEXT = f"""╭───────• 𝗔𝗥𝗔𝗦 •───────╮
│ **● ᴍʏ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ:**
├──────────────────────
│ **● ɴᴀᴍᴇ:** - Karar .
│ **● ᴜsᴇʀɴᴀᴍᴇ:** @Lx5x5
│ **● ɪᴅ:** 5427469031
│ **● ᴀɢᴇ:** 24
├──────────────────────
│ **● ᴅᴇᴠᴇʟᴏᴘᴇʀ:**
│ • sᴏᴜʀᴄᴇ ᴍᴀᴅᴇ ʙʏ ᴀʀᴀs
│ • ᴛʜᴀɴᴋs ꜰᴏʀ ᴜsɪɴɢ
╰──────────────────────╯"""

# نص بوتي
BOT_TEXT = f"""**⌔╎البـوت المسـاعد الخـاص بك هـو** """

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        query = event.text
        
        # قسم السورس
        if query.startswith("السورس") and event.query.user_id == bot.uid:
            buttons = [
                [Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5", style="danger")],
            ]
            
            await event.answer(
                [await builder.article(
                    title="🔥 JoKeRUB - السورس",
                    description="السورس الرسمي - اضغط للإرسال",
                    text=ROZ,
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )
        
        # قسم المطور
        elif query.startswith("المطور") and event.query.user_id == bot.uid:
            buttons = [
                [Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5", style="primary")],
            ]
            
            await event.answer(
                [await builder.article(
                    title="👨‍💻 مطور السورس",
                    description="المطور الرسمي لسورس آراس",
                    text=DEV_TEXT,
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )
        
        # قسم بوتي
        elif query.startswith("بوتي") and event.query.user_id == bot.uid:
            buttons = [
                [Button.url("‹ : أضغط هُنـا : ›", f"https://t.me/{Config.TG_BOT_USERNAME[1:]}", style="primary")],
            ]
            
            await event.answer(
                [await builder.article(
                    title="🤖 البوت المساعد",
                    description="البوت الخاص بك - اضغط للذهاب",
                    text=BOT_TEXT,
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )
        
        # ✅ قسم بنك (مع صورة)
        elif query.startswith("بنك") and event.query.user_id == bot.uid:
            # حساب وقت الاستجابة
            start = datetime.now()
            await l313l.get_me()  # ✅ طلب حقيقي إلى خوادم تليجرام
            end = datetime.now()
            ms = (end - start).microseconds / 1000
            text = f"""**ㅤㅤ**
┏━━━━━━━━━━━━━━━━┓
┃ ✦ **P𝑖𝑛𝑔 ➢** ‹ `{ms}` ›
┃ ✦ **U𝑠𝑒𝑟 N𝑎𝑚𝑒 ➢** ‹ {mention} › .
┗━━━━━━━━━━━━━━━━┛"""
            
            buttons = [
                [Button.url(f"‹  {Config.ALIVE_NAME}  ›", f"tg://user?id={USERID}", style="primary")],
            ]
            
            # ✅ صورة البنك
            BANK_IMG = "https://graph.org/file/f80a6c2a54cf797321e50-835d28e9d7d5658bc5.jpg"
            
            try:
                result = builder.photo(
                    BANK_IMG,
                    text=text,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="Markdown",
                )
            except Exception:
                result = builder.article(
                    title="🏦 بنك آراس",
                    description=f"سرعة البنك: {ms}",
                    text=text,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="Markdown",
                )
            
            await event.answer([result], cache_time=0)

# =========================================================== #
# الأوامر
# =========================================================== #

@l313l.ar_cmd(pattern="السورس$")
async def repo(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="المطور$")
async def dev_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "المطور")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="بوتي$")
async def bot_cmd(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "بوتي")
    await response[0].click(event.chat_id)
    await event.delete()

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
