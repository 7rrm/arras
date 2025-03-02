"""
تفاعل تلقائي مع رسائل المستخدم بإيموجي
تم الإنشاء بواسطة @YourUsername
"""

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import l313l, get_user_from_event
import random

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
async def enable_react(event):
    "لتفعيل التفاعل مع رسائل المستخدم"
    if event.reply_to_msg_id is None:
        return await edit_delete(event, "⌁︙يرجى الرد على الشخص الذي تـريد التفاعل مع رسائله.")
    catevent = await edit_or_reply(event, "⌁︙يتم تفعيل هذا الأمر، انتظر قليلاً...")
    user, _ = await get_user_from_event(event, catevent, nogroup=True)
    if not user:
        return
    if user.id == 705475246:  # يمكنك تغيير هذا الرقم إلى أي رقم آخر (مثلًا، لمنع التفاعل مع مطور البوت)
        return await edit_delete(event, "**᯽︙ لا يمكنني التفاعل مع رسائل مطوري! **")
    # تفعيل التفاعل مع المستخدم
    addgvar(f"react_{event.chat_id}_{user.id}", "true")
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
async def disable_react(event):
    "لإيقاف التفاعل مع رسائل المستخدم"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(event, "⌁︙يرجى الرد على الشخص الذي تـريد إيقاف التفاعل مع رسائله.")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    # إيقاف التفاعل مع المستخدم
    delgvar(f"react_{chat_id}_{user_id}")
    await edit_or_reply(event, "⌁︙تـم إيقاف التفاعل مع رسائل هذا المستخدم بنجاح ✅")


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
        # إيقاف التفاعل في جميع الدردشات
        for var in list(gvarstatus()):
            if var.startswith("react_"):
                delgvar(var)
        await edit_or_reply(event, "⌁︙تـم إيقاف التفاعل مع جميع المستخدمين في جميع الدردشات بنجاح ✅")
    else:
        # إيقاف التفاعل في الدردشة الحالية فقط
        chat_id = event.chat_id
        for var in list(gvarstatus()):
            if var.startswith(f"react_{chat_id}_"):
                delgvar(var)
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
    output_str = "⌁︙قائمة الأشخاص الذين تم التفاعل مع رسائلهم:\n\n"
    if input_str:
        # عرض جميع المستخدمين في جميع الدردشات
        for var in list(gvarstatus()):
            if var.startswith("react_"):
                _, chat_id, user_id = var.split("_")
                output_str += f"⌁︙ المستخدم: {user_id} في الدردشة: {chat_id}\n"
    else:
        # عرض المستخدمين في الدردشة الحالية فقط
        chat_id = event.chat_id
        for var in list(gvarstatus()):
            if var.startswith(f"react_{chat_id}_"):
                _, _, user_id = var.split("_")
                output_str += f"⌁︙ المستخدم: {user_id}\n"
    await edit_or_reply(event, output_str)


@l313l.ar_cmd(incoming=True, edited=False)
async def react_to_messages(event):
    "لإضافة تفاعل عشوائي على رسائل المستخدم"
    chat_id = event.chat_id
    user_id = event.sender_id
    if gvarstatus(f"react_{chat_id}_{user_id}") == "true":
        emoji = random.choice(EMOJI_LIST)  # اختيار إيموجي عشوائي من القائمة
        try:
            await event.react(emoji)
        except Exception as e:
            print(f"᯽︙ خطأ في التفاعل مع الرسالة:\n{str(e)}")
