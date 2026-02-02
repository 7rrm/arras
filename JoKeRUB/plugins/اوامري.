"""
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
        if query.startswith("اوامري") and event.query.user_id == bot.uid:
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


@bot.on(admin_cmd(outgoing=True, pattern="اوامري"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "اوامري")
    await response[0].click(event.chat_id)
    await event.delete()


# =========================================================== #
#                 معالجة زر البحث والتحميل                    #
# =========================================================== #
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"zdownload")))
@check_owner
async def _(event):
    commands_text_page1 = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.تفعيل يوت</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتفعيل/تعطيل استخدام الامر لدى الآخرين في المحادثات الخاصة & مجموعة محدده
<b>⪼ الأستخدام :</b> <code>.تفعيل يوت</code> في الخاص & <code>.تعطيل يوت</code> في مجموعة محدده  

<b>⦁ الأمر ⇚ ⟨</b> <code>.يوت</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتحميل الأغاني من اليوتيوب 
<b>⪼ الأستخدام :</b> <code>.يوت</code> + رابط & يوت + كلمة 

<b>⦁ الأمر ⇚ ⟨</b> <code>.تفعيل فيديو</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتفعيل/تعطيل استخدام الامر لدى الآخرين في المحادثات الخاصة & مجموعة محدده
<b>⪼ الأستخدام :</b> <code>.تفعيل فيديو</code> في الخاص & <code>.تعطيل فيديو</code> في مجموعة محدده  

<b>⦁ الأمر ⇚ ⟨</b> <code>.فيديو</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتحميل الفيديو من اليوتيوب 
<b>⪼ الأستخدام :</b> <code>.فيديو</code> + رابط & <code>.فيديو</code> + كلمة 

<b>⦁ الأمر ⇚ ⟨</b> <code>.سناب</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتحميل من سناب شات
<b>⪼ الأستخدام :</b> <code>.سناب</code> + رابط (فقط رابط)

<b>⦁ الأمر ⇚ ⟨</b> <code>.فيس</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتحميل من فيسبوك
<b>⪼ الأستخدام :</b> <code>.فيس</code> + رابط (فقط رابط)
</blockquote>"""
    
    buttons_page1 = [
        [Button.inline("الصفحة التالية ➡️", data="zdownload2")],
        [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]
    ]
    
    await event.edit(
        f"**🎯 أوامر البحث والتحميل - الصفحة 1/2:**\n\n{commands_text_page1}",
        parse_mode='HTML',
        buttons=buttons_page1
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"zdownload2")))
@check_owner
async def _(event):
    commands_text_page2 = """<blockquote>
<b>⦁ الأمر ⇚ ⟨</b> <code>.بنترست</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتحميل من بنترست
<b>⪼ الأستخدام :</b> <code>.بنترست</code> + رابط (فقط رابط)

<b>⦁ الأمر ⇚ ⟨</b> <code>.ساوند</code> <b>⟩</b>
<b>⪼ الوصف :</b> لتحميل الأغاني من ساوند كلاود
<b>⪼ الأستخدام :</b> <code>.ساوند</code> + رابط (فقط رابط)

<b>⦁ الأمر ⇚ ⟨</b> <code>.تحميل صوت</code> <b>⟩</b>
<b>⪼ الوصف :</b> تحميـل الاغـاني مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط
<b>⪼ الأستخدام :</b> <code>.تحميل صوت</code> + رابط (فقط رابط)

<b>⦁ الأمر ⇚ ⟨</b> <code>.تحميل فيديو</code> <b>⟩</b>
<b>⪼ الوصف :</b> تحميـل الفيديو مـن يوتيوب .. فيسبوك .. انستا .. الـخ عـبر الرابـط
<b>⪼ الأستخدام :</b> <code>.تحميل فيديو</code> + رابط (فقط رابط)
</blockquote>"""
    
    buttons_page2 = [
        [Button.inline("⬅️ الصفحة السابقة", data="zdownload")],
        [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]
    ]
    
    await event.edit(
        f"**🎯 أوامر البحث والتحميل - الصفحة 2/2:**\n\n{commands_text_page2}",
        parse_mode='HTML',
        buttons=buttons_page2
    )


# =========================================================== #
#                 معالجة زر القائمة الرئيسية                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"ROE")))
@check_owner
async def _(event):
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
    await event.edit(ROE, buttons=buttons)

# =========================================================== #
#                 معالجة الأزرار الأخرى                       #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"botvr")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]]
    await event.edit(
        "**🔗 رابط السورس:**\nhttps://github.com/username/source",
        buttons=buttons
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"acccount")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]]
    await event.edit(
        "**👤 معلومات الحساب:**\n\n"
        "**⪼ الاسم:** [اسمك]\n"
        "**⪼ اليوزر:** @username\n"
        "**⪼ الايدي:** `123456789`\n"
        "**⪼ الحالة:** نشط",
        buttons=buttons
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"broadcastz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]]
    await event.edit(
        "**📢 أوامر الإذاعة:**\n\n"
        "**⦁ .اذاعة خاص** - للإذاعة في الخاص\n"
        "**⦁ .اذاعة كروب** - للإذاعة في المجموعات\n"
        "**⦁ .اذاعة للكل** - للإذاعة للجميع",
        buttons=buttons
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"kalaysh")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]]
    await event.edit(
        "**🪁 أوامر الكلايش والتخصيص:**\n\n"
        "**⦁ .كلايش** - لعرض الكلايش\n"
        "**⦁ .كليشة + النص** - لإضافة كليشة\n"
        "**⦁ .حذف كليشة + الرقم** - لحذف كليشة",
        buttons=buttons
    )

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"funzed")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع للقائمة الرئيسية ↩️", data="ROE")]]
    await event.edit(
        "**🎃 أوامر التسلية والتحشيش:**\n\n"
        "**⦁ .اكس او** - لعبة XO\n"
        "**⦁ .كت** - كت تويت\n"
        "**⦁ .صراحه** - لعبة الصراحة",
        buttons=buttons
    )

# يمكنك إضافة المزيد من الأزرار بنفس الطريقة
# كل زر سيعرض محتواه مع زر رجوع فقط
"""
