from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import re
from datetime import datetime
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from JoKeRUB.plugins import mention
from ..core.managers import edit_or_reply
from . import l313l

# =========================================================== #
# متغيرات التخزين المؤقت والإعدادات
# =========================================================== #

user_font = {}          # نوع الخط لكل مستخدم
user_text_color = {}    # لون الخط
user_note_color = {}    # لون الدفتر

TARGET_BOT = "@e556bot"

# قائمة الخطوط (بالترتيب الذي يظهر في البوت)
AVAILABLE_FONTS = ["Amiri", "Cairo", "Lalezar", "Ghayaty", "Shahab", "Arial"]

# قائمة ألوان الخط (بالترتيب)
AVAILABLE_TEXT_COLORS = ["Black", "Blue", "Red", "Green", "Purple"]

# قائمة ألوان الدفتر (بالترتيب)
AVAILABLE_NOTE_COLORS = ["White", "Light Blue", "Beige", "Light Green", "Pink", "Light Yellow"]

# =========================================================== #
# نصوص القوائم الخاصة بأداة الإعدادات
# =========================================================== #

FONT_TEXT = "**📝 اختر نوع الخط الذي تريده:**"
TEXT_COLOR_TEXT = "**🎨 اختر لون الخط:**"
NOTE_COLOR_TEXT = "**📓 اختر لون الدفتر:**"

# =========================================================== #
# دالة تطبيق الإعدادات على البوت (تعتمد على النص الظاهر)
# =========================================================== #

async def apply_settings(client, font, text_color, note_color):
    """تطبيق الإعدادات على البوت @e556bot باستخدام النص الظاهر للأزرار"""
    try:
        async with client.conversation(TARGET_BOT, timeout=60) as conv:
            # 1. إرسال /start لبدء المحادثة
            await conv.send_message("/start")
            await asyncio.sleep(2)

            # 2. انتظار القائمة الرئيسية
            main_menu = await conv.get_response()
            if not main_menu.buttons:
                return False

            # ---------------------------------------------------------
            # 3. تغيير نوع الخط
            # ---------------------------------------------------------
            # البحث عن زر "نوع الخط" في القائمة الرئيسية
            font_type_button = None
            for row in main_menu.buttons:
                for btn in row:
                    if btn.text == "نوع الخط":
                        font_type_button = btn
                        break
                if font_type_button:
                    break

            if font_type_button:
                await font_type_button.click()
                await asyncio.sleep(2)

                # الحصول على قائمة الخطوط
                fonts_menu = await conv.get_response()
                if fonts_menu.buttons:
                    # البحث عن زر الخط المطلوب واختياره
                    target_font_button = None
                    for row in fonts_menu.buttons:
                        for btn in row:
                            if btn.text == font:
                                target_font_button = btn
                                break
                        if target_font_button:
                            break

                    if target_font_button:
                        await target_font_button.click()
                        await asyncio.sleep(2)

                        # الضغط على زر "الرسالة" للعودة إلى القائمة الرئيسية
                        back_button = None
                        back_response = await conv.get_response()
                        if back_response.buttons:
                            for row in back_response.buttons:
                                for btn in row:
                                    if btn.text == "الرسالة":
                                        back_button = btn
                                        break
                                if back_button:
                                    break
                        if back_button:
                            await back_button.click()
                            await asyncio.sleep(2)

            # ---------------------------------------------------------
            # 4. تغيير لون الخط
            # ---------------------------------------------------------
            # إعادة الحصول على القائمة الرئيسية بعد العودة
            main_menu = await conv.get_response()
            if not main_menu.buttons:
                main_menu = await conv.get_response()  # محاولة مرة أخرى

            # البحث عن زر "لون الخط"
            text_color_button = None
            for row in main_menu.buttons:
                for btn in row:
                    if btn.text == "لون الخط":
                        text_color_button = btn
                        break
                if text_color_button:
                    break

            if text_color_button:
                await text_color_button.click()
                await asyncio.sleep(2)

                # الحصول على قائمة ألوان الخط
                colors_menu = await conv.get_response()
                if colors_menu.buttons:
                    # البحث عن زر اللون المطلوب واختياره
                    target_color_button = None
                    for row in colors_menu.buttons:
                        for btn in row:
                            if btn.text == text_color:
                                target_color_button = btn
                                break
                        if target_color_button:
                            break

                    if target_color_button:
                        await target_color_button.click()
                        await asyncio.sleep(2)

                        # الضغط على زر "الرسالة" للعودة
                        back_button = None
                        back_response = await conv.get_response()
                        if back_response.buttons:
                            for row in back_response.buttons:
                                for btn in row:
                                    if btn.text == "الرسالة":
                                        back_button = btn
                                        break
                                if back_button:
                                    break
                        if back_button:
                            await back_button.click()
                            await asyncio.sleep(2)

            # ---------------------------------------------------------
            # 5. تغيير لون الدفتر
            # ---------------------------------------------------------
            # إعادة الحصول على القائمة الرئيسية
            main_menu = await conv.get_response()
            if not main_menu.buttons:
                main_menu = await conv.get_response()

            # البحث عن زر "لون الدفتر"
            note_color_button = None
            for row in main_menu.buttons:
                for btn in row:
                    if btn.text == "لون الدفتر":
                        note_color_button = btn
                        break
                if note_color_button:
                    break

            if note_color_button:
                await note_color_button.click()
                await asyncio.sleep(2)

                # الحصول على قائمة ألوان الدفتر
                pages_menu = await conv.get_response()
                if pages_menu.buttons:
                    # البحث عن زر اللون المطلوب واختياره
                    target_page_button = None
                    for row in pages_menu.buttons:
                        for btn in row:
                            if btn.text == note_color:
                                target_page_button = btn
                                break
                        if target_page_button:
                            break

                    if target_page_button:
                        await target_page_button.click()
                        await asyncio.sleep(2)

                        # الضغط على زر "الرسالة" للعودة
                        back_button = None
                        back_response = await conv.get_response()
                        if back_response.buttons:
                            for row in back_response.buttons:
                                for btn in row:
                                    if btn.text == "الرسالة":
                                        back_button = btn
                                        break
                                if back_button:
                                    break
                        if back_button:
                            await back_button.click()
                            await asyncio.sleep(2)

            return True

    except Exception as e:
        print(f"خطأ في تطبيق الإعدادات: {e}")
        return False


# =========================================================== #
# باقي الكود (الاستعلام المضمن، الأزرار، الأوامر) - يبقى كما هو
# =========================================================== #

# نصوص القوائم الخاصة بأداة الإعدادات (للاستعلام المضمن)
FONT_TEXT = "**📝 اختر نوع الخط الذي تريده:**"
TEXT_COLOR_TEXT = "**🎨 اختر لون الخط:**"
NOTE_COLOR_TEXT = "**📓 اختر لون الدفتر:**"

# قائمة الخطوط (كما في البوت)
FONTS = ["Amiri", "Cairo", "Lalezar", "Ghayaty", "Shahab", "Arial"]

# قائمة ألوان الخط (كما في البوت)
TEXT_COLORS = {
    "اسود": "Black",
    "ازرق": "Blue", 
    "احمر": "Red",
    "اخضر": "Green",
    "ارجواني": "Purple"
}

# قائمة ألوان الدفتر (كما في البوت)
NOTE_COLORS = {
    "ابيض": "White",
    "ازرق فاتح": "Light Blue",
    "بيجي": "Beige",
    "اخضر فاتح": "Light Green",
    "وردي": "Pink",
    "اصفر فاتح": "Light Yellow"
}

# =========================================================== #
# دالة حذف المحادثة
# =========================================================== #

async def delete_conv(client, bot_username, *msgs):
    """حذف الرسائل المرسلة في المحادثة"""
    try:
        async for msg in client.iter_messages(bot_username, limit=20):
            await msg.delete()
    except:
        pass

# =========================================================== #
# الاستعلام المضمن (اعدادات الدفتر)
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        query = event.text
        
        if query.startswith("الدفتر") and event.query.user_id == l313l.uid:
            buttons = [
                [Button.inline("📝 نوع الخط", data="font_menu", style="primary")],
                [Button.inline("🎨 لون الخط", data="text_color_menu", style="primary"),
                 Button.inline("📓 لون الدفتر", data="note_color_menu", style="primary")],
                [Button.inline("❌ إغلاق", data="close_menu", style="danger")]
            ]
            
            await event.answer(
                [await event.builder.article(
                    title="📓 اعدادات الدفتر",
                    description="تخصيص خط ولون الدفتر",
                    text="**⚙️ إعدادات الدفتر\nاختر الإعداد الذي تريد تغييره:**",
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )

# معالجات الأزرار (للاستعلام المضمن الخاص بنا)
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"font_menu")))
async def font_menu(event):
    buttons = []
    row = []
    for i, font in enumerate(FONTS):
        row.append(Button.inline(font, data=f"set_font_{font}", style="primary"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(FONT_TEXT, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"text_color_menu")))
async def text_color_menu(event):
    buttons = []
    row = []
    for color_name, color_code in TEXT_COLORS.items():
        row.append(Button.inline(color_name, data=f"set_text_color_{color_code}", style="primary"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(TEXT_COLOR_TEXT, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"note_color_menu")))
async def note_color_menu(event):
    buttons = []
    row = []
    for color_name, color_code in NOTE_COLORS.items():
        row.append(Button.inline(color_name, data=f"set_note_color_{color_code}", style="primary"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(NOTE_COLOR_TEXT, buttons=buttons, parse_mode="Markdown")

# حفظ الإعدادات
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_font_(.*)")))
async def set_font(event):
    font = event.data_match.group(1).decode()
    user_id = event.query.user_id
    user_font[user_id] = font
    addgvar(f"USER_FONT_{user_id}", font)
    await event.edit(f"✅ تم حفظ الخط: **{font}**", buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]], parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_text_color_(.*)")))
async def set_text_color(event):
    color_code = event.data_match.group(1).decode()
    user_id = event.query.user_id
    color_name = [k for k, v in TEXT_COLORS.items() if v == color_code][0]
    user_text_color[user_id] = color_code
    addgvar(f"USER_TEXT_COLOR_{user_id}", color_code)
    await event.edit(f"✅ تم حفظ لون الخط: **{color_name}**", buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]], parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_note_color_(.*)")))
async def set_note_color(event):
    color_code = event.data_match.group(1).decode()
    user_id = event.query.user_id
    color_name = [k for k, v in NOTE_COLORS.items() if v == color_code][0]
    user_note_color[user_id] = color_code
    addgvar(f"USER_NOTE_COLOR_{user_id}", color_code)
    await event.edit(f"✅ تم حفظ لون الدفتر: **{color_name}**", buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]], parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"back_to_main")))
async def back_to_main(event):
    buttons = [
        [Button.inline("📝 نوع الخط", data="font_menu", style="primary")],
        [Button.inline("🎨 لون الخط", data="text_color_menu", style="primary"), Button.inline("📓 لون الدفتر", data="note_color_menu", style="primary")],
        [Button.inline("❌ إغلاق", data="close_menu", style="danger")]
    ]
    await event.edit("**⚙️ إعدادات الدفتر\nاختر الإعداد الذي تريد تغييره:**", buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"close_menu")))
async def close_menu(event):
    await event.delete()
    await event.answer("❌ تم إغلاق القائمة", alert=True)

# =========================================================== #
# أوامر المستخدم
# =========================================================== #

@l313l.ar_cmd(pattern="اعدادات الدفتر$")
async def settings_command(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "الدفتر")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="اكتب (.*)")
async def write_note(event):
    user_id = event.sender_id
    text = event.pattern_match.group(1)
    
    if not text:
        return await edit_or_reply(event, "❌ الرجاء كتابة النص بعد الأمر\nمثال: `.اكتب مرحباً`")
    
    jokevent = await edit_or_reply(event, "⌔︙جـار إنشاء الدفتر...")
    start = datetime.now()
    
    # جلب الإعدادات المحفوظة للمستخدم
    font = user_font.get(user_id) or gvarstatus(f"USER_FONT_{user_id}") or "Amiri"
    text_color = user_text_color.get(user_id) or gvarstatus(f"USER_TEXT_COLOR_{user_id}") or "Black"
    note_color = user_note_color.get(user_id) or gvarstatus(f"USER_NOTE_COLOR_{user_id}") or "White"
    
    try:
        # تطبيق الإعدادات على البوت
        success = await apply_settings(event.client, font, text_color, note_color)
        if not success:
            await jokevent.edit("❌ فشل في تطبيق الإعدادات")
            return
        
        # إرسال النص إلى البوت
        async with event.client.conversation(TARGET_BOT, timeout=60) as conv:
            await conv.send_message(text)
            
            # انتظار رد البوت (الصورة)
            response = await conv.get_response()
            
            if response.photo or response.document:
                end = datetime.now()
                ms = (end - start).seconds
                
                await event.client.send_file(
                    event.chat_id,
                    response.media,
                    caption=f"**📸 تم إنشاء دفترك!**\n⏰ **الوقت:** `{ms} ثانية`\n\n**📝 النص:** `{text[:50]}...`\n\n**⚙️ الإعدادات:**\n• الخط: `{font}`\n• لون الخط: `{text_color}`\n• لون الدفتر: `{note_color}`"
                )
                await jokevent.delete()
            else:
                await jokevent.edit(f"**❌ لم يتم استلام صورة من البوت**\nرد البوت: {response.text[:100] if response.text else 'لا يوجد'}")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت، البوت لم يرد**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")
