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
# دالة تطبيق الإعدادات (نفس طريقة التجميع)
# =========================================================== #

async def apply_setting_immediately(setting_type, index):
    """تطبيق الإعداد فوراً على البوت - نفس طريقة التجميع"""
    try:
        # 1. إرسال /start
        await l313l.send_message(TARGET_BOT, '/start')
        await asyncio.sleep(3)
        
        # 2. جلب آخر رسالة (الرسالة التي تحتوي على الأزرار)
        msg0 = await l313l.get_messages(TARGET_BOT, limit=1)
        if not msg0 or not msg0[0].buttons:
            return False
        
        # حفظ معرف الرسالة (لأن البوت يعدل نفس الرسالة)
        msg_id = msg0[0].id
        chat_id = msg0[0].peer_id.channel_id if hasattr(msg0[0].peer_id, 'channel_id') else msg0[0].peer_id.user_id
        
        # 3. الضغط على الزر المناسب
        if setting_type == 'font':
            await msg0[0].click(0)  # زر "نوع الخط"
        elif setting_type == 'text_color':
            await msg0[0].click(2)  # زر "لون الخط"
        elif setting_type == 'note_color':
            await msg0[0].click(1)  # زر "لون الدفتر"
        
        await asyncio.sleep(3)
        
        # 4. جلب نفس الرسالة بعد التعديل (نفس المعرف)
        msg1 = await l313l.get_messages(TARGET_BOT, ids=msg_id)
        if not msg1 or not msg1.buttons:
            return False
        
        # 5. الضغط على الزر المطلوب
        await msg1.click(index)
        await asyncio.sleep(2)
        
        # 6. حذف المحادثة
        async for msg in l313l.iter_messages(TARGET_BOT, limit=10):
            await msg.delete()
        
        return True
        
    except Exception as e:
        print(f"خطأ: {e}")
        return False

# =========================================================== #
# نصوص القوائم
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
# قوائم الخطوط (عمودية)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"font_menu")))
async def font_menu(event):
    buttons = []
    for i, font in enumerate(FONTS):
        buttons.append([Button.inline(font, data=f"set_font_{i}", style="primary")])
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(FONT_TEXT, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"text_color_menu")))
async def text_color_menu(event):
    buttons = []
    for i, color in enumerate(TEXT_COLORS):
        buttons.append([Button.inline(color, data=f"set_text_color_{i}", style="primary")])
    buttons.append([Button.inline("🔙 رجوع", data="back_to_main", style="danger")])
    await event.edit(TEXT_COLOR_TEXT, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"note_color_menu")))
async def note_color_menu(event):
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
    
    success = await apply_setting_immediately('font', index)
    
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
    
    success = await apply_setting_immediately('text_color', index)
    
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
    
    success = await apply_setting_immediately('note_color', index)
    
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
    
    font_index = FONTS.index(font) if font in FONTS else 0
    color_index = TEXT_COLORS.index(text_color) if text_color in TEXT_COLORS else 0
    note_index = NOTE_COLORS.index(note_color) if note_color in NOTE_COLORS else 0
    
    try:
        # إرسال /start
        await l313l.send_message(TARGET_BOT, '/start')
        await asyncio.sleep(3)
        
        # القائمة الرئيسية
        msg = await l313l.get_messages(TARGET_BOT, limit=1)
        if not msg or not msg[0].buttons:
            return await jokevent.edit("❌ لم يتم استلام القائمة الرئيسية")
        
        msg_id = msg[0].id
        
        # تغيير نوع الخط
        await msg[0].click(0)
        await asyncio.sleep(3)
        
        msg = await l313l.get_messages(TARGET_BOT, ids=msg_id)
        if msg and msg.buttons:
            await msg.click(font_index)
            await asyncio.sleep(2)
        
        # تغيير لون الخط
        msg = await l313l.get_messages(TARGET_BOT, ids=msg_id)
        if msg and msg.buttons:
            await msg.click(2)
            await asyncio.sleep(3)
            
            msg = await l313l.get_messages(TARGET_BOT, ids=msg_id)
            if msg and msg.buttons:
                await msg.click(color_index)
                await asyncio.sleep(2)
        
        # تغيير لون الدفتر
        msg = await l313l.get_messages(TARGET_BOT, ids=msg_id)
        if msg and msg.buttons:
            await msg.click(1)
            await asyncio.sleep(3)
            
            msg = await l313l.get_messages(TARGET_BOT, ids=msg_id)
            if msg and msg.buttons:
                await msg.click(note_index)
                await asyncio.sleep(2)
        
        # إرسال النص
        await l313l.send_message(TARGET_BOT, text)
        await asyncio.sleep(4)
        
        # جلب الصورة
        response = await l313l.get_messages(TARGET_BOT, limit=1)
        
        if response and (response[0].photo or response[0].document):
            end = datetime.now()
            ms = (end - start).seconds
            
            await event.client.send_file(
                event.chat_id,
                response[0].media,
                caption=f"**📸 تم إنشاء دفترك!**\n⏰ **الوقت:** `{ms} ثانية`\n\n**📝 النص:** `{text[:50]}...`\n\n**⚙️ الإعدادات:**\n• الخط: `{font}`\n• لون الخط: `{text_color}`\n• لون الدفتر: `{note_color}`"
            )
            await jokevent.delete()
            
            # حذف المحادثة
            async for m in l313l.iter_messages(TARGET_BOT, limit=15):
                await m.delete()
        else:
            await jokevent.edit(f"**❌ لم يتم استلام صورة من البوت**")
                
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")
