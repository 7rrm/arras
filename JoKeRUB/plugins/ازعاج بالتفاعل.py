"""
created by @YourUsername
Idea by @YourUsername
"""

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import (
    l313l,
    edit_delete,
    get_user_from_event,
)
import random  # لإختيار إيموجي عشوائي

plugin_category = "fun"

# قائمة الإيموجيات التي سيتم استخدامها
EMOJI_LIST = ["👍", "❤️", "🔥", "🎉", "😂", "😍", "🤔", "👏", "🙌", "😎"]

@l313l.ar_cmd(
    pattern="تفاعل$",
    command=("تفاعل", plugin_category),
    info={
        "header": "لتفعيل التفاعل مع رسائل المستخدم.",
        "description": "الرد على المستخدم بهذا الأمر لإضافة تفاعل (إيموجي) على جميع رسائله.",
        "usage": "{tr}تفاعل <رد>",
    },
)
async def react(event):
    "لتفعيل التفاعل مع رسائل المستخدم"
    if event.reply_to_msg_id is None:
        return await edit_delete(event, "⌁︙يرجى الرد على الشخص الذي تـريد التفاعل مع رسائله.")
    catevent = await edit_or_reply(event, "⌁︙يتم تفعيل هذا الأمر، انتظر قليلاً...")
    user, rank = await get_user_from_event(event, catevent, nogroup=True)
    if not user:
        return
    if user.id == 5427469031:  # يمكنك تغيير هذا الرقم إلى أي رقم آخر (مثلًا، لمنع التفاعل مع مطور البوت)
        return await edit_delete(event, "**᯽︙ لا يمكنني التفاعل مع رسائل مطوري! **")
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = event.chat.title
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "⌁︙تـم تفعيل التفاعل مع رسائل هذا المستخدم مسبقًا ✅")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(catevent, f"᯽︙ خطأ:\n`{str(e)}`")
    else:
        await edit_or_reply(catevent, "⌁︙تـم تفعيل التفاعل مع رسائل هذا المستخدم بنجاح ✅\n⌁︙سيتم التفاعل مع جميع رسائله هنا.")


@l313l.ar_cmd(
    pattern="ايقاف التفاعل",
    command=("ايقاف التفاعل", plugin_category),
    info={
        "header": "لإيقاف التفاعل مع رسائل المستخدم.",
        "description": "الرد على المستخدم بهذا الأمر لإيقاف التفاعل مع رسائله.",
        "usage": "{tr}ايقاف التفاعل <رد>",
    },
)
async def stop_react(event):
    "لإيقاف التفاعل مع رسائل المستخدم"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(event, "⌁︙يرجى الرد على الشخص الذي تـريد إيقاف التفاعل مع رسائله.")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edit_delete(event, f"᯽︙ خطأ:\n`{str(e)}`")
        else:
            await edit_or_reply(event, "⌁︙تـم إيقاف التفاعل مع رسائل هذا المستخدم بنجاح ✅")
    else:
        await edit_or_reply(event, "⌁︙لم يتم تفعيل التفاعل مع رسائل هذا المستخدم ⚠️")


@l313l.ar_cmd(
    pattern="الغاء التفاعل( -a)?",
    command=("الغاء التفاعل", plugin_category),
    info={
        "header": "لإيقاف التفاعل مع جميع المستخدمين في هذه الدردشة.",
        "description": "لإيقاف التفاعل مع جميع المستخدمين في هذه الدردشة أو جميع الدردشات.",
        "flags": {"a": "لإيقاف التفاعل في جميع الدردشات"},
        "usage": [
            "{tr}الغاء التفاعل",
            "{tr}الغاء التفاعل -a",
        ],
    },
)
async def remove_react(event):
    "لإيقاف التفاعل مع جميع المستخدمين"
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(event, "⌁︙لم يتم تفعيل التفاعل مع أي شخص بالاصل ⚠️")
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"᯽︙ خطأ:\n`{str(e)}`", 10)
        else:
            await edit_or_reply(event, "⌁︙تـم إيقاف التفاعل مع جميع المستخدمين بنجاح ✅")
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(event, "⌁︙لم يتم تفعيل التفاعل مع أي شخص في هذه الدردشة ⚠️")
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"᯽︙ خطأ:\n`{str(e)}`", 10)
        else:
            await edit_or_reply(event, "⌁︙تـم إيقاف التفاعل مع جميع المستخدمين في هذه الدردشة بنجاح ✅")


@l313l.ar_cmd(
    pattern="قائمة المتفاعلين( -a)?$",
    command=("قائمة المتفاعلين", plugin_category),
    info={
        "header": "لعرض قائمة المستخدمين الذين تم التفاعل مع رسائلهم.",
        "flags": {
            "a": "لعرض المستخدمين في جميع الدردشات",
        },
        "usage": [
            "{tr}قائمة المتفاعلين",
            "{tr}قائمة المتفاعلين -a",
        ],
    },
)
async def list_react(event):
    "لعرض قائمة المستخدمين الذين تم التفاعل مع رسائلهم"
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "⌁︙قائمة الأشخاص الذين تم التفاعل مع رسائلهم:\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) > 0:
            for echos in lsts:
                if echos.chat_type == "Personal":
                    if echos.user_username:
                        private_chats += f"⌁︙ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    else:
                        private_chats += f"⌁︙ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                else:
                    if echos.user_username:
                        group_chats += f"⌁︙ [{echos.user_name}](https://t.me/{echos.user_username}) في الدردشة {echos.chat_name} (ID: `{echos.chat_id}`)\n"
                    else:
                        group_chats += f"⌁︙ [{echos.user_name}](tg://user?id={echos.user_id}) في الدردشة {echos.chat_name} (ID: `{echos.chat_id}`)\n"
        else:
            return await edit_or_reply(event, "⌁︙لم يتم تفعيل التفاعل مع أي شخص بالاصل ⚠️")
        if private_chats != "":
            output_str += "⌁︙الـدردشـات الـخاصة\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "⌁︙دردشـات الـمجموعات\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(event, "⌁︙لم يتم تفعيل التفاعل مع أي شخص في هذه الدردشة ⚠️")
        for echos in lsts:
            if echos.user_username:
                private_chats += f"⌁︙ [{echos.user_name}](https://t.me/{echos.user_username})\n"
            else:
                private_chats += f"⌁︙ [{echos.user_name}](tg://user?id={echos.user_id})\n"
        output_str = f"⌁︙الأشخاص الذين تم التفاعل مع رسائلهم في هذه الدردشة:\n" + private_chats

    await edit_or_reply(event, output_str)


@l313l.ar_cmd(incoming=True, edited=False)
async def react_to_messages(event):
    "لإضافة تفاعل عشوائي على رسائل المستخدم"
    if is_echo(event.chat_id, event.sender_id):
        emoji = random.choice(EMOJI_LIST)  # اختيار إيموجي عشوائي من القائمة
        try:
            await event.react(emoji)
        except Exception as e:
            print(f"᯽︙ خطأ في التفاعل مع الرسالة:\n{str(e)}")
