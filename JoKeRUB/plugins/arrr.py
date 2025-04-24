import re
from telethon import Button, events
from telethon.events import CallbackQuery
from l313l.razan.resources.assistant import *
from l313l.razan.resources.mybot import *
from JoKeRUB import l313l
from ..core import check_owner
from ..Config import Config

# الصورة الرئيسية للقائمة
JEP_IC = "https://graph.org/file/a467d3702fbc9ae391fe0-e6322ec96a2fd4c1f4.jpg"
ROE = "**♰ هـذه هي قائمة اوامـر السـورس  ♰**"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("مساعده") and event.query.user_id == bot.uid:
            buttons = [
                [Button.inline("اوامر الادمن 🧑‍💻", data="l313l0")],
                [
                    Button.inline("اوامر البوت 🤖", data="rozbot"),
                    Button.inline("الحساب 🆔", data="Jmrz"),
                    Button.inline("المجموعات 👥", data="gro"),
                ],
                [
                    Button.inline("الصيغ & الجهات ⚡", data="sejrz"),
                    Button.inline("الحماية & تلكراف ⚓", data="grrz"),
                ],
                [
                    Button.inline("اوامر التسلية 💫", data="tslrzj"),
                    Button.inline("الترحيبات & الردود 👋", data="r7brz"),
                ],
                [
                    Button.inline("اومر المساعدة ✨", data="krrznd"),
                    Button.inline("الملصقات وصور 🌃", data="jrzst"),
                ],
                [
                    Button.inline("التكرار والتنظيف 🚮", data="krrznd"),
                    Button.inline("الترفيـه ✨", data="rfhrz"),
                ],
                [
                    Button.inline("الأكستـرا ⚡", data="iiers"),
                    Button.inline("الانتحال والتقليد 🗣️", data="uscuxrz"),
                ],
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


