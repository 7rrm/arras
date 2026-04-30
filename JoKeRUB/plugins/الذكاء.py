# =========================================================== #
# ملف: groq_ai.py
# كود Groq AI - نسخة مصلحة بدون أخطاء
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

# الإعدادات الافتراضية
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 1.0

# تخزين إعدادات كل مستخدم
groq_user_model = {}
groq_user_temp = {}
groq_user_conversations = {}

# =========================================================== #
# دوال مساعدة مع معالجة الأخطاء
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
# دالة الرد من Groq مع معالجة الأخطاء
# =========================================================== #
async def get_groq_response(user_id, question):
    try:
        model = get_user_model(user_id)
        temp = get_user_temp(user_id)
        
        # إدارة سجل المحادثة
        if user_id not in groq_user_conversations:
            groq_user_conversations[user_id] = []
        
        # إضافة سؤال المستخدم
        groq_user_conversations[user_id].append({
            "role": "user",
            "content": question
        })
        
        # الاحتفاظ بآخر 8 رسائل فقط
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
            
            # التحقق من وجود البيانات المطلوبة
            if result and "choices" in result and len(result["choices"]) > 0:
                if "message" in result["choices"][0] and "content" in result["choices"][0]["message"]:
                    answer = result["choices"][0]["message"]["content"]
                    
                    # حفظ رد المساعد
                    groq_user_conversations[user_id].append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    return answer
                else:
                    return "⚠️ **تنسيق رد غير متوقع من الخادم**"
            else:
                return "⚠️ **تنسيق رد غير متوقع من الخادم**"
                
        elif response.status_code == 429:
            return "⚠️ **تم تجاوز حد الطلبات** (1000 طلب/يوم). حاول لاحقاً."
        else:
            error_text = f"⚠️ **خطأ {response.status_code}:** تحقق من المفتاح أو النموذج"
            try:
                error_data = response.json()
                if error_data and "error" in error_data:
                    error_text += f"\n{error_data['error'].get('message', '')}"
            except:
                pass
            return error_text
            
    except requests.exceptions.Timeout:
        return "⚠️ **انتهى الوقت** - لم يستجب الخادم، حاول مرة أخرى."
    except requests.exceptions.ConnectionError:
        return "⚠️ **خطأ في الاتصال** - تأكد من اتصالك بالإنترنت"
    except Exception as e:
        LOGS.error(f"خطأ في get_groq_response: {traceback.format_exc()}")
        return f"⚠️ **حدث خطأ:** {str(e)[:150]}"

# =========================================================== #
# عرض الإعدادات الرئيسية
# =========================================================== #
async def show_main_settings(event, edit_mode=False):
    try:
        user_id = event.sender_id if hasattr(event, 'sender_id') else event.sender_id
        
        model_name = get_user_model(user_id)
        model_desc = get_model_desc(model_name)
        temp = get_user_temp(user_id)
        conv_count = len(groq_user_conversations.get(user_id, []))
        
        temp_names = {
            0.0: "بارد جداً ❄️", 0.3: "بارد 🧊", 0.5: "معتدل 🌤️",
            0.7: "دافئ ☀️", 1.0: "طبيعي ⚖️", 1.2: "إبداعي 🎨",
            1.5: "مبدع جداً ✨", 1.7: "عشوائي 🎲", 2.0: "جنوني 🤪"
        }
        
        text = f"**🤖 إعدادات Groq AI**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
        text += f"**📌 النموذج:**\n{model_desc}\n\n"
        text += f"**🌡️ الحرارة:** `{temp}` - {temp_names.get(temp, 'طبيعي ⚖️')}\n\n"
        text += f"**💬 السجل:** {conv_count} رسالة\n\n"
        text += f"**⎉╎اختر ما تريد تغييره:**"
        
        buttons = [
            [Button.inline("🎛️ تغيير النموذج", b"groq_show_models")],
            [Button.inline("🌡️ تغيير الحرارة", b"groq_show_temp")],
            [Button.inline("🗑️ مسح السجل", b"groq_clear_chat")],
            [Button.inline("❌ إغلاق", b"groq_close")]
        ]
        
        if edit_mode and hasattr(event, 'edit'):
            await event.edit(text, buttons=buttons)
        else:
            return text, buttons
    except Exception as e:
        LOGS.error(f"خطأ في show_main_settings: {e}")
        if edit_mode and hasattr(event, 'edit'):
            await event.edit("**❌ حدث خطأ في عرض الإعدادات**")

# =========================================================== #
# عرض قائمة النماذج
# =========================================================== #
async def show_models_menu(event, edit_mode=False):
    try:
        buttons = []
        model_list = list(GROQ_MODELS.items())
        
        for i in range(0, len(model_list), 3):
            row = []
            for j in range(i, min(i+3, len(model_list))):
                key, model = model_list[j]
                row.append(Button.inline(f"{key} 📌", f"groq_model_{key}".encode()))
            buttons.append(row)
        
        buttons.append([Button.inline("🔙 رجوع", b"groq_back_to_settings")])
        
        text = "**🎛️ اختيار النموذج:**\n⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n\n"
        text += "**⚠️ ملاحظة:** تغيير النموذج سيؤدي إلى مسح سجل المحادثة\n\n"
        text += "**⎉╎النموذج الحالي:**\n"
        model_name = get_user_model(event.sender_id)
        model_desc = get_model_desc(model_name)
        text += f"• {model_desc}\n"
        
        if edit_mode and hasattr(event, 'edit'):
            await event.edit(text, buttons=buttons)
        else:
            return text, buttons
    except Exception as e:
        LOGS.error(f"خطأ في show_models_menu: {e}")

# =========================================================== #
# عرض قائمة درجات الحرارة
# =========================================================== #
async def show_temp_menu(event, edit_mode=False):
    try:
        temp_values = [0.0, 0.3, 0.5, 0.7, 1.0, 1.2, 1.5, 1.7, 2.0]
        temp_names = {
            0.0: "بارد جداً ❄️", 0.3: "بارد 🧊", 0.5: "معتدل 🌤️",
            0.7: "دافئ ☀️", 1.0: "طبيعي ⚖️", 1.2: "إبداعي 🎨",
            1.5: "مبدع جداً ✨", 1.7: "عشوائي 🎲", 2.0: "جنوني 🤪"
        }
        
        buttons = []
        row = []
        for i, temp in enumerate(temp_values):
            row.append(Button.inline(f"{temp_names[temp]}", f"groq_temp_{temp}".encode()))
            if len(row) == 3:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline("🔙 رجوع", b"groq_back_to_settings")])
        
        current_temp = get_user_temp(event.sender_id)
        
        text = "**🌡️ اختيار درجة الحرارة:**\n⋆┄─┄─┄─┄─┄─┄─┄┄⋆\n\n"
        text += f"**⎉╎الحرارة الحالية:** `{current_temp}`\n"
        text += f"**⎉╎الوصف:** {temp_names.get(current_temp, 'طبيعي ⚖️')}\n\n"
        text += "**⎉╎اختر الدرجة المناسبة:**"
        
        if edit_mode and hasattr(event, 'edit'):
            await event.edit(text, buttons=buttons)
        else:
            return text, buttons
    except Exception as e:
        LOGS.error(f"خطأ في show_temp_menu: {e}")

# =========================================================== #
# الأمر الرئيسي
# =========================================================== #
@l313l.ar_cmd(pattern="جروك(?: |$)(.*)")
async def groq_chat(event):
    try:
        question = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        
        # إذا لم يوجد سؤال، نعرض الإعدادات
        if not question and not reply_msg:
            zzz = await edit_or_reply(event, "**✧╎جـارِ تجهيز الإعدادات ...**")
            await show_main_settings(zzz, True)
            return
        
        # أمر الإعدادات
        if question and question.strip() in ["الاعدادات", "settings"]:
            zzz = await edit_or_reply(event, "**✧╎جـارِ تجهيز الإعدادات ...**")
            await show_main_settings(zzz, True)
            return
        
        # جلب السؤال من الرد
        if not question and reply_msg and reply_msg.text:
            question = reply_msg.text
        
        if not question:
            return await edit_or_reply(event, 
                "**✧╎🤖 Groq AI - الذكاء الاصطناعي**\n"
                "**⎉╎للرد على سؤال:** `.جروك نص السؤال`\n"
                "**⎉╎أو الرد على رسالة بـ:** `.جروك`\n"
                "**⎉╎للإعدادات:** `.جروك الاعدادات`\n"
                "**⎉╎لمسح السجل:** `.جروك مسح`")
        
        # أمر مسح السجل
        if question.strip() in ["مسح", "حذف", "clear"]:
            clear_user_conversation(event.sender_id)
            return await edit_or_reply(event, 
                "**✧╎🗑️ تم حذف سجل المحادثة بنجاح ✅**\n"
                "**⎉╎يمكنك الآن البدء من جديد**")
        
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
            f"**⎉╎للتغيير:** `.جروك الاعدادات`",
            link_preview=False
        )
    except Exception as e:
        LOGS.error(f"خطأ في groq_chat: {traceback.format_exc()}")
        await edit_or_reply(event, f"**❌ حدث خطأ: {str(e)[:100]}**")

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
            
            # رجوع للإعدادات الرئيسية
            if data == "groq_back_to_settings":
                await show_main_settings(event, True)
                await event.answer()
                return
            
            # إغلاق القائمة
            if data == "groq_close":
                await event.edit("**❌ تم إغلاق الإعدادات**")
                await event.answer()
                return
            
            # عرض قائمة النماذج
            if data == "groq_show_models":
                await show_models_menu(event, True)
                await event.answer()
                return
            
            # عرض قائمة الحرارة
            if data == "groq_show_temp":
                await show_temp_menu(event, True)
                await event.answer()
                return
            
            # مسح السجل
            if data == "groq_clear_chat":
                clear_user_conversation(event.sender_id)
                await event.answer("✅ تم مسح سجل المحادثة!", alert=True)
                await show_main_settings(event, True)
                return
            
            # اختيار نموذج جديد
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
                await show_main_settings(event, True)
                return
            
            # اختيار درجة حرارة جديدة
            if data.startswith("groq_temp_"):
                temp_value = float(data.replace("groq_temp_", ""))
                old_temp = get_user_temp(event.sender_id)
                if temp_value != old_temp:
                    save_user_temp(event.sender_id, temp_value)
                    await event.answer(f"✅ تم تغيير درجة الحرارة إلى: {temp_value}", alert=True)
                else:
                    await event.answer("ℹ️ هذه هي درجة الحرارة الحالية", alert=True)
                await show_main_settings(event, True)
                return
                
        except Exception as e:
            LOGS.error(f"خطأ في groq_callback: {traceback.format_exc()}")
            try:
                await event.answer(f"❌ خطأ: {str(e)[:50]}", alert=True)
            except:
                pass
