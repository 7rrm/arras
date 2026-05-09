# JoKeRUB module for purging unneeded messages(usually spam or ot).
import re
import asyncio
from asyncio import sleep

from telethon.errors import rpcbaseerrors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterEmpty,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

from JoKeRUB import l313l

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID
from telethon.extensions import markdown, html
from telethon.tl import types
from telethon.tl.types import MessageEntityCustomEmoji, MessageEntityTextUrl

plugin_category = "utils"


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
        
purgelist = {}

purgetype = {
    "ب": InputMessagesFilterVoice,
    "م": InputMessagesFilterDocument,
    "ح": InputMessagesFilterGif,
    "ص": InputMessagesFilterPhotos,
    "l": InputMessagesFilterGeo,
    "غ": InputMessagesFilterMusic,
    "r": InputMessagesFilterRoundVideo,
    "ق": InputMessagesFilterEmpty,
    "ر": InputMessagesFilterUrl,
    "ف": InputMessagesFilterVideo,
    # "ك": search
}


@l313l.ar_cmd(
    pattern="مسح(\s*| \d+)$",
    command=("مسح", plugin_category),
    info={
        "header": "To delete replied message.",
        "description": "Deletes the message you replied to in x(count) seconds if count is not used then deletes immediately",
        "usage": ["{tr}del <time in seconds>", "{tr}del"],
        "examples": "{tr}del 2",
    },
)
async def delete_it(event):
    "To delete replied message."
    input_str = event.pattern_match.group(1).strip()
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ⌔︙ تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "↜︙ لا يمـكنني الـحذف احـتاج صلاحيـات الادمـن",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "✧︙ عـذرا الـرسالة غيـر موجـودة")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ⌔︙ تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "↜︙ عـذرا الـرسالة لا استـطيع حـذفها")
    elif not input_str:
        await event.delete()

@l313l.ar_cmd(pattern="رسائلي$")
async def zed(event):
    zzm = "me"
    a = await bot.get_messages(event.chat_id, 0, from_user=zzm)
    await edit_or_reply(event, f"<b>✧╎لديـك هنـا ⇽</b>  <code>{a.total}</code>  <b>رسـالـه <a href='emoji/5884510167986343350'>✉️</a></b>", parse_mode=CustomParseMode("html"))

@l313l.ar_cmd(pattern="رسائله ?(.*)")
async def zed(event):
    k = await event.get_reply_message()
    if k:
        a = await bot.get_messages(event.chat_id, 0, from_user=k.sender_id)
        return await edit_or_reply(event, f"<b>✧╎لديـه هنـا ⇽</b>  <code>{a.total}</code>  <b>رسـالـه <a href='emoji/5884510167986343350'>✉️</a></b>", parse_mode=CustomParseMode("html"))
    zzm = event.pattern_match.group(1)
    if zzm:
        a = await bot.get_messages(event.chat_id, 0, from_user=zzm)
        return await edit_or_reply(event, f"<b>✧╎المستخـدم</b> {zzm} <b>لديـه هنـا ⇽</b>  <code>{a.total}</code>  <b>رسـالـه <a href='emoji/5884510167986343350'>✉️</a></b>", parse_mode=CustomParseMode("html"))
    else:
        await edit_or_reply(event, f"<b>✧╎بالـرد ع الشخص او بـ إضافة أيـدي او يـوزر الشخـص لـ الامـر</b>", parse_mode=CustomParseMode("html"))

@l313l.ar_cmd(
    pattern="مسح رسائلي$",
    command=("مسح رسائلي", plugin_category),
    info={
        "header": "To purge your latest messages.",
        "description": "Deletes x(count) amount of your latest messages.",
        "usage": "{tr}purgeme <count>",
        "examples": "{tr}purgeme 2",
    },
)
async def Hussein(event):
    "To purge your latest messages."
    message = event.text
    count = 0
    async for message in event.client.iter_messages(event.chat_id, from_user='me'):
        count += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
    "**✧╎أنتهى التنظيف** تم حذف " + str(count) + " من الرسائل التي تم أرسالها من قبلك في المجموعة .",    
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
        "**أنتهى التنظيف** تم حذف " + str(count) + " من الرسائل التي تم إرسالها من قبلك في المجموعة.",    
    )
    await sleep(5)
    await smsg.delete()


@l313l.ar_cmd(
    pattern="مسح رسائله$",
    command=("مسح رسائله", plugin_category),
    info={
        "header": "To purge user messages.",
        "description": "Deletes all messages of replied user.",
        "usage": "{tr}مسح رسائله <reply>",
        "examples": "{tr}مسح رسائله",
    },
)
async def Hussein(event):
    "To purge user messages."
    if not event.reply_to_msg_id:
        return await event.edit("**❌ يجب الرد على رسالة المستخدم**")
    
    reply = await event.get_reply_message()
    user_id = reply.sender_id
    
    count = 0
    async for message in event.client.iter_messages(event.chat_id, from_user=user_id):
        count += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        "**أنتهى التنظيف** تم حذف " + str(count) + " من الرسائل التي تم إرسالها من قبل المستخدم في المجموعة.",    
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "**أنتهى التنظيف** تم حذف " + str(count) + " من الرسائل التي تم إرسالها من قبل المستخدم في المجموعة.",    
        )
    await asyncio.sleep(5)
    await smsg.delete()

@l313l.ar_cmd(
    pattern="تنظيف(?:\s|$)([\s\S]*)",
    command=("تنظيف", plugin_category),
    info={
        "header": "لـحذف الـرسائل .",
        "description": "•  Deletes the x(count) amount of messages from the replied message\
        \n•  If you don't use count then deletes all messages from the replied messages\
        \n•  If you haven't replied to any message and used count then deletes recent x messages.\
        \n•  If you haven't replied to any message or havent mentioned any flag or count then doesnt do anything\
        \n•  If flag is used then selects that type of messages else will select all types\
        \n•  You can use multiple flags like -gi 10 (It will delete 10 images and 10 gifs but not 10 messages of combination images and gifs.)\
        ",
        "الاضافه": {
            "البصمات": "لحـذف الرسائل الـصوتية.",
            "الملفات": "لحـذف الملفات.",
            "المتحركه": "لحـذف المتحـركه.",
            "الصور": "لحـذف الـصور",
            "الاغاني": "لحـذف الاغاني",
            "الملصقات": "لحـذف الـملصقات",
            "الروابط": "لحـذف الـروابط",
            "الفديوهات": "لحـذف الفـيديوهـات",
            "كلمه": " لحذف جميع النصوص التي تحتوي هذه الكلمه في الكروب",
        },
        "ااستخدام": [
            "{tr}تنظيف <الاضافه(optional)> <count(x)> <reply> - to delete x flagged messages after reply",
            "{tr}تنظيف <الاضافه> <رقم> - لحذف رسائل الاضافه",
        ],
        "examples": [
            "{tr}تنظيف 40",
            "{tr}تنظيف -المتحركه 40",
            "{tr}تنظيف -كلمه الجوكر",
        ],
    },
)
async def fastpurger(event):  # sourcery no-metrics
    "To purge messages from the replied message"
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            if p_type is not None:
                for ty in p_type:
                    if ty in purgetype:
                        async for msg in event.client.iter_messages(
                            event.chat_id,
                            limit=int(input_str),
                            offset_id=reply.id - 1,
                            reverse=True,
                            filter=purgetype[ty],
                        ):
                            count += 1
                            msgs.append(msg)
                            if len(msgs) == 50:
                                await event.client.delete_messages(chat, msgs)
                                msgs = []
                        if msgs:
                            await event.client.delete_messages(chat, msgs)
                    elif ty == "كلمه":
                        error += f"\n᯽︙ الاضافه خـطأ"
                    else:
                        error += f"\n\n ✧︙ `{ty}`  : هـذه أضافـة خاطئـة "
            else:
                count += 1
                async for msg in event.client.iter_messages(
                    event.chat_id,
                    limit=(int(input_str) - 1),
                    offset_id=reply.id,
                    reverse=True,
                ):
                    msgs.append(msg)
                    count += 1
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
        elif input_str and p_type is not None:
            if p_type == "كلمه":
                try:
                    cont, inputstr = input_str.split(" ")
                except ValueError:
                    cont = "error"
                    inputstr = input_str
                cont = cont.strip()
                inputstr = inputstr.strip()
                if cont.isnumeric():
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        limit=int(cont),
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=inputstr,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                else:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=input_str,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            else:
                error += f"\n ✧︙ `{ty}`  : هـذه أضافـة خاطئـة "
        elif input_str:
            error += f"\n ✧︙ `.تنظيف {input_str}` الامـر خـطأ يـرجى الكتابة بـشكل صحيح"
        elif p_type is not None:
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        filter=purgetype[ty],
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                else:
                    error += f"\n ✧︙ `{ty}`  : هـذه أضافـة خاطئـة"
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id - 1
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
    elif p_type is not None and input_str:
        if p_type != "كلمه" and input_str.isnumeric():
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id, limit=int(input_str), filter=purgetype[ty]
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                elif ty == "الكتابه":
                    error += f"\n ✧︙ لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه"
                else:
                    error += f"\n ✧︙ `{ty}`  : هـذه أضافـة خاطئـة "
        elif p_type == "كلمه":
            try:
                cont, inputstr = input_str.split(" ")
            except ValueError:
                cont = "error"
                inputstr = input_str
            cont = cont.strip()
            inputstr = inputstr.strip()
            if cont.isnumeric():
                async for msg in event.client.iter_messages(
                    event.chat_id, limit=int(cont), search=inputstr
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            else:
                async for msg in event.client.iter_messages(
                    event.chat_id, search=input_str
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
        else:
            error += f"\n ✧︙ `{ty}`  : هـذه أضافـة خاطئـة "
    elif p_type is not None:
        for ty in p_type:
            if ty in purgetype:
                async for msg in event.client.iter_messages(
                    event.chat_id, filter=purgetype[ty]
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            elif ty == "كلمه":
                error += f"\n ✧︙ لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه"
            else:
                error += f"\n ✧︙ `{ty}`  : هـذه أضافـة خاطئـة "
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(chat, limit=int(input_str) + 1):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
    else:
        error += "\n ✧︙ لم يتـم تحـديد اضافـة يرجى ارسال  (`.اوامر التنظيف`) و رؤية اوامر التنظيف"
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "✧︙ اكـتمل الـتنظيف السـريع\n᯽︙ تـم حـذفㅤ" +  str(count)  + "ㅤمن الـرسائل"
    if error != "":
        result += f"\n\n**خـطأ:**{error}"
    if result == "":
        result += "✧︙ لا تـوجد رسـائل لـتنظيفها"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#التنـظيف \n{result}",
        )
    await sleep(5)
    await hi.delete()


@l313l.ar_cmd(pattern="احذف (.*)")
async def _(event):
    exe = event.text[5:]
    await l313l.get_dialogs()
    chat = exe
    await l313l.delete_dialog(chat, revoke=True)
    await edit_or_reply(event, "**⎉╎تم حذف الدردشة مع المستخدم .. بنجـاح ✓**")

from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import re
from ..core.managers import edit_or_reply
from ..Config import Config
from . import l313l
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

# =========================================================== #
# أنواع التنظيف
# =========================================================== #

purgetype = {
    "البصمات": InputMessagesFilterVoice,
    "الملفات": InputMessagesFilterDocument,
    "المتحركة": InputMessagesFilterGif,
    "الصور": InputMessagesFilterPhotos,
    "الاغاني": InputMessagesFilterMusic,
    "فيديو": InputMessagesFilterVideo,
    "الروابط": InputMessagesFilterUrl,
}

# =========================================================== #
# الاستعلام المضمن (تنظيف) - مع تمرير chat_id
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_clean_handler(event):
        builder = event.builder
        query = event.text
        
        if query.startswith("تنظيف") and event.query.user_id == l313l.uid:
            # ❌ لا يمكن الحصول على chat_id هنا
            # ✅ لذلك سنستقبله من المستخدم
            
            # ننتظر المستخدم يرسل chat_id (لكن هذا غير عملي)
            # الحل: تخزين chat_id في متغير مؤقت من الأمر السابق
            
            # بدلاً من ذلك، سنستخدم زر "تحديد الدردشة الحالية"
            buttons = [
                [Button.inline("📍 استخدام هذه الدردشة", data=f"clean_use_current", style="primary")],
                [Button.inline("❌ إلغاء", data="clean_cancel", style="danger")]
            ]
            
            text = "**🧹 تنظيف الدردشة**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\n"
            text += "⚠️ لا يمكن للبوت معرفة الدردشة تلقائياً.\n"
            text += "اضغط على الزر أدناه لاستخدام الدردشة الحالية:"
            
            result = builder.article(
                title="🧹 تنظيف المجموعة",
                description="اختر نوع الوسائط لحذفها",
                text=text,
                buttons=buttons,
                link_preview=False,
            )
            
            await event.answer([result], cache_time=0)

# =========================================================== #
# معالج استخدام الدردشة الحالية
# =========================================================== #

# قاموس مؤقت لتخزين chat_id
temp_chats = {}

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_use_current")))
async def clean_use_current(event):
    user_id = event.query.user_id
    
    if user_id != l313l.uid:
        return await event.answer("⚠️ هذا الأمر للمطور فقط!", alert=True)
    
    # ✅ الآن نعرف الدردشة (لأنها من CallbackQuery)
    target_chat_id = event.chat_id
    
    # حفظ chat_id مؤقتاً لاستخدامه في الخطوة التالية
    temp_chats[user_id] = target_chat_id
    
    # عرض أنواع التنظيف
    buttons = []
    row = []
    for name in purgetype.keys():
        row.append(Button.inline(name, data=f"clean_do_{name}", style="primary"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([Button.inline("🗑️ الكل", data="clean_do_all", style="danger")])
    buttons.append([Button.inline("❌ إلغاء", data="clean_cancel", style="danger")])
    
    text = "**🧹 اختر نوع التنظيف**\n⋆┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n\nاختر نوع الوسائط التي تريد حذفها:"
    
    await event.edit(text, buttons=buttons, parse_mode="Markdown")

# =========================================================== #
# معالج التنظيف الفعلي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_do_(.*)")))
async def clean_do_handler(event):
    clean_type = event.data_match.group(1).decode()
    user_id = event.query.user_id
    
    if user_id != l313l.uid:
        return await event.answer("⚠️ هذا الأمر للمطور فقط!", alert=True)
    
    # الحصول على chat_id من القاموس المؤقت
    target_chat_id = temp_chats.get(user_id)
    
    if not target_chat_id:
        return await event.edit("❌ حدث خطأ: لم يتم تحديد الدردشة.\nاستخدم الأمر مرة أخرى.", buttons=None)
    
    await event.edit(f"🧹 جاري حذف {clean_type}...", buttons=None)
    
    count = 0
    msgs = []
    
    try:
        filter_type = None if clean_type == "all" else purgetype.get(clean_type)
        
        async for msg in l313l.iter_messages(target_chat_id, filter=filter_type):
            count += 1
            msgs.append(msg)
            if len(msgs) >= 100:
                await l313l.delete_messages(target_chat_id, msgs)
                msgs = []
        if msgs:
            await l313l.delete_messages(target_chat_id, msgs)
        
        await event.edit(f"✅ تم حذف {count} من رسائل {clean_type}", buttons=None)
        
    except Exception as e:
        await event.edit(f"❌ حدث خطأ: {str(e)[:100]}", buttons=None)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"clean_cancel")))
async def clean_cancel(event):
    user_id = event.query.user_id
    
    if user_id != l313l.uid:
        return await event.answer("⚠️ هذا الأمر للمطور فقط!", alert=True)
    
    await event.edit("❌ تم إلغاء التنظيف", buttons=None)

# =========================================================== #
# أمر تنظيف
# =========================================================== #

@l313l.ar_cmd(pattern="التنظيف$")
async def clean_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "تنظيف")
    if response:
        await response[0].click(event.chat_id)
        await event.delete()
    else:
        await event.edit("❌ فشل في فتح قائمة التنظيف")
