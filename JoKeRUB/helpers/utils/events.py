import base64

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import MessageEntityMentionName

from ...Config import Config
from ...core.logger import logging
from ...core.managers import edit_delete

LOGS = logging.getLogger(__name__)


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def get_user_from_event(event):
    """ نسخة معدلة متوافقة مع السورس الجديد """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        try:
            user_object = await event.client.get_entity(previous_message.sender_id)
            return user_object
        except Exception as e:
            await edit_or_reply(event, f"**خطأ في جلب المستخدم:** {str(e)}")
            return None
    
    args = event.pattern_match.group(1)
    if not args:
        try:
            self_user = await event.client.get_me()
            return self_user
        except Exception as e:
            await edit_or_reply(event, f"**خطأ في جلب معلوماتك:** {str(e)}")
            return None
    
    try:
        if args.isnumeric() or (args.startswith("-") and args[1:].isnumeric()):
            args = int(args)
        
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                return await event.client.get_entity(user_id)
        
        return await event.client.get_entity(args)
    except Exception as e:
        await edit_or_reply(event, f"**خطأ في جلب المستخدم:** {str(e)}")
        return None

async def checking(l313l):
    cat_c = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    try:
        cat_channel = Get(cat_c)
        await l313l(cat_channel)
    except BaseException:
        pass
        
