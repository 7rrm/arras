from telethon import Button, events
from ..Config import Config
from ..core.managers import edit_or_reply

HELP = f"""
**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي {mention}**  
**🛂┊في قائمـة المسـاعـده والشـروحـات**  
**🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**  

[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 ♥](https://t.me/ZThon)
"""

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if query.startswith("مساعدة") and event.query.user_id == zedub.uid:
            buttons = [
                [Button.inline("البـحـث والتحميـل 🪄", data="zdownload")],
                [Button.inline("السـورس 🌐", data="botvr"), Button.inline("الحساب 🚹", data="acccount")],
                [Button.inline("الإذاعـة 🏟️", data="broadcastz")],
                [Button.inline("الكلايـش & التخصيص 🪁", data="kalaysh")],
                [Button.inline("المجمـوعـة 2⃣", data="groupv2"), Button.inline("المجمـوعـة 1⃣", data="groupv1")],
                [Button.inline("حماية المجموعات 🛗", data="grouppro")],
                [Button.inline("التسليـه & التحشيش 🎃", data="funzed")],
                [Button.inline("المرفقـات 🪁", data="extras"), Button.inline("الادوات 💡", data="toolzed")],
                [Button.inline("الفـارات 🎈", data="varszed")],
                [Button.inline("الذكـاء الاصطنـاعـي 🛸", data="ZEDAI")],
                [Button.inline("السوبـرات 🎡", data="superzzz"), Button.inline("التجميـع 🛗", data="pointzzz")],
            ]
            result = builder.article(
                title="قائمة المساعدة | زدثون",
                text=HELP,
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
