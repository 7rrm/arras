import re
from telethon import Button, events
from telethon.events import CallbackQuery
import json
import requests
from ..core import check_owner
from ..Config import Config
from . import l313l

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("تجربة"):
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "🎨 القائمة الرئيسية",
                            "callback_data": "test_main",
                            "style": "primary"
                        }
                    ]
                ]
            }
            
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "test_1",
                        "title": "🧪 تجربة الألوان",
                        "description": "اضغط لرؤية الأزرار الملونة",
                        "input_message_content": {
                            "message_text": "**🎨 مرحباً بك في تجربة الألوان**\nاختر الزر المناسب👇",
                            "parse_mode": "Markdown"
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            try:
                requests.post(url, json=inline_data)
            except Exception as e:
                print(f"❌ خطأ: {e}")

@l313l.ar_cmd(pattern="تجربة$")
async def test_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "تجربة")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# القائمة الرئيسية (كلها ملونة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"test_main")))
@check_owner
async def test_main(event):
    text = "**🎨 القائمة الرئيسية - اختر لونك المفضل:**"
    
    buttons = [
        [Button.inline("🔴 أحمر", data="red_menu", style="danger")],
        [Button.inline("🟢 أخضر", data="green_menu", style="success")],
        [Button.inline("🔵 أزرق", data="blue_menu", style="primary")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# إخفاء الأزرار فقط (دون حذف الرسالة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"hide_buttons")))
@check_owner
async def hide_buttons(event):
    """إخفاء الأزرار فقط مع الاحتفاظ بالنص"""
    try:
        # الحصول على النص الحالي
        if hasattr(event, 'message') and event.message:
            current_text = event.message.text
        else:
            current_text = "**🎨 القائمة الرئيسية - اختر لونك المفضل:**"
        
        await event.edit(current_text, buttons=None, parse_mode="Markdown")
        await event.answer("✅ تم إخفاء الأزرار!", alert=True)
    except Exception as e:
        await event.answer(f"❌ خطأ: {str(e)}", alert=True)

# =========================================================== #
# حذف الرسالة بالكامل
# =========================================================== #
'''
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"delete_message")))
@check_owner
async def delete_message(event):
    """حذف الرسالة بالكامل"""
    try:
        await event.answer("🗑️ تم حذف الرسالة", alert=True)
        await event.client.delete_messages(event.chat_id, event.message_id)
    except Exception as e:
        await event.answer(f"❌ لا يمكن حذف هذه الرسالة: {str(e)}", alert=True)
'''
@l313l.tgbot.on(CallbackQuery(data=re.compile(b"delete_message")))
@check_owner
async def delete_message(event):
    """حذف الرسالة بالكامل - يتجنب الرسائل الخدمية"""
    try:
        # جلب الرسالة للتأكد من أنها ليست خدمية
        message = await event.client.get_messages(event.chat_id, ids=event.message_id)
        
        # التحقق: هل هي رسالة خدمية؟
        if message.action is not None:
            await event.answer("❌ لا يمكن حذف الرسائل الخدمية (مثل دخول عضو، تغيير صورة، إلخ)!", alert=True)
            return
        
        # حذف الرسالة
        await event.client.delete_messages(event.chat_id, [event.message_id])
        await event.answer("✅ تم حذف الرسالة!", alert=True)
        
    except Exception as e:
        error_msg = str(e)
        if "message can't be deleted" in error_msg.lower():
            await event.answer("❌ لا يمكن حذف هذه الرسالة (قد تكون خدمية أو قديمة جداً).", alert=True)
        else:
            await event.answer(f"❌ خطأ: {error_msg[:50]}", alert=True)
# =========================================================== #
# القائمة الحمراء
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"red_menu")))
@check_owner
async def red_menu(event):
    text = "**🔴 أنت في القائمة الحمراء**\nجميع الأزرار هنا حمراء!"
    
    buttons = [
        [Button.inline("خيار أحمر 1", data="red_option_1", style="danger")],
        [Button.inline("خيار أحمر 2", data="red_option_2", style="danger")],
        [Button.inline("⬅️ رجوع", data="test_main", style="primary")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# القائمة الخضراء
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"green_menu")))
@check_owner
async def green_menu(event):
    text = "**🟢 أنت في القائمة الخضراء**\nجميع الأزرار هنا خضراء!"
    
    buttons = [
        [Button.inline("خيار أخضر 1", data="green_option_1", style="success")],
        [Button.inline("خيار أخضر 2", data="green_option_2", style="success")],
        [Button.inline("⬅️ رجوع", data="test_main", style="primary")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# القائمة الزرقاء
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"blue_menu")))
@check_owner
async def blue_menu(event):
    text = "**🔵 أنت في القائمة الزرقاء**\nجميع الأزرار هنا زرقاء!"
    
    buttons = [
        [Button.inline("خيار أزرق 1", data="blue_option_1", style="primary")],
        [Button.inline("خيار أزرق 2", data="blue_option_2", style="primary")],
        [Button.inline("⬅️ رجوع", data="test_main", style="primary")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# الخيارات الداخلية
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"red_option_1")))
@check_owner
async def red_option_1(event):
    text = "**🔴 لقد ضغطت على الخيار الأحمر 1**"
    buttons = [
        [Button.inline("⬅️ رجوع", data="red_menu", style="danger")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"red_option_2")))
@check_owner
async def red_option_2(event):
    text = "**🔴 لقد ضغطت على الخيار الأحمر 2**"
    buttons = [
        [Button.inline("⬅️ رجوع", data="red_menu", style="danger")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"green_option_1")))
@check_owner
async def green_option_1(event):
    text = "**🟢 لقد ضغطت على الخيار الأخضر 1**"
    buttons = [
        [Button.inline("⬅️ رجوع", data="green_menu", style="success")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"green_option_2")))
@check_owner
async def green_option_2(event):
    text = "**🟢 لقد ضغطت على الخيار الأخضر 2**"
    buttons = [
        [Button.inline("⬅️ رجوع", data="green_menu", style="success")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"blue_option_1")))
@check_owner
async def blue_option_1(event):
    text = "**🔵 لقد ضغطت على الخيار الأزرق 1**"
    buttons = [
        [Button.inline("⬅️ رجوع", data="blue_menu", style="primary")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"blue_option_2")))
@check_owner
async def blue_option_2(event):
    text = "**🔵 لقد ضغطت على الخيار الأزرق 2**"
    buttons = [
        [Button.inline("⬅️ رجوع", data="blue_menu", style="primary")],
        [Button.inline("🗑️ إخفاء الأزرار", data="hide_buttons", style="primary")],
        [Button.inline("❌ حذف الرسالة", data="delete_message", style="danger")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")
