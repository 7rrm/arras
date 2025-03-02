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
    # تفعيل التفاعل مع المستخدم
    addgvar(f"react_{event.chat_id}_{user.id}", "true")
    await edit_or_reply(catevent, "⌁︙تـم تفعيل التفاعل مع رسائل هذا المستخدم بنجاح ✅")


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


@l313l.ar_cmd(incoming=True, edited=False)
async def react_to_messages(event):
    "لإضافة تفاعل عشوائي على رسائل المستخدم"
    chat_id = event.chat_id
    user_id = event.sender_id
    if gvarstatus(f"react_{chat_id}_{user_id}") == "true":
        emoji = random.choice(EMOJI_LIST)  # اختيار إيموجي عشوائي من القائمة
        try:
            await event.client.send_reaction(
                entity=event.chat_id,
                message=event.id,
                reaction=emoji
            )
        except Exception as e:
            print(f"᯽︙ خطأ في التفاعل مع الرسالة:\n{str(e)}")
