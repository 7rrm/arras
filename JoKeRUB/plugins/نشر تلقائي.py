from telethon import *
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
import asyncio

from JoKeRUB import l313l

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from JoKeRUB.core.logger import logging
from ..sql_helper.globals import gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from . import *

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

@l313l.on(admin_cmd(pattern="(نشر_تلقائي|النشر_التلقائي)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "**᯽︙ عـذراً .. النشر التلقائي خـاص بالقنـوات فقـط**")
    jok = event.pattern_match.group(1)
    if not jok:
        return await edit_or_reply(event, "**᯽︙ عـذراً .. قـم بـ إضـافة معـرف/ايـدي القنـاة الى الامـر اولاً**")
    if jok.startswith("@"):
        JoKeRUB = jok
    elif jok.startswith("https://t.me/"):
        JoKeRUB = jok.replace("https://t.me/", "@")
    elif str(jok).startswith("-100"):
        JoKeRUB = str(jok).replace("-100", "")
    else:
        try:
            JoKeRUB = int(jok)
        except BaseException:
            return await edit_or_reply(event, "**᯽︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    try:
        JoKeRUB = (await event.client.get_entity(JoKeRUB)).id
    except BaseException:
        return await event.reply("**᯽︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    if is_post(str(JoKeRUB) , event.chat_id):
        return await edit_or_reply(event, "**᯽︙ النشـر التلقـائي من القنـاة ** `{jok}` **مفعـل مسبقـاً ✓**")
    add_post(str(JoKeRUB), event.chat_id)
    await edit_or_reply(event, f"**᯽︙ تم تفعيـل النشـر التلقـائي من القنـاة ** `{jok}` **بنجـاح ✓**")

@l313l.on(admin_cmd(pattern="(ايقاف_نشر|ايقاف_النشر)"))
async def _(event):
    if (event.is_private or event.is_group):
        return await edit_or_reply(event, "**᯽︙ عـذراً .. النشر التلقائي خـاص بالقنـوات فقـط**")
    jok = event.pattern_match.group(1)
    if not jok:
        return await edit_or_reply(event, "**᯽︙ عـذراً .. قـم بـ إضـافة معـرف/ايـدي القنـاة الى الامـر اولاً**")
    if jok.startswith("@"):
        JoKeRUB = jok
    elif jok.startswith("https://t.me/"):
        JoKeRUB = jok.replace("https://t.me/", "@")
    elif str(jok).startswith("-100"):
        JoKeRUB = str(jok).replace("-100", "")
    else:
        try:
            JoKeRUB = int(jok)
        except BaseException:
            return await edit_or_reply(event, "**᯽︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    try:
        JoKeRUB = (await event.client.get_entity(JoKeRUB)).id
    except BaseException:
        return await event.reply("**᯽︙ عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**✾╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
    if not is_post(str(JoKeRUB), event.chat_id):
        return await edit_or_reply(event, "**᯽︙ تم تعطيـل النشر التلقـائي لهـذه القنـاة هنـا .. بنجـاح ✓**")
    remove_post(str(JoKeRUB), event.chat_id)
    await edit_or_reply(event, f"**᯽︙ تم ايقـاف النشـر التلقـائي من** `{jok}`")

@l313l.on(admin_cmd(pattern="ارسال (.*)"))
async def send_to_groups(event):
    # الحصول على الرسالة من الأمر
    message = event.pattern_match.group(1)
    
    if not message:
        return await edit_or_reply(event, "**᯽︙ يرجى تحديد الرسالة المراد إرسالها**")
    
    # قائمة المجموعات المحددة (يمكنك تعديلها حسب احتياجاتك)
    target_groups = [
        -1001620950804,  # مثال: إيدي مجموعة 1 
        -1002468151715,  # مثال: إيدي مجموعة 2
        -1002661574486,  # مثال: إيدي مجموعة 2
        -1002299561292,  # مثال: إيدي مجموعة 2
      #  -100,  # مثال: إيدي مجموعة 2
    ]
    
    sent_count = 0
    failed_count = 0
    
    await edit_or_reply(event, f"**᯽︙ جاري إرسال الرسالة إلى {len(target_groups)} مجموعة...**")
    
    for group in target_groups:
        try:
            await l313l.send_message(group, message)
            sent_count += 1
            # إضافة تأخير لمدة ثانية واحدة بين كل إرسال
            await asyncio.sleep(2)
        except Exception as e:
            logging.error(f"فشل في إرسال الرسالة إلى {group}: {str(e)}")
            failed_count += 1
            # التأخير حتى في حالة الفشل للحفاظ على المعدل
            await asyncio.sleep(2)
    
    report = (
        f"**◈︙ تم إرسال الرسالة بنجاح إلى {sent_count} مجموعة\n"
        f"◈︙ فشل الإرسال إلى {failed_count} مجموعة\n"
        f"◈︙ الرسالة:**\n{message}"
    )
    
    await edit_or_reply(event, report)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#إرسال_الجماعي\n{report}",
        )

@l313l.ar_cmd(incoming=True, forword=None)
async def _(event):
    if event.is_private:
        return
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set  = get_all_post(chat_id)
    if channels_set == []:
        return
    for chat in channels_set:
        if event.media:
            await event.client.send_file(int(chat), event.media, caption=event.text)
        elif not event.media:
            await l313l.send_message(int(chat), event.message)
