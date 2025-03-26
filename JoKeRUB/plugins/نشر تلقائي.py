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
from ..sql_helper.broadcast_sql import add_broadcast_chat, get_all_broadcast_chats, remove_broadcast_chat
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
                user_id = probable_user_mention_entity.user_id
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

@l313l.on(admin_cmd(pattern="اضافة_مجموعة (-?\d+)"))
async def add_broadcast_group(event):
    chat_id = event.pattern_match.group(1)
    
    # التحقق من أن الأيدي صالح للمجموعات/القنوات
    if not chat_id.startswith("-100"):
        return await edit_or_reply(event, "**᯽︙ خطأ: يجب أن يكون أيدي المجموعة بصيغة -100123456789**")
    
    try:
        chat_id = int(chat_id)
        chat_entity = await event.client.get_entity(chat_id)
        
        # التأكد من أن الدردشة ليست خاصة
        if isinstance(chat_entity, (types.User, types.PeerUser)):
            return await edit_or_reply(event, "**᯽︙ لا يمكن إضافة الدردشات الخاصة**")
            
        title = getattr(chat_entity, 'title', 'مجموعة بدون اسم')
    except ValueError:
        return await edit_or_reply(event, "**᯽︙ خطأ: الأيدي يجب أن يكون رقمًا صحيحًا**")
    except Exception as e:
        return await edit_or_reply(event, f"**᯽︙ خطأ في الوصول إلى المجموعة:** `{str(e)}`")
    
    if add_broadcast_chat(chat_id):
        await edit_or_reply(event, f"**᯽︙ تمت إضافة المجموعة** `{title}` **بأيدي** `{chat_id}` **إلى قائمة البث بنجاح ✓**")
    else:
        await edit_or_reply(event, f"**᯽︙ المجموعة** `{title}` **موجودة بالفعل في قائمة البث**")
        
@l313l.on(admin_cmd(pattern="حذف_مجموعة ?(.*)"))
async def remove_broadcast_group(event):
    chat = event.pattern_match.group(1)
    if not chat:
        if event.is_private:
            return await edit_or_reply(event, "**᯽︙ لا يمكن حذف الدردشات الخاصة**")
        chat = event.chat_id
    
    try:
        chat_entity = await event.client.get_entity(chat)
        chat_id = chat_entity.id
        title = chat_entity.title if hasattr(chat_entity, 'title') else "دردشة خاصة"
    except Exception as e:
        return await edit_or_reply(event, f"**᯽︙ خطأ في الحصول على المجموعة:** `{str(e)}`")
    
    if remove_broadcast_chat(chat_id):
        await edit_or_reply(event, f"**᯽︙ تم حذف المجموعة** `{title}` **من قائمة البث بنجاح ✓**")
    else:
        await edit_or_reply(event, f"**᯽︙ المجموعة** `{title}` **غير موجودة في قائمة البث**")

@l313l.on(admin_cmd(pattern="عرض_المجموعات$"))
async def show_broadcast_groups(event):
    broadcast_chats = get_all_broadcast_chats()
    if not broadcast_chats:
        return await edit_or_reply(event, "**᯽︙ لا توجد مجموعات في قائمة البث**")
    
    message = "**᯽︙ قائمة المجموعات المضافة للبث:**\n\n"
    for chat_id in broadcast_chats:
        try:
            chat = await event.client.get_entity(int(chat_id))
            title = chat.title if hasattr(chat, 'title') else "دردشة خاصة"
            message += f"• **{title}** (`{chat_id}`)\n"
        except:
            message += f"• مجموعة غير متاحة (`{chat_id}`)\n"
    
    await edit_or_reply(event, message)

@l313l.on(admin_cmd(pattern="ارسال ?(.*)"))
async def send_to_groups(event):
    message = event.pattern_match.group(1)
    if not message:
        return await edit_or_reply(event, "**᯽︙ يرجى تحديد الرسالة المراد إرسالها**")
    
    broadcast_chats = get_all_broadcast_chats()
    if not broadcast_chats:
        return await edit_or_reply(event, "**᯽︙ لا توجد مجموعات في قائمة البث**")
    
    sent_count = 0
    failed_count = 0
    total = len(broadcast_chats)
    
    progress = await edit_or_reply(event, f"**᯽︙ جاري إرسال الرسالة إلى {total} مجموعة...**")
    
    for chat_id in broadcast_chats:
        try:
            await l313l.send_message(int(chat_id), message)
            sent_count += 1
            await progress.edit(
                f"**᯽︙ جاري الإرسال...\n"
                f"✅ تم بنجاح: {sent_count}\n"
                f"❌ فشل: {failed_count}\n"
                f"📊 الإجمالي: {total}**"
            )
            await asyncio.sleep(1)  # تأخير لمدة ثانية واحدة
        except Exception as e:
            logging.error(f"فشل في إرسال الرسالة إلى {chat_id}: {str(e)}")
            failed_count += 1
    
    report = (
        f"**᯽︙ تم الانتهاء من الإرسال الجماعي\n\n"
        f"✅ تم بنجاح: {sent_count}\n"
        f"❌ فشل: {failed_count}\n"
        f"📊 الإجمالي: {total}\n\n"
        f"📝 الرسالة:**\n{message}"
    )
    
    await progress.edit(report)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الإرسال_الجماعي\n{report}",
        )

@l313l.ar_cmd(incoming=True, forword=None)
async def _(event):
    if event.is_private:
        return
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set = get_all_post(chat_id)
    if channels_set == []:
        return
    for chat in channels_set:
        if event.media:
            await event.client.send_file(int(chat), event.media, caption=event.text)
        elif not event.media:
            await l313l.send_message(int(chat), event.message)
