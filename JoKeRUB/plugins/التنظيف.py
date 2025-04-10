# JoKeRUB module for purging unneeded messages(usually spam or ot).
import re
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

plugin_category = "utils"


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
                        BOTLOG_CHATID, "#الـمسـح \n ᯽︙ تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "↜︙ لا يمـكنني الـحذف احـتاج صلاحيـات الادمـن",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "᯽︙ عـذرا الـرسالة غيـر موجـودة")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ᯽︙ تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "↜︙ عـذرا الـرسالة لا استـطيع حـذفها")
    elif not input_str:
        await event.delete()

@l313l.ar_cmd(
    pattern="رسائلي$",
    command=("رسائلي", plugin_category),
    info={
        "header": "لعرض عدد رسائلك في الدردشة",
        "description": "يظهر عدد الرسائل التي أرسلتها في الدردشة الحالية (خاص أو مجموعة) - بالإحصاء الكامل",
        "usage": "{tr}رسائلي",
    },
)
async def my_messages_count(event):
    "لعرض عدد رسائلك في الدردشة (بدقة عالية وسرعة)"
    try:
        # الطريقة الأسرع مع الحفاظ على الدقة
        count = await event.client.get_messages_count(
            event.chat_id,
            from_user='me',
            limit=0  # 0 يعني جميع الرسائل دون حدود
        )
        await edit_or_reply(event, f"↜︙ عدد رسائلك في هذه الدردشة: **{count}** رسالة")
    except Exception as e:
        await edit_or_reply(event, f"᯽︙ حدث خطأ أثناء العد: `{str(e)}`")


@l313l.ar_cmd(
    pattern="رسائله(?: |$)(.*)",
    command=("رسائله", plugin_category),
    info={
        "header": "لعرض عدد رسائل المستخدم (بدقة عالية)",
        "description": "يظهر عدد رسائل المستخدم الذي تم الرد عليه أو تحديده باليوزر - بالإحصاء الكامل",
        "usage": [
            "{tr}رسائله بالرد على المستخدم",
            "{tr}رسائله + يوزر المستخدم",
        ],
    },
)
async def user_messages_count(event):
    "لعرض عدد رسائل المستخدم (بدقة وسرعة)"
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    
    if reply:
        user_id = reply.sender_id
    elif input_str:
        try:
            user = await event.client.get_entity(input_str)
            user_id = user.id
        except ValueError:
            return await edit_or_reply(event, "↜︙ لم يتم العثور على المستخدم!")
    else:
        return await edit_or_reply(event, "↜︙ يجب الرد على المستخدم أو كتابة يوزره مع الأمر!")
    
    try:
        # الطريقة المثلى للسرعة والدقة
        count = await event.client.get_messages_count(
            event.chat_id,
            from_user=user_id,
            limit=0  # 0 يعني جميع الرسائل
        )
        user = await event.client.get_entity(user_id)
        await edit_or_reply(event, f"↜︙ عدد رسائل [{user.first_name}](tg://user?id={user.id}) في هذه الدردشة: **{count}** رسالة")
    except Exception as e:
        await edit_or_reply(event, f"↜︙ حدث خطأ أثناء العد: `{str(e)}`")

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
    "**أنتهى التنظيف** تم حذف " + str(count) + " من الرسائل التي تم إرسالها من قبلك في المجموعة.",    
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
        "**أنتهى التنظيف** تم حذف " + str(count) + " من الرسائل التي تم إرسالها من قبلك في المجموعة.",    
    )
    await sleep(5)
    await smsg.delete()


# TODO: only sticker messages.
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
                        error += f"\n\n᯽︙ `{ty}`  : هـذه أضافـة خاطئـة "
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
                error += f"\n᯽︙ `{ty}`  : هـذه أضافـة خاطئـة "
        elif input_str:
            error += f"\n᯽︙ `.تنظيف {input_str}` الامـر خـطأ يـرجى الكتابة بـشكل صحيح"
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
                    error += f"\n᯽︙ `{ty}`  : هـذه أضافـة خاطئـة"
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
                    error += f"\n᯽︙ لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه"
                else:
                    error += f"\n᯽︙ `{ty}`  : هـذه أضافـة خاطئـة "
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
            error += f"\n᯽︙ `{ty}`  : هـذه أضافـة خاطئـة "
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
                error += f"\n᯽︙ لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه"
            else:
                error += f"\n᯽︙ `{ty}`  : هـذه أضافـة خاطئـة "
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
        error += "\n᯽︙ لم يتـم تحـديد اضافـة يرجى ارسال  (`.اوامر التنظيف`) و رؤية اوامر التنظيف"
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "᯽︙ اكـتمل الـتنظيف السـريع\n᯽︙ تـم حـذفㅤ" +  str(count)  + "ㅤمن الـرسائل"
    if error != "":
        result += f"\n\n**خـطأ:**{error}"
    if result == "":
        result += "᯽︙ لا تـوجد رسـائل لـتنظيفها"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#التنـظيف \n{result}",
        )
    await sleep(5)
    await hi.delete()
