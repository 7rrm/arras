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

user_font = {}          # نوع الخط لكل مستخدم
user_text_color = {}    # لون الخط
user_note_color = {}    # لون الدفتر
user_settings_applied = {}  # هل تم تطبيق الإعدادات مسبقاً

# إعدادات البوت الهدف
TARGET_BOT = "@e556bot"

# =========================================================== #
# نصوص القوائم
# =========================================================== #

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
# دالة تطبيق الإعدادات على البوت
# =========================================================== #

async def apply_settings(client, user_id, font, text_color, note_color):
    """تطبيق الإعدادات على البوت @e556bot"""
    try:
        async with client.conversation(TARGET_BOT, timeout=45) as conv:
            # استقبال رسالة الترحيب
            welcome = await conv.get_response()
            
            # انتظار القائمة الرئيسية
            main_menu = await conv.get_response()
            
            if not main_menu.buttons:
                return False
            
            # =========================================================== #
            # 1. تغيير نوع الخط
            # =========================================================== #
            
            # الضغط على زر "نوع الخط" (الزر الأول)
            await main_menu.click(0)
            await asyncio.sleep(1)
            
            # استقبال قائمة الخطوط
            font_list = await conv.get_response()
            
            if font_list.buttons:
                # البحث عن الخط المطلوب
                for row in font_list.buttons:
                    for btn in row:
                        if btn.text == font:
                            await btn.click()
                            await asyncio.sleep(1)
                            break
                    else:
                        continue
                    break
                
                # استقبال تأكيد أو رجوع
                confirm = await conv.get_response()
                # الضغط على زر الرجوع إذا وجد
                if confirm.buttons:
                    for row in confirm.buttons:
                        for btn in row:
                            if "رجوع" in btn.text or "الرسالة" in btn.text:
                                await btn.click()
                                await asyncio.sleep(1)
                                break
                        break
            
            # =========================================================== #
            # 2. تغيير لون الخط
            # =========================================================== #
            
            # العودة للقائمة الرئيسية (إذا لزم الأمر)
            try:
                back_to_menu = await conv.get_response()
                if back_to_menu.buttons:
                    # البحث عن زر "لون الخط"
                    for row in back_to_menu.buttons:
                        for btn in row:
                            if btn.text == "لون الخط":
                                await btn.click()
                                await asyncio.sleep(1)
                                break
                        else:
                            continue
                        break
                    else:
                        # إذا لم نجد، نضغط على الزر الثاني
                        await back_to_menu.click(1)
                        await asyncio.sleep(1)
            except:
                pass
            
            # استقبال قائمة ألوان الخط
            color_list = await conv.get_response()
            
            if color_list.buttons:
                # البحث عن اللون المطلوب
                for row in color_list.buttons:
                    for btn in row:
                        if btn.text == text_color:
                            await btn.click()
                            await asyncio.sleep(1)
                            break
                    else:
                        continue
                    break
                
                # استقبال تأكيد
                confirm2 = await conv.get_response()
                if confirm2.buttons:
                    for row in confirm2.buttons:
                        for btn in row:
                            if "رجوع" in btn.text or "الرسالة" in btn.text:
                                await btn.click()
                                await asyncio.sleep(1)
                                break
                        break
            
            # =========================================================== #
            # 3. تغيير لون الدفتر
            # =========================================================== #
            
            # العودة للقائمة الرئيسية
            try:
                back_to_menu2 = await conv.get_response()
                if back_to_menu2.buttons:
                    # البحث عن زر "لون الدفتر"
                    for row in back_to_menu2.buttons:
                        for btn in row:
                            if btn.text == "لون الدفتر":
                                await btn.click()
                                await asyncio.sleep(1)
                                break
                        else:
                            continue
                        break
                    else:
                        await back_to_menu2.click(2)
                        await asyncio.sleep(1)
            except:
                pass
            
            # استقبال قائمة ألوان الدفتر
            note_list = await conv.get_response()
            
            if note_list.buttons:
                # البحث عن اللون المطلوب
                for row in note_list.buttons:
                    for btn in row:
                        if btn.text == note_color:
                            await btn.click()
                            await asyncio.sleep(1)
                            break
                    else:
                        continue
                    break
                
                # استقبال تأكيد
                confirm3 = await conv.get_response()
                if confirm3.buttons:
                    for row in confirm3.buttons:
                        for btn in row:
                            if "رجوع" in btn.text or "الرسالة" in btn.text:
                                await btn.click()
                                await asyncio.sleep(1)
                                break
                        break
            
            return True
            
    except Exception as e:
        print(f"خطأ في تطبيق الإعدادات: {e}")
        return False

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

# =========================================================== #
# معالجات الأزرار
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"font_menu")))
async def font_menu(event):
    """عرض قائمة الخطوط"""
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
    """عرض قائمة ألوان الخط"""
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
    """عرض قائمة ألوان الدفتر"""
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
    
    await event.edit(f"✅ تم حفظ الخط: **{font}**\n\nسوف يُستخدم عند كتابة `.اكتب`", 
                     buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                     parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_text_color_(.*)")))
async def set_text_color(event):
    color_code = event.data_match.group(1).decode()
    user_id = event.query.user_id
    
    color_name = [k for k, v in TEXT_COLORS.items() if v == color_code][0]
    user_text_color[user_id] = color_code
    addgvar(f"USER_TEXT_COLOR_{user_id}", color_code)
    
    await event.edit(f"✅ تم حفظ لون الخط: **{color_name}**\n\nسوف يُستخدم عند كتابة `.اكتب`", 
                     buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                     parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_note_color_(.*)")))
async def set_note_color(event):
    color_code = event.data_match.group(1).decode()
    user_id = event.query.user_id
    
    color_name = [k for k, v in NOTE_COLORS.items() if v == color_code][0]
    user_note_color[user_id] = color_code
    addgvar(f"USER_NOTE_COLOR_{user_id}", color_code)
    
    await event.edit(f"✅ تم حفظ لون الدفتر: **{color_name}**\n\nسوف يُستخدم عند كتابة `.اكتب`", 
                     buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                     parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"back_to_main")))
async def back_to_main(event):
    """العودة إلى القائمة الرئيسية"""
    buttons = [
        [Button.inline("📝 نوع الخط", data="font_menu", style="primary")],
        [Button.inline("🎨 لون الخط", data="text_color_menu", style="primary"),
         Button.inline("📓 لون الدفتر", data="note_color_menu", style="primary")],
        [Button.inline("❌ إغلاق", data="close_menu", style="danger")]
    ]
    await event.edit("**⚙️ إعدادات الدفتر\nاختر الإعداد الذي تريد تغييره:**", 
                     buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"close_menu")))
async def close_menu(event):
    await event.delete()
    await event.answer("❌ تم إغلاق القائمة", alert=True)

# =========================================================== #
# أمر اعدادات الدفتر
# =========================================================== #

@l313l.ar_cmd(pattern="اعدادات الدفتر$")
async def repo(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        pass

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
    
    # جلب الإعدادات المحفوظة
    font = user_font.get(user_id) or gvarstatus(f"USER_FONT_{user_id}") or "Amiri"
    text_color = user_text_color.get(user_id) or gvarstatus(f"USER_TEXT_COLOR_{user_id}") or "Black"
    note_color = user_note_color.get(user_id) or gvarstatus(f"USER_NOTE_COLOR_{user_id}") or "White"
    
    try:
        # تطبيق الإعدادات على البوت
        await apply_settings(event.client, user_id, font, text_color, note_color)
        
        # إرسال النص إلى البوت
        async with event.client.conversation(TARGET_BOT, timeout=60) as conv:
            # إرسال النص
            purgeflag = await conv.send_message(text)
            
            # انتظار الرد (الصورة)
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
                
                # حذف المحادثة
                await delete_conv(event.client, TARGET_BOT, purgeflag)
                return
            else:
                await jokevent.edit(f"**❌ لم يتم استلام صورة من البوت**\n📝 رد البوت: `{response.text[:100] if response.text else 'لا يوجد'}`")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت، البوت لم يرد**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")
