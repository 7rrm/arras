# =========================================================== #
# كود Groq الكامل - مع أزرار تفاعلية
# =========================================================== #

import requests
import json
import re
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# =========================================================== #
# جميع النماذج المتاحة (17 نموذج)
# =========================================================== #
GROQ_MODELS = {
    "1": {"name": "openai/gpt-oss-120b", "desc": "GPT-OSS 120B - نموذج متقدم من OpenAI"},
    "2": {"name": "openai/gpt-oss-20b", "desc": "GPT-OSS 20B - نسخة أسرع وأخف"},
    "3": {"name": "llama-3.3-70b-versatile", "desc": "Llama 3.3 70B - نموذج قوي من Meta"},
    "4": {"name": "llama-3.1-8b-instant", "desc": "Llama 3.1 8B - سريع جداً"},
    "5": {"name": "mixtral-8x7b-32768", "desc": "Mixtral 8x7B - سياق طويل 32K"},
    "6": {"name": "meta-llama/llama-4-scout-17b-16e-instruct", "desc": "Llama 4 Scout 17B - أحدث نماذج Meta"},
    "7": {"name": "meta-llama/llama-4-maverick-17b-128e-instruct", "desc": "Llama 4 Maverick 17B - متقدم"},
    "8": {"name": "qwen/qwen3-32b", "desc": "Qwen 3 32B - استدلال قوي"},
    "9": {"name": "qwen/qwen3-14b", "desc": "Qwen 3 14B - نسخة متوسطة"},
    "10": {"name": "qwen/qwen3-8b", "desc": "Qwen 3 8B - نسخة سريعة"},
    "11": {"name": "moonshotai/kimi-k2-instruct-0905", "desc": "Kimi K2 - سياق عملاق 262K رمز"},
    "12": {"name": "deepseek-r1-distill-llama-70b", "desc": "DeepSeek R1 - استدلال متقدم"},
    "13": {"name": "mistral-saba-24b", "desc": "Mistral Saba - ممتاز للغة العربية"},
    "14": {"name": "allam-2-7b", "desc": "ALLaM 2 7B - نموذج عربي"},
    "15": {"name": "gemma2-9b-it", "desc": "Gemma 2 9B - من Google"},
    "16": {"name": "groq/compound", "desc": "Compound - نظام متكامل (بحث ويب)"},
    "17": {"name": "groq/compound-mini", "desc": "Compound Mini - نسخة أخف"},
}

# الإعدادات الافتراضية
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 1.0

# تخزين إعدادات كل مستخدم
user_model = {}
user_temp = {}
user_conversations = {}

# =========================================================== #
# دوال مساعدة
# =========================================================== #
def get_user_model(user_id):
    return user_model.get(user_id, DEFAULT_MODEL)

def get_user_temp(user_id):
    return user_temp.get(user_id, DEFAULT_TEMPERATURE)

def save_user_model(user_id, model):
    user_model[user_id] = model

def save_user_temp(user_id, temp):
    user_temp[user_id] = temp

def clear_user_conversation(user_id):
    if user_id in user_conversations:
        user_conversations[user_id] = []

# =========================================================== #
# دالة الرد من Groq مع السياق
# =========================================================== #
async def get_groq_response(user_id, question):
    try:
        model = get_user_model(user_id)
        temp = get_user_temp(user_id)
        
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        
        user_conversations[user_id].append({
            "role": "user",
            "content": question
        })
        
        if len(user_conversations[user_id]) > 8:
            user_conversations[user_id] = user_conversations[user_id][-8:]
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": user_conversations[user_id],
            "temperature": temp,
            "max_tokens": 2000,
            "top_p": 1,
            "stream": False
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            user_conversations[user_id].append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
        elif response.status_code == 429:
            return "⚠️ تم تجاوز حد الطلبات (1000 طلب/يوم). الرجاء المحاولة لاحقاً."
        else:
            return f"⚠️ خطأ {response.status_code}: تحقق من المفتاح أو النموذج"
            
    except Exception as e:
        return f"⚠️ حدث خطأ: {str(e)[:150]}"

# =========================================================== #
# الاستعلام المضمن (grokk)
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_grokk_handler(event):
        builder = event.builder
        query = event.text
        
        if query.startswith("grokk") and event.query.user_id == l313l.uid:
            buttons = [
                [Button.inline("النموذج", data="groq_models_menu", style="primary")],
                [Button.inline("الحرارة", data="groq_temp_menu", style="primary")],
                [Button.inline("السجل", data="groq_logs_menu", style="primary")],
                [Button.inline("إغلاق", data="groq_close", style="danger")]
            ]
            
            await event.answer(
                [await builder.article(
                    title="إعدادات الذكاء الاصطناعي",
                    description="تخصيص الذكاء الاصطناعي",
                    text="**اعدادات الذكاء الاصطناعي**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\nاختر الإعداد الذي تريد تغييره:",
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )

# =========================================================== #
# قائمة النماذج (مع وصف كل نموذج وأزرار 5 في سطر)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_models_menu")))
@check_owner
async def groq_models_menu(event):
    models_text = "**جميع النماذج المتاحة في Groq:**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    for key, model in GROQ_MODELS.items():
        models_text += f"**{key}** - {model['desc']}\n"
    models_text += "\n**اختر النموذج الذي تريده:**"
    
    buttons = []
    row = []
    for key in GROQ_MODELS.keys():
        row.append(Button.inline(f"{key}", data=f"groq_set_model_{key}", style="primary"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([Button.inline("رجوع", data="groq_back_to_main", style="danger")])
    await event.edit(models_text, buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_set_model_(\\d+)")))
@check_owner
async def groq_set_model(event):
    model_key = event.data_match.group(1).decode()
    user_id = event.query.user_id
    model_name = GROQ_MODELS[model_key]["name"]
    model_desc = GROQ_MODELS[model_key]["desc"]
    
    save_user_model(user_id, model_name)
    clear_user_conversation(user_id)
    
    await event.answer(f"✅ تم تغيير النموذج إلى: {model_desc}", alert=True)
    await groq_back_to_main(event)

# =========================================================== #
# قائمة الحرارة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_temp_menu")))
@check_owner
async def groq_temp_menu(event):
    current_temp = get_user_temp(event.query.user_id)
    
    buttons = [
        [Button.inline(f"{'✅ ' if current_temp == 0 else ''}0.0 - ثابت", data="groq_set_temp_0.0", style="primary")],
        [Button.inline(f"{'✅ ' if current_temp == 0.5 else ''}0.5 - منخفض", data="groq_set_temp_0.5", style="primary")],
        [Button.inline(f"{'✅ ' if current_temp == 1.0 else ''}1.0 - متوسط", data="groq_set_temp_1.0", style="primary")],
        [Button.inline(f"{'✅ ' if current_temp == 1.5 else ''}1.5 - إبداعي", data="groq_set_temp_1.5", style="primary")],
        [Button.inline(f"{'✅ ' if current_temp == 2.0 else ''}2.0 - عشوائي", data="groq_set_temp_2.0", style="primary")],
        [Button.inline("رجوع", data="groq_back_to_main", style="danger")]
    ]
    
    await event.edit("**اختر درجة الحرارة:**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
                     f"**الحرارة الحالية:** `{current_temp}`\n\n"
                     "0.0 = ردود ثابتة ومتوقعة\n"
                     "1.0 = ردود متوسطة الإبداع\n"
                     "2.0 = ردود عشوائية وإبداعية جداً",
                     buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_set_temp_(.*)")))
@check_owner
async def groq_set_temp(event):
    temp_value = float(event.data_match.group(1).decode())
    user_id = event.query.user_id
    
    save_user_temp(user_id, temp_value)
    
    await event.answer(f"✅ تم تغيير درجة الحرارة إلى: {temp_value}", alert=True)
    await groq_back_to_main(event)

# =========================================================== #
# قائمة السجل
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_logs_menu")))
@check_owner
async def groq_logs_menu(event):
    user_id = event.query.user_id
    conv_count = len(user_conversations.get(user_id, []))
    
    buttons = [
        [Button.inline("حذف السجل", data="groq_clear_logs", style="danger")],
        [Button.inline("رجوع", data="groq_back_to_main", style="primary")]
    ]
    
    await event.edit(f"**إدارة سجل المحادثة**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
                     f"**عدد الرسائل المحفوظة:** `{conv_count}`\n\n"
                     f"**الضغط على 'حذف السجل' سيمسح جميع رسائلك السابقة**",
                     buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_clear_logs")))
@check_owner
async def groq_clear_logs(event):
    user_id = event.query.user_id
    clear_user_conversation(user_id)
    
    await event.answer("✅ تم حذف سجل المحادثة", alert=True)
    await groq_back_to_main(event)

# =========================================================== #
# الرجوع للقائمة الرئيسية
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_back_to_main")))
@check_owner
async def groq_back_to_main(event):
    buttons = [
        [Button.inline("النموذج", data="groq_models_menu", style="primary")],
        [Button.inline("الحرارة", data="groq_temp_menu", style="primary")],
        [Button.inline("السجل", data="groq_logs_menu", style="primary")],
        [Button.inline("إغلاق", data="groq_close", style="danger")]
    ]
    
    await event.edit("**اعدادات الذكاء الاصطناعي**\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\nاختر الإعداد الذي تريد تغييره:",
                     buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# إغلاق القائمة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_close")))
@check_owner
async def groq_close(event):
    await event.edit("**تم إغلاق القائمة**", buttons=None, parse_mode="Markdown")

# =========================================================== #
# أمر اعدادات الذكاء (بدلاً من اعدادات جروك)
# =========================================================== #

@l313l.ar_cmd(pattern="اعدادات الذكاء$")
async def groq_settings_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# الأمر الرئيسي للمحادثة
# =========================================================== #

@l313l.ar_cmd(pattern="ار(?: |$)(.*)")
async def groq_chat(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, 
            "**بالرد على سؤال او بإضافة السؤال للأمر**\n"
            "**مثال:** `.ار من انت`\n\n"
            "**الأوامر المتاحة:**\n"
            "• `.اعدادات الذكاء` - لوحة تحكم تفاعلية\n"
            "• `.ار مسح` - مسح سجل المحادثة")
    
    # جلب السؤال من الرد
    if not question and event.reply_to_msg_id and zzz.text:
        question = zzz.text
    
    # أمر مسح المحادثة
    if question == "مسح" or question == "حذف":
        clear_user_conversation(event.sender_id)
        return await edit_or_reply(event, 
            "**تم حذف سجل الذكاء الاصطناعي .. بنجاح**\n"
            "**ارسـل الان (.ار + سؤالك) لـ البـدء من جديد**")
    
    # الرد على السؤال
    zed = await edit_or_reply(event, "**جـارِ الاتصـال بـ الذكاء الاصطناعي ...**")
    
    answer = await get_groq_response(event.sender_id, question)
    
    model = get_user_model(event.sender_id)
    temp = get_user_temp(event.sender_id)
    model_short = model.split("/")[-1]
    
    await zed.edit(
        f"ᯓ 𝗔𝗥𝗔𝗦 𝗔𝗜 - **الذكـاء الأصطناعَـي**\n"
        f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
        f"**السؤال:** {question[:30]}\n\n"
        f"~~الجواب:~~ `{answer}`\n"
        f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
        f"**النموذج:** `{model_short}`",
        link_preview=False
    )
