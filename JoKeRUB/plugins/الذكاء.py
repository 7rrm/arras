# =========================================================== #
# ملف: groq_ai.py
# كود Groq AI - نظام متكامل بالأزرار عبر Inline Query
# =========================================================== #

import asyncio
import requests
import json
import re
import traceback

from telethon import Button, events
from telethon.errors import FloodWaitError
from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import l313l, Config

LOGS = logging.getLogger(__name__)
plugin_category = "الذكاء الاصطناعي"

# =========================================================== #
# إعدادات Groq API
# =========================================================== #
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# =========================================================== #
# جميع النماذج المتاحة
# =========================================================== #
GROQ_MODELS = {
    "1": {"name": "openai/gpt-oss-120b", "desc": "GPT-OSS 120B - متقدم من OpenAI"},
    "2": {"name": "openai/gpt-oss-20b", "desc": "GPT-OSS 20B - أسرع وأخف"},
    "3": {"name": "llama-3.3-70b-versatile", "desc": "Llama 3.3 70B - قوي من Meta"},
    "4": {"name": "llama-3.1-8b-instant", "desc": "Llama 3.1 8B - سريع جداً"},
    "5": {"name": "mixtral-8x7b-32768", "desc": "Mixtral 8x7B - سياق 32K"},
    "6": {"name": "meta-llama/llama-4-scout-17b-16e-instruct", "desc": "Llama 4 Scout 17B - احدث نموذج"},
    "7": {"name": "meta-llama/llama-4-maverick-17b-128e-instruct", "desc": "Llama 4 Maverick 17B - متقدم"},
    "8": {"name": "qwen/qwen3-32b", "desc": "Qwen 3 32B - استدلال قوي"},
    "9": {"name": "qwen/qwen3-14b", "desc": "Qwen 3 14B - نسخة متوسطة"},
    "10": {"name": "qwen/qwen3-8b", "desc": "Qwen 3 8B - سريع"},
    "11": {"name": "moonshotai/kimi-k2-instruct-0905", "desc": "Kimi K2 - سياق 262K"},
    "12": {"name": "deepseek-r1-distill-llama-70b", "desc": "DeepSeek R1 - استدلال"},
    "13": {"name": "mistral-saba-24b", "desc": "Mistral Saba - ممتاز للعربية ⭐"},
    "14": {"name": "allam-2-7b", "desc": "ALLaM 2 7B - نموذج عربي"},
    "15": {"name": "gemma2-9b-it", "desc": "Gemma 2 9B - من Google"},
    "16": {"name": "groq/compound", "desc": "Compound - بحث ويب"},
    "17": {"name": "groq/compound-mini", "desc": "Compound Mini - خفيف"},
}

# درجات الحرارة
TEMPERATURE_VALUES = [0.0, 0.3, 0.5, 0.7, 1.0, 1.2, 1.5, 1.7, 2.0]
TEMPERATURE_NAMES = {
    0.0: "بارد جداً ❄️", 0.3: "بارد 🧊", 0.5: "معتدل 🌤️",
    0.7: "دافئ ☀️", 1.0: "طبيعي ⚖️", 1.2: "إبداعي 🎨",
    1.5: "مبدع جداً ✨", 1.7: "عشوائي 🎲", 2.0: "جنوني 🤪"
}

# الإعدادات الافتراضية
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 1.0

# تخزين إعدادات كل مستخدم
groq_user_model = {}
groq_user_temp = {}
groq_user_conversations = {}

# =========================================================== #
# دوال مساعدة
# =========================================================== #
def get_user_model(user_id):
    try:
        return groq_user_model.get(user_id, DEFAULT_MODEL)
    except Exception:
        return DEFAULT_MODEL

def get_user_temp(user_id):
    try:
        return groq_user_temp.get(user_id, DEFAULT_TEMPERATURE)
    except Exception:
        return DEFAULT_TEMPERATURE

def save_user_model(user_id, model):
    try:
        groq_user_model[user_id] = model
    except Exception as e:
        LOGS.error(f"خطأ في حفظ النموذج: {e}")

def save_user_temp(user_id, temp):
    try:
        groq_user_temp[user_id] = temp
    except Exception as e:
        LOGS.error(f"خطأ في حفظ الحرارة: {e}")

def clear_user_conversation(user_id):
    try:
        if user_id in groq_user_conversations:
            groq_user_conversations[user_id] = []
    except Exception as e:
        LOGS.error(f"خطأ في مسح السجل: {e}")

def get_model_desc(model_name):
    try:
        for key, model in GROQ_MODELS.items():
            if model.get("name") == model_name:
                return model.get("desc", model_name)
        return model_name
    except Exception:
        return model_name

# =========================================================== #
# دالة الرد من Groq
# =========================================================== #
async def get_groq_response(user_id, question):
    try:
        model = get_user_model(user_id)
        temp = get_user_temp(user_id)
        
        if user_id not in groq_user_conversations:
            groq_user_conversations[user_id] = []
        
        groq_user_conversations[user_id].append({
            "role": "user",
            "content": question
        })
        
        if len(groq_user_conversations[user_id]) > 8:
            groq_user_conversations[user_id] = groq_user_conversations[user_id][-8:]
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": groq_user_conversations[user_id],
            "temperature": temp,
            "max_tokens": 2000,
            "top_p": 1,
            "stream": False
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result and "choices" in result and len(result["choices"]) > 0:
                if "message" in result["choices"][0] and "content" in result["choices"][0]["message"]:
                    answer = result["choices"][0]["message"]["content"]
                    
                    groq_user_conversations[user_id].append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    return answer
                else:
                    return "⚠️ **تنسيق رد غير متوقع**"
            else:
                return "⚠️ **تنسيق رد غير متوقع**"
                
        elif response.status_code == 429:
            return "⚠️ **تم تجاوز حد الطلبات** (1000 طلب/يوم)"
        else:
            return f"⚠️ **خطأ {response.status_code}:** تحقق من المفتاح"
            
    except requests.exceptions.Timeout:
        return "⚠️ **انتهى الوقت** - حاول مرة أخرى"
    except Exception as e:
        LOGS.error(f"خطأ: {traceback.format_exc()}")
        return f"⚠️ **حدث خطأ:** {str(e)[:100]}"

# =========================================================== #
# الأوامر
# =========================================================== #

# أمر اعدادات جروك
@l313l.ar_cmd(pattern="اعدادات جروك$")
async def groq_settings_cmd(event):
    """عرض إعدادات Groq AI"""
    if Config.TG_BOT_USERNAME:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_settings")
        await response[0].click(event.chat_id)
        await event.delete()
    else:
        await edit_or_reply(event, "**- يرجى تعيين متغير TG_BOT_USERNAME اولا**")

# أمر جروك الرئيسي
@l313l.ar_cmd(pattern="جروك(?: |$)(.*)")
async def groq_chat(event):
    try:
        question = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        
        # إذا لم يوجد سؤال
        if not question and not reply_msg:
            return await edit_or_reply(event, 
                "**✧╎🤖 Groq AI - الذكاء الاصطناعي**\n"
                "**⎉╎للرد على سؤال:** `.جروك نص السؤال`\n"
                "**⎉╎أو الرد على رسالة بـ:** `.جروك`\n"
                "**⎉╎للإعدادات:** `.اعدادات جروك`\n"
                "**⎉╎لمسح السجل:** `.جروك مسح`")
        
        # أمر مسح السجل
        if question and question.strip() in ["مسح", "حذف", "clear"]:
            clear_user_conversation(event.sender_id)
            return await edit_or_reply(event, "**✧╎🗑️ تم حذف سجل المحادثة بنجاح ✅**")
        
        # جلب السؤال من الرد
        if not question and reply_msg and reply_msg.text:
            question = reply_msg.text
        
        if not question:
            return await edit_or_reply(event, "**❌ يرجى كتابة سؤال أو الرد على رسالة**")
        
        # الرد على السؤال
        zed = await edit_or_reply(event, "**✧╎🤔 جـارِ التفكير ...**")
        
        answer = await get_groq_response(event.sender_id, question)
        
        model = get_user_model(event.sender_id)
        temp = get_user_temp(event.sender_id)
        model_short = model.split("/")[-1].replace("-", " ").title()
        
        await zed.edit(
            f"**🤖 Groq AI**\n⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n\n"
            f"**• السؤال:** {question[:200]}\n\n"
            f"**• الجواب:** {answer}\n"
            f"⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n"
            f"**⎉╎النموذج:** `{model_short}`\n"
            f"**⎉╎الحرارة:** `{temp}`\n"
            f"**⎉╎للتغيير:** `.اعدادات جروك`",
            link_preview=False
        )
            
    except Exception as e:
        LOGS.error(f"خطأ: {traceback.format_exc()}")
        await edit_or_reply(event, f"**❌ حدث خطأ:** {str(e)[:100]}")

# =========================================================== #
# نظام Inline Query
# =========================================================== #
if Config.TG_BOT_USERNAME is not None and hasattr(l313l, 'tgbot') and l313l.tgbot is not None:

    @l313l.tgbot.on(events.InlineQuery)
    async def inline_handler_groq(event):
        builder = event.builder
        query = event.text
        
        # ✅ استعلام grokk_settings - القائمة الرئيسية
        if query.startswith("grokk_settings") and event.query.user_id == l313l.uid:
            user_id = event.query.user_id
            model_desc = get_model_desc(get_user_model(user_id))
            temp = get_user_temp(user_id)
            conv_count = len(groq_user_conversations.get(user_id, []))
            
            text = f"**🤖 إعدادات Groq AI**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
            text += f"**📌 النموذج:**\n{model_desc}\n\n"
            text += f"**🌡️ الحرارة:** `{temp}` - {TEMPERATURE_NAMES.get(temp, 'طبيعي ⚖️')}\n\n"
            text += f"**💬 السجل:** {conv_count} رسالة\n\n"
            text += f"**⎉╎اختر ما تريد تغييره:**"
            
            buttons = [
                [Button.inline("🎛️ النموذج", data="groq_show_models")],
                [Button.inline("🌡️ الحرارة", data="groq_show_temp")],
                [Button.inline("🗑️ السجل", data="groq_show_chat")],
                [Button.inline("❌ إغلاق", data="groq_close")]
            ]
            
            result = builder.article(
                title="🎛️ إعدادات Groq AI",
                text=text,
                buttons=buttons,
                parse_mode="md"
            )
            await event.answer([result])
            return
        
        # ✅ استعلام grokk_models - قائمة النماذج
        if query.startswith("grokk_models") and event.query.user_id == l313l.uid:
            buttons = []
            
            buttons.append([Button.inline("1 - GPT-OSS 120B (متقدم)", data="groq_model_1")])
            buttons.append([Button.inline("2 - GPT-OSS 20B (سريع)", data="groq_model_2")])
            buttons.append([Button.inline("3 - Llama 3.3 70B (قوي)", data="groq_model_3")])
            buttons.append([Button.inline("4 - Llama 3.1 8B (سريع جداً)", data="groq_model_4")])
            buttons.append([Button.inline("5 - Mixtral 8x7B (سياق طويل)", data="groq_model_5")])
            buttons.append([Button.inline("6 - Llama 4 Scout 17B", data="groq_model_6")])
            buttons.append([Button.inline("7 - Llama 4 Maverick 17B", data="groq_model_7")])
            buttons.append([Button.inline("8 - Qwen 3 32B (استدلال)", data="groq_model_8")])
            buttons.append([Button.inline("9 - Qwen 3 14B (متوسط)", data="groq_model_9")])
            buttons.append([Button.inline("10 - Qwen 3 8B (سريع)", data="groq_model_10")])
            buttons.append([Button.inline("11 - Kimi K2 (سياق 262K)", data="groq_model_11")])
            buttons.append([Button.inline("12 - DeepSeek R1 (استدلال)", data="groq_model_12")])
            buttons.append([Button.inline("13 - Mistral Saba (عربي ⭐)", data="groq_model_13")])
            buttons.append([Button.inline("14 - ALLaM 2 7B (عربي)", data="groq_model_14")])
            buttons.append([Button.inline("15 - Gemma 2 9B (Google)", data="groq_model_15")])
            buttons.append([Button.inline("16 - Compound (بحث ويب)", data="groq_model_16")])
            buttons.append([Button.inline("17 - Compound Mini (خفيف)", data="groq_model_17")])
            buttons.append([Button.inline("🔙 رجوع", data="groq_back_main")])
            
            text = f"**🎛️ اختيار النموذج:**\n⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n\n"
            text += "**⚠️ ملاحظة:** تغيير النموذج سيؤدي إلى مسح سجل المحادثة\n\n"
            text += f"**⎉╎النموذج الحالي:**\n{get_model_desc(get_user_model(event.query.user_id))}"
            
            result = builder.article(
                title="🎛️ تغيير النموذج",
                text=text,
                buttons=buttons,
                parse_mode="md"
            )
            await event.answer([result])
            return
        
        # ✅ استعلام grokk_temp - قائمة الحرارة
        if query.startswith("grokk_temp") and event.query.user_id == l313l.uid:
            buttons = []
            
            buttons.append([Button.inline("0.0 - بارض جداً ❄️", data="groq_temp_0.0")])
            buttons.append([Button.inline("0.3 - بارد 🧊", data="groq_temp_0.3")])
            buttons.append([Button.inline("0.5 - معتدل 🌤️", data="groq_temp_0.5")])
            buttons.append([Button.inline("0.7 - دافئ ☀️", data="groq_temp_0.7")])
            buttons.append([Button.inline("1.0 - طبيعي ⚖️", data="groq_temp_1.0")])
            buttons.append([Button.inline("1.2 - إبداعي 🎨", data="groq_temp_1.2")])
            buttons.append([Button.inline("1.5 - مبدع جداً ✨", data="groq_temp_1.5")])
            buttons.append([Button.inline("1.7 - عشوائي 🎲", data="groq_temp_1.7")])
            buttons.append([Button.inline("2.0 - جنوني 🤪", data="groq_temp_2.0")])
            buttons.append([Button.inline("🔙 رجوع", data="groq_back_main")])
            
            current_temp = get_user_temp(event.query.user_id)
            
            text = f"**🌡️ اختيار درجة الحرارة:**\n⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n\n"
            text += f"**⎉╎الحرارة الحالية:** `{current_temp}`\n"
            text += f"**⎉╎الوصف:** {TEMPERATURE_NAMES.get(current_temp, 'طبيعي ⚖️')}\n\n"
            text += "**⎉╎اختر الدرجة المناسبة:**"
            
            result = builder.article(
                title="🌡️ تغيير درجة الحرارة",
                text=text,
                buttons=buttons,
                parse_mode="md"
            )
            await event.answer([result])
            return
        
        # ✅ استعلام grokk_chat - قائمة السجل
        if query.startswith("grokk_chat") and event.query.user_id == l313l.uid:
            user_id = event.query.user_id
            conv_count = len(groq_user_conversations.get(user_id, []))
            
            buttons = [
                [Button.inline("🗑️ حذف السجل", data="groq_clear_chat")],
                [Button.inline("🔙 رجوع", data="groq_back_main")]
            ]
            
            text = f"**🗑️ إدارة السجل:**\n⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n\n"
            text += f"**⎉╎عدد الرسائل في السجل:** `{conv_count}` رسالة\n\n"
            
            if conv_count > 0:
                text += "**⎉╎سيتم حذف جميع رسائل المحادثة السابقة**\n"
                text += "**⎉╎لن يتمكن الـ AI من تذكر السياق السابق**"
            else:
                text += "**⎉╎السجل فارغ حالياً**"
            
            result = builder.article(
                title="🗑️ إدارة السجل",
                text=text,
                buttons=buttons,
                parse_mode="md"
            )
            await event.answer([result])
            return

# =========================================================== #
# معالجة الأزرار
# =========================================================== #
if Config.TG_BOT_USERNAME is not None and hasattr(l313l, 'tgbot') and l313l.tgbot is not None:

    @l313l.tgbot.on(events.CallbackQuery)
    async def groq_callback(event):
        try:
            if not event.data:
                return
            
            data = event.data.decode() if isinstance(event.data, bytes) else event.data
            
            # الرجوع للقائمة الرئيسية
            if data == "groq_back_main":
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_settings")
                await response[0].click(event.chat_id)
                await event.answer()
                return
            
            # إغلاق
            if data == "groq_close":
                await event.edit("**❌ تم إغلاق الإعدادات**")
                await event.answer()
                return
            
            # عرض قائمة النماذج
            if data == "groq_show_models":
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_models")
                await response[0].click(event.chat_id)
                await event.answer()
                return
            
            # عرض قائمة الحرارة
            if data == "groq_show_temp":
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_temp")
                await response[0].click(event.chat_id)
                await event.answer()
                return
            
            # عرض قائمة السجل
            if data == "groq_show_chat":
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_chat")
                await response[0].click(event.chat_id)
                await event.answer()
                return
            
            # حذف السجل
            if data == "groq_clear_chat":
                clear_user_conversation(event.sender_id)
                await event.answer("✅ تم حذف سجل المحادثة!", alert=True)
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_settings")
                await response[0].click(event.chat_id)
                return
            
            # اختيار نموذج
            if data.startswith("groq_model_"):
                model_key = data.replace("groq_model_", "")
                if model_key in GROQ_MODELS:
                    new_model = GROQ_MODELS[model_key]["name"]
                    old_model = get_user_model(event.sender_id)
                    if new_model != old_model:
                        save_user_model(event.sender_id, new_model)
                        clear_user_conversation(event.sender_id)
                        await event.answer(f"✅ تم تغيير النموذج إلى:\n{GROQ_MODELS[model_key]['desc']}", alert=True)
                    else:
                        await event.answer("ℹ️ هذا هو النموذج الحالي بالفعل", alert=True)
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_settings")
                await response[0].click(event.chat_id)
                return
            
            # اختيار درجة حرارة
            if data.startswith("groq_temp_"):
                temp_value = float(data.replace("groq_temp_", ""))
                old_temp = get_user_temp(event.sender_id)
                if temp_value != old_temp:
                    save_user_temp(event.sender_id, temp_value)
                    await event.answer(f"✅ تم تغيير درجة الحرارة إلى: {temp_value}", alert=True)
                else:
                    await event.answer("ℹ️ هذه هي درجة الحرارة الحالية", alert=True)
                response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk_settings")
                await response[0].click(event.chat_id)
                return
                
        except Exception as e:
            LOGS.error(f"خطأ: {traceback.format_exc()}")
            try:
                await event.answer(f"❌ خطأ: {str(e)[:50]}", alert=True)
            except:
                pass
