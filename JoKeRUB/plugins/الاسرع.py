from JoKeRUB import l313l  # استيراد المتغير l313l من الريبو الخاص بك
from telethon import events
from ..core.managers import edit_or_reply  # استيراد دالة edit_or_reply

# قاموس لتخزين صيغة السؤال لكل مجموعة
question_formats = {}

@l313l.ar_cmd(
    pattern="start$",  # الأمر /start
    command=("start", plugin_category),  # تعريف الأمر والفئة
    info={
        "header": "بدء البوت",
        "description": "يرحب بك البوت ويشرح كيفية استخدامه.",
        "usage": "{tr}start",
    },
)
async def start(event):
    "بدء البوت وشرح كيفية استخدامه"
    await edit_or_reply(event, "مرحبًا! أنا يوزر بوت تفكيك الكلمات. استخدم الأمر `.set_question` متبوعًا بصيغة السؤال لتعيينها.")

@l313l.ar_cmd(
    pattern="set_question (.*)",  # الأمر /set_question
    command=("set_question", plugin_category),  # تعريف الأمر والفئة
    info={
        "header": "تعيين صيغة السؤال",
        "description": "يقوم بتعيين صيغة السؤال التي سيتم استخدامها لتفكيك الكلمات.",
        "usage": "{tr}set_question <صيغة السؤال>",
    },
)
async def set_question(event):
    "تعيين صيغة السؤال"
    question = event.pattern_match.group(1).strip()  # استخراج صيغة السؤال من الرسالة
    if question:
        question_formats[event.chat_id] = question  # حفظ صيغة السؤال في القاموس
        await edit_or_reply(event, f"تم تعيين صيغة السؤال إلى: {question}")
    else:
        await edit_or_reply(event, "يرجى إرسال صيغة السؤال بعد الأمر `.set_question`.")

@l313l.ar_cmd(incoming=True)
async def handle_message(event):
    "تفكيك الكلمات بناءً على صيغة السؤال"
    chat_id = event.chat_id
    text = event.text

    if chat_id in question_formats:
        question = question_formats[chat_id]
        if question in text:
            # استخراج الكلمة التي تأتي بعد صيغة السؤال
            parts = text.split(question)
            if len(parts) > 1:
                word_to_dismantle = parts[1].strip()
                if word_to_dismantle:
                    # تفكيك الكلمة إلى حروف
                    dismantled_word = " ".join(list(word_to_dismantle))
                    await edit_or_reply(event, f"{dismantled_word}")
                else:
                    await edit_or_reply(event, "لم يتم العثور على كلمة لتفكيكها.")
            else:
                await edit_or_reply(event, "صيغة السؤال غير صحيحة.")
    else:
        await edit_or_reply(event, "يرجى تعيين صيغة السؤال أولاً باستخدام الأمر `.set_question`.")
