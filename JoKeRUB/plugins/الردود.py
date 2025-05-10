import re
import random

from JoKeRUB import l313l

from ..core.managers import edit_or_reply
from ..sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"
ROZTEXT = "عـذرا لا يمكـنك اضافـة رد هـنا"

# قائمة كلايش الترحيب
WELCOME_MESSAGES = [
    "**يڪَِـمـࢪ نـورِت .**",
    "**نـوࢪت .**",
    "**ءنَـرت**",
    "**شـهالـڪيڪ بـڪروبنــا .**",
    "**ضَـۅويت .**",
]

# دالة للحصول على قائمة المجموعات المفعلة للترحيب
def get_welcome_chats():
    welcome_chats = gvarstatus("WELCOME_CHATS")
    return set(map(int, welcome_chats.split(","))) if welcome_chats else set()

# دالة لإضافة مجموعة إلى قائمة المجموعات المفعلة للترحيب
def add_welcome_chat(chat_id):
    welcome_chats = get_welcome_chats()
    welcome_chats.add(chat_id)
    addgvar("WELCOME_CHATS", ",".join(map(str, welcome_chats)))

# دالة لإزالة مجموعة من قائمة المجموعات المفعلة للترحيب
def remove_welcome_chat(chat_id):
    welcome_chats = get_welcome_chats()
    welcome_chats.discard(chat_id)
    if welcome_chats:
        addgvar("WELCOME_CHATS", ",".join(map(str, welcome_chats)))
    else:
        delgvar("WELCOME_CHATS")

@l313l.ar_cmd(incoming=True)
async def filter_incoming_handler(handler):  # sourcery no-metrics
    if handler.sender_id == handler.client.uid:
        return
    name = handler.raw_text
    filters = get_filters(handler.chat_id)
    if not filters:
        return
    a_user = await handler.get_sender()
    chat = await handler.get_chat()
    me = await handler.client.get_me()
    title = chat.title or "this chat"
    participants = await handler.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            if trigger.f_mesg_id:
                msg_o = await handler.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                await handler.reply(
                    msg_o.message.format(
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
                    ),
                    file=msg_o.media,
                )
            elif trigger.reply:
                await handler.reply(
                    trigger.reply.format(
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
                    ),
                )

@l313l.ar_cmd(
    pattern="رد ([\s\S]*)",
    command=("رد", plugin_category),
    info={
        "header": "To save filter for the given keyword.",
        "description": "If any user sends that filter then your bot will reply.",
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
        "note": "For saving media/stickers as filters you need to set PRIVATE_GROUP_BOT_API_ID.",
        "usage": "{tr}filter <keyword>",
    },
)
async def add_new_filter(new_handler):
    "To save the filter"
    keyword = new_handler.pattern_match.group(1)
    string = new_handler.text.partition(keyword)[2]
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await new_handler.client.send_message(
                BOTLOG_CHATID,
                f"#الــرد\
            \nايدي الدردشه: {new_handler.chat_id}\
            \nالـكيبورد: {keyword}\
            \n\nالرسالة التالية حفظت كرد ارسل معلومات الرد لرؤية الرد  ،  لاتقم بحذف ارسالة !!",
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                new_handler,
                "⌯︙يتطلب حفظ الوسائط كرد  تعيين PRIVATE_GROUP_BOT_API_ID\n قـم بعمل مجموعه وقم باخذ ايدي المجموعه عبر اي بوت بعدها ارسل\n .set var PRIVATE_GROUP_BOT_API_ID + ايدي المجموعة ",
            )
            return
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "**᯽︙ الـرد {} تـم اضـافتة بنـجـاح ✓**"
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "added"))
    remove_filter(str(new_handler.chat_id), keyword)
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(new_handler, success.format(keyword, "Updated"))
    await edit_or_reply(new_handler, f"Error while setting filter for {keyword}")

@l313l.ar_cmd(
    pattern="تفعيل ترحيب الايدي$",
    command=("تفعيل ترحيب الايدي", plugin_category),
    info={
        "header": "To enable welcome messages in the current chat.",
        "description": "When enabled, the bot will automatically reply with a welcome message when a user sends 'ا'.",
        "usage": "{tr}تفعيل ترحيب الايدي",
    },
)
async def enable_welcome(event):
    "To enable welcome messages in the current chat."
    chat_id = event.chat_id
    add_welcome_chat(chat_id)
    await edit_or_reply(event, "**تم تفعيل الترحيب في هذه المجموعة بنجاح ✓**")

@l313l.ar_cmd(
    pattern="تعطيل ترحيب الايدي$",
    command=("تعطيل ترحيب الايدي", plugin_category),
    info={
        "header": "To disable welcome messages in the current chat.",
        "description": "When disabled, the bot will no longer send welcome messages in this chat.",
        "usage": "{tr}تعطيل ترحيب الايدي",
    },
)
async def disable_welcome(event):
    "To disable welcome messages in the current chat."
    chat_id = event.chat_id
    remove_welcome_chat(chat_id)
    await edit_or_reply(event, "**تم تعطيل الترحيب في هذه المجموعة بنجاح ✓**")

@l313l.ar_cmd(incoming=True)
async def welcome_message(handler):
    if handler.sender_id == handler.client.uid:
        return
    chat_id = handler.chat_id
    welcome_chats = get_welcome_chats()
    if chat_id not in welcome_chats:
        return
    if handler.raw_text == "ا":
        a_user = await handler.get_sender()
        mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
        welcome_message = random.choice(WELCOME_MESSAGES).format(mention=mention)
        await handler.reply(welcome_message)


@l313l.ar_cmd(
    pattern="الردود$",
    command=("الردود", plugin_category),
    info={
        "header": "To list all filters in that chat.",
        "description": "Lists all active (of your userbot) filters in a chat.",
        "usage": "{tr}filters",
    },
)
async def on_snip_list(event):
    "To list all filters in that chat."
    OUT_STR = "**᯽︙لا توجد ردود مضافة في هذه الدردشه  🔍**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "**᯽︙لا توجد ردود مضافة في هذه الدردشة  🔍**":
            OUT_STR = "**᯽︙الردود التي تم اضافتها في هذه الدردشة**\n"
        OUT_STR += "⌯︙{}\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="Available Filters in the Current Chat",
        file_name="filters.text",
    )


@l313l.ar_cmd(
    pattern="حذف رد ([\s\S]*)",
    command=("حذف رد", plugin_category),
    info={
        "header": "To delete that filter . so if user send that keyword bot will not reply",
        "usage": "{tr}stop <keyword>",
    },
)
async def remove_a_filter(r_handler):
    "Stops the specified keyword."
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("**᯽︙الـرد {} غير موجود **".format(filt))
    else:
        await r_handler.edit("**᯽︙ الـرد {} تـم حـذفة بنـجـاح ✓**".format(filt))


@l313l.ar_cmd(
    pattern="حذف الردود$",
    command=("حذف الردود", plugin_category),
    info={
        "header": "To delete all filters in that group.",
        "usage": "{tr}rmfilters",
    },
)
async def on_all_snip_delete(event):
    "To delete all filters in that group."
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, f"**᯽︙ تم حذف الردود في الدردشة الحالية بنجاح ✓**")
    else:
        await edit_or_reply(event, f"᯽︙لا توجد ردود في هذه المجموعة  ")


# قائمة رموز التوحيد لكل مجموعة
UNITY_SYMBOLS = {}

# دالة للحصول على قائمة المجموعات المفعلة للتوحيد
def get_unity_chats():
    unity_chats = gvarstatus("UNITY_CHATS")
    return set(map(int, unity_chats.split(","))) if unity_chats else set()

# دالة للحصول على رمز التوحيد لمجموعة معينة
def get_unity_symbol(chat_id):
    return UNITY_SYMBOLS.get(chat_id, "⍣")

# دالة لإضافة مجموعة إلى قائمة المجموعات المفعلة للتوحيد
def add_unity_chat(chat_id, symbol="⍣"):
    unity_chats = get_unity_chats()
    unity_chats.add(chat_id)
    UNITY_SYMBOLS[chat_id] = symbol
    addgvar("UNITY_CHATS", ",".join(map(str, unity_chats)))

# دالة لإزالة مجموعة من قائمة المجموعات المفعلة للتوحيد
def remove_unity_chat(chat_id):
    unity_chats = get_unity_chats()
    unity_chats.discard(chat_id)
    if chat_id in UNITY_SYMBOLS:
        del UNITY_SYMBOLS[chat_id]
    if unity_chats:
        addgvar("UNITY_CHATS", ",".join(map(str, unity_chats)))
    else:
        delgvar("UNITY_CHATS")

@l313l.ar_cmd(
    pattern="تفعيل التوحيد(?:\\s+(.*))?$",
    command=("تفعيل التوحيد", plugin_category),
    info={
        "header": "لتفعيل رسائل التوحيد في المجموعة الحالية",
        "description": "عند التفعيل، سيقوم البوت بالرد برمز التوحيد عندما يرسل أحد الأعضاء 'توحيد'",
        "استخدام": [
            "{tr}تفعيل التوحيد",
            "{tr}تفعيل التوحيد [الرمز]",
        ],
        "أمثلة": [
            "{tr}تفعيل التوحيد ⍣",
        ],
    },
)
async def enable_unity(event):
    "لتفعيل رسائل التوحيد في المجموعة الحالية"
    chat_id = event.chat_id
    symbol = event.pattern_match.group(1) or "⍣"
    add_unity_chat(chat_id, symbol)
    await edit_or_reply(
        event, 
        f"**تم تفعيل التوحيد في هذه المجموعة بنجاح ✓**\n"
        f"**رمز التوحيد:** `{symbol}`"
    )

@l313l.ar_cmd(
    pattern="تعطيل التوحيد$",
    command=("تعطيل التوحيد", plugin_category),
    info={
        "header": "لتعطيل رسائل التوحيد في المجموعة الحالية",
        "description": "عند التعطيل، لن يرسل البوت رسائل التوحيد في هذه المجموعة",
        "استخدام": "{tr}تعطيل التوحيد",
    },
)
async def disable_unity(event):
    "لتعطيل رسائل التوحيد في المجموعة الحالية"
    chat_id = event.chat_id
    remove_unity_chat(chat_id)
    await edit_or_reply(event, "**تم تعطيل التوحيد في هذه المجموعة بنجاح ✓**")

@l313l.ar_cmd(incoming=True)
async def unity_message(handler):
    if handler.sender_id == handler.client.uid:
        return
    chat_id = handler.chat_id
    unity_chats = get_unity_chats()
    if chat_id not in unity_chats:
        return
    
    if handler.raw_text.strip() == "توحيد":
        symbol = get_unity_symbol(chat_id)
        response = (
            f"**التوحيد هوَ  ❬ `{symbol}` ❭ أضغِط للنسَخ .**\n\n"
            f"`{symbol}`"
        )
        await handler.reply(response)
