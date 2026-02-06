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
                [Button.inline("اوامر الادارة 👮", data="admin_commands")],
                [
                    Button.inline("اوامر التنظيف 🧹", data="clean_cmd"),
                    Button.inline("اوامر المسح 🗑️", data="delete_cmd"),
                ],
                [Button.inline("اوامر الوقت والتاريخ 📅", data="time_date_cmd")],
                [
                    Button.inline("اوامر الوقتي 🔄", data="timely_cmd"),
                    Button.inline("اوامر الصلاة 🕌", data="prayer_cmd"),
                ],
                [Button.inline("اوامر المساعدة 🆘", data="help_commands")],
                [
                    Button.inline("اوامر الروابط 🔗", data="link_commands"),
                    Button.inline("اوامر الكشف 🔍", data="detect_commands"),
                ],
                [Button.inline("اوامر التسلية والميمز 😂", data="fun_meme_commands")],
                [
                    Button.inline("اوامر الاذاعة 📢", data="broadcast_commands"),
                    Button.inline("اوامر التحويل 🔄", data="convert_commands"),
                ],
                [Button.inline("اوامر الجهات 👥", data="contacts_commands")],
                [
                    Button.inline("اوامر الحساب 👤", data="account_commands"),
                    Button.inline("اوامر الفارات ⚙️", data="var_commands"),
                ],
                [Button.inline("اوامر التجميع 💰", data="collect_commands")],
                [
                    Button.inline("اوامر وعد 🏦", data="w3d_commands"),
                    Button.inline("اوامر الاذكار 📿", data="azkar_commands"),
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
        [Button.inline("اوامر الادارة 👮", data="admin_commands")],
        [
            Button.inline("اوامر التنظيف 🧹", data="clean_cmd"),
            Button.inline("اوامر المسح 🗑️", data="delete_cmd"),
        ],
        [Button.inline("اوامر الوقت والتاريخ 📅", data="time_date_cmd")],
        [
            Button.inline("اوامر الوقتي 🔄", data="timely_cmd"),
            Button.inline("اوامر الصلاة 🕌", data="prayer_cmd"),
        ],
        [Button.inline("اوامر المساعدة 🆘", data="help_commands")],
        [
            Button.inline("اوامر الروابط 🔗", data="link_commands"),
            Button.inline("اوامر الكشف 🔍", data="detect_commands"),
        ],
        [Button.inline("اوامر التسلية والميمز 😂", data="fun_meme_commands")],
        [
            Button.inline("اوامر الاذاعة 📢", data="broadcast_commands"),
            Button.inline("اوامر التحويل 🔄", data="convert_commands"),
        ],
        [Button.inline("اوامر الجهات 👥", data="contacts_commands")],
        [
            Button.inline("اوامر الحساب 👤", data="account_commands"),
            Button.inline("اوامر الفارات ⚙️", data="var_commands"),
        ],
        [Button.inline("اوامر التجميع 💰", data="collect_commands")],
        [
            Button.inline("اوامر وعد 🏦", data="w3d_commands"),
            Button.inline("اوامر الاذكار 📿", data="azkar_commands"),
        ],
    ]
    await event.edit(HELP, buttons=butze, link_preview=False)

# =========================================================== #
#                      أوامر الإدارة الرئيسية                #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"admin_commands")))
@check_owner
async def _(event):
    await event.edit(
        "**👮 أوامر الإدارة**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [Button.inline("اوامر الحظر 🚫", data="ban_cmd")],
            [
                Button.inline("اوامر الكتم 🤫", data="mute_cmd"),
                Button.inline("اوامر التثبيت 📌", data="pin_cmd"),
            ],
            [Button.inline("اوامر الاشراف 👥", data="super_cmd")],
            [
                Button.inline("اوامر التحذيرات ⚠️", data="warn_cmd"),
                Button.inline("اوامر الملكية 👑", data="ownership_cmd"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر الحظر                     #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"ban_cmd")))
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
            [Button.inline("رجوع لأوامر الإدارة ↩️", data="admin_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر الكتم                     #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"mute_cmd")))
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
            [Button.inline("رجوع لأوامر الإدارة ↩️", data="admin_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر التثبيت                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"pin_cmd")))
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
            [Button.inline("رجوع لأوامر الإدارة ↩️", data="admin_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر الاشراف                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"super_cmd")))
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
            [Button.inline("رجوع لأوامر الإدارة ↩️", data="admin_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر التحذيرات                 #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"warn_cmd")))
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
            [Button.inline("رجوع لأوامر الإدارة ↩️", data="admin_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر الملكية                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"ownership_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الملكية 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.ملكية` ⦘**\n"
        "❐ نقل ملكية القناة لشخص\n"
        "❐ طريقة الاستخدام: `.ملكية معرف الشخص`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الإدارة ↩️", data="admin_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر التنظيف                  #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"clean_cmd")))
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
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر المسح                    #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"delete_cmd")))
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
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#           صفحة تفصيلية لأوامر الوقت والتاريخ               #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"time_date_cmd")))
@check_owner
async def _(event):
    await event.edit(
        "**📅 أوامر الوقت والتاريخ**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [Button.inline("اوامر الوقت والتاريخ ⏰", data="time_date_detailed")],
            [
                Button.inline("اوامر الرسائل الموقته ⏳", data="temp_msg_cmd"),
                Button.inline("اوامر اللستة 📋", data="list_cmd"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الوقت والتاريخ
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"time_date_detailed")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الوقت والتاريخ 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تاريخ` ⦘**\n"
        "❐ عرض سجل أسماء الحساب\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.الوقت` ⦘**\n"
        "❐ عرض الوقت على شكل ملصق\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.وقت` ⦘**\n"
        "❐ عرض الوقت على شكل كتابة\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.مؤقت` ⦘**\n"
        "❐ إرسال رسالة مؤقتة\n"
        "❐ طريقة الاستخدام: `.مؤقت 5 النص`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للوقت والتاريخ ↩️", data="time_date_cmd")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الرسائل الموقتة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"temp_msg_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الرسائل الموقتة 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.ضبط_المؤقت` ⦘**\n"
        "❐ ضبط وقت حذف الرسائل تلقائياً\n"
        "❐ طريقة الاستخدام: `.ضبط_المؤقت 10`\n\n"
        "**☑️ ⦗ `.تعطيل_المؤقت` ⦘**\n"
        "❐ إيقاف حذف الرسائل التلقائي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.مؤقت` ⦘**\n"
        "❐ إرسال رسالة مؤقتة\n"
        "❐ طريقة الاستخدام: `.مؤقت 5 النص`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للوقت والتاريخ ↩️", data="time_date_cmd")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر اللستة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"list_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر اللستة 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.لستة` ⦘**\n"
        "❐ صنع لستة شفافة للمنشور\n"
        "❐ طريقة الاستخدام: مع المنشور\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للوقت والتاريخ ↩️", data="time_date_cmd")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر الوقتي                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"timely_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الوقتي 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تفعيل_وقتي` ⦘**\n"
        "❐ تفعيل إرسال الوقت التلقائي\n"
        "❐ طريقة الاستخدام: في المجموعة\n\n"
        "**☑️ ⦗ `.تعطيل_وقتي` ⦘**\n"
        "❐ تعطيل إرسال الوقت التلقائي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#               صفحة تفصيلية لأوامر الصلاة                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"prayer_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الصلاة 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.صلاة` ⦘**\n"
        "❐ الحصول على أوقات الصلاة\n"
        "❐ طريقة الاستخدام: `.صلاة المحافظة`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر المساعدة                #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"help_commands")))
@check_owner
async def _(event):
    await event.edit(
        "**🆘 أوامر المساعدة**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [Button.inline("اوامر المساعدة 🆘", data="help_detailed")],
            [
                Button.inline("اوامر كوكل 🔎", data="google_cmd"),
                Button.inline("اوامر السرعة ⚡", data="speed_cmd"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر المساعدة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"help_detailed")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المساعدة 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.موقع` ⦘**\n"
        "❐ الحصول على مكان في الخريطة\n"
        "❐ طريقة الاستخدام: `.موقع المكان`\n\n"
        "**☑️ ⦗ `.جد بكج` ⦘**\n"
        "❐ معرفة وجود البكج أو المكتبة\n"
        "❐ طريقة الاستخدام: `.جد بكج الاسم`\n\n"
        "**☑️ ⦗ `.صورة` ⦘**\n"
        "❐ الحصول على صورة الحساب\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.صوره كلها` ⦘**\n"
        "❐ الحصول على جميع صور الحساب\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.سرعة النت` ⦘**\n"
        "❐ قياس سرعة الانترنت\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.بنك` ⦘**\n"
        "❐ قياس سرعة البنك\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.حساب` ⦘**\n"
        "❐ لأرسال رابط لحساب الشخص\n"
        "❐ طريقة الاستخدام: `.حساب + ايدي الشخص`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للمساعدة ↩️", data="help_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر كوكل
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"google_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر كوكل 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.صور` ⦘**\n"
        "❐ الحصول على صور من جوجل\n"
        "❐ طريقة الاستخدام: `.صور 10 النص`\n\n"
        "**☑️ ⦗ `.استخرج` ⦘**\n"
        "❐ استخراج النصوص من الصور\n"
        "❐ طريقة الاستخدام: `.استخرج عربي بالرد`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للمساعدة ↩️", data="help_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر السرعة
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"speed_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السرعة 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.سرعة النت` ⦘**\n"
        "❐ قياس سرعة الانترنت\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.بنك` ⦘**\n"
        "❐ قياس سرعة البنك\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للمساعدة ↩️", data="help_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الروابط                 #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"link_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الروابط 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.دنس` ⦘**\n"
        "❐ كشف نظام دومين الموقع\n"
        "❐ طريقة الاستخدام: `.دنس الرابط`\n\n"
        "**☑️ ⦗ `.مصغر` ⦘**\n"
        "❐ تصغير الرابط\n"
        "❐ طريقة الاستخدام: بالرد على الرابط\n\n"
        "**☑️ ⦗ `.رابط_مخفي` ⦘**\n"
        "❐ إخفاء الرابط في مسافة معينة\n"
        "❐ طريقة الاستخدام: بالرد على الرابط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الكشف                   #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"detect_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكشف 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.الايدي` ⦘**\n"
        "❐ عرض معلومات الكروب\n"
        "❐ طريقة الاستخدام: أرسل الامر في الكروب\n\n"
        "**☑️ ⦗ `.ايدي` ⦘**\n"
        "❐ عرض معلومات العضو بشكل مبسط\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.ا` ⦘ او ⦗ `.i` ⦘**\n"
        "❐ عرض معلومات العضو بشكل مبسط **نسخه الايموجي المميز** ال i تضهر الكليشة بالغة الانكليزيه\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.كشف` ⦘**\n"
        "❐ عرض معلومات العضو\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "**☑️ ⦗ `.لايك` ⦘**\n"
        "❐ عرض معلوماتك\n"
        "❐ طريقة الاستخدام: ارسل الامر فقط\n\n"
        "**☑️ ⦗ `.المعجبين` ⦘**\n"
        "❐ لـ عرض معجبينك\n"
        "❐ طريقة الاستخدام: ارسل الامر فقط\n\n"
        "**☑️ ⦗ `.مسح المعجبين` ⦘**\n"
        "❐ لـ مسح معجبينك\n"
        "❐ طريقة الاستخدام: بالرد على الشخص\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#              صفحة تفصيلية لأوامر التسلية والميمز           #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"fun_meme_commands")))
@check_owner
async def _(event):
    await event.edit(
        "**😂 أوامر التسلية والميمز**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [Button.inline("اوامر التسلية 🎮", data="fun_cmd")],
            [
                Button.inline("اوامر التحشيش 🤣", data="meme_cmd"),
                Button.inline("اوامر البلي والكت 🎯", data="play_cmd"),
            ],
            [
                Button.inline("اوامر النسب 📊", data="rate_cmd"),
                Button.inline("اوامر الرفع ⬆️", data="raise_cmd"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر التسلية
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"fun_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التسلية 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تسلية 1` ⦘**\n"
        "**☑️ ⦗ `.تسلية 2` ⦘**\n"
        "**☑️ ⦗ `.تسلية 3` ⦘**\n"
        "**☑️ ⦗ `.تسلية 4` ⦘**\n"
        "**☑️ ⦗ `.تسلية 5` ⦘**\n"
        "**☑️ ⦗ `.تسلية 6` ⦘**\n"
        "**☑️ ⦗ `.تسلية 7` ⦘**\n"
        "**☑️ ⦗ `.تسلية 8` ⦘**\n"
        "**☑️ ⦗ `.رفع ادمن` ⦘**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للتسلية والميمز ↩️", data="fun_meme_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر التحشيش
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"meme_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحشيش 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**جميع الأوامر تستخدم بالرد على الشخص**\n\n"
        "**⦗ `.رفع تاج` ⦘** - **⦗ `.رفع بكلبي` ⦘** - **⦗ `.رفع مطي` ⦘**\n"
        "**⦗ `.رفع جلب` ⦘** - **⦗ `.رفع قرد` ⦘** - **⦗ `.رفع مرتي` ⦘**\n"
        "**⦗ `.رفع زوجي` ⦘** - **⦗ `.نسبة الانوثة` ⦘** - **⦗ `.نسبة الحب` ⦘**\n"
        "**⦗ `.نسبة الغباء` ⦘** - **⦗ `.رفع زاحف` ⦘** - **⦗ `.رفع كحبة` ⦘**\n"
        "**⦗ `.رفع فرخ` ⦘** - **⦗ `.رزله` ⦘** - **⦗ `.رفع صاك` ⦘**\n"
        "**⦗ `.رفع حاته` ⦘** - **⦗ `.رفع بقره` ⦘** - **⦗ `.رفع ايجة` ⦘**\n"
        "**⦗ `.رفع زبال` ⦘** - **⦗ `.رفع كواد` ⦘** - **⦗ `.رفع ديوث` ⦘**\n"
        "**⦗ `.رفع مجنب` ⦘** - **⦗ `.رفع مميز` ⦘** - **⦗ `.رفع ادمن` ⦘**\n"
        "**⦗ `.رفع منشئ` ⦘** - **⦗ `.رفع مالك` ⦘** - **⦗ `.رفع وصخ` ⦘**\n"
        "**⦗ `.نسبة الكذب` ⦘** - **⦗ `.نسبة الدياثه` ⦘**\n"
        "**⦗ `.نسبة الشذوذ` ⦘** - **⦗ `.نسبة الجمال` ⦘**\n"
        "**⦗ `.نسبة الخيانه` ⦘**\n\n"
        "**☑️ ⦗ `.رفع` + كلمة  ⦘**\n"
        "❐ لـ رفع الشخص بالكلمة التي وضعتها\n"
        "❐ طريقة الاستخدام: ارسل الامر مع وضع كلمة\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للتسلية والميمز ↩️", data="fun_meme_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر البلي والكت
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"play_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البلي والكت 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.بلي` ⦘**\n"
        "**☑️ ⦗ `.كت` ⦘**\n"
        "**☑️ ⦗ `.خيروك` ⦘**\n"
        "**☑️ ⦗ `.غنيلي` ⦘**\n"
        "**☑️ ⦗ `.شعر` ⦘**\n"
        "**☑️ ⦗ `.فلم` ⦘**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للتسلية والميمز ↩️", data="fun_meme_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر النسب
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"rate_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر النسب 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**جميع الأوامر تستخدم بالرد على الشخص**\n\n"
        "**☑️ ⦗ `.نسبة الانوثة` ⦘**\n"
        "**☑️ ⦗ `.نسبة الحب` ⦘**\n"
        "**☑️ ⦗ `.نسبة الغباء` ⦘**\n"
        "**☑️ ⦗ `.نسبة الكذب` ⦘**\n"
        "**☑️ ⦗ `.نسبة الدياثه` ⦘**\n"
        "**☑️ ⦗ `.نسبة الشذوذ` ⦘**\n"
        "**☑️ ⦗ `.نسبة الجمال` ⦘**\n"
        "**☑️ ⦗ `.نسبة الخيانه` ⦘**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للتسلية والميمز ↩️", data="fun_meme_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الرفع
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"raise_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الرفع 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**جميع الأوامر تستخدم بالرد على الشخص**\n\n"
        "**☑️ ⦗ `.رفع تاج` ⦘**\n"
        "**☑️ ⦗ `.رفع بكلبي` ⦘**\n"
        "**☑️ ⦗ `.رفع مطي` ⦘**\n"
        "**☑️ ⦗ `.رفع جلب` ⦘**\n"
        "**☑️ ⦗ `.رفع قرد` ⦘**\n"
        "**☑️ ⦗ `.رفع مرتي` ⦘**\n"
        "**☑️ ⦗ `.رفع زوجي` ⦘**\n"
        "**☑️ ⦗ `.رفع زاحف` ⦘**\n"
        "**☑️ ⦗ `.رفع كحبة` ⦘**\n"
        "**☑️ ⦗ `.رفع فرخ` ⦘**\n"
        "**☑️ ⦗ `.رفع صاك` ⦘**\n"
        "**☑️ ⦗ `.رفع حاته` ⦘**\n"
        "**☑️ ⦗ `.رفع بقره` ⦘**\n"
        "**☑️ ⦗ `.رفع ايجة` ⦘**\n"
        "**☑️ ⦗ `.رفع زبال` ⦘**\n"
        "**☑️ ⦗ `.رفع كواد` ⦘**\n"
        "**☑️ ⦗ `.رفع ديوث` ⦘**\n"
        "**☑️ ⦗ `.رفع مجنب` ⦘**\n"
        "**☑️ ⦗ `.رفع مميز` ⦘**\n"
        "**☑️ ⦗ `.رفع ادمن` ⦘**\n"
        "**☑️ ⦗ `.رفع منشئ` ⦘**\n"
        "**☑️ ⦗ `.رفع مالك` ⦘**\n"
        "**☑️ ⦗ `.رفع وصخ` ⦘**\n\n"
        "**☑️ ⦗ `.رفع` + كلمة ⦘**\n"
        "❐ لـ رفع الشخص بالكلمة التي وضعتها\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للتسلية والميمز ↩️", data="fun_meme_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الاذاعة                 #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"broadcast_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الإذاعة 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.وجه` ⦘**\n"
        "❐ إذاعة نص للمجموعات\n"
        "❐ طريقة الاستخدام: `.وجه النص`\n\n"
        "**☑️ ⦗ `.حول` ⦘**\n"
        "❐ إذاعة نص للخاص\n"
        "❐ طريقة الاستخدام: `.حول النص`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر التحويل                 #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"convert_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحويل 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تحويل صورة` ⦘**\n"
        "❐ تحويل الملصق إلى صورة\n"
        "❐ طريقة الاستخدام: بالرد على الملصق\n\n"
        "**☑️ ⦗ `.تحويل ملصق` ⦘**\n"
        "❐ تحويل الصورة إلى ملصق\n"
        "❐ طريقة الاستخدام: بالرد على الصورة\n\n"
        "**☑️ ⦗ `.تحويل voice` ⦘**\n"
        "❐ تحويل المقطع إلى بصمة صوتية\n"
        "❐ طريقة الاستخدام: بالرد على المقطع\n\n"
        "**☑️ ⦗ `.تحويل mp3` ⦘**\n"
        "❐ تحويل البصمة إلى مقطع mp3\n"
        "❐ طريقة الاستخدام: بالرد على البصمة\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الجهات                  #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"contacts_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الجهات 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.ضيف` ⦘**\n"
        "❐ إضافة أعضاء من مجموعة أخرى\n"
        "❐ طريقة الاستخدام: `.ضيف رابط المجموعة`\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الحساب                  #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"account_commands")))
@check_owner
async def _(event):
    await event.edit(
        "**👤 أوامر الحساب**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [
                Button.inline("اوامر الحساب 📊", data="account_detailed"),
                Button.inline("اوامر الترفيه 🎮", data="entertainment_cmd"),
            ],
            [
                Button.inline("اوامر الالعاب الذكية 🧠", data="smart_games_cmd"),
                Button.inline("اوامر الميمز 🎭", data="meme_voices_cmd"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الحساب
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"account_detailed")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الحساب 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.كروباتي مالك` ⦘** , **⦗ `.كروباتي ادمن` ⦘**\n"
        "**⦗ `.كروباتي الكل` ⦘**\n"
        "❐ لـ عرض قوائم بمجموعاتك\n\n"
        "**☑️ ⦗ `.قنواتي مالك` ⦘** - **⦗ `.قنواتي ادمن` ⦘**\n"
        "**⦗ `.قنواتي الكل` ⦘**\n"
        "❐ لـ عرض قوائم بقنواتك\n\n"
        "**☑️ ⦗ `.معلوماتي` ⦘**\n"
        "❐ لـ عرض قائمة ب عدد الاشخاص والكروبات الموجودة في حسابك\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.حسابي` ⦘**\n"
        "❐ نسخه مبسطه من أمر معلوماتي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.مغادرة القنوات` ⦘**\n\n"
        "**☑️ ⦗ `.مغادرة الكروبات` ⦘**\n\n"
        "**☑️ ⦗ `.تصفية الخاص` ⦘**\n\n"
        "**☑️ ⦗ `.تصفية البوتات` ⦘**\n"
        "**☑️ ⦗ `.حظر_البوتات` ⦘**\n\n"
        "**الفرق بين ( `.تصفية البوتات` ) و ( `.حظر_البوتات` )**\n"
        "**تصفية البوتات**: هي حذف المحادثة فقط يعني ب أمكان البوت يراسلك\n"
        "**حظر_البوتات:** هي حذف وحظر البوتات ولا يمكن البوت أن يراسلك\n\n"
        "**❐ إذا أردت دردشة معينه لاتنشمل في التصفية**\n"
        "**__قم **__بوضعها في الأرشيف\n\n"
        "**❐ طريقة الاستخدام: إرسال الأمر فقط**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الحساب ↩️", data="account_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الترفيه
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"entertainment_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الترفيه 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.بلي` ⦘**\n"
        "**☑️ ⦗ `.كت` ⦘**\n"
        "**☑️ ⦗ `.خيروك` ⦘**\n"
        "**☑️ ⦗ `.غنيلي` ⦘**\n"
        "**☑️ ⦗ `.شعر` ⦘**\n"
        "**☑️ ⦗ `.فلم` ⦘**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الحساب ↩️", data="account_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الألعاب الذكية
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"smart_games_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الألعاب الذكية 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.محيبس` ⦘**\n"
        "❐ لعبة محيبس تستطيع أستخدامها انت أو شخص أخر\n"
        "❐ فكرة العبة: أيجاد المحبس\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.نرد2` ⦘**\n"
        "❐ لعبة نرد ذكية تستطيع لعبها ويا مجموعة من الاشخاص\n"
        "❐ فكرة العبة: أقل شخص يحصل على نقاط بعد رمي النرد يخرج من العبة\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.احكام` ⦘**\n"
        "❐ لعبة ذكية تسمح بالمشاركة عده أشخاص\n"
        "❐ فكرة العبة: عند بدء العبة سيختار البوت 2 أشخاص __الاول__ الحاكم و__الثاني__المحكوم\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الحساب ↩️", data="account_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الميمز
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"meme_voices_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر بصمات الميمز 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.ميمز` ⦘**\n"
        "❐ بوضع رابط المقطع الصوتي مع الامر واسم الميمز\n"
        "❐ مثال : .ميمز + رابط البصمه + اسم الميمز الي تريده\n\n"
        "**☑️ ⦗ `.ازالة` ⦘**\n"
        "❐ إزالة بصمة معينة بوضع أسمها مع الامر\n\n"
        "**☑️ ⦗ `.قائمة الميمز` ⦘**\n"
        "❐ عرض قائمة البصمات المضافة\n\n"
        "**☑️ ⦗ `.ازالة_البصمات` ⦘**\n"
        "❐ إزالة جميع البصمات المضافة\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الحساب ↩️", data="account_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الفارات                  #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"var_commands")))
@check_owner
async def _(event):
    await event.edit(
        "**⚙️ أوامر الفارات**\n\n"
        "**⎉╎اختر الأمر الذي تريد معرفته:**",
        buttons=[
            [Button.inline("اوامر الفارات 🎈", data="vars_detailed")],
            [
                Button.inline("اوامر التخصيص 🪁", data="custom_cmd"),
                Button.inline("اوامر الاسم 🏷️", data="name_cmd"),
            ],
            [
                Button.inline("اوامر البايو 📝", data="bio_cmd"),
                Button.inline("الكروب الوقتي 🕒", data="group_timely_cmd"),
            ],
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الفارات
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"vars_detailed")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الفارات 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.جلب` ⦘**\n"
        "❐ جلب قيمة فار معين\n"
        "❐ طريقة الاستخدام: `.جلب اسم الفار`\n\n"
        "**☑️ ⦗ `.وضع توقيت` ⦘**\n"
        "❐ وضع المنطقة الزمنية\n"
        "❐ طريقة الاستخدام: بالرد على المنطقة\n\n"
        "**☑️ ⦗ `.وضع رمز الاسم` ⦘**\n"
        "❐ وضع رمز الاسم\n"
        "❐ طريقة الاستخدام: بالرد على الرمز\n\n"
        "**☑️ ⦗ `.وضع الكروب` ⦘**\n"
        "❐ وضع اسم الكروب\n"
        "❐ طريقة الاستخدام: بالرد على الاسم\n\n"
        "**☑️ ⦗ `.وضع البايو` ⦘**\n"
        "❐ وضع البايو\n"
        "❐ طريقة الاستخدام: بالرد على النبذة\n\n"
        "**☑️ ⦗ `.وضع لون وقتي` ⦘**\n"
        "❐ وضع لون الوقتي\n"
        "❐ طريقة الاستخدام: بالرد على اللون\n\n"
        "**☑️ ⦗ `.وضع الصورة` ⦘**\n"
        "❐ وضع الصورة الشخصية\n"
        "❐ طريقة الاستخدام: بالرد على رابط الصورة\n\n"
        "**☑️ ⦗ `.وضع صورة الكروب` ⦘**\n"
        "❐ وضع صورة الكروب\n"
        "❐ طريقة الاستخدام: بالرد على رابط الصورة\n\n"
        "**☑️ ⦗ `.وضع زخرفة الارقام` ⦘**\n"
        "❐ وضع زخرفة الأرقام\n"
        "❐ طريقة الاستخدام: بالرد على الأرقام\n\n"
        "**☑️ ⦗ `.وضع اسم` ⦘**\n"
        "❐ وضع الاسم\n"
        "❐ طريقة الاستخدام: بالرد على الاسم\n\n"
        "**☑️ ⦗ `.وضع كروب التخزين` ⦘**\n"
        "❐ وضع كروب التخزين\n"
        "❐ طريقة الاستخدام: بالرد على الأيدي\n\n"
        "**☑️ ⦗ `.وضع كروب الحفظ` ⦘**\n"
        "❐ وضع كروب الحفظ\n"
        "❐ طريقة الاستخدام: بالرد على الأيدي\n\n"
        "**تنويه: استخدم (محو) بدل (وضع) لحذف الفار**\n\n"
        "**•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•**\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الفارات ↩️", data="var_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الاسم
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"name_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الاسم 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.اسم وقتي` ⦘**\n"
        "❐ إضافة اسم وقتي في خانة 1\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.اسم وقتي2` ⦘**\n"
        "❐ إضافة اسم وقتي في خانة 2\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.انهاء اسم وقتي` ⦘**\n"
        "❐ إنهاء الاسم الوقتي 1 و 2\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.اوامر الاسم الوقتي` ⦘**\n"
        "❐ لـ عرض الاوامر الخاصه ب اسم الوقتي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.الصورة الوقتية` ⦘**\n"
        "❐ وضع صورة تتغير مع الوقت\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.انهاء الصورة الوقتية` ⦘**\n"
        "❐ إنهاء الصورة الوقتية\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الفارات ↩️", data="var_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر البايو
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"bio_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البايو 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.بايو وقتي` ⦘**\n"
        "❐ إضافة بايو وقتي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.انهاء البايو الوقتي` ⦘**\n"
        "❐ إنهاء البايو الوقتي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الفارات ↩️", data="var_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# صفحة تفصيلية لأوامر الكروب الوقتي
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"group_timely_cmd")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الكروب الوقتي 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.كروب وقتي` ⦘**\n"
        "❐ إضافة كروب وقتي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.انهاء كروب وقتي` ⦘**\n"
        "❐ إنهاء الكروب الوقتي\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.كروب صورة وقتي` ⦘**\n"
        "❐ تشغيل الصورة الوقتية للمجموعة\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.انهاء كروب صورة وقتي` ⦘**\n"
        "❐ إنهاء الصورة الوقتية للمجموعة\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع لأوامر الفارات ↩️", data="var_commands")],
            [Button.inline("القائمة الرئيسية 🏠", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر التجميع                  #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"collect_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التجميع 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.تجميع العرب` ⦘**\n"
        "**☑️ ⦗ `.تجميع دعمكم` ⦘**\n"
        "**☑️ ⦗ `.تجميع الجوكر` ⦘**\n"
        "**☑️ ⦗ `.تجميع المليار` ⦘**\n"
        "**☑️ ⦗ `.تجميع العقاب` ⦘**\n"
        "**☑️ ⦗ `.تجميع المليون` ⦘**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر وعد                     #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"w3d_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر وعد 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.راتب وعد` ⦘**\n"
        "❐ تجميع الأموال كل 10 دقائق\n"
        "❐ طريقة الاستخدام: في المجموعة\n\n"
        "**☑️ ⦗ `.ايقاف راتب وعد` ⦘**\n"
        "❐ إيقاف تجميع الراتب\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.سرقة وعد` ⦘**\n"
        "❐ سرقة أموال شخص كل 10 دقائق\n"
        "❐ طريقة الاستخدام: `.سرقة وعد ايدي الشخص`\n\n"
        "**☑️ ⦗ `.ايقاف سرقة وعد` ⦘**\n"
        "❐ إيقاف سرقة الأموال\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.بخشيش وعد` ⦘**\n"
        "❐ أخذ بخشيش كل 10 دقائق\n"
        "❐ طريقة الاستخدام: في المجموعة\n\n"
        "**☑️ ⦗ `.ايقاف بخشيش وعد` ⦘**\n"
        "❐ إيقاف أخذ البخشيش\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "**☑️ ⦗ `.استثمار وعد` ⦘**\n"
        "❐ استثمار الأموال كل 20 دقيقة\n"
        "❐ طريقة الاستخدام: في المجموعة\n\n"
        "**☑️ ⦗ `.ايقاف استثمار وعد` ⦘**\n"
        "❐ إيقاف الاستثمار\n"
        "❐ طريقة الاستخدام: إرسال الأمر فقط\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )

# =========================================================== #
#                صفحة تفصيلية لأوامر الاذكار                 #
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"azkar_commands")))
@check_owner
async def _(event):
    text = (
        "**𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الأذكار 𓆪**\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "**☑️ ⦗ `.اذكار الصباح` ⦘**\n"
        "**☑️ ⦗ `.اذكار المساء` ⦘**\n"
        "**☑️ ⦗ `.اذكار النوم` ⦘**\n"
        "**☑️ ⦗ `.اذكار الصلاة` ⦘**\n"
        "**☑️ ⦗ `.اذكار الاستيقاظ` ⦘**\n"
        "**☑️ ⦗ `.احاديث` ⦘**\n\n"
        "**❐ عرض الأذكار**\n"
        "**❐ طريقة الاستخدام: إرسال الأمر فقط**\n\n"
        "•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•\n"
        "⌔︙Dev : @Lx5x5"
    )
    
    await event.edit(
        text,
        buttons=[
            [Button.inline("رجوع للقائمة الرئيسية ↩️", data="ZEDHELP")],
        ],
        link_preview=False
    )
