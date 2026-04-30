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
# إعدادات Groq - النماذج والإعدادات
# =========================================================== #

from groq import Groq
import json

# =========================================================== #
# تهيئة عميل Groq
# =========================================================== #
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

# =========================================================== #
# قائمة النماذج المتاحة في Groq (17 نموذجاً)
# =========================================================== #
GROQ_MODELS = {
    # 🤖 نماذج الإنتاج
    "1": {"name": "openai/gpt-oss-120b", "desc": "GPT-OSS 120B - نموذج متقدم من OpenAI"},
    "2": {"name": "openai/gpt-oss-20b", "desc": "GPT-OSS 20B - نسخة أسرع وأخف"},
    "3": {"name": "llama-3.3-70b-versatile", "desc": "Llama 3.3 70B - نموذج قوي من Meta"},
    "4": {"name": "llama-3.1-8b-instant", "desc": "Llama 3.1 8B - سريع جداً"},
    "5": {"name": "mixtral-8x7b-32768", "desc": "Mixtral 8x7B - سياق طويل 32K"},
    
    # 🎯 نماذج معاينة
    "6": {"name": "meta-llama/llama-4-scout-17b-16e-instruct", "desc": "Llama 4 Scout 17B - أحدث نماذج Meta"},
    "7": {"name": "meta-llama/llama-4-maverick-17b-128e-instruct", "desc": "Llama 4 Maverick 17B - متقدم"},
    "8": {"name": "qwen/qwen3-32b", "desc": "Qwen 3 32B - استدلال قوي"},
    "9": {"name": "qwen/qwen3-14b", "desc": "Qwen 3 14B - نسخة متوسطة"},
    "10": {"name": "qwen/qwen3-8b", "desc": "Qwen 3 8B - نسخة سريعة"},
    "11": {"name": "moonshotai/kimi-k2-instruct-0905", "desc": "Kimi K2 - سياق عملاق 262K رمز"},
    "12": {"name": "deepseek-r1-distill-llama-70b", "desc": "DeepSeek R1 - استدلال متقدم"},
    "13": {"name": "mistral-saba-24b", "desc": "Mistral Saba - ممتاز للغة العربية ⭐"},
    "14": {"name": "allam-2-7b", "desc": "ALLaM 2 7B - نموذج عربي"},
    "15": {"name": "gemma2-9b-it", "desc": "Gemma 2 9B - من Google"},
    
    # 🛠️ الأنظمة المتكاملة
    "16": {"name": "groq/compound", "desc": "Compound - نظام متكامل بحث ويب"},
    "17": {"name": "groq/compound-mini", "desc": "Compound Mini - نسخة أخف"},
}

# الإعدادات الافتراضية
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
DEFAULT_GROQ_TEMPERATURE = 1.0
DEFAULT_GROQ_MAX_TOKENS = 2000

# قاموس لتخزين محادثات المستخدمين (سياق المحادثة لكل مستخدم)
user_groq_conversations = {}

# =========================================================== #
# دوال مساعدة
# =========================================================== #

def get_user_groq_settings(user_id):
    """الحصول على إعدادات Groq للمستخدم"""
    settings_json = gvarstatus(f"GROQ_SETTINGS_{user_id}")
    if settings_json:
        return json.loads(settings_json)
    return {
        "model": DEFAULT_GROQ_MODEL,
        "temperature": DEFAULT_GROQ_TEMPERATURE,
        "max_tokens": DEFAULT_GROQ_MAX_TOKENS
    }

def save_user_groq_settings(user_id, settings):
    """حفظ إعدادات Groq للمستخدم"""
    addgvar(f"GROQ_SETTINGS_{user_id}", json.dumps(settings))

def clear_user_conversation(user_id):
    """مسح سجل محادثة المستخدم"""
    if user_id in user_groq_conversations:
        user_groq_conversations[user_id] = []

async def get_groq_response(user_id, question):
    """الحصول على رد من Groq"""
    try:
        settings = get_user_groq_settings(user_id)
        
        # إدارة سجل المحادثة
        if user_id not in user_groq_conversations:
            user_groq_conversations[user_id] = []
        
        # إضافة سؤال المستخدم
        user_groq_conversations[user_id].append({
            "role": "user",
            "content": question
        })
        
        # الاحتفاظ بآخر 10 رسائل فقط
        if len(user_groq_conversations[user_id]) > 10:
            user_groq_conversations[user_id] = user_groq_conversations[user_id][-10:]
        
        # استدعاء Groq API
        completion = groq_client.chat.completions.create(
            model=settings["model"],
            messages=user_groq_conversations[user_id],
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"],
            top_p=1,
            stream=False
        )
        
        answer = completion.choices[0].message.content
        
        # حفظ رد المساعد
        user_groq_conversations[user_id].append({
            "role": "assistant",
            "content": answer
        })
        
        return answer
        
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            return "⚠️ **تم تجاوز حد الطلبات** (1000 طلب/يوم). الرجاء المحاولة لاحقاً."
        elif "does not exist" in error_msg.lower():
            return "⚠️ **النموذج غير متاح**. استخدم `.اعدادات جروك` لتغيير النموذج."
        elif "Request too large" in error_msg:
            # مسح المحادثة تلقائياً عند تجاوز الحد
            clear_user_conversation(user_id)
            return "⚠️ **تم تجاوز حد الرموز.**\n\nتم مسح سجل المحادثة تلقائياً. أعد إرسال سؤالك."
        return f"⚠️ **حدث خطأ:** {error_msg[:150]}"

# =========================================================== #
# تحديث قائمة النماذج (واجهة تفاعلية)
# =========================================================== #

async def update_models_message(event, user_id, page=0):
    """تحديث رسالة النماذج مع أزرار التنقل"""
    model_keys = list(GROQ_MODELS.keys())
    items_per_page = 4  # عدد النماذج في كل صفحة
    total_pages = (len(model_keys) + items_per_page - 1) // items_per_page
    
    if page >= total_pages:
        page = 0
    if page < 0:
        page = total_pages - 1
    
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(model_keys))
    current_keys = model_keys[start_idx:end_idx]
    
    settings = get_user_groq_settings(user_id)
    current_model = settings["model"]
    
    # بناء النص
    text = f"**🤖 إعدادات Groq AI**\n"
    text += f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**🌡️ درجة الحرارة:** `{settings['temperature']}`\n"
    text += f"**📝 الحد الأقصى:** `{settings['max_tokens']}` رمز\n\n"
    text += f"**📋 النماذج المتاحة (الصفحة {page + 1}/{total_pages}):**\n"
    
    for key in current_keys:
        model = GROQ_MODELS[key]
        current = " ✅" if current_model == model["name"] else ""
        text += f"\n`{key}` - {model['desc']}{current}"
    
    # بناء الأزرار
    buttons = []
    
    # أزرار التنقل بين الصفحات
    nav_buttons = []
    if page > 0:
        nav_buttons.append(Button.inline("◀️ السابق", data=f"groq_models_page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(Button.inline("التالي ▶️", data=f"groq_models_page_{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    
    # أزرار النماذج في الصفحة الحالية
    model_buttons = []
    for key in current_keys:
        model_buttons.append(Button.inline(f"{key}", data=f"groq_select_model_{key}"))
    if model_buttons:
        buttons.append(model_buttons)
    
    # أزرار التحكم العامة
    buttons.append([
        Button.inline("🌡️ تغيير الحرارة", data="groq_temp_settings"),
        Button.inline("🗑️ مسح المحادثة", data="groq_clear_chat")
    ])
    buttons.append([
        Button.inline("📖 نموذج الاستخدام", data="groq_info"),
        Button.inline("❌ إغلاق", data="close_panel")
    ])
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

async def update_temp_message(event, user_id):
    """تحديث رسالة تغيير درجة الحرارة"""
    settings = get_user_groq_settings(user_id)
    
    text = f"**🌡️ تغيير درجة الحرارة**\n"
    text += f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**القيمة الحالية:** `{settings['temperature']}`\n\n"
    text += f"**المدى المسموح:** 0.0 إلى 2.0\n\n"
    text += f"**الوصف:**\n"
    if settings['temperature'] <= 0.5:
        text += f"• ردود ثابتة ومتوقعة\n"
    elif settings['temperature'] <= 1.5:
        text += f"• ردود متوسطة الإبداع\n"
    else:
        text += f"• ردود عشوائية وإبداعية جداً\n\n"
    
    text += f"**⎉╎أرسل القيمة الجديدة (0.0 - 2.0)**"
    
    buttons = [
        [Button.inline("🔽 0.5", data="groq_set_temp_0.5"),
         Button.inline("⚖️ 1.0", data="groq_set_temp_1.0"),
         Button.inline("🔼 1.5", data="groq_set_temp_1.5")],
        [Button.inline("🔄 عشوائي 2.0", data="groq_set_temp_2.0")],
        [Button.inline("◀️ رجوع", data="groq_back_to_main")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# أوامر المستخدم
# =========================================================== #

@l313l.ar_cmd(pattern="اعدادات جروك(?: |$)(.*)")
async def groq_settings_cmd(event):
    """إظهار إعدادات Groq"""
    # استخدام الاستعلام المضمن مثل كليشات الايدي
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "groq_settings")
    if response:
        await response[0].click(event.chat_id)
        await event.delete()
    else:
        await event.reply("❌ لا يمكن فتح الإعدادات حالياً")

@l313l.ar_cmd(pattern="جروك(?: |$)(.*)")
async def groq_chat_cmd(event):
    """الرد على الأسئلة باستخدام Groq"""
    global user_groq_conversations
    
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    
    # التحقق من وجود سؤال
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, 
            "**✧╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n"
            "**⌔╎مثـــال :**\n"
            "`.جروك من هو مكتشف الجاذبية الارضية`\n\n"
            "**⚙️ للإعدادات:** `.اعدادات جروك`")
    
    # جلب السؤال من الرد
    if not question and event.reply_to_msg_id and zzz.text: 
        question = zzz.text
    
    if not event.reply_to_msg_id: 
        question = event.pattern_match.group(1)
    
    # أمر مسح السجل الخاص
    if question == "مسح" or question == "حذف":
        clear_user_conversation(event.sender_id)
        return await edit_or_reply(event, 
            "**✧╎تم حذف سجل الذكاء الاصطناعي .. بنجاح ✅**\n"
            "**⎉╎ارسـل الان(.جروك + سؤالك) لـ البـدء من جديد**")
    
    # إرسال رسالة جاري المعالجة
    zed = await edit_or_reply(event, 
        "**✧╎جـارِ الاتصـال بـ Groq AI**\n"
        "**⎉╎الرجـاء الانتظـار .. لحظـات**")
    
    # الحصول على الإجابة
    answer = await get_groq_response(event.sender_id, question)
    
    if answer:
        settings = get_user_groq_settings(event.sender_id)
        await zed.edit(
            f"ᯓ 𝗚𝗿𝗼𝗾 𝗔𝗜 -💡- **الذكاء الاصطناعي**\n"
            f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
            f"**• س/ {question[:100]}**\n\n"
            f"**• ج/ {answer}**\n\n"
            f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
            f"**⎉╎النموذج:** `{settings['model'].split('/')[-1]}`\n"
            f"**⎉╎الحرارة:** `{settings['temperature']}`\n"
            f"**⎉╎للإعدادات:** `.اعدادات جروك`\n"
            f"**⎉╎لمسح السجل:** `.جروك مسح`",
            link_preview=False
        )

# =========================================================== #
# الاستعلامات المضمنة لواجهة الإعدادات
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler_groq(event):
        query = event.text
        user_id = event.query.user_id
        
        # ✅ استعلام إعدادات Groq
        if query.startswith("groq_settings") and user_id == l313l.uid:
            user_id = event.query.user_id
            settings = get_user_groq_settings(user_id)
            
            text = f"**🤖 إعدادات Groq AI**\n"
            text += f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
            
            # معرفة النموذج الحالي
            current_model_name = "غير معروف"
            for key, model in GROQ_MODELS.items():
                if model["name"] == settings["model"]:
                    current_model_name = model["desc"]
                    break
            
            text += f"**📌 النموذج الحالي:**\n`{current_model_name}`\n\n"
            text += f"**🌡️ درجة الحرارة:** `{settings['temperature']}`\n"
            text += f"**📝 الحد الأقصى:** `{settings['max_tokens']}` رمز\n\n"
            text += f"**💬 إجمالي المحادثات:** {len(user_groq_conversations.get(user_id, []))} رسالة\n\n"
            text += f"**⎉╎يمكنك تغيير الإعدادات من الأزرار أدناه**"
            
            buttons = [
                [Button.inline("🎛️ النماذج", data="groq_show_models"),
                 Button.inline("🌡️ الحرارة", data="groq_temp_settings")],
                [Button.inline("🗑️ مسح المحادثة", data="groq_clear_chat"),
                 Button.inline("📖 معلومات", data="groq_info")],
                [Button.inline("❌ إغلاق", data="close_panel")]
            ]
            
            result = builder.article(
                title="🤖 إعدادات Groq AI",
                description=f"النموذج: {current_model_name} | الحرارة: {settings['temperature']}",
                text=text,
                buttons=buttons,
                link_preview=False,
                parse_mode="Markdown",
            )
            await event.answer([result], cache_time=0)

# =========================================================== #
# أزرار التفاعل (CallbackQuery) لإعدادات Groq
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_show_models")))
async def groq_show_models(event):
    """عرض قائمة النماذج"""
    user_id = event.query.user_id
    await update_models_message(event, user_id, page=0)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_models_page_(\\d+)")))
async def groq_models_page(event):
    """التنقل بين صفحات النماذج"""
    match = re.match(rb"groq_models_page_(\\d+)", event.data)
    if match:
        page = int(match.group(1).decode())
        user_id = event.query.user_id
        await update_models_message(event, user_id, page)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_select_model_(\\d+)")))
async def groq_select_model(event):
    """اختيار نموذج معين"""
    match = re.match(rb"groq_select_model_(\\d+)", event.data)
    if match:
        model_key = match.group(1).decode()
        user_id = event.query.user_id
        
        if model_key in GROQ_MODELS:
            settings = get_user_groq_settings(user_id)
            settings["model"] = GROQ_MODELS[model_key]["name"]
            save_user_groq_settings(user_id, settings)
            # مسح المحادثة عند تغيير النموذج
            clear_user_conversation(user_id)
            
            await event.answer(f"✅ تم تغيير النموذج إلى: {GROQ_MODELS[model_key]['desc']}", alert=True)
            # العودة إلى قائمة النماذج
            await update_models_message(event, user_id, page=0)
        else:
            await event.answer("❌ نموذج غير موجود!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_temp_settings")))
async def groq_temp_settings(event):
    """إظهار إعدادات درجة الحرارة"""
    user_id = event.query.user_id
    await update_temp_message(event, user_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_set_temp_(\\d+(?:\\.\\d+)?)")))
async def groq_set_temp(event):
    """تعيين درجة حرارة جديدة"""
    match = re.match(rb"groq_set_temp_(\\d+(?:\\.\\d+)?)", event.data)
    if match:
        temp_value = float(match.group(1).decode())
        user_id = event.query.user_id
        
        if 0 <= temp_value <= 2:
            settings = get_user_groq_settings(user_id)
            settings["temperature"] = temp_value
            save_user_groq_settings(user_id, settings)
            await event.answer(f"✅ تم تغيير درجة الحرارة إلى {temp_value}", alert=True)
            # العودة إلى الإعدادات الرئيسية
            await groq_show_main_menu(event)
        else:
            await event.answer("❌ القيمة يجب أن تكون بين 0 و 2!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_clear_chat")))
async def groq_clear_chat(event):
    """مسح سجل المحادثة"""
    user_id = event.query.user_id
    clear_user_conversation(user_id)
    await event.answer("✅ تم مسح سجل المحادثة بنجاح!", alert=True)
    await groq_show_main_menu(event)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_info")))
async def groq_info(event):
    """عرض معلومات عن Groq"""
    text = f"**ℹ️ معلومات Groq AI**\n"
    text += f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**⚡ السرعة:** حتى 1400 رمز/ثانية\n"
    text += f"**🎯 النماذج:** 17 نموذج مختلف\n"
    text += f"**🌐 الـ API:** مجاني (1000 طلب/يوم)\n\n"
    text += f"**📝 الأوامر:**\n"
    text += f"• `.جروك [سؤال]` - اسأل الذكاء الاصطناعي\n"
    text += f"• `.جروك مسح` - مسح سجل المحادثة\n"
    text += f"• `.اعدادات جروك` - فتح لوحة التحكم\n\n"
    text += f"**💡 ملاحظة:** البوت يتذكر آخر 10 رسائل للحفاظ على السياق"
    
    buttons = [[Button.inline("◀️ رجوع", data="groq_back_to_main")]]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"groq_back_to_main")))
async def groq_back_to_main(event):
    """العودة إلى القائمة الرئيسية"""
    user_id = event.query.user_id
    settings = get_user_groq_settings(user_id)
    
    # معرفة النموذج الحالي
    current_model_name = "غير معروف"
    for key, model in GROQ_MODELS.items():
        if model["name"] == settings["model"]:
            current_model_name = model["desc"]
            break
    
    text = f"**🤖 إعدادات Groq AI**\n"
    text += f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**📌 النموذج الحالي:**\n`{current_model_name}`\n\n"
    text += f"**🌡️ درجة الحرارة:** `{settings['temperature']}`\n"
    text += f"**📝 الحد الأقصى:** `{settings['max_tokens']}` رمز\n\n"
    text += f"**⎉╎يمكنك تغيير الإعدادات من الأزرار أدناه**"
    
    buttons = [
        [Button.inline("🎛️ النماذج", data="groq_show_models"),
         Button.inline("🌡️ الحرارة", data="groq_temp_settings")],
        [Button.inline("🗑️ مسح المحادثة", data="groq_clear_chat"),
         Button.inline("📖 معلومات", data="groq_info")],
        [Button.inline("❌ إغلاق", data="close_panel")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# دالة لعرض القائمة الرئيسية
async def groq_show_main_menu(event):
    """عرض القائمة الرئيسية"""
    user_id = event.query.user_id
    settings = get_user_groq_settings(user_id)
    
    # معرفة النموذج الحالي
    current_model_name = "غير معروف"
    for key, model in GROQ_MODELS.items():
        if model["name"] == settings["model"]:
            current_model_name = model["desc"]
            break
    
    text = f"**🤖 إعدادات Groq AI**\n"
    text += f"⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"**📌 النموذج الحالي:**\n`{current_model_name}`\n\n"
    text += f"**🌡️ درجة الحرارة:** `{settings['temperature']}`\n"
    text += f"**📝 الحد الأقصى:** `{settings['max_tokens']}` رمز\n\n"
    text += f"**⎉╎يمكنك تغيير الإعدادات من الأزرار أدناه**"
    
    buttons = [
        [Button.inline("🎛️ النماذج", data="groq_show_models"),
         Button.inline("🌡️ الحرارة", data="groq_temp_settings")],
        [Button.inline("🗑️ مسح المحادثة", data="groq_clear_chat"),
         Button.inline("📖 معلومات", data="groq_info")],
        [Button.inline("❌ إغلاق", data="close_panel")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")
