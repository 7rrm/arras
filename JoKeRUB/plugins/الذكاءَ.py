# =========================================================== #
# كود Groq الكامل - مع أزرار تفاعلية + DeepSeek + Claude
# =========================================================== #

import requests
import json
import re
import time
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

# استخدام المفتاح من متغيرات البيئة
GROQ_API_KEY = Config.GROQ_API_KEY
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# =========================================================== #
# إعدادات Firebase (لـ DeepSeek و Claude)
# =========================================================== #

FIREBASE_KEY = "AIzaSyA27E7jUV8osRY7NzwP2fZwGoTkp5gJhZw"
MULTI_SEARCH_URL = "https://ai-multi-search-backend-321697147922.europe-west6.run.app/ask"

FIREBASE_HEADERS = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 16; 2311DRK48G Build/BP2A.250605.031.A3)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/json",
    'X-Android-Package': "com.lmtechstudio.aimultisearch",
    'X-Android-Cert': "5D08264B44E0E53FBCCC70B4F016474CC6C5AB5C",
    'Accept-Language': "ar-EG, en-US",
    'X-Client-Version': "Android/Fallback/X23001000/FirebaseCore-Android",
    'X-Firebase-GMPID': "1:321697147922:android:26e6fb8e30dcc23dfffccb",
    'X-Firebase-Client': "H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA"
}

# تكوينات النماذج عبر Firebase
FIREBASE_CONFIG = {
    'deepseek': {
        "app_version": "1.2.8",
        "search_id": "f0a6705c-e33e-4288-a3ef-c91cd6564b59",
        "prompt_prefix": "Never reply in Chinese unless explicitly asked.\n"
    },
    'claude': {
        "app_version": "1.2.8",
        "search_id": "825a35c5-aac2-49d7-8317-5b7a68ae6cae",
        "prompt_prefix": ""
    }
}

firebase_token = None
firebase_token_expiry = 0

def get_firebase_token():
    global firebase_token, firebase_token_expiry
    if firebase_token and time.time() < firebase_token_expiry - 60:
        return firebase_token
    
    r = requests.post(
        "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser",
        params={'key': FIREBASE_KEY},
        data=json.dumps({"clientType": "CLIENT_TYPE_ANDROID"}),
        headers=FIREBASE_HEADERS
    )
    data = r.json()
    firebase_token = "Bearer " + data["idToken"]
    firebase_token_expiry = time.time() + int(data["expiresIn"])
    return firebase_token

def make_firebase_prompt(question, provider):
    """توليد الـ prompt المناسب لكل نموذج"""
    prefix = FIREBASE_CONFIG[provider].get("prompt_prefix", "")
    base = (
        "You MUST answer in the EXACT same language as the user question.\n"
        "Do NOT change language.\nDo NOT mix languages.\nDo NOT translate unless explicitly asked.\n\n"
        "Formatting rules:\n- No tables.\n- No markdown tables.\n- No ASCII tables.\n"
        "- Do NOT use pipe characters: |\n- Use clean bullet points or short paragraphs.\n\n"
        f"User question:\n{question}"
    )
    return (prefix + base) if prefix else base

async def get_firebase_response(question, provider):
    """الحصول على رد من النماذج عبر Firebase (DeepSeek أو Claude)"""
    try:
        current_token = get_firebase_token()
        cfg = FIREBASE_CONFIG[provider]
        
        payload = {
            "provider": provider,
            "prompt": make_firebase_prompt(question, provider),
            "plan": "ULTRA",
            "app_version": cfg["app_version"]
        }
        
        headers = {
            'User-Agent': "okhttp/4.12.0",
            'Accept-Encoding': "gzip",
            'authorization': current_token,
            'x-plan': "ULTRA",
            'x-app-version': cfg["app_version"],
            'x-search-id': cfg["search_id"],
            'x-search-expected': "2",
            'content-type': "application/json; charset=utf-8"
        }
        
        # ✅ استخدام stream=True
        response = requests.post(MULTI_SEARCH_URL, data=json.dumps(payload), headers=headers, timeout=90, stream=True)
        
        full_answer = ""
        
        # ✅ تجميع الأجزاء من التدفق
        for line in response.iter_lines():
            if line:
                try:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data = json.loads(line_str[6:])
                        if 'content' in data:
                            full_answer += data['content']
                        elif 'answer' in data:
                            full_answer += data['answer']
                except:
                    continue
        
        # ✅ لا تحاول قراءة response.json() مرة أخرى!
        if not full_answer:
            return f"⚠️ خطأ {provider}: لم يتم استلام رد"
        
        return full_answer
            
    except Exception as e:
        return f"⚠️ خطأ في الاتصال بـ {provider}: {str(e)[:100]}"

# =========================================================== #
# جميع النماذج المتاحة
# =========================================================== #
GROQ_MODELS = {
    # 🤖 OpenAI
    "1": {"name": "openai/gpt-oss-120b", "desc": "GPT-OSS 120B - نموذج متقدم من OpenAI"},
    "2": {"name": "openai/gpt-oss-20b", "desc": "GPT-OSS 20B - نسخة أسرع وأخف"},
    "3": {"name": "openai/gpt-oss-safeguard-20b", "desc": "GPT-OSS Safeguard - حماية المحتوى"},
    
    # 🦙 Meta
    "4": {"name": "llama-3.3-70b-versatile", "desc": "Llama 3.3 70B - نموذج قوي من Meta"},
    "5": {"name": "llama-3.1-8b-instant", "desc": "Llama 3.1 8B - سريع جداً"},
    "6": {"name": "meta-llama/llama-4-scout-17b-16e-instruct", "desc": "Llama 4 Scout 17B"},
    
    # 🛠️ Groq Systems
    "7": {"name": "groq/compound", "desc": "Compound - نظام متكامل (بحث ويب + كود)"},
    "8": {"name": "groq/compound-mini", "desc": "Compound Mini - نسخة أخف"},
    
    # ☁️ Alibaba Cloud
    "9": {"name": "qwen/qwen3-32b", "desc": "Qwen 3 32B - استدلال قوي"},
    
    # 🤖 DeepSeek (مضاف)
    "10": {"name": "deepseek/firebase", "desc": "DeepSeek V3 - نموذج قوي مجاني (عبر Firebase)"},
    
    # 🤖 Claude (مضاف)
    "11": {"name": "claude/firebase", "desc": "Claude 3 - نموذج متقدم مجاني (عبر Firebase)"},
}

# الإعدادات الافتراضية
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 1.0

# تخزين إعدادات كل مستخدم
user_model = {}
user_temp = {}
user_conversations = {}
user_chat_count = {}

# =========================================================== #
# دوال مساعدة
# =========================================================== #
def get_user_model(user_id):
    return user_model.get(user_id, DEFAULT_MODEL)

def get_user_temp(user_id):
    return user_temp.get(user_id, DEFAULT_TEMPERATURE)

def get_user_chat_count(user_id):
    return user_chat_count.get(user_id, 0)

def save_user_model(user_id, model):
    user_model[user_id] = model

def save_user_temp(user_id, temp):
    user_temp[user_id] = temp

def clear_user_conversation(user_id):
    if user_id in user_conversations:
        user_conversations[user_id] = []
    user_chat_count[user_id] = 0

def increment_chat_count(user_id):
    user_chat_count[user_id] = user_chat_count.get(user_id, 0) + 1

# =========================================================== #
# دالة الرد الرئيسية (تدعم Groq + DeepSeek + Claude)
# =========================================================== #
async def get_ai_response(user_id, question):
    model = get_user_model(user_id)
    
    # ✅ إذا كان النموذج من Firebase (DeepSeek أو Claude)
    if model == "deepseek/firebase":
        return await get_firebase_response(question, "deepseek")
    elif model == "claude/firebase":
        return await get_firebase_response(question, "claude")
    
    # ✅ باقي الكود لـ Groq
    try:
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
        
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            
            user_conversations[user_id].append({
                "role": "assistant",
                "content": answer
            })
            
            increment_chat_count(user_id)
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
            user_id = event.query.user_id
            model = get_user_model(user_id)
            temp = get_user_temp(user_id)
            conv_count = get_user_chat_count(user_id)
            
            # الحصول على وصف النموذج
            model_desc = "غير معروف"
            for key, m in GROQ_MODELS.items():
                if m["name"] == model:
                    model_desc = m["desc"]
                    break
            
            text = f"ᯓ 𝗔𝗥𝗔𝗦 𝗔𝗜 - الذكـاء الأصطناعَـي\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
            text += f"النمـوذج:\n`{model_desc}`\n\n"
            text += f"الحـرارة: {temp}\n"
            text += f"السجـل: {conv_count}\n\n"
            text += f"اختر الإعداد الذي تريد تغييره:"
            
            buttons = [
                [Button.inline("‹ : النـمـوذج : ›", data="groq_models_menu", style="primary")],
                [Button.inline("‹ : الحَـراره : ›", data="groq_temp_menu", style="primary")],
                [Button.inline("‹ : الـسـجل : ›", data="groq_logs_menu", style="primary")],
                [Button.inline("❌ إغلاق", data="groq_close", style="danger")]
            ]
            
            await event.answer(
                [await builder.article(
                    title="إعدادات الذكاء الاصطناعي",
                    description="تخصيص الذكاء الاصطناعي",
                    text=text,
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
    models_text = "**جميع النماذج المتاحة:**\n\n"
    for key, model in GROQ_MODELS.items():
        models_text += f"{key} - {model['desc']}\n"
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
    
    await event.edit("**اختر درجة الحرارة:**\n\n"
                     f"الحرارة الحالية: {current_temp}\n\n"
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
    conv_count = get_user_chat_count(user_id)
    
    buttons = [
        [Button.inline("‹ : حَـذف الـسجـل : ›", data="groq_clear_logs", style="danger")],
        [Button.inline("رجوع", data="groq_back_to_main", style="primary")]
    ]
    
    await event.edit(f"**إدارة سجل المحادثة**\n\n"
                     f"عدد المحادثات: {conv_count}\n\n"
                     f"الضغط على 'حذف السجل' سيمسح جميع رسائلك السابقة",
                     buttons=buttons, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_clear_logs")))
@check_owner
async def groq_clear_logs(event):
    user_id = event.query.user_id
    clear_user_conversation(user_id)
    
    await event.answer("✅ تم حذف سجل المحادثة", alert=True)
    await groq_back_to_main(event)

# =========================================================== #
# الرجوع للقائمة الرئيسية (تعرض الإعدادات الحالية)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_back_to_main")))
@check_owner
async def groq_back_to_main(event):
    user_id = event.query.user_id
    model = get_user_model(user_id)
    temp = get_user_temp(user_id)
    conv_count = get_user_chat_count(user_id)
    
    # الحصول على وصف النموذج
    model_desc = "غير معروف"
    for key, m in GROQ_MODELS.items():
        if m["name"] == model:
            model_desc = m["desc"]
            break
    
    text = f"اعدادات الذكاء الاصطناعي\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
    text += f"النموذج:\n{model_desc}\n\n"
    text += f"الحرارة: {temp}\n\n"
    text += f"السجل: {conv_count}\n\n"
    text += f"اختر الإعداد الذي تريد تغييره:"
    
    buttons = [
        [Button.inline("النموذج", data="groq_models_menu", style="primary")],
        [Button.inline("الحرارة", data="groq_temp_menu", style="primary")],
        [Button.inline("السجل", data="groq_logs_menu", style="primary")],
        [Button.inline("إغلاق", data="groq_close", style="danger")]
    ]
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# إغلاق القائمة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"groq_close")))
@check_owner
async def groq_close(event):
    await event.edit("تم إغلاق القائمة", buttons=None, parse_mode="Markdown")

# =========================================================== #
# أمر اعدادات الذكاء
# =========================================================== #

@l313l.ar_cmd(pattern="اعدادات الذكاء$")
async def groq_settings_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "grokk")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# الأمر الرئيسي للمحادثة
# =========================================================== #

def markdown_to_html(text):
    """تحويل Markdown إلى HTML"""
    # **نص** → <b>نص</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # _نص_ → <i>نص</i>
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
    # `نص` → <code>نص</code>  
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

@l313l.ar_cmd(pattern="ار(?: |$)(.*)")
async def groq_chat(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, 
            "بالرد على سؤال او بإضافة السؤال للأمر\n"
            "مثال: .ار من انت\n\n"
            "الأوامر المتاحة:\n"
            "• .اعدادات الذكاء - لوحة تحكم تفاعلية\n"
            "• .ار مسح - مسح سجل المحادثة")
    
    # جلب السؤال من الرد
    if not question and event.reply_to_msg_id and zzz.text:
        question = zzz.text
    
    # أمر مسح المحادثة
    if question == "مسح" or question == "حذف":
        clear_user_conversation(event.sender_id)
        return await edit_or_reply(event, 
            "تم حذف سجل الذكاء الاصطناعي .. بنجاح\n"
            "ارسـل الان (.ار + سؤالك) لـ البـدء من جديد")
    
    # الرد على السؤال
    zed = await edit_or_reply(event, "جـارِ الاتصـال بـ الذكاء الاصطناعي ...")
    
    answer = await get_ai_response(event.sender_id, question)
    
    model = get_user_model(event.sender_id)
    temp = get_user_temp(event.sender_id)
    model_short = model.split("/")[-1]
    
    # ✅ تحويل Markdown إلى HTML
    answer_html = markdown_to_html(answer)
    
    # ✅ تنسيق الجواب مع blockquote
    formatted_answer = f"<blockquote expandable>{answer_html}</blockquote>"
    
    # ✅ بناء النص الكامل للرسالة
    full_message = (
        f"<b>ᯓ 𝗔𝗥𝗔𝗦 𝗔𝗜 - الذكـاء الأصطناعَـي</b>\n"
        f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
        f"<blockquote><b>❓السؤال:</b> <code>{question[:50]}</code></blockquote>\n"
        f"<b>الجـواب:</b> {formatted_answer}\n"
        f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
        f"<b>النموذج:</b> <code>{model_short}</code>"
    )
    
    # ✅ التحقق من طول الرسالة (حد تليجرام 4096 حرف)
    MAX_LENGTH = 4000  # ترك مسافة أمان
    
    if len(full_message) > MAX_LENGTH:
        # إذا كان الرد طويلاً، قم بتقسيمه
        simple_answer = answer_html
        simple_message = (
            f"<b>ᯓ 𝗔𝗥𝗔𝗦 𝗔𝗜 - الذكـاء الأصطناعَـي</b>\n"
            f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
            f"<blockquote><b>❓السؤال:</b> <code>{question[:50]}</code></blockquote>\n"
            f"<b>الجـواب:</b>\n{simple_answer}\n"
            f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
            f"<b>النموذج:</b> <code>{model_short}</code>"
        )
        
        if len(simple_message) > MAX_LENGTH:
            # إذا كان لا يزال طويلاً، قسّم الرد إلى رسائل متعددة
            await zed.edit(f"<b>ᯓ 𝗔𝗥𝗔𝗦 𝗔𝗜 - الذكـاء الأصطناعَـي</b>\n⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n<b>السؤال:</b> <code>{question[:100]}</code>\n\n<b>الجـواب طويل جداً، سيتم تقسيمه:</b>", parse_mode="HTML")
            
            # تقسيم الرد إلى أجزاء
            chunk_size = 3500
            for i in range(0, len(answer_html), chunk_size):
                chunk = answer_html[i:i+chunk_size]
                await event.reply(f"<b>📄 جزء {i//chunk_size + 1}:</b>\n{chunk}", parse_mode="HTML")
            
            # إرسال معلومات النموذج في النهاية
            await event.reply(
                f"⋆┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
                f"<b>النموذج:</b> <code>{model_short}</code>",
                parse_mode="HTML"
            )
        else:
            await zed.edit(simple_message, parse_mode="HTML", link_preview=False)
    else:
        await zed.edit(full_message, parse_mode="HTML", link_preview=False)
