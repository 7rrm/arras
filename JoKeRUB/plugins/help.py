from telethon import Button, events
from telethon.tl.functions.users import GetUsersRequest

from . import l313l
from ..Config import Config

@l313l.ar_cmd(pattern="مساعده")
async def help(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await l313l.get_me()
        if query.startswith("مساعدة") and event.query.user_id == l313l.uid:
            buttons = [
                [Button.inline("البـحـث والتحميـل 🪄", data="kdownload")],
                [
                    Button.inline("السـورس 🌐", data="botvr"),
                    Button.inline("الحساب 🚹", data="acccount"),
                ],
                [
                    Button.inline("الإذاعـة 🏟️", data="broadcastz"),
                ],
                [
                    Button.inline("الكلايـش & التخصيص 🪁", data="kalaysh"),
                ],
                [
                    Button.inline("المجمـوعـة 2⃣", data="groupv2"),
                    Button.inline("المجمـوعـة 1⃣", data="groupv1"),
                ],
                [
                    Button.inline("حماية المجموعات 🛗", data="grouppro"),
                ],
                [
                    Button.inline("التسليـه & التحشيش 🎃", data="funzed"),
                ],
                [
                    Button.inline("المرفقـات 🪁", data="extras"),
                    Button.inline("الادوات 💡", data="toolzed"),
                ],
                [
                    Button.inline("الفـارات 🎈", data="varszed"),
                ],
                [
                    Button.inline("الذكـاء الاصطنـاعـي 🛸", data="ZEDAI"),
                ],
                [
                    Button.inline("السوبـرات 🎡", data="superzzz"),
                    Button.inline("التجميـع 🛗", data="pointzzz"),
                ],
            ]
            result = builder.article(
                title="l313l",
                text="**مرحباً بك في قائمة المساعدة**\n\nيمكنك تصفح الأقسام المختلفة باستخدام الأزرار أدناه:",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"kdownload")))
@check_owner
async def zed_help(event):
    zelzal = "⤶ عـذراً عـزيـزي 🤷🏻‍♀\n⤶ هـذه اللوحه لا تشتغل في الخاص\n⤶ لـ إظهـار لوحـة المسـاعـدة 👇\n\n⤶ ارســل (.مساعده) في اي مجمـوعـه"
    try:
        await event.edit(
            "[ᯓ 𝗭𝗧𝗵𝗼𝗻 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 - اوامــر البحـث والتحميــل 🛰](t.me/ZThon) .\n\n**⎉╎اليك عـزيـزي شـࢪوحـات اوامـر البحث والتحميـل من جميـع مواقـع الـ سوشـل ميديـا :**\n\n",
            buttons=[
                [
                    Button.inline("فيديو", data="vedzed"),
                    Button.inline("بحث", data="songzed"),
                ],
                [
                    Button.inline("فيس بوك", data="facebook"),
                ],
                [
                    Button.inline("تحميل صوت", data="downsou"),
                    Button.inline("تحميل فيديو", data="downved"),
                ],
                [
                    Button.inline("متحركات", data="giff"),
                    Button.inline("ملصقات", data="stickkers"),
                ],
                [
                    Button.inline("يوتيوب", data="youtubb"),
                    Button.inline("ساوند كلود", data="soundcloud"),
                ],
                [
                    Button.inline("انستا", data="insta"),
                    Button.inline("بنترست", data="pentrist"),
                    Button.inline("تيك توك", data="tiktok"),
                ],
                [
                    Button.inline("كتـاب", data="bookzzz"),
                    Button.inline("منشور مقيد", data="savzzz"),
                    Button.inline("ستوري", data="storyzzz"),
                ],
                [
                    Button.inline("بحث قنوات + مجموعات", data="telech"),
                ],
                [
                    Button.inline("بحث كلمه داخل المجموعة", data="telecg"),
                ],
                [Button.inline("رجوع", data="ZEDHELP")],
            ],
        link_preview=False)
    except Exception:
        await event.answer(zelzal, cache_time=0, alert=True)
        
