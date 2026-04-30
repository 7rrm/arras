import asyncio
import contextlib
import re
import random
import time
import os
import requests
from datetime import datetime

from telethon import Button, events
from telethon.events import CallbackQuery
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest

from . import StartTime, l313l, mention
from ..core import check_owner
from ..Config import Config
from ..utils import Zed_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus


# =========================================================== #
# إعدادات Groq المتقدمة - بالأزرار (نسخة بدون تعارض)
# =========================================================== #

import requests
import json
from telethon import Button
from telethon.events import CallbackQuery

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# =========================================================== #
# النماذج المتاحة
# =========================================================== #
GROQ_MODELS = {
    "1": {"name": "openai/gpt-oss-120b", "desc": "GPT-OSS 120B - نموذج متقدم"},
    "2": {"name": "openai/gpt-oss-20b", "desc": "GPT-OSS 20B - أسرع وأخف"},
    "3": {"name": "llama-3.3-70b-versatile", "desc": "Llama 3.3 70B - قوي من Meta"},
    "4": {"name": "llama-3.1-8b-instant", "desc": "Llama 3.1 8B - سريع جداً"},
    "5": {"name": "mixtral-8x7b-32768", "desc": "Mixtral 8x7B - سياق طويل"},
    "6": {"name": "mistral-saba-24b", "desc": "Mistral Saba - ممتاز بالعربية ⭐"},
    "7": {"name": "gemma2-9b-it", "desc": "Gemma 2 9B - من Google"},
}

# الإعدادات الافتراضية
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 1.0

# تخزين إعدادات كل مستخدم
user_groq_settings = {}
user_groq_conversations = {}

# =========================================================== #
# دوال مساعدة
# =========================================================== #
def get_user_settings(user_id):
    if user_id not in user_groq_settings:
        user_groq_settings[user_id] = {
            "model": DEFAULT_MODEL,
            "temperature": DEFAULT_TEMPERATURE
        }
    return user_groq_settings[user_id]

def save_user_settings(user_id, settings):
    user_groq_settings[user_id] = settings

# =========================================================== #
# دالة الرد من Groq
# =========================================================== #
async def get_groq_response(user_id, question):
    try:
        settings = get_user_settings(user_id)
        
        if user_id not in user_groq_conversations:
            user_groq_conversations[user_id] = []
        
        user_groq_conversations[user_id].append({
            "role": "user",
            "content": question
        })
        
        if len(user_groq_conversations[user_id]) > 10:
            user_groq_conversations[user_id] = user_groq_conversations[user_id][-10:]
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": settings["model"],
            "messages": user_groq_conversations[user_id],
            "temperature": settings["temperature"],
            "max_tokens": 2000,
            "stream": False
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            user_groq_conversations[user_id].append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
        else:
            return f"⚠️ خطأ {response.status_code}"
            
    except Exception as e:
        return f"⚠️ خطأ: {str(e)[:100]}"

# =========================================================== #
# عرض قائمة النماذج (أزرار)
# =========================================================== #
async def show_models_menu(event, user_id, page=0):
    items_per_page = 3
    model_keys = list(GROQ_MODELS.keys())
    total_pages = (len(model_keys) + items_per_page - 1) // items_per_page
    
    if page >= total_pages:
        page = 0
    if page < 0:
        page = total_pages - 1
    
    start = page * items_per_page
    end = min(start + items_per_page, len(model_keys))
    
    settings = get_user_settings(user_id)
    current_model = settings["model"]
    
    text = "**🎛️ النماذج المتاحة:**\n\n"
    for key in model_keys[start:end]:
        model = GROQ_MODELS[key]
        mark = " ✅" if current_model == model["name"] else ""
        text += f"**{key}** - {model['desc']}{mark}\n"
    
    text += f"\n📄 الصفحة {page + 1}/{total_pages}"
    
    buttons = []
    nav_buttons = []
    
    if page > 0:
        nav_buttons.append(Button.inline("◀️ رجوع", data=f"models_page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(Button.inline("التالي ▶️", data=f"models_page_{page+1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    
    model_buttons = []
    for key in model_keys[start:end]:
        model_buttons.append(Button.inline(GROQ_MODELS[key]["desc"][:20], data=f"select_model_{key}"))
    if model_buttons:
        buttons.append(model_buttons)
    
    buttons.append([Button.inline("◀️ رجوع للقائمة", data="back_to_main")])
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# عرض القائمة الرئيسية
# =========================================================== #
async def show_main_menu(event, user_id):
    settings = get_user_settings(user_id)
    
    current_model_name = "غير معروف"
    for key, model in GROQ_MODELS.items():
        if model["name"] == settings["model"]:
            current_model_name = model["desc"]
            break
    
    text = f"**🤖 إعدادات Groq AI**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**📌 النموذج:** {current_model_name}\n"
    text += f"**🌡️ درجة الحرارة:** {settings['temperature']}\n\n"
    text += f"**💬 عدد رسائل السجل:** {len(user_groq_conversations.get(user_id, []))}\n\n"
    text += "**⎉╎اختر الإعداد الذي تريد تغييره:**"
    
    buttons = [
        [Button.inline("🎛️ تغيير النموذج", data="show_models")],
        [Button.inline("🌡️ تغيير درجة الحرارة", data="temp_menu")],
        [Button.inline("🗑️ مسح المحادثة", data="clear_chat")],
        [Button.inline("❌ إغلاق", data="close_panel")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# قائمة درجة الحرارة
# =========================================================== #
async def show_temp_menu(event, user_id):
    settings = get_user_settings(user_id)
    
    text = f"**🌡️ تغيير درجة الحرارة**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**القيمة الحالية:** `{settings['temperature']}`\n\n"
    text += "**المدى المسموح:** 0.0 إلى 2.0\n\n"
    text += "**الوصف:**\n"
    
    if settings['temperature'] <= 0.5:
        text += "• ردود ثابتة ومتوقعة\n"
    elif settings['temperature'] <= 1.5:
        text += "• ردود متوسطة الإبداع\n"
    else:
        text += "• ردود عشوائية وإبداعية\n"
    
    buttons = [
        [Button.inline("❄️ 0.5 (ثابت)", data="set_temp_0.5"),
         Button.inline("⚖️ 1.0 (وسط)", data="set_temp_1.0")],
        [Button.inline("🔥 1.5 (إبداعي)", data="set_temp_1.5"),
         Button.inline("🎲 2.0 (عشوائي)", data="set_temp_2.0")],
        [Button.inline("◀️ رجوع", data="back_to_main")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# الأمر الرئيسي لفتح الإعدادات
# =========================================================== #
@l313l.ar_cmd(pattern="اعدادات جروك$")
async def groq_settings_cmd(event):
    user_id = event.sender_id
    settings = get_user_settings(user_id)
    
    current_model_name = "غير معروف"
    for key, model in GROQ_MODELS.items():
        if model["name"] == settings["model"]:
            current_model_name = model["desc"]
            break
    
    text = f"**🤖 إعدادات Groq AI**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**📌 النموذج:** {current_model_name}\n"
    text += f"**🌡️ درجة الحرارة:** {settings['temperature']}\n\n"
    text += "**⎉╎اختر الإعداد الذي تريد تغييره:**"
    
    buttons = [
        [Button.inline("🎛️ تغيير النموذج", data="show_models")],
        [Button.inline("🌡️ تغيير درجة الحرارة", data="temp_menu")],
        [Button.inline("🗑️ مسح المحادثة", data="clear_chat")],
        [Button.inline("❌ إغلاق", data="close_panel")]
    ]
    
    await event.reply(text, buttons=buttons, parse_mode="Markdown")
    await event.delete()

# =========================================================== #
# أمر المحادثة الرئيسي
# =========================================================== #
@l313l.ar_cmd(pattern="جروك(?: |$)(.*)")
async def groq_chat(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, 
            "**✧╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n"
            "**مثال:** `.جروك من انت`\n\n"
            "**⚙️ للإعدادات:** `.اعدادات جروك`")
    
    if not question and event.reply_to_msg_id and zzz.text:
        question = zzz.text
    
    zed = await edit_or_reply(event, "**✧╎جـارِ الاتصـال بـ Groq AI ...**")
    
    answer = await get_groq_response(event.sender_id, question)
    
    settings = get_user_settings(event.sender_id)
    model_short = settings["model"].split("/")[-1]
    
    await zed.edit(
        f"ᯓ **Groq AI** - الذكاء الاصطناعي\n"
        f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
        f"**• سؤال:** {question[:150]}\n\n"
        f"**• جواب:** {answer}\n"
        f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
        f"**⎉╎النموذج:** `{model_short}`\n"
        f"**⎉╎الحرارة:** `{settings['temperature']}`\n"
        f"**⎉╎للإعدادات:** `.اعدادات جروك`",
        link_preview=False
    )

# =========================================================== #
# معالج الأزرار (CallbackQuery)
# =========================================================== #
@l313l.tgbot.on(CallbackQuery(data=b"show_models"))
async def on_show_models(event):
    user_id = event.query.user_id
    await show_models_menu(event, user_id, 0)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"models_page_(\d+)")))
async def on_models_page(event):
    user_id = event.query.user_id
    page = int(event.data.decode().split("_")[-1])
    await show_models_menu(event, user_id, page)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"select_model_(\d+)")))
async def on_select_model(event):
    user_id = event.query.user_id
    model_key = event.data.decode().split("_")[-1]
    
    if model_key in GROQ_MODELS:
        settings = get_user_settings(user_id)
        settings["model"] = GROQ_MODELS[model_key]["name"]
        save_user_settings(user_id, settings)
        user_groq_conversations[user_id] = []
        await event.answer(f"✅ تم تغيير النموذج إلى: {GROQ_MODELS[model_key]['desc']}", alert=True)
    
    await show_main_menu(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=b"temp_menu"))
async def on_temp_menu(event):
    user_id = event.query.user_id
    await show_temp_menu(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"set_temp_(\d+(?:\.\d+)?)")))
async def on_set_temp(event):
    user_id = event.query.user_id
    temp_value = float(event.data.decode().split("_")[-1])
    
    if 0 <= temp_value <= 2:
        settings = get_user_settings(user_id)
        settings["temperature"] = temp_value
        save_user_settings(user_id, settings)
        await event.answer(f"✅ تم تغيير درجة الحرارة إلى {temp_value}", alert=True)
    
    await show_main_menu(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=b"clear_chat"))
async def on_clear_chat(event):
    user_id = event.query.user_id
    user_groq_conversations[user_id] = []
    await event.answer("✅ تم مسح سجل المحادثة!", alert=True)
    await show_main_menu(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=b"back_to_main"))
async def on_back_to_main(event):
    user_id = event.query.user_id
    await show_main_menu(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=b"close_panel"))
async def on_close_panel(event):
    await event.edit("❌ تم إغلاق القائمة", buttons=None)
