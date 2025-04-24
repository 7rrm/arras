import re
from telethon import Button, events
from telethon.events import CallbackQuery
from JoKeRUB import l313l
from ..core import check_owner
from ..Config import Config

# الصورة الرئيسية للقائمة
JEP_IC = "https://graph.org/file/a467d3702fbc9ae391fe0-e6322ec96a2fd4c1f4.jpg"
ROE = "**♰ هـذه هي قائمة اوامـر السـورس ♰**"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("مساعده") and event.query.user_id == bot.uid:
            buttons = [
                [Button.inline("البـحـث والتحميـل 🪄", data="search_download")],
            ]
            if JEP_IC and JEP_IC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    JEP_IC, text=ROE, buttons=buttons, link_preview=False
                )
            elif JEP_IC:
                result = builder.document(
                    JEP_IC,
                    title="JoKeRUB",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="JoKeRUB",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)

    @tgbot.on(events.CallbackQuery(pattern="search_download"))
    async def search_download_buttons(event):
        await event.edit(
            buttons=[
                [Button.inline("بحـث", data="search"), Button.inline("فـيديو", data="video")],
                [Button.inline("سـاونـد", data="sound")],
                [Button.inline("تحميل صوت", data="download_sound"), Button.inline("تحميل فـيديو", data="download_video")],
                [Button.inline("سـناب", data="snap")],
                [Button.inline("انـستـا", data="insta"), Button.inline("فـيسبـوك", data="facebook")],
                [Button.inline("بـنترسـت", data="pinterest")]
            ]
        )


@bot.on(admin_cmd(outgoing=True, pattern="مساعده"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "مساعده")
    await response[0].click(event.chat_id)
    await event.delete()
