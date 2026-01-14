import re
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = "**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        
        if query.startswith("مساعدة"):
            buttons = [
                [Button.inline("البـحـث والتحميـل 🪄", data="zdownload")],
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
                title="قائمة المساعدة",
                text=HELP,
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)

@l313l.ar_cmd(pattern="مساعدة$")
async def help(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

# القائمة الرئيسية
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"ZEDHELP")))
@check_owner
async def _(event):
    butze = [
        [Button.inline("البـحـث والتحميـل 🪄", data="zdownload")],
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
    await event.edit(HELP, buttons=butze, link_preview=False)

# صفحة الكلايش
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"kalaysh")))
@check_owner
async def _(event):
    await event.edit(
        "**🪁 أوامر الكلايش والتخصيص**\n\n"
        "**⎉╎اليك عـزيـزي قنـوات تخصيص كلايـش السـورس**\n"
        "**⎉╎القنوات تحتوي على كلايش متنوعه + اوامر اضافة الكلايش**",
        buttons=[
            [Button.url("كلايش حماية الخاص", "https://t.me/zzkrr")],
            [Button.url("كلايش الايدي", "https://t.me/zziddd")],
            [Button.url("كلايش الفحص", "https://t.me/zzclll")],
            [Button.inline("رجــوع", data="ZEDHELP")],
        ],
    link_preview=False)

# =========================================================== #
#                 صفحة البحث والتحميل (الأزرار)                #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"zdownload")))
@check_owner
async def _(event):
    buttons = [
        [
            Button.inline("اليوتيوب 🎵", data="yt_cmd"),
            Button.inline("فيديو 📹", data="video_cmd"),
        ],
        [
            Button.inline("سناب شات 👻", data="snap_cmd"),
            Button.inline("فيسبوك 📘", data="fb_cmd"),
        ],
        [
            Button.inline("بنترست 📌", data="pint_cmd"),
            Button.inline("ساوند كلود 🎧", data="sound_cmd"),
        ],
        [
            Button.inline("تحميل صوت 🔊", data="dl_audio"),
            Button.inline("تحميل فيديو 📥", data="dl_video"),
        ],
        [
            Button.inline("رجــوع ↩️", data="ZEDHELP"),
        ],
    ]
    
    await event.edit(
        "**🎯 أوامر البحث والتحميل**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**\n"
        "**⎉╎كل زر يمثل أمر من أوامر البحث والتحميل**",
        buttons=buttons,
        link_preview=False
    )

# =========================================================== #
#               صفحات تفصيلية لكل أمر (بدون HTML)             #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"yt_cmd")))
@check_owner
async def _(event):
    text = (
    "**🎵 أمر اليوتيوب**\n\n"
    "**⦁** `.تفعيل`/`.تعطيل يوت`\n\n"
    "**⪼ الوصـف**\n"
    "لتفعيل/ لتعطيل بحث اليوتيوب لدى الآخرين \n\n"
    "**⪼ الاسـتخدام **\n"
    "`.تفعيل يوت` في جميع المحادثات الخاصة & في مجموعة محدده \n"
    "`.تعطيل يوت` في جميع المحادثات الخاصة & في مجموعة محدده \n\n"
    "**ملاحضه **\n"
    "عند كتابتك لللأمر في الخاص سيتم تفعيل امر اليوت في جميع المحادثات الخاصه \n\n"
    "او عند كتابته في مجموعة سيتم أخذ هذه المجموعة فقط \n\n"
    "━━━━━━━━━━━━━━\n\n"
    "**⦁** `.يوت`\n\n"
    "**⪼ الوصـف**\n"
    "لتحميل الأغاني من اليوتيوب\n\n"
    "**⪼ الاسـتخدام **\n"
    "`.يوت` + رابط & `.يوت` + كلمة"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"video_cmd")))
@check_owner
async def _(event):
    text = (
        "**📹 أمر الفيديو**\n\n"
        "**⦁ الأمر ⇚** `.تفعيل فيديو` **⇚**\n\n"
        "**⪼ الوصف :** لتفعيل/تعطيل استخدام الامر لدى الآخرين في المحادثات الخاصة & مجموعة محدده\n\n"
        "**⪼ الأستخدام :** `.تفعيل فيديو` في الخاص & `.تعطيل فيديو` في مجموعة محدده\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "**⦁ الأمر ⇚** `.فيديو` **⇚**\n\n"
        "**⪼ الوصف :** لتحميل الفيديو من اليوتيوب\n\n"
        "**⪼ الأستخدام :** `.فيديو` + رابط & `.فيديو` + كلمة"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"snap_cmd")))
@check_owner
async def _(event):
    text = (
        "**👻 أمر السناب شات**\n\n"
        "**⦁ الأمر ⇚** `.سناب` **⇚**\n\n"
        "**⪼ الوصف :** لتحميل من سناب شات\n\n"
        "**⪼ الأستخدام :** `.سناب` + رابط (فقط رابط)"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"fb_cmd")))
@check_owner
async def _(event):
    text = (
        "**📘 أمر الفيسبوك**\n\n"
        "**⦁ الأمر ⇚** `.فيس` **⇚**\n\n"
        "**⪼ الوصف :** لتحميل من فيسبوك\n\n"
        "**⪼ الأستخدام :** `.فيس` + رابط (فقط رابط)"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"pint_cmd")))
@check_owner
async def _(event):
    text = (
        "**📌 أمر بنترست**\n\n"
        "**⦁ الأمر ⇚** `.بنترست` **⇚**\n\n"
        "**⪼ الوصف :** لتحميل من بنترست\n\n"
        "**⪼ الأستخدام :** `.بنترست` + رابط (فقط رابط)"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"sound_cmd")))
@check_owner
async def _(event):
    text = (
        "**🎧 أمر ساوند كلاود**\n\n"
        "**⦁ الأمر ⇚** `.ساوند` **⇚**\n\n"
        "**⪼ الوصف :** لتحميل الأغاني من ساوند كلاود\n\n"
        "**⪼ الأستخدام :** `.ساوند` + رابط (فقط رابط)"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"dl_audio")))
@check_owner
async def _(event):
    text = (
        "**🔊 أمر تحميل صوت**\n\n"
        "**⦁ الأمر ⇚** `.تحميل صوت` **⇚**\n\n"
        "**⪼ الوصف :** تحميـل الاغـاني مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط\n\n"
        "**⪼ الأستخدام :** `.تحميل صوت` + رابط (فقط رابط)"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"dl_video")))
@check_owner
async def _(event):
    text = (
        "**📥 أمر تحميل فيديو**\n\n"
        "**⦁ الأمر ⇚** `.تحميل فيديو` **⇚**\n\n"
        "**⪼ الوصف :** تحميـل الفيديو مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط\n\n"
        "**⪼ الأستخدام :** `.تحميل فيديو` + رابط (فقط رابط)"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               باقي الصفحات (بنفس التنسيق)                    #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"botvr")))
@check_owner
async def _(event):
    text = (
        "**🌐 معلومات السورس**\n\n"
        "**⦁ اسم السورس :** `l313l`\n\n"
        "**⦁ المطور :** `مطور السورس`\n\n"
        "**⦁ الرابط :** `https://github.com/username/l313l`\n\n"
        "**⦁ قناة السورس :** `@l3_3_3l`"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجــوع ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"acccount")))
@check_owner
async def _(event):
    text = (
        "**🚹 معلومات الحساب**\n\n"
        "**⦁ لمعرفة معلومات حسابك :**\n\n"
        "**⪼ استخدام :** `.ايدي`\n\n"
        "**⪼ أو :** `.معلوماتي`"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجــوع ↩️", data="ZEDHELP")],
        ],
        link_preview=False
)
