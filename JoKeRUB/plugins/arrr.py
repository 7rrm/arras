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
                [Button.inline("البـحـث والتحميـل 🪄", data="search_download_menu")],
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

    async def show_main_menu(event):
        buttons = [
            [Button.inline("البـحـث والتحميـل 🪄", data="search_download_menu")],
        ]
        await event.edit(
            text=ROE,
            buttons=buttons
        )

    @tgbot.on(events.CallbackQuery(pattern=r"search_download_menu"))
    async def search_download_buttons(event):
        await event.edit(
            text="**♰ قائمة البحث والتحميل ♰**",
            buttons=[
                [Button.inline("بحـث", data="search_cmd"), Button.inline("فـيديو", data="video_cmd")],
                [Button.inline("سـاونـد", data="sound_cmd")],
                [Button.inline("تحميل صوت", data="download_sound_cmd"), Button.inline("تحميل فـيديو", data="download_video_cmd")],
                [Button.inline("سـناب", data="snap_cmd")],
                [Button.inline("انـستـا", data="insta_cmd"), Button.inline("فـيسبـوك", data="facebook_cmd")],
                [Button.inline("بـنترسـت", data="pinterest_cmd")],
                [Button.inline("رجـوع", data="main_menu")]
            ]
        )

    @tgbot.on(events.CallbackQuery(pattern="main_menu"))
    async def back_to_main(event):
        await show_main_menu(event)


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

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"search_cmd")))
@check_owner
async def search_command(event):
    await event.edit(
        """[ᯓ  𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - اوامــر البحـث والتحميــل 🛰](t.me/ZThon) .
**- الامـر :**
**⪼** `.بحث`

**- الوصـف :**
لـ البحث وتحميـل الاغاني والمقاطـع الصوتيـه من يوتيـوب

**- الاستخـدام :**
`.بحث` + اسـم الاغنيـه

**- مثـال :**
`.بحث حسين الجسمي احبك`""",
        buttons=[
            [Button.inline("رجوع", data="search_download_menu")],
        ],
    link_preview=False)
