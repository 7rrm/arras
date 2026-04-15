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
        [Button.inline("❌ إغلاق", data="close_test", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

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
        [Button.inline("⬅️ رجوع للألوان", data="test_main", style="primary")],
        [Button.inline("❌ إغلاق", data="close_test", style="danger")]
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
        [Button.inline("⬅️ رجوع للألوان", data="test_main", style="primary")],
        [Button.inline("❌ إغلاق", data="close_test", style="danger")]
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
        [Button.inline("⬅️ رجوع للألوان", data="test_main", style="primary")],
        [Button.inline("❌ إغلاق", data="close_test", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# الخيارات الداخلية (مع ألوان مختلفة)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"red_option_1")))
@check_owner
async def red_option_1(event):
    text = "**🔴 لقد ضغطت على الخيار الأحمر 1**"
    buttons = [[Button.inline("⬅️ رجوع", data="red_menu", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"red_option_2")))
@check_owner
async def red_option_2(event):
    text = "**🔴 لقد ضغطت على الخيار الأحمر 2**"
    buttons = [[Button.inline("⬅️ رجوع", data="red_menu", style="danger")]]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"green_option_1")))
@check_owner
async def green_option_1(event):
    text = "**🟢 لقد ضغطت على الخيار الأخضر 1**"
    buttons = [[Button.inline("⬅️ رجوع", data="green_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"green_option_2")))
@check_owner
async def green_option_2(event):
    text = "**🟢 لقد ضغطت على الخيار الأخضر 2**"
    buttons = [[Button.inline("⬅️ رجوع", data="green_menu", style="success")]]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"blue_option_1")))
@check_owner
async def blue_option_1(event):
    text = "**🔵 لقد ضغطت على الخيار الأزرق 1**"
    buttons = [[Button.inline("⬅️ رجوع", data="blue_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"blue_option_2")))
@check_owner
async def blue_option_2(event):
    text = "**🔵 لقد ضغطت على الخيار الأزرق 2**"
    buttons = [[Button.inline("⬅️ رجوع", data="blue_menu", style="primary")]]
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# إغلاق
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"close_test")))
@check_owner
async def close_test(event):
    await event.delete()
