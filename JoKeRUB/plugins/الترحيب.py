# Copyright (C) 2021 JoKeRUB TEAM
# FILES WRITTEN BY  @lMl10l

from telethon import events
from telethon.utils import get_display_name
import datetime
import random
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from . import BOTLOG_CHATID

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
'''
# قائمة بكليشات الترحيب التي يرسلها البوت الإداري
ADMIN_WELCOME_MESSAGES = [
    "︙عـمࢪي جمـاࢦك نـوࢪنـا ❤️‍🔥🎗️ .",
    "⌔︙هَــْـِْـْْـِلاّ ؏ـُمࢪيِ نــْـِْورت ڪـَروبنه☆🦋💞",
    "⌔︙شَـهٛـݪډَخِـوࢦ ۽َݪـطيـفـہَ ؟ 🦋💞˛",
    "⌔︙هہ‌‏لآ عمـريـ טּـورت ڪروبنهہ‌",
    "⌔︙- اطلق من يدخل نورتنا يحبيبي ❤️‍🔥",
    "⌔︙شههݪ دخۄݪݪ ٲݪفخمم ہٰ  🔥؟؟",
    "⌔︙- ههَلݪأ ۅللهۂ بـ ڪݛوبنهه. 🍭❤️",
    "⌔︙هَِـلا يڪَِـمـࢪ نورِت كـروب 💞🦋 .",
    "⌔︙- شعشعت مجموعتنا يروحي 💓💓 :  .",
    "⌔︙شـنيعـسـݪ وُدخــݪ ݪݪڪࢪووب 🍇💞.",
]

# قائمة بكليشات الترحيب التي يرسلها حسابك
CUSTOM_WELCOME_MESSAGES = [
    "**نَـورت**↜  {mention}",
    "**هُـِݪآإ**↜  {mention}",
    "**يهُـِݪآإ**↜  {mention}",
    "**ءنـرت عزيزي**↜  {mention}",
    "**هَِـلا يڪَِمر**↜  {mention}",
    "**ٵطلق من يدخݪ نورتنـﺂ**↜  {mention}",
]

# أمر التفعيل
@l313l.ar_cmd(
    pattern="تفعيل الترحيب$",
    command=("تفعيل الترحيب", plugin_category),
    info={
        "header": "لتشغيل ميزة الرد على ترحيب البوت الإداري في هذه الدردشة.",
        "description": "عند التفعيل، سيقوم حسابك بالرد على رسائل ترحيب البوت الإداري برسالة ترحيب أخرى في هذه الدردشة فقط.",
        "usage": "{tr}تفعيل الترحيب الخاص",
    },
)
async def enable_custom_welcome(event):
    "لتشغيل ميزة الرد على ترحيب البوت الإداري في هذه الدردشة."
    chat_id = event.chat_id
    if gvarstatus(f"custom_welcome_{chat_id}") is not None:
        return await edit_delete(event, "**᯽︙ الميزة مفعلة بالفعل في هذه الدردشة!**")
    addgvar(f"custom_welcome_{chat_id}", "true")
    await edit_delete(event, "**᯽︙ تم تفعيل الترحيب الخاص في هذه الدردشة بنجاح ✓**")

# أمر التعطيل
@l313l.ar_cmd(
    pattern="تعطيل الترحيب$",
    command=("تعطيل الترحيب", plugin_category),
    info={
        "header": "لإيقاف ميزة الرد على ترحيب البوت الإداري في هذه الدردشة.",
        "description": "عند التعطيل، لن يقوم حسابك بالرد على رسائل ترحيب البوت الإداري في هذه الدردشة.",
        "usage": "{tr}تعطيل الترحيب الخاص",
    },
)
async def disable_custom_welcome(event):
    "لإيقاف ميزة الرد على ترحيب البوت الإداري في هذه الدردشة."
    chat_id = event.chat_id
    if gvarstatus(f"custom_welcome_{chat_id}") is None:
        return await edit_delete(event, "**᯽︙ الميزة معطلة بالفعل في هذه الدردشة!**")
    delgvar(f"custom_welcome_{chat_id}")
    await edit_delete(event, "**᯽︙ تم تعطيل الترحيب الخاص في هذه الدردشة بنجاح ✓**")

# الاستماع لرسائل البوت الإداري
@l313l.on(events.NewMessage)
async def reply_to_admin_welcome(event):
    chat_id = event.chat_id
    
    # التحقق من أن الميزة مفعلة في هذه الدردشة
    if gvarstatus(f"custom_welcome_{chat_id}") is None:
        return
    
    # التحقق من أن الرسالة مرسلة من البوت الإداري
    if event.sender_id == 1839897340:  # استبدل ADMIN_BOT_ID بمعرف البوت الإداري
        # التحقق من أن الرسالة تحتوي على كليشة ترحيب
        if any(welcome_message in event.message.text for welcome_message in ADMIN_WELCOME_MESSAGES):
            # استخراج منشن الشخص المنضم من رسالة البوت
            mention = None
            if "tg://user?id=" in event.message.text:
                user_id = event.message.text.split("tg://user?id=")[1].split(")")[0]
                user = await event.client.get_entity(int(user_id))
                mention = f"[{user.first_name}](tg://user?id={user.id})"
            
            # إذا تم العثور على منشن، قم بالرد برسالة ترحيب أخرى
            if mention:
                # اختيار كليشة ترحيب عشوائية
                welcome_message = random.choice(CUSTOM_WELCOME_MESSAGES).format(mention=mention)
                await event.reply(
                    welcome_message,
                    parse_mode="markdown",
                )
                
                '''
                
@l313l.on(events.ChatAction)
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = get_display_name(await event.get_chat()) or "this chat"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = f"<a href='tg://user?id={a_user.id}'>{a_user.first_name}</a>"
        my_mention = f"<a href='tg://user?id={me.id}'>{me.first_name}</a>"
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
                link_preview = True
            elif cws.reply:
                current_saved_welcome_message = cws.reply
                link_preview = False
        current_saved_welcome_message = current_saved_welcome_message.format(
            mention=mention,
            title=title,
            count=count,
            first=first,
            last=last,
            fullname=fullname,
            username=username,
            userid=userid,
            my_first=my_first,
            my_last=my_last,
            my_fullname=my_fullname,
            my_username=my_username,
            my_mention=my_mention,
            التاريخ=datetime.datetime.now().strftime("%d-%m-%Y"),
            الوقت=datetime.datetime.now().strftime("%I:%M %p").replace("AM", "صباحًا").replace("PM", "مساءً"),
        )
        current_message = await event.reply(
            current_saved_welcome_message,
            file=file_media,
            parse_mode="html",
            link_preview=link_preview,
        )
        update_previous_welcome(event.chat_id, current_message.id)
@l313l.ar_cmd(
    pattern="ترحيب(?:\s|$)([\s\S]*)",
    command=("ترحيب", plugin_category),
    info={
        "header": "To welcome new users in chat.",
        "description": "Saves the message as a welcome note in the chat. And will send welcome message to every new user in group who ever joins newly in group.",
        "option": {
            "{mention}": "To mention the user",
            "{title}": "To get chat name in message",
            "{count}": "To get group members",
            "{first}": "To use user first name",
            "{last}": "To use user last name",
            "{fullname}": "To use user full name",
            "{userid}": "To use userid",
            "{username}": "To use user username",
            "{my_first}": "To use my first name",
            "{my_fullname}": "To use my full name",
            "{my_last}": "To use my last name",
            "{my_mention}": "To mention myself",
            "{my_username}": "To use my username.",
        },
        "usage": [
            "{tr}savewelcome <welcome message>",
            "reply {tr}savewelcome to text message or supported media with text as media caption",
        ],
        "examples": "{tr}savewelcome Hi {mention}, Welcome to {title} chat",
    },
)
async def save_welcome(event):
    "To set welcome message in chat."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔︙رسالة الترحيب  :\
                \n⌔︙ايدي الدردشة  : {event.chat_id}\
                \n⌔︙يتم حفظ الرسالة التالية كملاحظة ترحيبية لـ 🔖 : {event.chat.title}, ",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await edit_or_reply(
                event,
                "`Saving media as part of the welcome note requires the BOTLOG_CHATID to be set.`",
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**᯽︙ الترحيب {} بنجاح ✓**"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم الحفظ"))
    rm_welcome_setting(event.chat_id)
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم التحديث"))
    await edit_or_reply("**᯽︙ هـنالك خـطأ في وضـع الـترحيب هـنا**")


@l313l.ar_cmd(
    pattern="حذف الترحيب$",
    command=("حذف الترحيب", plugin_category),
    info={
        "header": "To turn off welcome message in group.",
        "description": "Deletes the welcome note for the current chat.",
        "usage": "{tr}clearwelcome",
    },
)
async def del_welcome(event):
    "To turn off welcome message"
    if rm_welcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**᯽︙ تم حذف الترحيب بنجاح ✓**")
    else:
        await edit_or_reply(event, "**᯽︙ ليـس لـدي اي تـرحيبـات بالأصـل ✓**")


@l313l.ar_cmd(
    pattern="الترحيب$",
    command=("الترحيب", plugin_category),
    info={
        "header": "To check current welcome message in group.",
        "usage": "{tr}listwelcome",
    },
)
async def show_welcome(event):
    "To show current welcome message in group"
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        return await edit_or_reply(event, "**᯽︙ لم يتم حفظ اي ترحيب هنا**")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "᯽︙ أنا الان اقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "᯽︙ أنا الان اقوم بالترحيب بالمستخدمين الجدد مع هذه الرسالة"
        )
        await event.reply(cws.reply, link_preview=False)


@l313l.ar_cmd(
    pattern="الترحيب (تشغيل|ايقاف)$",
    command=("cleanwelcome", plugin_category),
    info={
        "header": "To turn off or turn on of deleting previous welcome message.",
        "description": "if you want to delete previous welcome message and send new one turn on it by deafult it will be on. Turn it off if you need",
        "usage": "{tr}cleanwelcome <on/off>",
    },
)
async def del_welcome(event):
    "To turn off or turn on of deleting previous welcome message."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("clean_welcome") is None:
            return await edit_delete(event, "**تم تشغيل الترحيب بنجاح ✓ **")
        delgvar("clean_welcome")
        return await edit_delete(
            event,
            "__From now on previous welcome message will be deleted and new welcome message will be sent.__",
        )
    if gvarstatus("clean_welcome") is None:
        addgvar("clean_welcome", "false")
        return await edit_delete(
            event, "__From now on previous welcome message will not be deleted .__"
        )
    await edit_delete(event, "** تم تعطيل الترحيب بنجاح ✓")

'''
from telethon import events
from telethon.utils import get_display_name
from JoKeRUB import l313l
from ..core.managers import edit_delete
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import random
import asyncio  # أضفنا استيراد asyncio

plugin_category = "utils"

# قائمة بكليشات الترحيب (تم تغيير الاسم إلى WELCOME_TEXTS)
WELCOME_TEXTS = [
    "**نَـورت**↜  {mention}",
    "**هُـِݪآإ**↜  {mention}",
    "**يهُـِݪآإ**↜  {mention}",
    "**ءنـرت عزيزي**↜  {mention}",
    "**هَِـلا يڪَِمر**↜  {mention}",
    "**ٵطلق من يدخݪ نورتنـﺂ**↜  {mention}",
]

@l313l.ar_cmd(
    pattern="تفعيل_الترحيب$",
    command=("تفعيل_الترحيب", plugin_category),
    info={
        "header": "لتشغيل ميزة الترحيب التلقائي",
        "usage": "{tr}تفعيل_الترحيب",
    },
)
async def enable_welcome(event):
    "لتشغيل الترحيب التلقائي"
    if gvarstatus("welcome_enabled") == "true":
        return await edit_delete(event, "**✓ الترحيب مفعل بالفعل!**")
    addgvar("welcome_enabled", "true")
    await edit_delete(event, "**✓ تم تفعيل الترحيب بنجاح**")

@l313l.ar_cmd(
    pattern="تعطيل_الترحيب$",
    command=("تعطيل_الترحيب", plugin_category),
    info={
        "header": "لإيقاف ميزة الترحيب التلقائي",
        "usage": "{tr}تعطيل_الترحيب",
    },
)
async def disable_welcome(event):
    "لإيقاف الترحيب التلقائي"
    if gvarstatus("welcome_enabled") != "true":
        return await edit_delete(event, "**✓ الترحيب معطل بالفعل!**")
    delgvar("welcome_enabled")
    await edit_delete(event, "**✓ تم تعطيل الترحيب بنجاح**")

@l313l.on(events.ChatAction)
async def welcome_handler(event):
    try:
        if not gvarstatus("welcome_enabled") == "true":
            return
            
        if event.user_joined or event.user_added:
            user = await event.get_user()
            chat = await event.get_chat()
            
            # تجنب الترحيب إذا كان المستخدم بوت
            if user.bot:
                return
                
            mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
            welcome_message = random.choice(WELCOME_TEXTS).format(mention=mention)
            
            # إضافة تأخير 3 ثواني قبل إرسال الرسالة
            await asyncio.sleep(3)
            await event.reply(welcome_message)
            
    except Exception as e:
        print(f"Error in welcome handler: {e}")



import random
import re
from telethon import events
from telethon.tl.types import User
from telethon.tl import types
from telethon.extensions import html, markdown  # هذا غير موجود في الكود 1

# قائمة بكليشات الترحيب التي يرسلها حسابك
CUSTOM_WELCOME_MESSAGES = [
    "<b>نَـورت</b>↜{mention} {emoji}",
    "<b>هُـِݪآإ</b>↜ {mention} {emoji}",
    "<b>يهُـِݪآإ</b>↜ {mention} {emoji}",
    "<b>ءنـرت عزيزي</b>↜ {mention} {emoji}",
    "<b>هَِـلا يڪَِمر</b>↜ {mention} {emoji}",
    "<b>ٵطلق من يدخݪ نورتنـﺂ</b>↜ {mention} {emoji}",
]
# قائمة إيموجيات البريميوم
PREMIUM_EMOJIS = [
    "5413554183502572090",  # إيموجي بريميوم 1
    "4994551343201912011",  # إيموجي بريميوم 2
    # يمكنك إضافة المزيد هنا
]

# كلاس التحليل المخصص (مأخوذ من الكود الثاني)
class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
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

# تخزين إعدادات الترحيب
admin_welcome_text = None  # نص ترحيب البوت الإداري
active_chats = {}  # {chat_id: admin_bot_id}

# =============== الأوامر ===============

@l313l.ar_cmd(
    pattern="تفعيل نص ترحيب (.*)",
    command=("تفعيل نص ترحيب", plugin_category),
    info={
        "header": "لتحديد نص ترحيب البوت الإداري الذي تريد البحث عنه",
        "description": "إذا كان هناك نص قديم، يتم استبداله بالنص الجديد تلقائياً",
        "usage": "{tr}تفعيل نص ترحيب <النص>",
        "examples": ["{tr}تفعيل نص ترحيب نورتنـا", "{tr}تفعيل نص ترحيب أهلاً وسهلاً"],
    },
)
async def set_admin_welcome(event):
    "لتحديد نص ترحيب البوت الإداري (يستبدل القديم)"
    global admin_welcome_text
    text = event.pattern_match.group(1).strip()
    
    if not text:
        return await edit_delete(event, "**᯽︙ يرجى كتابة نص الترحيب!**")
    
    # إذا كان هناك نص قديم، إعلام المستخدم أنه تم استبداله
    old_text = admin_welcome_text
    admin_welcome_text = text
    
    if old_text:
        await edit_delete(event, f"**᯽︙ تم تحديث نص الترحيب بنجاح ✓**\n**القديم:** `{old_text}`\n**الجديد:** `{text}`")
    else:
        await edit_delete(event, f"**᯽︙ تم حفظ نص الترحيب بنجاح ✓**\n`{text}`")

@l313l.ar_cmd(
    pattern="تفعيل الترحيب (-?\d+) (\d+)$",
    command=("تفعيل الترحيب", plugin_category),
    info={
        "header": "لتشغيل نظام الترحيب في مجموعة معينة",
        "description": "يحدد المجموعة والبوت الإداري الذي سيتم مراقبته",
        "usage": "{tr}تفعيل الترحيب <ايدي_المجموعة> <ايدي_البوت_الاداري>",
        "examples": ["{tr}تفعيل الترحيب -100123456789 1839897340"],
    },
)
async def enable_welcome(event):
    "لتشغيل نظام الترحيب في مجموعة"
    global admin_welcome_text
    
    if admin_welcome_text is None:
        return await edit_delete(event, "**᯽︙ يرجى تحديد نص الترحيب أولاً!**\nاستخدم: `.تفعيل نص ترحيب <النص>`")
    
    chat_id = int(event.pattern_match.group(1))
    admin_bot_id = int(event.pattern_match.group(2))
    
    if chat_id in active_chats:
        # إذا المجموعة مفعلة بالفعل، نحدث بيانات البوت فقط
        old_bot_id = active_chats[chat_id]
        if old_bot_id == admin_bot_id:
            return await edit_delete(event, f"**᯽︙ الترحيب مفعل بالفعل في هذه المجموعة!**\nالبوت الإداري: `{admin_bot_id}`")
        else:
            active_chats[chat_id] = admin_bot_id
            await edit_delete(event, f"**᯽︙ تم تحديث إعدادات الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\n**البوت القديم:** `{old_bot_id}`\n**البوت الجديد:** `{admin_bot_id}`")
    else:
        active_chats[chat_id] = admin_bot_id
        await edit_delete(event, f"**᯽︙ تم تفعيل الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\nالبوت الإداري: `{admin_bot_id}`")

@l313l.ar_cmd(
    pattern="تعطيل الترحيب (-?\d+)$",
    command=("تعطيل الترحيب", plugin_category),
    info={
        "header": "لتعطيل نظام الترحيب في مجموعة معينة",
        "description": "يوقف المراقبة في المجموعة المحددة ويحذف إعداداتها",
        "usage": "{tr}تعطيل الترحيب <ايدي_المجموعة>",
        "examples": ["{tr}تعطيل الترحيب -100123456789"],
    },
)
async def disable_welcome(event):
    "لتعطيل نظام الترحيب في مجموعة (يحذف إعداداتها)"
    chat_id = int(event.pattern_match.group(1))
    
    if chat_id not in active_chats:
        return await edit_delete(event, "**᯽︙ الترحيب غير مفعل في هذه المجموعة!**")
    
    deleted_bot_id = active_chats[chat_id]
    del active_chats[chat_id]
    
    # إذا لم تعد هناك مجموعات مفعلة، نحذف نص الترحيب أيضاً
    if not active_chats:
        global admin_welcome_text
        if admin_welcome_text:
            old_text = admin_welcome_text
            admin_welcome_text = None
            await edit_delete(event, f"**᯽︙ تم تعطيل الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\nالبوت الإداري: `{deleted_bot_id}`\n\n**تم حذف نص الترحيب أيضاً:** `{old_text}`")
        else:
            await edit_delete(event, f"**᯽︙ تم تعطيل الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\nالبوت الإداري: `{deleted_bot_id}`")
    else:
        await edit_delete(event, f"**᯽︙ تم تعطيل الترحيب في المجموعة `{chat_id}` بنجاح ✓**\nالبوت الإداري: `{deleted_bot_id}`")

@l313l.ar_cmd(
    pattern="تعطيل الترحيب الكل$",
    command=("تعطيل الترحيب الكل", plugin_category),
    info={
        "header": "لتعطيل نظام الترحيب في جميع المجموعات",
        "description": "يحذف جميع إعدادات الترحيب (النص والمجموعات)",
        "usage": "{tr}تعطيل الترحيب الكل",
    },
)
async def disable_all_welcome(event):
    "لتعطيل نظام الترحيب في جميع المجموعات (يحذف كل شيء)"
    global admin_welcome_text, active_chats
    
    if not active_chats and admin_welcome_text is None:
        return await edit_delete(event, "**᯽︙ لا توجد إعدادات ترحيب حالياً!**")
    
    # حفظ البيانات قبل الحذف لعرضها
    old_text = admin_welcome_text
    old_chats_count = len(active_chats)
    
    # حذف كل شيء
    admin_welcome_text = None
    active_chats.clear()
    
    message = "**᯽︙ تم تعطيل جميع إعدادات الترحيب بنجاح ✓**\n\n"
    
    if old_text:
        message += f"**نص الترحيب المحذوف:** `{old_text}`\n"
    
    if old_chats_count > 0:
        message += f"**عدد المجموعات المحذوفة:** `{old_chats_count}`\n"
    
    await edit_delete(event, message)

@l313l.ar_cmd(
    pattern="عرض ترحيبات$",
    command=("عرض ترحيبات", plugin_category),
    info={
        "header": "لعرض الإعدادات الحالية للترحيب",
        "description": "يعرض نص الترحيب والمجموعات المفعلة",
        "usage": "{tr}عرض ترحيبات",
    },
)
async def show_welcome_settings(event):
    "لعرض إعدادات الترحيب الحالية"
    global admin_welcome_text
    
    if admin_welcome_text is None and not active_chats:
        return await edit_delete(event, "**᯽︙ لا توجد إعدادات ترحيب حالياً!**")
    
    message = "**᯽︙ إعدادات نظام الترحيب:**\n\n"
    
    if admin_welcome_text:
        message += f"**نص الترحيب:** `{admin_welcome_text}`\n\n"
    else:
        message += "**⚠️ لا يوجد نص ترحيب محفوظ**\n\n"
    
    if active_chats:
        message += f"**عدد المجموعات المفعلة:** `{len(active_chats)}`\n\n"
        message += "**المجموعات المفعلة:**\n"
        for chat_id, bot_id in active_chats.items():
            message += f"• المجموعة: `{chat_id}` | البوت: `{bot_id}`\n"
    else:
        message += "**لا توجد مجموعات مفعلة**"
    
    await edit_or_reply(event, message)

# =============== المستمع ===============

@l313l.on(events.NewMessage)
async def reply_to_admin_welcome(event):
    global admin_welcome_text
    
    # التحقق من الأساسيات
    if not event.is_group:
        return
    
    if admin_welcome_text is None:
        return
    
    # التحقق إذا كانت المجموعة مفعلة
    if event.chat_id not in active_chats:
        return
    
    # التحقق إذا كانت الرسالة من البوت الإداري المحدد لهذه المجموعة
    if event.sender_id != active_chats[event.chat_id]:
        return
    
    # التحقق إذا كانت الرسالة تحتوي على نص الترحيب
    if admin_welcome_text not in event.message.text:
        return
    
    # استخراج المستخدم من الرسالة
    user_entity = None
    
    # أولاً: البحث عن يوزر (@username)
    if event.message.text:
        # البحث عن @username
        username_match = re.search(r'@(\w+)', event.message.text)
        if username_match:
            username = username_match.group(1)
            try:
                # محاولة الحصول على كيان المستخدم من اليوزر
                user = await event.client.get_entity(username)
                if isinstance(user, User):
                    user_entity = user
            except:
                pass
    
    # ثانياً: إذا لم يجد يوزر، البحث عن منشن (tg://user?id=)
    if not user_entity and "tg://user?id=" in event.message.text:
        try:
            # استخراج الـ ID من الرابط
            user_id_match = re.search(r'tg://user\?id=(\d+)', event.message.text)
            if user_id_match:
                user_id = int(user_id_match.group(1))
                user = await event.client.get_entity(user_id)
                if isinstance(user, User):
                    user_entity = user
        except:
            pass
    
    # إذا لم يتم العثور على مستخدم، لا نرد
    if not user_entity:
        return
    
    # اختيار إيموجي بريميوم عشوائي
    selected_emoji = random.choice(PREMIUM_EMOJIS)
    
    # بناء رسالة الترحيب مع الإيموجي
    if user_entity.username:
        mention_text = f"@{user_entity.username}"
    else:
        user_name = user_entity.first_name or "المستخدم"
        mention_text = f"[{user_name}](tg://user?id={user_entity.id})"
    
    # اختيار رسالة ترحيب عشوائية
    welcome_template = random.choice(CUSTOM_WELCOME_MESSAGES)
    welcome_text = welcome_template.format(mention=mention_text, emoji=f'<a href="emoji/{selected_emoji}">❤️</a>')

    await asyncio.sleep(3)
    try:
        await event.client.send_message(
            event.chat_id,
            welcome_text,
            parse_mode=CustomParseMode("html"),  # استخدام وضع HTML لدعم الإيموجيات
            link_preview=False
        )
    except Exception as e:
        print(f"خطأ في إرسال الترحيب: {e}")

# =============== رسالة المساعدة ===============

@l313l.ar_cmd(
    pattern="الترحيب1$",
    command=("الترحيب", plugin_category),
    info={
        "header": "لعرض معلومات عن نظام الترحيب",
        "description": "يعرض كيفية استخدام نظام الترحيب",
        "usage": "{tr}الترحيب",
    },
)
async def welcome_info(event):
    "لعرض معلومات عن نظام الترحيب"
    info_message = """
**◈︙︙ نظام الترحيب المتقدم**

**الأوامر المتاحة:**

1. **تحديد/تحديث نص ترحيب البوت الإداري:**
   `.تفعيل نص ترحيب <النص>`
   - إذا كان هناك نص قديم، يتم استبداله تلقائياً
   مثال: `.تفعيل نص ترحيب "نورتنـا"`

2. **تفعيل النظام في مجموعة:**
   `.تفعيل الترحيب <ايدي_المجموعة> <ايدي_البوت_الاداري>`
   مثال: `.تفعيل الترحيب -100123456789 1839897340`

3. **عرض الإعدادات:**
   `.عرض ترحيبات`

4. **تعطيل في مجموعة (يحذف إعداداتها):**
   `.تعطيل الترحيب <ايدي_المجموعة>`
   - إذا كانت آخر مجموعة، يحذف نص الترحيب أيضاً

5. **تعطيل كل شيء (نسخة إعادة ضبط):**
   `.تعطيل الترحيب الكل`
   - يحذف كل الإعدادات (النص والمجموعات)

**المميزات الجديدة:**
- إضافة إيموجيات بريميوم عشوائية في كل ترحيب
- الإيموجيات المتاحة: {}
- استخدام وضع HTML لدعم الإيموجيات المخصصة

**ملاحظات:**
- النظام يبحث عن نص الترحيب في رسائل البوت الإداري
- يحاول استخراج اليوزر أولاً (`@username`)
- إذا لم يجد يوزر، يستخرج المنشن
- يرد باليوزر إذا موجود، وإلا بالمنشن
""".format(", ".join(PREMIUM_EMOJIS))
    await edit_or_reply(event, info_message)

# =============== إضافة أوامر لإدارة الإيموجيات ===============

@l313l.ar_cmd(
    pattern="اضافة ايموجي (\d+)$",
    command=("اضافة ايموجي", plugin_category),
    info={
        "header": "لإضافة إيموجي بريميوم إلى القائمة",
        "description": "يضيف ID إيموجي بريميوم جديد إلى قائمة الإيموجيات",
        "usage": "{tr}اضافة ايموجي <ايدي_الايموجي>",
        "examples": ["{tr}اضافة ايموجي 5413554183502572090"],
    },
)
async def add_emoji(event):
    "لإضافة إيموجي بريميوم إلى القائمة"
    emoji_id = event.pattern_match.group(1).strip()
    
    if not emoji_id.isdigit():
        return await edit_delete(event, "**᯽︙ يرجى إدخال ID صحيح للإيموجي!**")
    
    if emoji_id in PREMIUM_EMOJIS:
        return await edit_delete(event, f"**᯽︙ الإيموجي `{emoji_id}` موجود بالفعل في القائمة!**")
    
    PREMIUM_EMOJIS.append(emoji_id)
    await edit_delete(event, f"**᯽︙ تمت إضافة الإيموجي بنجاح ✓**\n**ID:** `{emoji_id}`\n**عدد الإيموجيات الآن:** `{len(PREMIUM_EMOJIS)}`")

@l313l.ar_cmd(
    pattern="حذف ايموجي (\d+)$",
    command=("حذف ايموجي", plugin_category),
    info={
        "header": "لحذف إيموجي بريميوم من القائمة",
        "description": "يحذف ID إيموجي بريميوم من قائمة الإيموجيات",
        "usage": "{tr}حذف ايموجي <ايدي_الايموجي>",
        "examples": ["{tr}حذف ايموجي 5413554183502572090"],
    },
)
async def remove_emoji(event):
    "لحذف إيموجي بريميوم من القائمة"
    emoji_id = event.pattern_match.group(1).strip()
    
    if not emoji_id.isdigit():
        return await edit_delete(event, "**᯽︙ يرجى إدخال ID صحيح للإيموجي!**")
    
    if emoji_id not in PREMIUM_EMOJIS:
        return await edit_delete(event, f"**᯽︙ الإيموجي `{emoji_id}` غير موجود في القائمة!**")
    
    PREMIUM_EMOJIS.remove(emoji_id)
    await edit_delete(event, f"**᯽︙ تم حذف الإيموجي بنجاح ✓**\n**ID:** `{emoji_id}`\n**عدد الإيموجيات المتبقية:** `{len(PREMIUM_EMOJIS)}`")

@l313l.ar_cmd(
    pattern="عرض ايموجيات$",
    command=("عرض ايموجيات", plugin_category),
    info={
        "header": "لعرض قائمة الإيموجيات البريميوم",
        "description": "يعرض جميع إيموجيات البريميوم المضافة للنظام",
        "usage": "{tr}عرض ايموجيات",
    },
)
async def show_emojis(event):
    "لعرض قائمة الإيموجيات البريميوم"
    if not PREMIUM_EMOJIS:
        return await edit_delete(event, "**᯽︙ لا توجد إيموجيات في القائمة!**\nاستخدم: `.اضافة ايموجي <ID>`")
    
    message = f"**᯽︙ قائمة الإيموجيات البريميوم:**\n\n"
    for i, emoji_id in enumerate(PREMIUM_EMOJIS, 1):
        message += f"**{i}.** `{emoji_id}`\n"
    
    message += f"\n**المجموع:** `{len(PREMIUM_EMOJIS)}` إيموجي"
    await edit_or_reply(event, message)
'''


import random
import re
import asyncio
from collections import deque
from telethon import events
from telethon.tl.types import User
from telethon.tl import types
from telethon.extensions import html, markdown

# قائمة بكليشات الترحيب التي يرسلها حسابك
CUSTOM_WELCOME_MESSAGES = [
    "<b>نَـورت</b>↜{mention} {emoji}",
    "<b>هُـِݪآإ</b>↜ {mention} {emoji}",
    "<b>يهُـِݪآإ</b>↜ {mention} {emoji}",
    "<b>ءنـرت عَزيزي</b>↜ {mention} {emoji}",
    #"<b>هَِـلا يڪَِمر</b>↜ {mention} {emoji}",
    "<b>ٵطلق من يدخݪ نورتنـﺂ</b>↜ {mention} {emoji}",
]

# قائمة إيموجيات البريميوم
PREMIUM_EMOJIS = [
    "5413554183502572090",  # إيموجي بريميوم 1
    "4994551343201912011",  # إيموجي بريميوم 2
]

# =============== نظام صف الانتظار ===============
welcome_queue = deque()  # صف الانتظار للترحيبات
#is_processing = False    # هل تتم معالجة الآن؟
DELAY_SECONDS = 3        # 3 ثواني بين كل ترحيب

# كلاس التحليل المخصص
class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
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

# تخزين إعدادات الترحيب
admin_welcome_text = None  # نص ترحيب البوت الإداري
active_chats = {}  # {chat_id: admin_bot_id}

# =============== معالج صف الانتظار ===============
async def process_queue():
    """معالجة صف الانتظار بفاصل 3 ثواني بين كل ترحيب"""
    global is_processing
    
    is_processing = True
    while welcome_queue:
        # أخذ الترحيب الأول من الصف
        chat_id, user_entity, event = welcome_queue.popleft()
        
        # التحقق إذا كانت المجموعة لا تزال مفعلة
        if chat_id not in active_chats:
            continue
        
        # بناء رسالة الترحيب مع الإيموجي
        selected_emoji = random.choice(PREMIUM_EMOJIS)
        
        if user_entity.username:
            mention_text = f"@{user_entity.username}"
        else:
            user_name = user_entity.first_name or "المستخدم"
            mention_text = f"[{user_name}](tg://user?id={user_entity.id})"
        
        # اختيار رسالة ترحيب عشوائية
        welcome_template = random.choice(CUSTOM_WELCOME_MESSAGES)
        welcome_text = welcome_template.format(mention=mention_text, emoji=f'<a href="emoji/{selected_emoji}">❤️</a>')
        
        # إرسال الترحيب
        try:
            await event.client.send_message(
                chat_id,
                welcome_text,
                parse_mode=CustomParseMode("html"),
                link_preview=False
            )
        except Exception as e:
        
        # ⏱️ انتظار 3 ثواني قبل الترحيب التالي
        if welcome_queue:  # إذا كان هناك المزيد في الصف
            await asyncio.sleep(DELAY_SECONDS)
    
    #is_processing = False

# =============== الأوامر ===============

@l313l.ar_cmd(
    pattern="تفعيل نص ترحيب (.*)",
    command=("تفعيل نص ترحيب", plugin_category),
    info={
        "header": "لتحديد نص ترحيب البوت الإداري الذي تريد البحث عنه",
        "description": "إذا كان هناك نص قديم، يتم استبداله بالنص الجديد تلقائياً",
        "usage": "{tr}تفعيل نص ترحيب <النص>",
        "examples": ["{tr}تفعيل نص ترحيب نورتنـا", "{tr}تفعيل نص ترحيب أهلاً وسهلاً"],
    },
)
async def set_admin_welcome(event):
    "لتحديد نص ترحيب البوت الإداري (يستبدل القديم)"
    global admin_welcome_text
    text = event.pattern_match.group(1).strip()
    
    if not text:
        return await edit_delete(event, "**᯽︙ يرجى كتابة نص الترحيب!**")
    
    # إذا كان هناك نص قديم، إعلام المستخدم أنه تم استبداله
    old_text = admin_welcome_text
    admin_welcome_text = text
    
    if old_text:
        await edit_delete(event, f"**᯽︙ تم تحديث نص الترحيب بنجاح ✓**\n**القديم:** `{old_text}`\n**الجديد:** `{text}`")
    else:
        await edit_delete(event, f"**᯽︙ تم حفظ نص الترحيب بنجاح ✓**\n`{text}`")

@l313l.ar_cmd(
    pattern="تفعيل الترحيب (-?\d+) (\d+)$",
    command=("تفعيل الترحيب", plugin_category),
    info={
        "header": "لتشغيل نظام الترحيب في مجموعة معينة",
        "description": "يحدد المجموعة والبوت الإداري الذي سيتم مراقبته",
        "usage": "{tr}تفعيل الترحيب <ايدي_المجموعة> <ايدي_البوت_الاداري>",
        "examples": ["{tr}تفعيل الترحيب -100123456789 1839897340"],
    },
)
async def enable_welcome(event):
    "لتشغيل نظام الترحيب في مجموعة"
    global admin_welcome_text
    
    if admin_welcome_text is None:
        return await edit_delete(event, "**᯽︙ يرجى تحديد نص الترحيب أولاً!**\nاستخدم: `.تفعيل نص ترحيب <النص>`")
    
    chat_id = int(event.pattern_match.group(1))
    admin_bot_id = int(event.pattern_match.group(2))
    
    if chat_id in active_chats:
        # إذا المجموعة مفعلة بالفعل، نحدث بيانات البوت فقط
        old_bot_id = active_chats[chat_id]
        if old_bot_id == admin_bot_id:
            return await edit_delete(event, f"**᯽︙ الترحيب مفعل بالفعل في هذه المجموعة!**\nالبوت الإداري: `{admin_bot_id}`")
        else:
            active_chats[chat_id] = admin_bot_id
            await edit_delete(event, f"**᯽︙ تم تحديث إعدادات الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\n**البوت القديم:** `{old_bot_id}`\n**البوت الجديد:** `{admin_bot_id}`")
    else:
        active_chats[chat_id] = admin_bot_id
        await edit_delete(event, f"**᯽︙ تم تفعيل الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\nالبوت الإداري: `{admin_bot_id}`")

@l313l.ar_cmd(
    pattern="تعطيل الترحيب (-?\d+)$",
    command=("تعطيل الترحيب", plugin_category),
    info={
        "header": "لتعطيل نظام الترحيب في مجموعة معينة",
        "description": "يوقف المراقبة في المجموعة المحددة ويحذف إعداداتها",
        "usage": "{tr}تعطيل الترحيب <ايدي_المجموعة>",
        "examples": ["{tr}تعطيل الترحيب -100123456789"],
    },
)
async def disable_welcome(event):
    "لتعطيل نظام الترحيب في مجموعة (يحذف إعداداتها)"
    chat_id = int(event.pattern_match.group(1))
    
    if chat_id not in active_chats:
        return await edit_delete(event, "**᯽︙ الترحيب غير مفعل في هذه المجموعة!**")
    
    deleted_bot_id = active_chats[chat_id]
    del active_chats[chat_id]
    
    # إذا لم تعد هناك مجموعات مفعلة، نحذف نص الترحيب أيضاً
    if not active_chats:
        global admin_welcome_text
        if admin_welcome_text:
            old_text = admin_welcome_text
            admin_welcome_text = None
            await edit_delete(event, f"**᯽︙ تم تعطيل الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\nالبوت الإداري: `{deleted_bot_id}`\n\n**تم حذف نص الترحيب أيضاً:** `{old_text}`")
        else:
            await edit_delete(event, f"**᯽︙ تم تعطيل الترحيب بنجاح ✓**\nالمجموعة: `{chat_id}`\nالبوت الإداري: `{deleted_bot_id}`")
    else:
        await edit_delete(event, f"**᯽︙ تم تعطيل الترحيب في المجموعة `{chat_id}` بنجاح ✓**\nالبوت الإداري: `{deleted_bot_id}`")

@l313l.ar_cmd(
    pattern="تعطيل الترحيب الكل$",
    command=("تعطيل الترحيب الكل", plugin_category),
    info={
        "header": "لتعطيل نظام الترحيب في جميع المجموعات",
        "description": "يحذف جميع إعدادات الترحيب (النص والمجموعات)",
        "usage": "{tr}تعطيل الترحيب الكل",
    },
)
async def disable_all_welcome(event):
    "لتعطيل نظام الترحيب في جميع المجموعات (يحذف كل شيء)"
    global admin_welcome_text, active_chats, welcome_queue
    
    if not active_chats and admin_welcome_text is None:
        return await edit_delete(event, "**᯽︙ لا توجد إعدادات ترحيب حالياً!**")
    
    # حفظ البيانات قبل الحذف لعرضها
    old_text = admin_welcome_text
    old_chats_count = len(active_chats)
    old_queue_count = len(welcome_queue)
    
    # حذف كل شيء
    admin_welcome_text = None
    active_chats.clear()
    welcome_queue.clear()
    
    message = "**᯽︙ تم تعطيل جميع إعدادات الترحيب بنجاح ✓**\n\n"
    
    if old_text:
        message += f"**نص الترحيب المحذوف:** `{old_text}`\n"
    
    if old_chats_count > 0:
        message += f"**عدد المجموعات المحذوفة:** `{old_chats_count}`\n"
    
    if old_queue_count > 0:
        message += f"**عدد الترحيبات الملغاة من الصف:** `{old_queue_count}`\n"
    
    await edit_delete(event, message)

@l313l.ar_cmd(
    pattern="عرض ترحيبات$",
    command=("عرض ترحيبات", plugin_category),
    info={
        "header": "لعرض الإعدادات الحالية للترحيب",
        "description": "يعرض نص الترحيب والمجموعات المفعلة",
        "usage": "{tr}عرض ترحيبات",
    },
)
async def show_welcome_settings(event):
    "لعرض إعدادات الترحيب الحالية"
    global admin_welcome_text
    
    if admin_welcome_text is None and not active_chats:
        return await edit_delete(event, "**᯽︙ لا توجد إعدادات ترحيب حالياً!**")
    
    message = "**᯽︙ إعدادات نظام الترحيب:**\n\n"
    
    if admin_welcome_text:
        message += f"**نص الترحيب:** `{admin_welcome_text}`\n\n"
    else:
        message += "**⚠️ لا يوجد نص ترحيب محفوظ**\n\n"
    
    if active_chats:
        message += f"**عدد المجموعات المفعلة:** `{len(active_chats)}`\n\n"
        message += "**المجموعات المفعلة:**\n"
        for chat_id, bot_id in active_chats.items():
            message += f"• المجموعة: `{chat_id}` | البوت: `{bot_id}`\n"
        
        # إضافة معلومات عن الصف
        message += f"\n**📊 حالة صف الترحيبات:**\n"
        message += f"• الترحيبات في الانتظار: `{len(welcome_queue)}`\n"
       # message += f"• هل تتم المعالجة الآن: `{'نعم ✅' if is_processing else 'لا ⏸️'}`\n"
        message += f"• التأخير بين الترحيبات: `{DELAY_SECONDS} ثواني`\n"
    else:
        message += "**لا توجد مجموعات مفعلة**"
    
    await edit_or_reply(event, message)

# ===============  ===============


# =============== المستمع للترحيبات ===============
@l313l.on(events.NewMessage)
async def reply_to_admin_welcome(event):
    global admin_welcome_text
    
    # التحقق من الأساسيات
    if not event.is_group:
        return
    
    if admin_welcome_text is None:
        return
    
    # التحقق إذا كانت المجموعة مفعلة
    if event.chat_id not in active_chats:
        return
    
    # التحقق إذا كانت الرسالة من البوت الإداري المحدد لهذه المجموعة
    if event.sender_id != active_chats[event.chat_id]:
        return
    
    # التحقق إذا كانت الرسالة تحتوي على نص الترحيب
    if admin_welcome_text not in event.message.text:
        return
    
    # استخراج المستخدم من الرسالة
    user_entity = None
    
    # أولاً: البحث عن يوزر (@username)
    if event.message.text:
        # البحث عن @username
        username_match = re.search(r'@(\w+)', event.message.text)
        if username_match:
            username = username_match.group(1)
            try:
                # محاولة الحصول على كيان المستخدم من اليوزر
                user = await event.client.get_entity(username)
                if isinstance(user, User):
                    user_entity = user
            except:
                pass
    
    # ثانياً: إذا لم يجد يوزر، البحث عن منشن (tg://user?id=)
    if not user_entity and "tg://user?id=" in event.message.text:
        try:
            # استخراج الـ ID من الرابط
            user_id_match = re.search(r'tg://user\?id=(\d+)', event.message.text)
            if user_id_match:
                user_id = int(user_id_match.group(1))
                user = await event.client.get_entity(user_id)
                if isinstance(user, User):
                    user_entity = user
        except:
            pass
    
    # إذا لم يتم العثور على مستخدم، لا نضيف للصف
    if not user_entity:
        return
    
    # إضافة الترحيب لصف الانتظار
    welcome_queue.append((event.chat_id, user_entity, event))
    
    # بدء المعالجة إذا لم تكن جارية
    if not is_processing:
        asyncio.create_task(process_queue())

# =============== رسالة المساعدة ===============

@l313l.ar_cmd(
    pattern="الترحيب1$",
    command=("الترحيب", plugin_category),
    info={
        "header": "لعرض معلومات عن نظام الترحيب",
        "description": "يعرض كيفية استخدام نظام الترحيب",
        "usage": "{tr}الترحيب",
    },
)
async def welcome_info(event):
    "لعرض معلومات عن نظام الترحيب"
    info_message = f"""
**◈︙︙ نظام الترحيب المتقدم**

**الأوامر المتاحة:**

1. **تحديد/تحديث نص ترحيب البوت الإداري:**
   `.تفعيل نص ترحيب <النص>`
   - إذا كان هناك نص قديم، يتم استبداله تلقائياً
   مثال: `.تفعيل نص ترحيب "نورتنـا"`

2. **تفعيل النظام في مجموعة:**
   `.تفعيل الترحيب <ايدي_المجموعة> <ايدي_البوت_الاداري>`
   مثال: `.تفعيل الترحيب -100123456789 1839897340`

3. **عرض الإعدادات:**
   `.عرض ترحيبات`

4. **تعطيل في مجموعة (يحذف إعداداتها):**
   `.تعطيل الترحيب <ايدي_المجموعة>`
   - إذا كانت آخر مجموعة، يحذف نص الترحيب أيضاً

5. **تعطيل كل شيء (نسخة إعادة ضبط):**
   `.تعطيل الترحيب الكل`
   - يحذف كل الإعدادات (النص والمجموعات والصف)

**المميزات:**
- **نظام صف الانتظار:** يخزن جميع الترحيبات الواردة
- **تأخير {DELAY_SECONDS} ثواني بين كل ترحيب:** لمنع التكرار السريع
- **إيموجيات بريميوم عشوائية** في كل ترحيب
- **الحفاظ على الترحيبات الأصلية:** لا يحذف ترحيبات البوت الإداري

**الإيموجيات المتاحة:** {', '.join(PREMIUM_EMOJIS)}
"""
    await edit_or_reply(event, info_message)

# =============== إضافة أوامر لإدارة الإيموجيات ===============

@l313l.ar_cmd(
    pattern="اضافة ايموجي (\d+)$",
    command=("اضافة ايموجي", plugin_category),
    info={
        "header": "لإضافة إيموجي بريميوم إلى القائمة",
        "description": "يضيف ID إيموجي بريميوم جديد إلى قائمة الإيموجيات",
        "usage": "{tr}اضافة ايموجي <ايدي_الايموجي>",
        "examples": ["{tr}اضافة ايموجي 5413554183502572090"],
    },
)
async def add_emoji(event):
    "لإضافة إيموجي بريميوم إلى القائمة"
    emoji_id = event.pattern_match.group(1).strip()
    
    if not emoji_id.isdigit():
        return await edit_delete(event, "**᯽︙ يرجى إدخال ID صحيح للإيموجي!**")
    
    if emoji_id in PREMIUM_EMOJIS:
        return await edit_delete(event, f"**᯽︙ الإيموجي `{emoji_id}` موجود بالفعل في القائمة!**")
    
    PREMIUM_EMOJIS.append(emoji_id)
    await edit_delete(event, f"**᯽︙ تمت إضافة الإيموجي بنجاح ✓**\n**ID:** `{emoji_id}`\n**عدد الإيموجيات الآن:** `{len(PREMIUM_EMOJIS)}`")

@l313l.ar_cmd(
    pattern="حذف ايموجي (\d+)$",
    command=("حذف ايموجي", plugin_category),
    info={
        "header": "لحذف إيموجي بريميوم من القائمة",
        "description": "يحذف ID إيموجي بريميوم من قائمة الإيموجيات",
        "usage": "{tr}حذف ايموجي <ايدي_الايموجي>",
        "examples": ["{tr}حذف ايموجي 5413554183502572090"],
    },
)
async def remove_emoji(event):
    "لحذف إيموجي بريميوم من القائمة"
    emoji_id = event.pattern_match.group(1).strip()
    
    if not emoji_id.isdigit():
        return await edit_delete(event, "**᯽︙ يرجى إدخال ID صحيح للإيموجي!**")
    
    if emoji_id not in PREMIUM_EMOJIS:
        return await edit_delete(event, f"**᯽︙ الإيموجي `{emoji_id}` غير موجود في القائمة!**")
    
    PREMIUM_EMOJIS.remove(emoji_id)
    await edit_delete(event, f"**᯽︙ تم حذف الإيموجي بنجاح ✓**\n**ID:** `{emoji_id}`\n**عدد الإيموجيات المتبقية:** `{len(PREMIUM_EMOJIS)}`")

@l313l.ar_cmd(
    pattern="عرض ايموجيات$",
    command=("عرض ايموجيات", plugin_category),
    info={
        "header": "لعرض قائمة الإيموجيات البريميوم",
        "description": "يعرض جميع إيموجيات البريميوم المضافة للنظام",
        "usage": "{tr}عرض ايموجيات",
    },
)
async def show_emojis(event):
    "لعرض قائمة الإيموجيات البريميوم"
    if not PREMIUM_EMOJIS:
        return await edit_delete(event, "**᯽︙ لا توجد إيموجيات في القائمة!**\nاستخدم: `.اضافة ايموجي <ID>`")
    
    message = f"**᯽︙ قائمة الإيموجيات البريميوم:**\n\n"
    for i, emoji_id in enumerate(PREMIUM_EMOJIS, 1):
        message += f"**{i}.** `{emoji_id}`\n"
    
    message += f"\n**المجموع:** `{len(PREMIUM_EMOJIS)}` إيموجي"
    await edit_or_reply(event, message)
