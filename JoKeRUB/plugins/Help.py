import re
import html
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = f"**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗟𝟯𝟭𝟯𝗟 ♥️](https://t.me/l3_3_3l)\n\n"

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
        "**🪁 أوامر الكلايش والتخصيص**\n\n**⎉╎اليك عـزيـزي قنـوات تخصيص كلايـش السـورس**\n**⎉╎القنوات تحتوي على كلايش متنوعه + اوامر اضافة الكلايش**",
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
    # أزرار البحث والتحميل - كل زرين في سطر
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
            Button.inline("تحميل فيديo 📥", data="dl_video"),
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
#               صفحات تفصيلية لكل أمر                           #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"yt_cmd")))
@check_owner
async def _(event):
    text = """<b>🎵 أمر اليوتيوب</b>

<code>.تفعيل يوت</code> - لتفعيل/تعطيل استخدام الأمر
<code>.يوت</code> + رابط - لتحميل الأغاني من اليوتيوب
<code>.يوت</code> + كلمة - للبحث وتحميل من اليوتيوب"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"video_cmd")))
@check_owner
async def _(event):
    text = """<b>📹 أمر الفيديو</b>

<code>.تفعيل فيديو</code> - لتفعيل/تعطيل استخدام الأمر
<code>.فيديو</code> + رابط - لتحميل الفيديو من اليوتيوب
<code>.فيديو</code> + كلمة - للبحث وتحميل فيديو"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"snap_cmd")))
@check_owner
async def _(event):
    text = """<b>👻 أمر السناب شات</b>

<code>.سناب</code> + رابط - لتحميل من سناب شات
(يجب أن يكون الرابط من موقع سناب شات فقط)"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"fb_cmd")))
@check_owner
async def _(event):
    text = """<b>📘 أمر الفيسبوك</b>

<code>.فيس</code> + رابط - لتحميل من فيسبوك
(يدعم فيديو وصوت من الفيسبوك)"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"pint_cmd")))
@check_owner
async def _(event):
    text = """<b>📌 أمر بنترست</b>

<code>.بنترست</code> + رابط - لتحميل من بنترست
(يدعم تحميل الصور من بنترست)"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"sound_cmd")))
@check_owner
async def _(event):
    text = """<b>🎧 أمر ساوند كلاود</b>

<code>.ساوند</code> + رابط - لتحميل الأغاني من ساوند كلاود
(يدعم تحميل الأغاني من ساوند كلاود)"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"dl_audio")))
@check_owner
async def _(event):
    text = """<b>🔊 أمر تحميل صوت</b>

<code>.تحميل صوت</code> + رابط - لتحميل الصوت من أي موقع
(يدعم يوتيوب، فيسبوك، انستجرام، تيك توك، إلخ)"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"dl_video")))
@check_owner
async def _(event):
    text = """<b>📥 أمر تحميل فيديو</b>

<code>.تحميل فيديو</code> + رابط - لتحميل الفيديو من أي موقع
(يدعم يوتيوب، فيسبوك، انستجرام، تيك توك، إلخ)"""
    
    await event.edit(
        text,
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

# =========================================================== #
#               باقي الصفحات (يمكنك إضافتها لاحقاً)            #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"botvr")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجــوع", data="ZEDHELP")]]
    await event.edit(
        "**🔗 رابط السورس:**\nhttps://github.com/username/l313l",
        buttons=buttons
    )
