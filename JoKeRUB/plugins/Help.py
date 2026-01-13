import re
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = f"**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗟𝟯𝟭𝟯𝗟 ♥️](https://t.me/l3_3_3l)\n\n"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        
        if query.startswith("مساعدة"):
            buttons = [
                [Button.inline("البـحـث والتحميـل 🪄", data="zdownload")],
                [Button.inline("السـورس 🌐", data="botvr")],
                [Button.inline("الحساب 🚹", data="acccount")],
                [Button.inline("رجوع", data="ZEDHELP")]
            ]
            result = builder.article(
                title="قائمة المساعدة",
                text=HELP,
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)

@l313l.on(events.NewMessage(pattern=r"^\.مساعدة$"))
async def help(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"ZEDHELP")))
async def _(event):
    await event.edit(
        HELP,
        buttons=[
            [Button.inline("البـحـث والتحميـل 🪄", data="zdownload")],
            [Button.inline("الكلايـش", data="kalaysh")],
            [Button.inline("رجوع", data="back")]
        ],
        link_preview=False
    )
