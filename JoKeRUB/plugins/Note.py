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

# قائمة الخطوط (بالترتيب)
FONTS = ["Amiri", "Cairo", "Lalezar", "Ghayaty", "Shahab", "Arial"]

# قائمة ألوان الخط
TEXT_COLORS = ["Black", "Blue", "Red", "Green", "Purple"]

# قائمة ألوان الدفتر
NOTE_COLORS = ["White", "Light Blue", "Beige", "Light Green", "Pink", "Light Yellow"]

# =========================================================== #
# دالة تطبيق الإعدادات فوراً (باستخدام l313l)
# =========================================================== #

async def apply_setting_immediately(setting_type, value, index):
    """تطبيق الإعداد فوراً على البوت باستخدام l313l"""
    try:
        async with l313l.conversation(TARGET_BOT, timeout=45) as conv:
            # إرسال /start
            await conv.send_message("/start")
            await asyncio.sleep(1.5)
            
            # استقبال القائمة الرئيسية
            main_menu = await conv.get_response()
            
            if not main_menu.buttons:
                return False
            
            # =========================================================== #
            # الضغط على الزر المناسب حسب النوع
            # =========================================================== #
            
            if setting_type == 'font':
                # الضغط على زر "نوع الخط" (الزر الأول)
                await main_menu.click(0)
                await asyncio.sleep(1.5)
                
                # استقبال قائمة الخطوط
                font_list = await conv.get_response()
                
                if font_list.buttons:
                    # الضغط على الزر حسب الرقم الذي اختاره المستخدم
                    btn_index = 0
                    for row in font_list.buttons:
                        for btn in row:
                            if btn_index == index:
                                await btn.click()
                                await asyncio.sleep(1.5)
                                break
                            btn_index += 1
                        else:
                            continue
                        break
                    
                    # الضغط على زر "الرسالة" للرجوع
                    confirm = await conv.get_response()
                    if confirm.buttons:
                        for row in confirm.buttons:
                            for btn in row:
                                if btn.text == "الرسالة":
                                    await btn.click()
                                    await asyncio.sleep(1.5)
                                    break
                            break
            
            elif setting_type == 'text_color':
                # الضغط على زر "لون الخط" (الزر الثاني)
                await main_menu.click(1)
                await asyncio.sleep(1.5)
                
                # استقبال قائمة ألوان الخط
                color_list = await conv.get_response()
                
                if color_list.buttons:
                    btn_index = 0
                    for row in color_list.buttons:
                        for btn in row:
                            if btn_index == index:
                                await btn.click()
                                await asyncio.sleep(1.5)
                                break
                            btn_index += 1
                        else:
                            continue
                        break
                    
                    confirm = await conv.get_response()
                    if confirm.buttons:
                        for row in confirm.buttons:
                            for btn in row:
                                if btn.text == "الرسالة":
                                    await btn.click()
                                    await asyncio.sleep(1.5)
                                    break
                            break
            
            elif setting_type == 'note_color':
                # الضغط على زر "لون الدفتر" (الزر الثالث)
                await main_menu.click(2)
                await asyncio.sleep(1.5)
                
                # استقبال قائمة ألوان الدفتر
                note_list = await conv.get_response()
                
                if note_list.buttons:
                    btn_index = 0
                    for row in note_list.buttons:
                        for btn in row:
                            if btn_index == index:
                                await btn.click()
                                await asyncio.sleep(1.5)
                                break
                            btn_index += 1
                        else:
                            continue
                        break
                    
                    confirm = await conv.get_response()
                    if confirm.buttons:
                        for row in confirm.buttons:
                            for btn in row:
                                if btn.text == "الرسالة":
                                    await btn.click()
                                    await asyncio.sleep(1.5)
                                    break
                            break
            
            # حذف جميع رسائل المحادثة
            await delete_conv(TARGET_BOT)
            
            return True
            
    except Exception as e:
        print(f"خطأ: {e}")
        return False

async def delete_conv(bot_username):
    """حذف جميع رسائل المحادثة مع البوت باستخدام l313l"""
    try:
        async for msg in l313l.iter_messages(bot_username, limit=30):
            await msg.delete()
    except:
        pass

# =========================================================== #
# نصوص القوائم (للإعدادات)
# =========================================================== #

FONT_TEXT = "**📝 اختر نوع الخط الذي تريده:**"
TEXT_COLOR_TEXT = "**🎨 اختر لون الخط:**"
NOTE_COLOR_TEXT = "**📓 اختر لون الدفتر:**"

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
# قوائم الخطوط (عمودية - كل زر في سطر منفصل)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"font_menu")))
async def font_menu(event):
    """عرض قائمة الخطوط - عمودية"""
    buttons = []
    for i, font in enumerate(FONTS):
        buttons.append([Button.inline(font, data=f"set_font_{i}", style="primary")])
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(FONT_TEXT, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"text_color_menu")))
async def text_color_menu(event):
    """عرض قائمة ألوان الخط - عمودية"""
    buttons = []
    for i, color in enumerate(TEXT_COLORS):
        buttons.append([Button.inline(color, data=f"set_text_color_{i}", style="primary")])
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(TEXT_COLOR_TEXT, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"note_color_menu")))
async def note_color_menu(event):
    """عرض قائمة ألوان الدفتر - عمودية"""
    buttons = []
    for i, color in enumerate(NOTE_COLORS):
        buttons.append([Button.inline(color, data=f"set_note_color_{i}", style="primary")])
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(NOTE_COLOR_TEXT, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# حفظ الإعدادات وتطبيقها فوراً
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_font_(\\d+)")))
async def set_font(event):
    index = int(event.data_match.group(1))
    user_id = event.query.user_id
    font = FONTS[index]
    
    user_font[user_id] = font
    addgvar(f"USER_FONT_{user_id}", font)
    
    await event.edit(f"✅ تم حفظ الخط: **{font}**\n\n⌔︙جـار تطبيق الإعداد على البوت...", parse_mode="Markdown")
    
    # ✅ استخدام l313l بدلاً من event.client
    success = await apply_setting_immediately('font', font, index)
    
    if success:
        await event.edit(f"✅ تم حفظ وتطبيق الخط: **{font}**", 
                         buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                         parse_mode="Markdown")
    else:
        await event.edit(f"✅ تم حفظ الخط: **{font}**\n\n⚠️ حدث خطأ في تطبيق الإعداد", 
                         buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                         parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_text_color_(\\d+)")))
async def set_text_color(event):
    index = int(event.data_match.group(1))
    user_id = event.query.user_id
    color = TEXT_COLORS[index]
    
    user_text_color[user_id] = color
    addgvar(f"USER_TEXT_COLOR_{user_id}", color)
    
    await event.edit(f"✅ تم حفظ لون الخط: **{color}**\n\n⌔︙جـار تطبيق الإعداد على البوت...", parse_mode="Markdown")
    
    success = await apply_setting_immediately('text_color', color, index)
    
    if success:
        await event.edit(f"✅ تم حفظ وتطبيق لون الخط: **{color}**", 
                         buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                         parse_mode="Markdown")
    else:
        await event.edit(f"✅ تم حفظ لون الخط: **{color}**\n\n⚠️ حدث خطأ في تطبيق الإعداد", 
                         buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                         parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"set_note_color_(\\d+)")))
async def set_note_color(event):
    index = int(event.data_match.group(1))
    user_id = event.query.user_id
    color = NOTE_COLORS[index]
    
    user_note_color[user_id] = color
    addgvar(f"USER_NOTE_COLOR_{user_id}", color)
    
    await event.edit(f"✅ تم حفظ لون الدفتر: **{color}**\n\n⌔︙جـار تطبيق الإعداد على البوت...", parse_mode="Markdown")
    
    success = await apply_setting_immediately('note_color', color, index)
    
    if success:
        await event.edit(f"✅ تم حفظ وتطبيق لون الدفتر: **{color}**", 
                         buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                         parse_mode="Markdown")
    else:
        await event.edit(f"✅ تم حفظ لون الدفتر: **{color}**\n\n⚠️ حدث خطأ في تطبيق الإعداد", 
                         buttons=[[Button.inline("🔙 رجوع", data="back_to_main", style="primary")]],
                         parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"back_to_main")))
async def back_to_main(event):
    buttons = [
        [Button.inline("📝 نوع الخط", data="font_menu", style="primary")],
        [Button.inline("🎨 لون الخط", data="text_color_menu", style="primary"),
         Button.inline("📓 لون الدفتر", data="note_color_menu", style="primary")],
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
    
    font = user_font.get(user_id) or gvarstatus(f"USER_FONT_{user_id}") or "Amiri"
    text_color = user_text_color.get(user_id) or gvarstatus(f"USER_TEXT_COLOR_{user_id}") or "Black"
    note_color = user_note_color.get(user_id) or gvarstatus(f"USER_NOTE_COLOR_{user_id}") or "White"
    
    try:
        async with l313l.conversation(TARGET_BOT, timeout=60) as conv:
            await conv.send_message("/start")
            await asyncio.sleep(1.5)
            
            main_menu = await conv.get_response()
            
            # تطبيق جميع الإعدادات الثلاثة
            # نوع الخط
            await main_menu.click(0)
            await asyncio.sleep(1)
            font_list = await conv.get_response()
            font_index = FONTS.index(font) if font in FONTS else 0
            btn_counter = 0
            for row in font_list.buttons:
                for btn in row:
                    if btn_counter == font_index:
                        await btn.click()
                        break
                    btn_counter += 1
                else:
                    continue
                break
            await asyncio.sleep(1)
            confirm = await conv.get_response()
            for row in confirm.buttons:
                for btn in row:
                    if btn.text == "الرسالة":
                        await btn.click()
                        break
                break
            await asyncio.sleep(1)
            
            # لون الخط
            main_menu = await conv.get_response()
            await main_menu.click(1)
            await asyncio.sleep(1)
            color_list = await conv.get_response()
            color_index = TEXT_COLORS.index(text_color) if text_color in TEXT_COLORS else 0
            btn_counter = 0
            for row in color_list.buttons:
                for btn in row:
                    if btn_counter == color_index:
                        await btn.click()
                        break
                    btn_counter += 1
                else:
                    continue
                break
            await asyncio.sleep(1)
            confirm = await conv.get_response()
            for row in confirm.buttons:
                for btn in row:
                    if btn.text == "الرسالة":
                        await btn.click()
                        break
                break
            await asyncio.sleep(1)
            
            # لون الدفتر
            main_menu = await conv.get_response()
            await main_menu.click(2)
            await asyncio.sleep(1)
            note_list = await conv.get_response()
            note_index = NOTE_COLORS.index(note_color) if note_color in NOTE_COLORS else 0
            btn_counter = 0
            for row in note_list.buttons:
                for btn in row:
                    if btn_counter == note_index:
                        await btn.click()
                        break
                    btn_counter += 1
                else:
                    continue
                break
            await asyncio.sleep(1)
            confirm = await conv.get_response()
            for row in confirm.buttons:
                for btn in row:
                    if btn.text == "الرسالة":
                        await btn.click()
                        break
                break
            await asyncio.sleep(1)
            
            # إرسال النص
            await conv.send_message(text)
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
                async for msg in l313l.iter_messages(TARGET_BOT, limit=20):
                    await msg.delete()
            else:
                await jokevent.edit(f"**❌ لم يتم استلام صورة**")
                
    except asyncio.TimeoutError:
        await jokevent.edit("**⌔︙انتهى الوقت، البوت لم يرد**")
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")
