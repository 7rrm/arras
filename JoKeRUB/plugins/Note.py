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
# متغيرات التخزين المؤقت
# =========================================================== #

user_font = {}
user_text_color = {}
user_note_color = {}

TARGET_BOT = "@e556bot"

# =========================================================== #
# نصوص القوائم
# =========================================================== #

FONT_TEXT = "**📝 اختر نوع الخط الذي تريده:**"
TEXT_COLOR_TEXT = "**🎨 اختر لون الخط:**"
NOTE_COLOR_TEXT = "**📓 اختر لون الدفتر:**"

FONTS = ["Amiri", "Cairo", "Lalezar", "Ghayaty", "Shahab", "Arial"]

TEXT_COLORS = {
    "اسود": "Black",
    "ازرق": "Blue", 
    "احمر": "Red",
    "اخضر": "Green",
    "ارجواني": "Purple"
}

NOTE_COLORS = {
    "ابيض": "White",
    "ازرق فاتح": "Light Blue",
    "بيجي": "Beige",
    "اخضر فاتح": "Light Green",
    "وردي": "Pink",
    "اصفر فاتح": "Light Yellow"
}

# =========================================================== #
# دالة تطبيق الإعدادات
# =========================================================== #

async def apply_settings(client, font, text_color, note_color):
    """تطبيق الإعدادات على البوت @e556bot"""
    try:
        async with client.conversation(TARGET_BOT, timeout=60) as conv:
            # إرسال /start
            await conv.send_message("/start")
            await asyncio.sleep(1.5)
            
            # استقبال القائمة الرئيسية
            main_menu = await conv.get_response()
            
            if not main_menu.buttons:
                return False
            
            # =========================================================== #
            # 1. تغيير نوع الخط
            # =========================================================== #
            
            # الضغط على زر "نوع الخط" (choose_font)
            for row in main_menu.buttons:
                for btn in row:
                    if btn.data == b"choose_font":
                        await btn.click()
                        await asyncio.sleep(1.5)
                        break
                else:
                    continue
                break
            
            # استقبال قائمة الخطوط
            font_list = await conv.get_response()
            
            if font_list.buttons:
                # اختيار الخط المطلوب
                font_data = f"font_{font}".encode()
                for row in font_list.buttons:
                    for btn in row:
                        if btn.data == font_data:
                            await btn.click()
                            await asyncio.sleep(1.5)
                            break
                    else:
                        continue
                    break
                
                # الضغط على زر "الرسالة" للرجوع
                confirm = await conv.get_response()
                if confirm.buttons:
                    for row in confirm.buttons:
                        for btn in row:
                            if "الرسالة" in btn.text:
                                await btn.click()
                                await asyncio.sleep(1.5)
                                break
                        break
            
            # =========================================================== #
            # 2. تغيير لون الخط
            # =========================================================== #
            
            # العودة للقائمة الرئيسية
            main_menu2 = await conv.get_response()
            
            # الضغط على زر "لون الخط" (choose_text_color)
            for row in main_menu2.buttons:
                for btn in row:
                    if btn.data == b"choose_text_color":
                        await btn.click()
                        await asyncio.sleep(1.5)
                        break
                else:
                    continue
                break
            
            # استقبال قائمة ألوان الخط
            color_list = await conv.get_response()
            
            if color_list.buttons:
                # اختيار اللون المطلوب
                color_data = f"text_color_{text_color}".encode()
                for row in color_list.buttons:
                    for btn in row:
                        if btn.data == color_data:
                            await btn.click()
                            await asyncio.sleep(1.5)
                            break
                    else:
                        continue
                    break
                
                # الضغط على زر "الرسالة" للرجوع
                confirm2 = await conv.get_response()
                if confirm2.buttons:
                    for row in confirm2.buttons:
                        for btn in row:
                            if "الرسالة" in btn.text:
                                await btn.click()
                                await asyncio.sleep(1.5)
                                break
                        break
            
            # =========================================================== #
            # 3. تغيير لون الدفتر
            # =========================================================== #
            
            # العودة للقائمة الرئيسية
            main_menu3 = await conv.get_response()
            
            # الضغط على زر "لون الدفتر" (choose_page_color)
            for row in main_menu3.buttons:
                for btn in row:
                    if btn.data == b"choose_page_color":
                        await btn.click()
                        await asyncio.sleep(1.5)
                        break
                else:
                    continue
                break
            
            # استقبال قائمة ألوان الدفتر
            page_list = await conv.get_response()
            
            if page_list.buttons:
                # اختيار اللون المطلوب
                page_data = f"page_color_{note_color}".encode()
                for row in page_list.buttons:
                    for btn in row:
                        if btn.data == page_data:
                            await btn.click()
                            await asyncio.sleep(1.5)
                            break
                    else:
                        continue
                    break
                
                # الضغط على زر "الرسالة" للرجوع
                confirm3 = await conv.get_response()
                if confirm3.buttons:
                    for row in confirm3.buttons:
                        for btn in row:
                            if "الرسالة" in btn.text:
                                await btn.click()
                                await asyncio.sleep(1.5)
                                break
                        break
            
            return True
            
    except Exception as e:
        print(f"خطأ: {e}")
        return False

# =========================================================== #
# الاستعلام المضمن
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

# =========================================================== #
# معالجات الأزرار (كما هي)
# =========================================================== #

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

# =========================================================== #
# حفظ الإعدادات
# =========================================================== #

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
# أمر اعدادات الدفتر
# =========================================================== #

@l313l.ar_cmd(pattern="اعدادات الدفتر$")
async def repo(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "الدفتر")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# أمر .اكتب
# =========================================================== #

@l313l.ar_cmd(pattern="اكتب (.*)")
async def write_note(event):
    user_id = event.sender_id
    text = event.pattern_match.group(1)
    
    if not text:
        return await edit_or_reply(event, "❌ الرجاء كتابة النص بعد الأمر\nمثال: `.اكتب مرحباً`")
    
    jokevent = await edit_or_reply(event, "⌔︙جـار إنشاء الدفتر...")
    start = datetime.now()
    
    font = user_font.get(user_id) or gvarstatus(f"USER_FONT_{user_id}") or "Amiri"
    text_color = user_text_color.get(user_id) or gvarstatus(f"USER_TEXT_COLOR_{user_id}") or "Black"
    note_color = user_note_color.get(user_id) or gvarstatus(f"USER_NOTE_COLOR_{user_id}") or "White"
    
    try:
        # تطبيق الإعدادات
        await apply_settings(event.client, font, text_color, note_color)
        
        # إرسال النص
        async with event.client.conversation(TARGET_BOT, timeout=60) as conv:
            purgeflag = await conv.send_message(text)
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
                return
            else:
                await jokevent.edit(f"**❌ لم يتم استلام صورة**")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙خطأ:**\n`{str(e)}`")
