import re
from telethon import Button, events
from telethon.events import CallbackQuery
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
                [Button.inline("اوامر الادمن 🧑‍💻", data="ljsjs")],
                [
                    Button.inline("اوامر البوت 🤖", data="rozbonsnst"),
                    Button.inline("الحساب 🆔", data="Jmrssbz"),
                    Button.inline("المجموعات 👥", data="grsbsbo"),
                ],
                [
                    Button.inline("الصيغ & الجهات ⚡", data="sejbsbsrz"),
                    Button.inline("الحماية & تلكراف ⚓", data="gbsbrrz"),
                ],
                [
                    Button.inline("اوامر التسلية 💫", data="tslrzbzbsj"),
                    Button.inline("الترحيبات & الردود 👋", data="r7brsbsbsz"),
                ],
                [
                    Button.inline("اومر المساعدة ✨", data="krrzbsbsnd"),
                    Button.inline("الملصقات وصور 🌃", data="jrzsbzbzzt"),
                ],
                [
                    Button.inline("التكرار والتنظيف 🚮", data="krrbzbssznd"),
                    Button.inline("الترفيـه ✨", data="rfhbsbrz"),
                ],
                [
                    Button.inline("الأكستـرا ⚡", data="iierbzbzs"),
                    Button.inline("الانتحال والتقليد 🗣️", data="uscuxbzbzrz"),
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


