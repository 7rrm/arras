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
                [Button.inline("م1 - أوامر الإدارة 👮", data="m1_main")],
                [
                    Button.inline("م2 - أوامر المجموعة 👥", data="m2_main"),
                    Button.inline("م3 - الترحيب والردود 🎭", data="m3_main"),
                ],
                [
                    Button.inline("م4 - حماية الخاص 🛡️", data="m4_main"),
                    Button.inline("م5 - المنشن والانتحال 🎯", data="m5_main"),
                ],
                [
                    Button.inline("م6 - التحميل والترجمة 📥", data="m6_main"),
                    Button.inline("م7 - المنع والقفل 🔒", data="m7_main"),
                ],
                [
                    Button.inline("م8 - التنظيف والتكرار 🧹", data="m8_main"),
                    Button.inline("م9 - التخصيص والفارات ⚙️", data="m9_main"),
                ],
                [
                    Button.inline("م10 - الوقتي والتشغيل ⏰", data="m10_main"),
                    Button.inline("م11 - الكشف والروابط 🔍", data="m11_main"),
                ],
                [
                    Button.inline("م12 - المساعدة والإذاعة 🆘", data="m12_main"),
                    Button.inline("م13 - الإرسال والأذكار 📿", data="m13_main"),
                ],
                [
                    Button.inline("م14 - الملصقات وكوكل 🎨", data="m14_main"),
                    Button.inline("م15 - التسلية والميمز 😂", data="m15_main"),
                ],
                [
                    Button.inline("م16 - الصيغ والجهات 🔄", data="m16_main"),
                    Button.inline("م17 - التمبلر والزغرفة ✨", data="m17_main"),
                ],
                [
                    Button.inline("م18 - الحساب والترفيه 🎮", data="m18_main"),
                    Button.inline("م19 - الميوزك والتشغيل 🎵", data="m19_main"),
                ],
                [
                    Button.inline("م20 - تجميع النقاط وبوت وعد 💰", data="m20_main"),
                    Button.inline("م21 - الذاتية للبصمات والصور 🎭", data="m21_main"),
                ],
            ]
            result = builder.article(
                title="قائمة المساعدة - آراس",
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

# =========================================================== #
#                   القائمة الرئيسية (ZEDHELP)               #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"ZEDHELP")))
@check_owner
async def _(event):
    butze = [
        [Button.inline("م1 - أوامر الإدارة 👮", data="m1_main")],
        [
            Button.inline("م2 - أوامر المجموعة 👥", data="m2_main"),
            Button.inline("م3 - الترحيب والردود 🎭", data="m3_main"),
        ],
        [
            Button.inline("م4 - حماية الخاص 🛡️", data="m4_main"),
            Button.inline("م5 - المنشن والانتحال 🎯", data="m5_main"),
        ],
        [
            Button.inline("م6 - التحميل والترجمة 📥", data="m6_main"),
            Button.inline("م7 - المنع والقفل 🔒", data="m7_main"),
        ],
        [
            Button.inline("م8 - التنظيف والتكرار 🧹", data="m8_main"),
            Button.inline("م9 - التخصيص والفارات ⚙️", data="m9_main"),
        ],
        [
            Button.inline("م10 - الوقتي والتشغيل ⏰", data="m10_main"),
            Button.inline("م11 - الكشف والروابط 🔍", data="m11_main"),
        ],
        [
            Button.inline("م12 - المساعدة والإذاعة 🆘", data="m12_main"),
            Button.inline("م13 - الإرسال والأذكار 📿", data="m13_main"),
        ],
        [
            Button.inline("م14 - الملصقات وكوكل 🎨", data="m14_main"),
            Button.inline("م15 - التسلية والميمز 😂", data="m15_main"),
        ],
        [
            Button.inline("م16 - الصيغ والجهات 🔄", data="m16_main"),
            Button.inline("م17 - التمبلر والزغرفة ✨", data="m17_main"),
        ],
        [
            Button.inline("م18 - الحساب والترفيه 🎮", data="m18_main"),
            Button.inline("م19 - الميوزك والتشغيل 🎵", data="m19_main"),
        ],
        [
            Button.inline("م20 - تجميع النقاط وبوت وعد 💰", data="m20_main"),
            Button.inline("م21 - الذاتية للبصمات والصور 🎭", data="m21_main"),
        ],
    ]
    await event.edit(HELP, buttons=butze, link_preview=False)

# =========================================================== #
#                         م1 - أوامر الإدارة                 #
# =========================================================== #

# صفحة م1 الرئيسية (الازرار الفرعية)
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m1_main")))
@check_owner
async def _(event):
    await event.edit(
        "**👮 أوامر الإدارة - م1**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الحظر 🚫", data="m1_ban"),
                Button.inline("اوامر الكتم 🤫", data="m1_mute"),
            ],
            [
                Button.inline("اوامر التثبيت 📌", data="m1_pin"),
                Button.inline("اوامر الاشراف 👥", data="m1_super"),
            ],
            [Button.inline("اوامر التحذيرات ⚠️", data="m1_warn")],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الحظر
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m1_ban")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحظر 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.حظر` ⦘**\n"
        "❐ لحظر عضو من المجموعة\n"
        "❐ طريقة الاستخدام: `.حظࢪ` بالرد على العضو او كتابة يوزره\n\n"
        "**☑️ ⦗ `.الغاء حظر` ⦘**\n"
        "❐ لألغاء حظر عضو محظور\n"
        "❐ طريقة الاستخدام: `.الغاء حظࢪ` بالرد على العضو او كتابة يوزره\n\n"
        "**☑️ ⦗ `.حظر مؤقت` ⦘**\n"
        "❐ لحظر عضو مؤقتاً لمدة محددة\n"
        "❐ طريقة الاستخدام: `.حظࢪ مؤقت 1h السبب`\n\n"
        "**☑️ ⦗ `.مسح المحظورين` ⦘**\n"
        "❐ لحذف جميع المحظورين\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم1 ↩️", data="m1_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الكتم
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m1_mute")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكتم 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.كتم` ⦘**\n"
        "❐ كتم عضو في المجموعة\n"
        "❐ طريقة الاستخدام: `.كتم` بالرد على العضو او كتابة يوزره\n\n"
        "**☑️ ⦗ `.الغاء كتم` ⦘**\n"
        "❐ إلغاء كتم عضو مكتوم\n"
        "❐ طريقة الاستخدام: `.الغاء كتم` بالرد على العضو او كتابة يوزره\n\n"
        "**☑️ ⦗ `.كتم_مؤقت` ⦘**\n"
        "❐ كتم عضو مؤقتاً لمدة محددة\n"
        "❐ طريقة الاستخدام: `.كتم_مؤقت 1h السبب`\n\n"
        "**☑️ ⦗ `.مسح المكتومين` ⦘**\n"
        "❐ حذف جميع المكتومين\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم1 ↩️", data="m1_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر التثبيت
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m1_pin")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التثبيت 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تثبيت` ⦘**\n"
        "❐ تثبيت رسالة في المجموعة\n"
        "❐ طريقة الاستخدام: `.تثبيت` بالرد على الرسالة\n\n"
        "**☑️ ⦗ `.الغاء تثبيت` ⦘**\n"
        "❐ إلغاء تثبيت رسالة مثبتة\n"
        "❐ طريقة الاستخدام: `.الغاء تثبيت`\n\n"
        "**☑️ ⦗ `.تثبيت بالتنبيه` ⦘**\n"
        "❐ تثبيت رسالة مع تنبيه للأعضاء\n"
        "❐ طريقة الاستخدام: `.تثبيت بالتنبيه` بالرد على الرسالة\n\n"
        "**☑️ ⦗ `.المثبتات` ⦘**\n"
        "❐ عرض الرسائل المثبتة\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم1 ↩️", data="m1_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الاشراف
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m1_super")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الاشراف 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.رفع مشرف` ⦘**\n"
        "❐ رفع عضو إلى مشرف في المجموعة\n"
        "❐ طريقة الاستخدام: `.رفع مشرف` بالرد على العضو\n\n"
        "**☑️ ⦗ `.تنزيل مشرف` ⦘**\n"
        "❐ تنزيل مشرف من إدارة المجموعة\n"
        "❐ طريقة الاستخدام: `.تنزيل مشرف` بالرد على المشرف\n\n"
        "**☑️ ⦗ `.المشرفين` ⦘**\n"
        "❐ عرض قائمة المشرفين\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.صلاحيات` ⦘**\n"
        "❐ عرض صلاحيات المشرفين\n"
        "❐ طريقة الاستخدام: `.صلاحيات`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم1 ↩️", data="m1_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر التحذيرات
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m1_warn")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحذيرات 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تحذير` ⦘**\n"
        "❐ تحذير عضو مع سبب\n"
        "❐ طريقة الاستخدام: `.تحذير السبب` بالرد على العضو\n\n"
        "**☑️ ⦗ `.التحذيرات` ⦘**\n"
        "❐ عرض تحذيرات العضو\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.مسح التحذيرات` ⦘**\n"
        "❐ حذف تحذيرات العضو\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم1 ↩️", data="m1_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                         م2 - أوامر المجموعة                 #
# =========================================================== #

# صفحة م2 الرئيسية
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m2_main")))
@check_owner
async def _(event):
    await event.edit(
        "**👥 أوامر المجموعة - م2**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر التفاعل 📱", data="m2_interact"),
                Button.inline("اوامر الاعدادات ⚙️", data="m2_settings"),
            ],
            [
                Button.inline("اوامر الصوت 🎤", data="m2_voice"),
                Button.inline("اوامر الترتيب 📊", data="m2_order"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر التفاعل
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m2_interact")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التفاعل 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تفاعل` ⦘**\n"
        "❐ قياس تفاعل المجموعة\n"
        "❐ طريقة الاستخدام: `.تفاعل`\n\n"
        "**☑️ ⦗ `.نشاط` ⦘**\n"
        "❐ عرض النشاط اليومي\n"
        "❐ طريقة الاستخدام: `.نشاط`\n\n"
        "**☑️ ⦗ `.تاج` ⦘**\n"
        "❐ منح تاج لأكثر الأعضاء تفاعلاً\n"
        "❐ طريقة الاستخدام: `.تاج`\n\n"
        "**☑️ ⦗ `.اكثر تفاعل` ⦘**\n"
        "❐ عرض أكثر الأعضاء تفاعلاً\n"
        "❐ طريقة الاستخدام: `.اكثر تفاعل`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم2 ↩️", data="m2_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                     م3 - الترحيب والردود                    #
# =========================================================== #

# صفحة م3 الرئيسية
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m3_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🎭 الترحيب والردود - م3**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الترحيب 🤗", data="m3_welcome"),
                Button.inline("اوامر الردود 🔄", data="m3_reply"),
            ],
            [
                Button.inline("ترحيب البوت 🤖", data="m3_botwelcome"),
                Button.inline("كلايش الترحيب 📝", data="m3_welcometext"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الترحيب
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m3_welcome")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الترحيب 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.ترحيب` ⦘**\n"
        "❐ وضع رسالة ترحيب للمجموعة\n"
        "❐ طريقة الاستخدام: `.ترحيب النص`\n\n"
        "**☑️ ⦗ `.الترحيب` ⦘**\n"
        "❐ عرض رسالة الترحيب الحالية\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.حذف الترحيب` ⦘**\n"
        "❐ حذف رسالة الترحيب\n"
        "❐ طريقة الاستخدام: `.حذف الترحيب`\n\n"
        "**☑️ ⦗ `.تفعيل الترحيب` ⦘**\n"
        "❐ تفعيل الترحيب التلقائي\n"
        "❐ طريقة الاستخدام: `.تفعيل الترحيب`\n\n"
        "**☑️ ⦗ `.تعطيل الترحيب` ⦘**\n"
        "❐ تعطيل الترحيب التلقائي\n"
        "❐ طريقة الاستخدام: `.تعطيل الترحيب`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم3 ↩️", data="m3_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الردود
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m3_reply")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الردود 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.رد اضف` ⦘**\n"
        "❐ إضافة رد تلقائي\n"
        "❐ طريقة الاستخدام: `.رد اضف الكلمة الرد`\n\n"
        "**☑️ ⦗ `.رد حذف` ⦘**\n"
        "❐ حذف رد تلقائي\n"
        "❐ طريقة الاستخدام: `.رد حذف الكلمة`\n\n"
        "**☑️ ⦗ `.الردود` ⦘**\n"
        "❐ عرض قائمة الردود\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.مسح الردود` ⦘**\n"
        "❐ حذف جميع الردود\n"
        "❐ طريقة الاستخدام: `.مسح الردود`\n\n"
        "**☑️ ⦗ `.رد` ⦘**\n"
        "❐ تشغيل رد تلقائي\n"
        "❐ طريقة الاستخدام: `.رد الكلمة`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم3 ↩️", data="m3_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                    باقي الصفحات الرئيسية                    #
# =========================================================== #

# م4 - حماية الخاص
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m4_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🛡️ حماية الخاص - م4**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الحماية 🔐", data="m4_protection"),
                Button.inline("اوامر السماح ✅", data="m4_allow"),
            ],
            [
                Button.inline("اوامر القائمة 📋", data="m4_list"),
                Button.inline("اوامر التلكراف 📧", data="m4_telegram"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م5 - المنشن والانتحال
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m5_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🎯 المنشن والانتحال - م5**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر المنشن @", data="m5_mention"),
                Button.inline("اوامر الانتحال 🎭", data="m5_impersonate"),
            ],
            [
                Button.inline("اوامر التاك #️⃣", data="m5_tag"),
                Button.inline("اوامر الاعادة 🔄", data="m5_restore"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م6 - التحميل والترجمة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m6_main")))
@check_owner
async def _(event):
    await event.edit(
        "**📥 التحميل والترجمة - م6**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر التحميل 📥", data="m6_download"),
                Button.inline("اوامر الترجمة 🌐", data="m6_translate"),
            ],
            [
                Button.inline("اوامر اليوتيوب 🎵", data="m6_youtube"),
                Button.inline("اوامر انستجرام 📷", data="m6_instagram"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م7 - المنع والقفل
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m7_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🔒 المنع والقفل - م7**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر القفل 🔒", data="m7_lock"),
                Button.inline("اوامر الفتح 🔓", data="m7_unlock"),
            ],
            [
                Button.inline("اوامر المنع 🚫", data="m7_block"),
                Button.inline("قائمة المنع 📋", data="m7_blocklist"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م8 - التنظيف والتكرار
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m8_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🧹 التنظيف والتكرار - م8**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر التنظيف 🧹", data="m8_clean"),
                Button.inline("اوامر المسح 🗑️", data="m8_delete"),
            ],
            [
                Button.inline("اوامر التكرار 🔁", data="m8_repeat"),
                Button.inline("اوامر المؤقت ⏳", data="m8_temporary"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر التنظيف
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m8_clean")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التنظيف 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تنظيف` ⦘**\n"
        "❐ حذف عدد معين من الرسائل\n"
        "❐ طريقة الاستخدام: `.تنظيف 10`\n\n"
        "**☑️ ⦗ `.تنظيف` ⦘**\n"
        "❐ تنظيف حسب النوع مع (-)\n"
        "❐ طريقة الاستخدام: `.تنظيف -ح`\n\n"
        "**الاضافات:**\n"
        "- (-ب): حذف الرسائل الصوتية\n"
        "- (-م): حذف الملفات\n"
        "- (-ح): حذف المتحركة\n"
        "- (-ص): حذف الصور\n"
        "- (-غ): حذف الأغاني\n"
        "- (-ق): حذف الملصقات\n"
        "- (-ر): حذف الروابط\n"
        "- (-ف): حذف الفيديوهات\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم8 ↩️", data="m8_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر المسح
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m8_delete")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المسح 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.مسح` ⦘**\n"
        "❐ حذف رسالة محددة\n"
        "❐ طريقة الاستخدام: بالرد على الرسالة\n\n"
        "**☑️ ⦗ `.مسح رسائلي` ⦘**\n"
        "❐ حذف جميع رسائلك\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لم8 ↩️", data="m8_main")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                استمرار باقي الصفحات الرئيسية                #
# =========================================================== #

# م9 - التخصيص والفارات
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m9_main")))
@check_owner
async def _(event):
    await event.edit(
        "**⚙️ التخصيص والفارات - م9**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الفارات 🎈", data="m9_vars"),
                Button.inline("اوامر التخصيص 🪁", data="m9_custom"),
            ],
            [
                Button.inline("اوامر الجلب 📥", data="m9_get"),
                Button.inline("اوامر الوضع 🛠️", data="m9_set"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م10 - الوقتي والتشغيل
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m10_main")))
@check_owner
async def _(event):
    await event.edit(
        "**⏰ الوقتي والتشغيل - م10**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الوقتي 🔄", data="m10_timely"),
                Button.inline("اوامر التشغيل ⚡", data="m10_run"),
            ],
            [
                Button.inline("اوامر التحديث 🔄", data="m10_update"),
                Button.inline("اوامر الاطفاء 🔌", data="m10_shutdown"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م11 - الكشف والروابط
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m11_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🔍 الكشف والروابط - م11**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الكشف 🔍", data="m11_detect"),
                Button.inline("اوامر الروابط 🔗", data="m11_links"),
            ],
            [
                Button.inline("اوامر الكوكل 🔎", data="m11_google"),
                Button.inline("اوامر الاستخراج 📄", data="m11_extract"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م12 - المساعدة والإذاعة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m12_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🆘 المساعدة والإذاعة - م12**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر المساعدة 🆘", data="m12_help"),
                Button.inline("اوامر الاذاعه 📢", data="m12_broadcast"),
            ],
            [
                Button.inline("اوامر التوجيه 📨", data="m12_forward"),
                Button.inline("اوامر الاستعلام ❓", data="m12_inquiry"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م13 - الإرسال والأذكار
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m13_main")))
@check_owner
async def _(event):
    await event.edit(
        "**📿 الإرسال والأذكار - م13**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الاذكار 📿", data="m13_azkar"),
                Button.inline("اوامر الإرسال 📨", data="m13_send"),
            ],
            [
                Button.inline("اوامر الصلاة 🕌", data="m13_prayer"),
                Button.inline("اوامر الدعاء 🙏", data="m13_dua"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م14 - الملصقات وكوكل
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m14_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🎨 الملصقات وكوكل - م14**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الملصقات 🎭", data="m14_stickers"),
                Button.inline("اوامر الكوكل 🔎", data="m14_google"),
            ],
            [
                Button.inline("اوامر الصور 🖼️", data="m14_images"),
                Button.inline("اوامر البحث 🔍", data="m14_search"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م15 - التسلية والميمز
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m15_main")))
@check_owner
async def _(event):
    await event.edit(
        "**😂 التسلية والميمز - م15**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر التسلية 🎮", data="m15_fun"),
                Button.inline("اوامر التحشيش 🤣", data="m15_memes"),
            ],
            [
                Button.inline("اوامر النسب 📊", data="m15_rates"),
                Button.inline("اوامر الرفع ⬆️", data="m15_raise"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م16 - الصيغ والجهات
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m16_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🔄 الصيغ والجهات - م16**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر التحويل 🔄", data="m16_convert"),
                Button.inline("اوامر الجهات 👥", data="m16_contacts"),
            ],
            [
                Button.inline("اوامر الصيغ 📁", data="m16_formats"),
                Button.inline("اوامر النقل 📤", data="m16_transfer"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م17 - التمبلر والزغرفة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m17_main")))
@check_owner
async def _(event):
    await event.edit(
        "**✨ التمبلر والزغرفة - م17**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الزغرفة ✨", data="m17_decoration"),
                Button.inline("اوامر التمبلر 📝", data="m17_tumbler"),
            ],
            [
                Button.inline("اوامر الخطوط 🖋️", data="m17_fonts"),
                Button.inline("اوامر التنسيق 🎨", data="m17_formatting"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م18 - الحساب والترفيه
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m18_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🎮 الحساب والترفيه - م18**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الحساب 👤", data="m18_account"),
                Button.inline("اوامر الترفيه 🎮", data="m18_entertainment"),
            ],
            [
                Button.inline("اوامر الالعاب 🎯", data="m18_games"),
                Button.inline("اوامر المغادرة 🚪", data="m18_leave"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م19 - الميوزك والتشغيل
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m19_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🎵 الميوزك والتشغيل - م19**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الميوزك 🎵", data="m19_music"),
                Button.inline("اوامر التشغيل ▶️", data="m19_play"),
            ],
            [
                Button.inline("اوامر التحميل 🎧", data="m19_download"),
                Button.inline("اوامر القوائم 📋", data="m19_playlists"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م20 - تجميع النقاط وبوت وعد
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m20_main")))
@check_owner
async def _(event):
    await event.edit(
        "**💰 تجميع النقاط وبوت وعد - م20**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر التجميع 💰", data="m20_collect"),
                Button.inline("اوامر وعد 🏦", data="m20_w3d"),
            ],
            [
                Button.inline("اوامر الراتب 💸", data="m20_salary"),
                Button.inline("اوامر السرقة 🎯", data="m20_steal"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# م21 - الذاتية للبصمات والصور
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"m21_main")))
@check_owner
async def _(event):
    await event.edit(
        "**🎭 الذاتية للبصمات والصور - م21**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("الصوره الذاتيه 📸", data="m21_selfphoto"),
                Button.inline("البصمه الذاتيه 🎤", data="m21_selfvoice"),
            ],
            [
                Button.inline("اوامر الحفظ 💾", data="m21_save"),
                Button.inline("اوامر الجلب 📥", data="m21_get"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )
