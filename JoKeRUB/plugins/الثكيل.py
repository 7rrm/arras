#المطور aRRas
import asyncio
from telethon import events
from JoKeRUB import l313l

hussein_enabled = False
aljoker_enabled = False
JOKER_ID = {}

# تعريف الأمرين: .تفكيك و .ت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^[\.\/](تفكيك|ت) (.*)'))
async def break_word(event):
    
    text = event.pattern_match.group(2)
    letters = ' '.join(list(text))
    await event.respond(letters)
    
    await event.delete()

import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
word_game_enabled = False
word_game_allowed_user_id = None  # معرف الشخص أو البوت المسموح له
word_game_trigger_text = "- اسرع واحد يكتب الكلمه ->"  # النص المحفز الافتراضي

# تفعيل ميزة الكلمات مع معرف الشخص أو البوت
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل كلمات(?: (\d+))?$'))
async def enable_word_game(event):
    global word_game_enabled, word_game_allowed_user_id
    user_id = event.pattern_match.group(1)  # الحصول على المعرف إذا تم إدخالها

    if user_id:
        word_game_allowed_user_id = int(user_id)  # تعيين المعرف المسموح له
    else:
        # إذا لم يتم إدخال معرف، يتم إعلام المستخدم بضرورة إدخال معرف
        await event.edit("**᯽︙ يرجى إدخال معرف صحيح بعد الأمر.**")
        return

    word_game_enabled = True
    await event.edit(f"ش")

# تعطيل ميزة الكلمات
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل كلمات$'))
async def disable_word_game(event):
    global word_game_enabled, word_game_allowed_user_id
    word_game_enabled = False
    word_game_allowed_user_id = None  # إلغاء تعيين المعرف المسموح له
    await event.edit("**᯽︙ تم تعطيل ميزة الكلمات بنجاح ✅**")

# تفعيل نص محفز مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص كلمات (.*)$'))
async def set_word_game_trigger_text(event):
    global word_game_trigger_text
    word_game_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"ش")

# الرد التلقائي على الرسائل
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_word_game(event):
    global word_game_enabled, word_game_allowed_user_id, word_game_trigger_text
    
    # التحقق من أن الميزة مفعلة وأن الرسالة من المعرف المسموح له
    if word_game_enabled and event.sender_id == word_game_allowed_user_id:
        if word_game_trigger_text in event.raw_text:
            # استخراج الكلمة بين الأقواس (أي من () أو {})
            match = re.search(r'[\({]([^)}]+)[\)}]', event.raw_text)
            if match:
                word = match.group(1).strip()  # إزالة المسافات الزائدة
                # إزالة النقطة من نهاية الكلمة إذا وجدت
                if word.endswith('.'):
                    word = word[:-1]
                # تأخير الرد بـ 1 ثانية
                await asyncio.sleep(1)
                # إرسال رسالة جديدة تحتوي على الكلمة المستخرجة (بدون الرد على الرسالة الأصلية)
                await event.client.send_message(event.chat_id, word)

# باقي الكود الح

import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
articles_enabled = False
articles_chat_id = None
articles_allowed_user_ids = set()
articles_trigger_text = "⌔︙اكتبها بدون فواصل"
reply_mode = False
reply_delay = 3

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.(/?)تفعيل مقالات(?:\s+(\d+))?(?:\s+(-?\d+))?$'))
async def enable_articles_bot(event):
    global articles_enabled, articles_chat_id, articles_allowed_user_ids, reply_mode
    user_id = event.pattern_match.group(2)
    group_id = event.pattern_match.group(3)
    is_reply_mode = bool(event.pattern_match.group(1))
    
    if not user_id:
        await event.edit("**⚠️ يرجى إدخال معرف المستخدم/البوت بعد الأمر**\nمثال: `.تفعيل مقالات 123456789`\nأو `/تفعيل مقالات` للوضع العادي")
        return
    
    articles_allowed_user_ids.add(int(user_id))
    reply_mode = is_reply_mode
    
    if group_id:
        articles_chat_id = int(group_id)
    else:
        articles_chat_id = event.chat_id
    
    articles_enabled = True
    mode_text = "وضع الرد" if is_reply_mode else "الوضع العادي"
    await event.edit(f"**✅ تم تفعيل المقالات بنجاح**\n"
                    f"المجموعة: `{articles_chat_id}`\n"
                    f"المستخدم المسموح: `{user_id}`\n"
                    f"الوضع: `{mode_text}`")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل مقالات$'))
async def disable_articles_bot(event):
    global articles_enabled, articles_chat_id, articles_allowed_user_ids, reply_mode
    articles_enabled = False
    articles_chat_id = None
    articles_allowed_user_ids.clear()
    reply_mode = False
    await event.edit("**✅ تم تعطيل المقالات بنجاح**")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص مقالات (.*)$'))
async def set_articles_trigger_text(event):
    global articles_trigger_text
    articles_trigger_text = event.pattern_match.group(1)
    await event.edit(f"**✅ تم تعيين نص المقالات إلى:** `{articles_trigger_text}`")

@l313l.on(events.NewMessage(incoming=True))
async def process_articles(event):
    global articles_enabled, articles_chat_id, articles_allowed_user_ids, articles_trigger_text, reply_mode, reply_delay
    
    if not articles_enabled or event.chat_id != articles_chat_id or event.sender_id not in articles_allowed_user_ids:
        return
    
    if reply_mode:
        # وضع الرد: يتأكد من أن الرسالة رد على رسالة البوت وتحتوي على النص المحفز
        if not event.is_reply:
            return
            
        replied_msg = await event.get_reply_message()
        if replied_msg.sender_id != l313l.uid or articles_trigger_text not in event.raw_text:
            return
            
        # في وضع الرد، نأخذ النص قبل النص المحفز فقط
        text_to_process = event.raw_text.split(articles_trigger_text)[0].strip()
        delay = reply_delay
    else:
        # الوضع العادي: يتأكد من وجود النص المحفز في الرسالة الحالية
        if articles_trigger_text not in event.raw_text:
            return
            
        # في الوضع العادي، نأخذ النص قبل النص المحفز فقط
        text_to_process = event.raw_text.split(articles_trigger_text)[0].strip()
        delay = reply_delay
    
    # تنظيف النص من الرموز واستبدالها بمسافات
    cleaned_text = text_to_process.replace("*", " ").replace("/", " ").replace("،", " ").replace(",", " ")
    
    # إزالة المسافات الزائدة
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    if cleaned_text:
        await asyncio.sleep(delay)
        await event.respond(cleaned_text)





# باقي الكود الحالي...
import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
flags_enabled = False
flags_chat_id = None
flags_allowed_user_ids = set()
flags_trigger_text = "⌔︙اسرع واحد يكتب اسم الدولة للعلم↫"
reply_mode = False  # متغير جديد لتحديد وضع الرد

# قاموس الأعلام والبلدان
flags_dict = {
    "🇯🇴": "الأردن",
    "🇪🇸": "إسبانيا",
    "🇷🇺": "روسيا",
    "🇮🇷": "ايران",
    "🇷🇴": "رومانيا",
    "🇺🇦": "أوكرانيا",
    "🇱🇾": "ليبيا",
    "🇶🇦": "قطر",
    "🇲🇦": "المغرب",
    "🇹🇳": "تونس",
    "🇦🇪": "الامارات",
    "🇻🇪": "فنزويلا",
    "🇨🇳": "الصين",
    "🇪🇬": "مصر",
    "🇮🇶": "العراق",
    "🇸🇦": "السعوديه",
    "🇩🇿": "الجزائر",
    "🇰🇵": "كوريا الشمالية",
    "🇸🇩": "السودان",
    "🇵🇰": "باكستان",
    "🇺🇸": "امريكا",
    "🇰🇼": "الكويت",
    "🇧🇷": "البرازيل",
    "🇫🇷": "فرنسا",
    "🇵🇸": "فلسطين",
    "🇧🇭": "البحرين",
    "🇸🇾": "سوريا",
    "🇳🇱": "هولندا",
    "🇸🇪": "السويد",
    "🇾🇪": "اليمن",
    "🇸🇸": "السودان",
    "🇦🇹": "النمسا",
    "🇯🇵": "اليابان",
    "🇱🇧": "لبنان",
    "🇲🇷": "موريتانيا",
    "🇦🇺": "استراليا",
    "🇮🇹": "ايطاليا",
    "🇬🇷": "اليونان",
    "🇬🇧": "بريطانيا",
    "🇷🇴": "رومانيا",
    "🇨🇭": "سويسرا",
}

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.(/?)تفعيل اعلام(?:\s+(\d+))?(?:\s+(-?\d+))?$'))
async def enable_flags_bot(event):
    global flags_enabled, flags_chat_id, flags_allowed_user_ids, reply_mode
    user_id = event.pattern_match.group(2)
    group_id = event.pattern_match.group(3)
    is_reply_mode = bool(event.pattern_match.group(1))  # إذا كان هناك / قبل الأمر
    
    if not user_id:
        await event.edit("**⚠️ يرجى إدخال معرف المستخدم/البوت بعد الأمر**\nمثال: `.تفعيل اعلام 123456789`\nأو `/تفعيل اعلام` للوضع العادي")
        return
    
    flags_allowed_user_ids.add(int(user_id))
    reply_mode = is_reply_mode  # تعيين وضع الرد
    
    if group_id:
        flags_chat_id = int(group_id)
    else:
        flags_chat_id = event.chat_id
    
    flags_enabled = True
    mode_text = "وضع الرد" if is_reply_mode else "الوضع العادي"
    await event.edit(f"**✅ تم تفعيل الأعلام بنجاح**\n"
                    f"المجموعة: `{flags_chat_id}`\n"
                    f"المستخدم المسموح: `{user_id}`\n"
                    f"الوضع: `{mode_text}`")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل اعلام$'))
async def disable_flags_bot(event):
    global flags_enabled, flags_chat_id, flags_allowed_user_ids, reply_mode
    flags_enabled = False
    flags_chat_id = None
    flags_allowed_user_ids.clear()
    reply_mode = False
    await event.edit("**✅ تم تعطيل الأعلام بنجاح**")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص اعلام (.*)$'))
async def set_flags_trigger_text(event):
    global flags_trigger_text
    flags_trigger_text = event.pattern_match.group(1)
    await event.edit(f"**✅ تم تعيين نص الأعلام إلى:** `{flags_trigger_text}`")

@l313l.on(events.NewMessage(incoming=True))
async def process_flags(event):
    global flags_enabled, flags_chat_id, flags_allowed_user_ids, flags_trigger_text, flags_dict, reply_mode
    
    if not flags_enabled or event.chat_id != flags_chat_id or event.sender_id not in flags_allowed_user_ids:
        return
    
    if reply_mode:
        # وضع الرد: يتأكد من أن الرسالة رد على رسالة البوت وتحتوي على النص المحفز
        if not event.is_reply:
            return
            
        replied_msg = await event.get_reply_message()
        if replied_msg.sender_id != l313l.uid or flags_trigger_text not in event.raw_text:
            return
            
        text_to_process = event.raw_text
    else:
        # الوضع العادي: يتأكد من وجود النص المحفز في الرسالة الحالية
        if flags_trigger_text not in event.raw_text:
            return
            
        text_to_process = event.raw_text
    
    # البحث عن العلم داخل الأقواس (إذا وجد)
    flag_with_brackets = re.search(r'[\({]([^})]+)[\)}]', text_to_process)
    if flag_with_brackets:
        flag = flag_with_brackets.group(1).strip()
        if flag.endswith('.'):
            flag = flag[:-1]
    else:
        # إذا لم يكن هناك أقواس، يتم البحث عن العلم مباشرة
        flag = text_to_process.split(flags_trigger_text)[-1].strip()
    
    # البحث عن العلم في القاموس
    if flag in flags_dict:
        country = flags_dict[flag]
        await asyncio.sleep(1)
        await event.reply(country)

import asyncio
import re
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
break_enabled = False
active_chat_id = None
break_allowed_user_ids = set()
break_trigger_text = "⌔︙فكك :"
reply_mode = False  # متغير جديد لتحديد وضع الرد

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.(/?)تفعيل تفكيك(?:\s+(\d+))?(?:\s+(-?\d+))?$'))
async def enable_break_bot(event):
    global break_enabled, active_chat_id, break_allowed_user_ids, reply_mode
    user_id = event.pattern_match.group(2)
    group_id = event.pattern_match.group(3)
    is_reply_mode = bool(event.pattern_match.group(1))  # إذا كان هناك / قبل الأمر
    
    if not user_id:
        await event.edit("**⚠️ يرجى إدخال معرف المستخدم/البوت بعد الأمر**\nمثال: `.تفعيل تفكيك 123456789`\nأو `.تفعيل تفكيك` للوضع العادي")
        return
    
    break_allowed_user_ids.add(int(user_id))
    reply_mode = is_reply_mode  # تعيين وضع الرد
    
    if group_id:
        active_chat_id = int(group_id)
    else:
        active_chat_id = event.chat_id
    
    break_enabled = True
    mode_text = "وضع الرد" if is_reply_mode else "الوضع العادي"
    await event.edit(f"**✅ تم تفعيل التفكيك بنجاح**\n"
                    f"المجموعة: `{active_chat_id}`\n"
                    f"المستخدم المسموح: `{user_id}`\n"
                    f"الوضع: `{mode_text}`")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل تفكيك$'))
async def disable_break_bot(event):
    global break_enabled, active_chat_id, break_allowed_user_ids, reply_mode
    break_enabled = False
    active_chat_id = None
    break_allowed_user_ids.clear()
    reply_mode = False
    await event.edit("**✅ تم تعطيل التفكيك بنجاح**")

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص تفكيك (.*)$'))
async def set_break_trigger_text(event):
    global break_trigger_text
    break_trigger_text = event.pattern_match.group(1)
    await event.edit(f"**✅ تم تعيين نص التفكيك إلى:** `{break_trigger_text}`")

@l313l.on(events.NewMessage(incoming=True))
async def break_word_on_trigger(event):
    global break_enabled, active_chat_id, break_allowed_user_ids, break_trigger_text, reply_mode
    
    if not break_enabled or event.chat_id != active_chat_id or event.sender_id not in break_allowed_user_ids:
        return
    
    if reply_mode:
        # وضع الرد: يتأكد من أن الرسالة رد على رسالة البوت وتحتوي على النص المحفز
        if not event.is_reply:
            return
            
        replied_msg = await event.get_reply_message()
        if replied_msg.sender_id != l313l.uid or break_trigger_text not in event.raw_text:
            return
            
        text_to_search = event.raw_text
        delay = 1
    else:
        # الوضع العادي: يتأكد من وجود النص المحفز في الرسالة الحالية
        if break_trigger_text not in event.raw_text:
            return
            
        text_to_search = event.raw_text.split(break_trigger_text)[-1]
        delay = 1
    
    # البحث عن الأقواس {} أو ()
    match = re.search(r'[{(]([^})]+)[})]', text_to_search)
    if match:
        word = match.group(1).strip()
        word = re.sub(r'[\s\n]+', '', word)
        if word:
            letters = ' '.join(list(word))
            await asyncio.sleep(delay)
            await event.reply(letters)


import asyncio
from telethon import events
from JoKeRUB import l313l

# تعريف المتغيرات العامة
meanings_enabled = False
active_chat_id = None
meanings_allowed_user_ids = set()  # مجموعة لتخزين معرفات المستخدمين المسموح لهم
meanings_trigger_text = "⌔︙اسرع واحد يدز معنى السمايل ~ "  # النص المحفز الافتراضي للمعان

# قاموس السمايلات ومعانيها
smiley_meanings = {
    "🐭": "فأر",
    "🍎": "تفاحه",
    "🦁": "اسد",
    "🐓": "ديك",
    "🐄": "بقره",
    "🦂": "عقرب",
    "🦉": "بومه",
    "🐫": "جمل",
    "🦋": "ف��اشه",
    "🐟": "سمكه",
    "🐔": "دجاجه",
    "🦈": "قرش",
    "🐺": "ذئب",
    "🐧": "بطريق",
    "🐝": "نحله",
    "🐸": "ضفدع",
    "🐬": "دولفين",
    "🐅": "نمر",
    "🦇": "خفاش",
    # يمكنك إضافة المزيد من السمايلات ومعانيها هنا
}

# تفعيل ميزة المعاني
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل معاني(?: (\d+(?:,\d+)*))?$'))
async def enable_meanings_bot(event):
    global meanings_enabled, active_chat_id, meanings_allowed_user_ids
    ids_input = event.pattern_match.group(1)  # الحصول على المعرفات إذا تم إدخالها

    # إضافة المعرفات إلى المجموعة
    if ids_input:
        meanings_allowed_user_ids.update(map(int, ids_input.split(',')))
    else:
        # إذا لم يتم إدخال معرفات، يتم إعلام المستخدم بضرورة إدخال معرفات
        await event.edit("**᯽︙ يرجى إدخال معرفات صحيحة بعد الأمر.**")
        return

    active_chat_id = event.chat_id  # حفظ معرف المجموعة
    meanings_enabled = True
    await event.edit(f"ش")
                   #  f"**المعرفات المسموحة:** {', '.join(map(str, meanings_allowed_user_ids))}")

# تعطيل ميزة المعاني
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل معاني$'))
async def disable_meanings_bot(event):
    global meanings_enabled, active_chat_id, meanings_allowed_user_ids
    active_chat_id = None  # إلغاء تفعيل المجموعة
    meanings_enabled = False
    meanings_allowed_user_ids.clear()  # مسح جميع المعرفات المسموحة
    await event.edit("**᯽︙ تم تعطيل معاني السمايلات في جميع المجموعات بنجاح ✅**")

# تفعيل نص محفز مخصص
@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.تفعيل نص معاني (.*)$'))
async def set_meanings_trigger_text(event):
    global meanings_trigger_text
    meanings_trigger_text = event.pattern_match.group(1)  # تعيين النص المحفز المخصص
    await event.edit(f"ش")

# الرد التلقائي على السمايلات
@l313l.on(events.NewMessage(incoming=True))
async def auto_reply_meanings(event):
    global meanings_enabled, active_chat_id, meanings_allowed_user_ids, meanings_trigger_text, smiley_meanings
    
    # التحقق من أن الرسالة في المجموعة المفعلة ومن المستخدم المسموح له
    if meanings_enabled and event.chat_id == active_chat_id and event.sender_id in meanings_allowed_user_ids:
        if meanings_trigger_text in event.raw_text:
            # البحث عن السمايل في الرسالة
            for smiley, meaning in smiley_meanings.items():
                if smiley in event.raw_text:
                    # إرسال معنى السمايل كرسالة جديدة (بدون رد)
                    await event.client.send_message(event.chat_id, f"{meaning}")
                    break

                    
@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mark_as_read(event):
    global aljoker_enabled, JOKER_ID
    sender_id = event.sender_id
    if aljoker_enabled and sender_id in JOKER_ID:
        joker_time = JOKER_ID[sender_id]
        if joker_time > 0:
            await asyncio.sleep(joker_time)
        await event.mark_read()

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر تعطيل$'))
async def Hussein(event):
    global aljoker_enabled
    aljoker_enabled = False
    await event.edit('**᯽︙ تم تعطيل امر التكبر بنجاح ✅**')

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.التكبر (\d+) (\d+)$'))
async def Hussein(event):
    global aljoker_enabled, JOKER_ID
    joker_time = int(event.pattern_match.group(1))
    user_id = int(event.pattern_match.group(2)) 
    JOKER_ID[user_id] = joker_time
    aljoker_enabled = True
    await event.edit(f'**᯽︙ تم تفعيل امر التكبر بنجاح مع  {joker_time} ثانية للمستخدم {user_id}**')

@l313l.on(events.NewMessage(outgoing=True, pattern=r'^\.مود التكبر تعطيل$'))
async def Hussein(event):
    global hussein_enabled
    hussein_enabled = False
    await event.edit('**᯽︙ تم تعطيل امر التكبر على الجميع بنجاح ✅**')
    
@l313l.on(admin_cmd(pattern=f"مود التكبر (\d+)"))
async def Hussein(event):
    global hussein_enabled, hussein_time
    hussein_time = int(event.pattern_match.group(1))
    hussein_enabled = True
    await event.edit(f'**᯽︙ تم تفعيل امر التكبر بنجاح مع  {hussein_time} ثانية**')

@l313l.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def Hussein(event):
    global hussein_enabled
    if hussein_enabled:
        await asyncio.sleep(hussein_time)
        await event.mark_read()
        

from telethon import events
import random
import time
from telethon.tl.custom import Button
from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.quotes_sql import (
    add_chat_quote,
    get_chat_quote,
    get_all_quotes_chats,
    update_chat_quote,
    remove_chat_quote,
    remove_all_quotes,
    count_enabled_quotes,
    count_all_quotes
)
from ..helpers import reply_id
from ..helpers.utils import _format
from telethon.extensions import markdown, html
from telethon.tl import types

plugin_category = "utils"

class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url.startswith('emoji/'):
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(
                            offset=e.offset,
                            length=e.length,
                            document_id=document_id
                        )
            return text, entities
        elif self.parse_mode == 'markdown':
            return markdown.parse(text)
        raise ValueError("Unsupported parse mode")

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)


# مجموعة الاقتباسات
messages_collection = [
    "• وَعَسَىٰ بِالصَّبْرِ نَنَالُ أَعْظَمَ مِمَّا حَلَمْنَا بِهِ .",
    "• وَتَظُنُّ أَنَّك هَالِكٌ ثُمَّ يَأْتِي لُطْفُ اللَّهِ .", 
    "• رُبَّمَا يُسَاقُ إِلَيْكَ قَدَرٌ مِنَ اللَّهِ ، خَيْرًا مِنْ كُلِّ أَحْلَامِكَ .",
    "• ثُمَّ يُعَوِّضُكَ اللَّهُ بِمَا يَلِيقُ لِقَلْبِكَ .",
    "• وَتوكَّل على الله وكفىٰ باللهِ وَكيلًا .",
    "• لَنْ يَتْرُكَكَ اللَّهُ.. هُوَ القَائِلُ:\n ﴿إِنِّي مَعَكُمَا أَسْمَعُ وَأَرَى﴾ .",
    "• اللهُمَّ اختَرْ لِي ، وَلَا تُخَيرْنِي 🤍 .",
    "• وَّعَسَى الْـقَـآدِمُ  كُلـهُ  خَـيْرًا،\nوَعَسى أَنْ يُّهْبنَا ﷲ أَعْظَمَ مِمَّا حَلَمْنَا بِـهِ .",
    "• اللهُم اسْتَجِب لنَا مَا نَعجزُ عَن قَوْلهِ وَأَنتَ أَعلَمُ بهِ .",
    "﴿ وَاللَّهُ يَعْلَمُ مَا فِي قُلُوبِكُمْ ﴾\n - فَأَطْمَئِنُوا .",
    "• الحَمدُ لِلَّهِ عَلىٰ كُل شَيءٍ .",
    "• وَلَعَل اللهَ فِي لَحْظَةٍ مَا،\nيُغَيرُ كُلَّ الذِي تَظُنهُ لَن يَتَغَير .",
    "﴿ فَإِنِّي قَرِيبٌ ﴾\n- عُمْقُ الْأَمَانِ فِي كَلِمَتَيْنِ .",
    "- عَنْ رَغَبَاتِكَ وَمَطَالِبِكَ :\n﴿ يَأْتِ بِهَا اللَّهُ ، إِنَّ اللَّهَ لَطِيفٌ خَبِيرٌ ﴾",
    "• وَرَاءَ كُلِّ شَيْءٍ لَمْ يَكْتَمِلْ ، خَيْرًا أَرَادَهُ اللَّهُ لَكَ ."
]

admin_id = l313l.uid

# تخزين سريع في الذاكرة
last_reply_time = {}
trigger_symbols = {'.', '،', ',', '-'}

def is_quotes_enabled(chat_id):
    chat = get_chat_quote(chat_id)
    return chat.is_enabled == 1 if chat else False

def get_quotes_delay(chat_id):
    chat = get_chat_quote(chat_id)
    return int(chat.delay_time) if chat and chat.delay_time.isdigit() else 0

@l313l.ar_cmd(
    pattern="تفعيل الاقتباس(?:\s+(-?\d+))?(?:\s+(\d+))?$",
    command=("تفعيل الاقتباس", plugin_category),
    info={
        "header": "لتشغيل ميزة الاقتباسات في مجموعة محددة مع وقت تأخير اختياري",
        "usage": [
            "{tr}تفعيل الاقتباس - للتشغيل في المجموعة الحالية",
            "{tr}تفعيل الاقتباس <ايدي المجموعة> - للتشغيل في مجموعة محددة",
            "{tr}تفعيل الاقتباس <ايدي المجموعة> <الوقت بالثواني> - للتشغيل مع وقت تأخير"
        ],
    },
)
async def enable_quotes(event):
    chat_input = event.pattern_match.group(1)
    delay_input = event.pattern_match.group(2)
    
    if chat_input:
        try:
            chat_id = int(chat_input)
            if chat_id > 0:
                chat_id = int(f"-100{chat_id}")
        except ValueError:
            return await edit_delete(event, "**✧︙ رقم المجموعة غير صحيح!**")
    else:
        chat_id = event.chat_id
    
    delay_time = 0
    if delay_input and delay_input.isdigit():
        delay_time = int(delay_input)
    
    # الحصول على اسم المجموعة
    chat_title = ""
    try:
        chat = await event.client.get_entity(chat_id)
        chat_title = chat.title if hasattr(chat, 'title') else ""
    except:
        pass
    
    if is_quotes_enabled(chat_id):
        current_delay = get_quotes_delay(chat_id)
        if delay_time > 0:
            return await edit_or_reply(
                event,
                f"<b>◈︙الاقتبـاسات مفعلـة بالفعل</b> <a href='emoji/5348296085334934565'>✅</a>\n"
                f"<b>✧╎المجموعـة:</b> <code>{chat_title if chat_title else chat_id}</code>\n"
                f"<b>✧╎وقت التأخيـر:</b> <code>{current_delay}</code> ثانيـة",
                parse_mode=CustomParseMode("html")
            )
        else:
            return await edit_or_reply(
                event,
                f"<b>◈︙الاقتبـاسات مفعلـة بالفعل</b> <a href='emoji/5348296085334934565'>✅</a>\n"
                f"<b>✧╎المجموعـة:</b> <code>{chat_title if chat_title else chat_id}</code>",
                parse_mode=CustomParseMode("html")
            )
    
    # إضافة أو تحديث في قاعدة البيانات
    add_chat_quote(chat_id, chat_title, delay_time, 1)
    
    await edit_or_reply(
        event,
        f"<b>◈︙تم تفعيـل الاقتبـاسات</b> <a href='emoji/5348125643852758491'>🔔</a>\n"
        f"<b>✧╎المجموعـة:</b> <code>{chat_title if chat_title else chat_id}</code>\n"
        f"<b>✧╎الايـدي:</b> <code>{chat_id}</code>\n"
        f"<b>✧╎وقت التأخيـر:</b> <code>{delay_time if delay_time > 0 else 'بدون'}</code> ثانيـة",
        parse_mode=CustomParseMode("html")
    )

@l313l.ar_cmd(
    pattern="تعطيل الاقتباس(?:\s+(-?\d+))?$",
    command=("تعطيل الاقتباس", plugin_category),
    info={
        "header": "لإيقاف ميزة الاقتباسات في مجموعة محددة",
        "usage": [
            "{tr}تعطيل الاقتباس - للإيقاف في المجموعة الحالية", 
            "{tr}تعطيل الاقتباس <ايدي المجموعة> - للإيقاف في مجموعة محددة"
        ],
    },
)
async def disable_quotes(event):
    chat_input = event.pattern_match.group(1)
    
    if chat_input:
        try:
            chat_id = int(chat_input)
            if chat_id > 0:
                chat_id = int(f"-100{chat_id}")
        except ValueError:
            return await edit_delete(event, "**✧︙ رقم المجموعة غير صحيح!**")
    else:
        chat_id = event.chat_id
    
    if not is_quotes_enabled(chat_id):
        return await edit_or_reply(
            event,
            f"<b>◈︙الاقتبـاسات معطلـة بالفعل</b> <a href='emoji/5348296085334934565'>🔕</a>\n"
            f"<b>✧╎المجموعـة:</b> <code>{chat_id}</code>",
            parse_mode=CustomParseMode("html")
        )
    
    # تحديث الحالة في قاعدة البيانات
    update_chat_quote(chat_id, is_enabled=0)
    
    # حذف من الذاكرة المؤقتة
    if chat_id in last_reply_time:
        del last_reply_time[chat_id]
    
    await edit_or_reply(
        event,
        f"<b>◈︙تم تعطيـل الاقتبـاسات</b> <a href='emoji/5348125643852758491'>🔔</a>\n"
        f"<b>✧╎المجموعـة:</b> <code>{chat_id}</code>\n"
        f"<b>✧╎تـم حـذف إعدادات التأخيـر</b>",
        parse_mode=CustomParseMode("html")
    )

@l313l.ar_cmd(
    pattern="الاقتباس$",
    command=("الاقتباس", plugin_category),
    info={
        "header": "لعرض جميع المجموعات التي تم تفعيل الاقتباسات فيها",
        "usage": "{tr}الاقتباس",
    },
)
async def show_active_quotes(event):
    # التحقق إذا كان المستخدم هو المالك
    if event.sender_id != admin_id:
        return await edit_delete(event, "**✧︙ هذا الأمر متاح فقط للمالك!**")
    
    active_chats = get_all_quotes_chats()
    total_count = count_enabled_quotes()
    
    if not active_chats:
        return await edit_or_reply(
            event,
            f"<b>◈︙لا توجـد مجموعـات مفعلـة للاقتبـاسات</b> <a href='emoji/5348296085334934565'>🔕</a>",
            parse_mode=CustomParseMode("html")
        )
    
    output = f"<b>𓆩 Quᴏᴛᴇs ᴀʀRᴀS - قائمـة المجموعات المفعلـة</b> <a href='emoji/5348125643852758491'>🔔</a><b>𓆪</b>\n"
    output += f"<b>• إجمالي عـدد المجموعات:</b> {total_count}\n"
    output += "<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>\n\n"
    
    for i, chat in enumerate(active_chats, start=1):
        delay_text = f" | التأخيـر: {chat.delay_time} ث" if int(chat.delay_time) > 0 else ""
        chat_name = chat.chat_title if chat.chat_title else f"المجموعة {chat.chat_id}"
        
        output += f"<b>{i}.</b> - المجموعـة : <code>{chat_name}</code>\n"
        output += f"- الايـدي : <code>{chat.chat_id}</code>{delay_text}\n\n"
    
    await edit_or_reply(
        event,
        output,
        parse_mode=CustomParseMode("html"),
        caption=f"<b>⧗╎قائمـة المجموعات المفعلـة</b> <a href='emoji/5348125643852758491'>🔔</a>",
        file_name="quotes_chats.txt",
    )

@l313l.ar_cmd(
    pattern="مسح قائمة الاقتباس$",
    command=("مسح قائمة الاقتباس", plugin_category),
    info={
        "header": "لتعطيل الاقتباسات في جميع المجموعات وحذف القائمة",
        "usage": "{tr}مسح قائمة الاقتباس",
        "warning": "هذا الأمر لا يمكن التراجع عنه!",
    },
)
async def disable_all_quotes(event):
    # التحقق إذا كان المستخدم هو المالك
    if event.sender_id != admin_id:
        return await edit_delete(event, "**✧︙ هذا الأمر متاح فقط للمالك!**")
    
    total_chats = count_all_quotes()
    enabled_chats = count_enabled_quotes()
    
    if total_chats == 0:
        return await edit_or_reply(
            event,
            f"<b>◈︙لا توجـد مجموعـات في قائمـة الاقتبـاسات</b> <a href='emoji/5348296085334934565'>🔕</a>",
            parse_mode=CustomParseMode("html")
        )
    
    # طلب التأكيد
    confirm_message = await edit_or_reply(
        event,
        f"<b>⚠️ تأكيـد العمليـة ⚠️</b>\n"
        f"<b>✧╎سيتـم تعطيـل الاقتبـاسات في {enabled_chats} مجموعـة</b>\n"
        f"<b>✧╎اكتب</b> <code>.تأكيد</code> <b>خلال 30 ثانيـة للمواصلـة</b>\n"
        f"<b>✧╎او اكتب</b> <code>.الغاء</code> <b>للإلغـاء</b>",
        parse_mode=CustomParseMode("html")
    )
    
    try:
        # انتظار رد المستخدم لمدة 30 ثانية
        response = await l313l.wait_for(
            events.NewMessage(from_users=admin_id, pattern=r"^(\.تأكيد|\.الغاء)$"),
            timeout=30
        )
        
        if response.text == ".الغاء":
            await confirm_message.edit(
                f"<b>◈︙تم إلغـاء العمليـة</b> <a href='emoji/5348125643852758491'>✅</a>",
                parse_mode=CustomParseMode("html")
            )
            return
            
        # إذا كان التأكيد، تنفيذ العملية
        removed_count = remove_all_quotes()
        
        # مسح الذاكرة المؤقتة
        last_reply_time.clear()
        
        await confirm_message.edit(
            f"<b>◈︙تم مسـح قائمـة الاقتبـاسات</b> <a href='emoji/5348125643852758491'>✅</a>\n"
            f"<b>✧╎عـدد المجموعات المحذوفـة:</b> {removed_count}\n"
            f"<b>✧╎تـم حـذف جميـع الإعدادات</b>",
            parse_mode=CustomParseMode("html")
        )
        
    except TimeoutError:
        await confirm_message.edit(
            f"<b>◈︙انتهـى وقـت الانتظـار</b> <a href='emoji/5348296085334934565'>⏰</a>\n"
            f"<b>✧╎تم إلغـاء العمليـة</b>",
            parse_mode=CustomParseMode("html")
        )

@l313l.on(events.NewMessage)
async def quotes_handler(event):
    # تحقق سريع من الشروط الأساسية أولاً
    if not event.is_group or event.sender_id == admin_id:
        return
    
    chat_id = event.chat_id
    
    # تحقق سريع من التفعيل
    if not is_quotes_enabled(chat_id):
        return
    
    # تحقق سريع من الرموز باستخدام set
    message_text = event.message.text.strip()
    if message_text not in trigger_symbols:
        return
    
    # الآن تحقق من الوقت (آخر خطوة)
    delay_time = get_quotes_delay(chat_id)
    
    if delay_time > 0:
        current_time = time.monotonic()
        last_time = last_reply_time.get(chat_id, 0)
        
        if current_time - last_time < delay_time:
            return
        
        last_reply_time[chat_id] = current_time
    
    # إرسال الرد
    selected_message = random.choice(messages_collection)
    caption = f"<blockquote>\n{selected_message}\n</blockquote>"
    await event.respond(caption, parse_mode='html')

@l313l.ar_cmd(
    pattern="اعدادات الاقتباس(?:\s+(-?\d+))?$",
    command=("اعدادات الاقتباس", plugin_category),
    info={
        "header": "لعرض إعدادات الاقتباسات في مجموعة محددة",
        "usage": [
            "{tr}اعدادات الاقتباس - للإعدادات في المجموعة الحالية",
            "{tr}اعدادات الاقتباس <ايدي المجموعة> - للإعدادات في مجموعة محددة"
        ],
    },
)
async def quotes_settings(event):
    chat_input = event.pattern_match.group(1)
    
    if chat_input:
        try:
            chat_id = int(chat_input)
            if chat_id > 0:
                chat_id = int(f"-100{chat_id}")
        except ValueError:
            return await edit_delete(event, "**✧︙ رقم المجموعة غير صحيح!**")
    else:
        chat_id = event.chat_id
    
    chat = get_chat_quote(chat_id)
    
    if not chat:
        return await edit_or_reply(
            event,
            f"<b>◈︙لا توجـد إعدادات لهـذه المجموعـة</b> <a href='emoji/5348296085334934565'>🔕</a>\n"
            f"<b>✧╎المجموعـة:</b> <code>{chat_id}</code>",
            parse_mode=CustomParseMode("html")
        )
    
    status = "مفعـل ✅" if chat.is_enabled == 1 else "معطل 🔕"
    delay_text = f"{chat.delay_time} ثانيـة" if int(chat.delay_time) > 0 else "بدون تأخيـر"
    
    await edit_or_reply(
        event,
        f"<b>𓆩 إعدادات الاقتبـاسات</b> <a href='emoji/5348125643852758491'>⚙️</a><b>𓆪</b>\n"
        f"<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>\n\n"
        f"<b>✧ المجموعـة:</b> <code>{chat.chat_title if chat.chat_title else chat.chat_id}</code>\n"
        f"<b>✧ الايـدي:</b> <code>{chat.chat_id}</code>\n"
        f"<b>✧ الحالـة:</b> {status}\n"
        f"<b>✧ وقـت التأخيـر:</b> {delay_text}\n\n"
        f"<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>",
        parse_mode=CustomParseMode("html"),
        file_name="quotes_settings.txt"
)
