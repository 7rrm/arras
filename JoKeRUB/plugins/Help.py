import re
import html
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = f"**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

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
#               صفحات تفصيلية لكل أمر (بتنسيق الاقتباس)        #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"yt_cmd")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.تفعيل يوت</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتفعيل/تعطيل استخدام الامر لدى الآخرين في المحادثات الخاصة & مجموعة محدده
<b>⪼ الأستخدام :</b> <code>.تفعيل يوت</code> في الخاص & <code>.تعطيل يوت</code> في مجموعة محدده  

<b>⦁ الأمر ⇚ ⟨</b> <code>.يوت</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتحميل الأغاني من اليوتيوب 
<b>⪼ الأستخدام :</b> <code>.يوت</code> + رابط & يوت + كلمة 
</blockquote>"""
    
    await event.edit(
        f"🎵 أمر اليوتيوب\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"video_cmd")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.تفعيل فيديو</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتفعيل/تعطيل استخدام الامر لدى الآخرين في المحادثات الخاصة & مجموعة محدده
<b>⪼ الأستخدام :</b> <code>.تفعيل فيديو</code> في الخاص & <code>.تعطيل فيديو</code> في مجموعة محدده  

<b>⦁ الأمر ⇚ ⟨</b> <code>.فيديو</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتحميل الفيديو من اليوتيوب 
<b>⪼ الأستخدام :</b> <code>.فيديو</code> + رابط & <code>.فيديو</code> + كلمة 
</blockquote>"""
    
    await event.edit(
        f"📹 أمر الفيديو\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"snap_cmd")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.سناب</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتحميل من سناب شات
<b>⪼ الأستخدام :</b> <code>.سناب</code> + رابط (فقط رابط)
</blockquote>"""
    
    await event.edit(
        f"👻 أمر السناب شات\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"fb_cmd")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.فيس</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتحميل من فيسبوك
<b>⪼ الأستخدام :</b> <code>.فيس</code> + رابط (فقط رابط)
</blockquote>"""
    
    await event.edit(
        f"📘 أمر الفيسبوك\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"pint_cmd")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.بنترست</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتحميل من بنترست
<b>⪼ الأستخدام :</b> <code>.بنترست</code> + رابط (فقط رابط)
</blockquote>"""
    
    await event.edit(
        f"📌 أمر بنترست\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"sound_cmd")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.ساوند</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> لتحميل الأغاني من ساوند كلاود
<b>⪼ الأستخدام :</b> <code>.ساوند</code> + رابط (فقط رابط)
</blockquote>"""
    
    await event.edit(
        f"🎧 أمر ساوند كلاود\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"dl_audio")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.تحميل صوت</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> تحميـل الاغـاني مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط
<b>⪼ الأستخدام :</b> <code>.تحميل صوت</code> + رابط (فقط رابط)
</blockquote>"""
    
    await event.edit(
        f"🔊 أمر تحميل صوت\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"dl_video")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.تحميل فيديو</code> <b>⟩</b>\n
<b>⪼ الوصف :</b> تحميـل الفيديو مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط
<b>⪼ الأستخدام :</b> <code>.تحميل فيديو</code> + رابط (فقط رابط)
</blockquote>"""
    
    await event.edit(
        f"📥 أمر تحميل فيديو\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجوع للبحث والتحميل ↩️", data="zdownload")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ]
    )

# =========================================================== #
#               باقي الصفحات (بنفس التنسيق)                    #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"botvr")))
@check_owner
async def _(event):
    text = """<blockquote>
<b>⦁ اسم السورس :</b> <code>l313l</code>
<b>⦁ المطور :</b> <code>مطور السورس</code>
<b>⦁ الرابط :</b> <code>https://github.com/username/l313l</code>
<b>⦁ قناة السورس :</b> <code>@l3_3_3l</code>
</blockquote>"""
    
    await event.edit(
        f"**🌐 معلومات السورس**\n\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجــوع ↩️", data="ZEDHELP")],
        ]
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"acccount")))
@check_owner
async def _(event):
    # يمكنك إضافة معلومات الحساب هنا
    text = """<blockquote>
<b>⦁ لمعرفة معلومات حسابك :</b>
<b>⪼ استخدام :</b> <code>.ايدي</code>
<b>⪼ أو :</b> <code>.معلوماتي</code>
</blockquote>"""
    
    await event.edit(
        f"**🚹 معلومات الحساب**\n\n{text}",
        parse_mode='HTML',
        buttons=[
            [Button.inline("رجــوع ↩️", data="ZEDHELP")],
        ]
    )

# يمكنك إضافة باقي الأزرار بنفس الطريقة...
