import os
from telethon import Button, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from ..Config import Config
from ..helpers.utils import reply_id
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

LOGS = logging.getLogger(os.path.basename(__name__))

async def get_user_from_event(event):
    """الحصول على المستخدم من الحدث (رد أو معرف أو ذكر)."""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(f"**⎉╎حدث خطأ: {str(err)}**")
            return None
    return user_object

async def get_user_info(user, event):
    """الحصول على معلومات المستخدم (الاسم، المعرف، الرقم)."""
    full_user = (await event.client(GetFullUserRequest(user.id))).full_user
    first_name = user.first_name or ""
    full_name = full_user.private_forward_name or first_name
    username = f"@{user.username}" if user.username else "None"
    return user.id, full_name, username

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def send_secret_message(event):
    """إرسال همسة سرية إلى مستخدم معين."""
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return await event.edit("**⎉╎يجب الرد على مستخدم أو كتابة معرفه!**")

    # الحصول على معلومات المستخدم
    try:
        target_user = await get_user_from_event(event)
        user_id, full_name, username = await get_user_info(target_user, event)
    except Exception as e:
        return await event.edit(f"**⎉╎حدث خطأ: {str(e)}**")

    # حفظ معلومات المستخدم في المتغيرات العامة
    delgvar("hmsa_id")
    delgvar("hmsa_name")
    delgvar("hmsa_user")
    addgvar("hmsa_id", user_id)
    addgvar("hmsa_name", full_name)
    addgvar("hmsa_user", username)

    # إنشاء زر الهمسة
    button_text = "اضـغـط هنـا"
    query = f"secret {gvarstatus('hmsa_id')} \nهلو"
    button = [Button.switch_inline(button_text, query=query, same_peer=True)]

    # إرسال الاستعلام إلى البوت
    try:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "zelzal")
        if response:
            await response[0].click(event.chat_id)
            await event.delete()
        else:
            await event.edit("**⎉╎عـذراً .. لم أتمكن من العثور على نتائج**")
    except Exception as e:
        await event.edit(f"**⎉╎حدث خطأ: {str(e)}**")
