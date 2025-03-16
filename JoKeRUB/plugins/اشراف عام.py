#    جميع الحقوق محفوظة كتابة وتعديل  :   @lMl10l
#    اخمط مع ذكر الحقوق غيرها انت مطور فاشل
marculs=9
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                            MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                              EditBannedRequest,
                                                EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (ChannelParticipantsAdmins,
                                 ChatAdminRights,
                                   ChatBannedRights,
                                     MessageEntityMentionName,
                                       MessageMediaPhoto)
from JoKeRUB.utils import admin_cmd
from ..Config import Config
from JoKeRUB import CMD_HELP, l313l
up_admin = Config.UP_ET or "ارفع"
down_admin = Config.DOWN_ET or "تزل"
async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("▾∮ لا يمكنك بدون ايدي المستخدم")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("▾∮ هنالك خطأ يرجى تبليغنا @jepthon", str(err))           
    return user_obj, extra

global hawk,moth
hawk="admin"
moth="owner"
async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj
@l313l.on(admin_cmd(pattern="{up_admin} ?(.*)"))
async def gben(JoKeRUB):
    dc = razan = JoKeRUB
    i = 0
    sender = await dc.get_sender()
    me = await JoKeRUB.client.get_me()
    await razan.edit("▾∮ يتم رفع المستخدم في جميع المجموعات")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await JoKeRUB.get_chat()
    if JoKeRUB.is_private:
        user = JoKeRUB.chat
        rank = JoKeRUB.pattern_match.group(1)
    else:
        JoKeRUB.chat.title
    try:
        user, rank = await get_full_user(JoKeRUB)
    except:
        pass
    if me == user:
       l313l = await razan.edit("▾∮ لا استطيع رفع نفسي 🧸🤍،")
       return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await razan.edit(f"**▾∮ هنالك شي خطأ**")
    if user:
        telchanel = [d.entity.id
                     for d in await JoKeRUB.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=True,
                               invite_users=True,
                                change_info=True,
                                 ban_users=True,
                                  delete_messages=True,
                                   pin_messages=True)
        for x in telchanel:
          try:
             await JoKeRUB.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await razan.edit(f"**▾∮ يتم الرفع في **: `{i}` من المجموعات")
          except:
             pass
    else:
        await razan.edit(f"**▾∮ يجب عليك الرد على المستخدم اولا **")
    return await razan.edit(
        f"**▾∮المستخدم [{user.first_name}](tg://user?id={user.id})\n▾∮ تم رفعه في : {i} من المجموعات**"
    )

@l313l.on(admin_cmd(pattern="{down_admin} ?(.*)"))
async def gben(JoKeRUB):
    dc = razan = JoKeRUB
    i = 0
    sender = await dc.get_sender()
    me = await JoKeRUB.client.get_me()
    await razan.edit("**▾∮ يتم تنزيل الشخص من رتبة الاشراف في جميع الكروبات**")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await JoKeRUB.get_chat()
    if JoKeRUB.is_private:
        user = JoKeRUB.chat
        rank = JoKeRUB.pattern_match.group(1)
    else:
        JoKeRUB.chat.title
    try:
        user, rank = await get_full_user(JoKeRUB)
    except:
        pass
    if me == user:
       l313l = await razan.edit("▾∮ لا استطيع تنزيل نفسي 🧸🤍")
       return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await razan.edit(f"**▾∮ هنالك شي خطأ**")
    if user:
        telchanel = [d.entity.id
                     for d in await JoKeRUB.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=None,
                               invite_users=None,
                                change_info=None,
                                 ban_users=None,
                                  delete_messages=None,
                                   pin_messages=None)
        for x in telchanel:
          try:
             await JoKeRUB.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await razan.edit(f"**▾∮ يتم تنزيله في **: `{i}` من المجموعات")
          except:
             pass
    else:
        await razan.edit(f"**▾∮ يجب عليك الرد على المستخدم اولا **")
    return await razan.edit(
        f"**▾∮المستخدم [{user.first_name}](tg://user?id={user.id})\n▾∮ تم تنزيله في : {i} من المجموعات**"
    )

CMD_HELP.update(
    {
        "اشراف عام": ".ارفع <بالرد ؏ شخص>\
\n لرفع المستخدم مشرف في جميع المجموعات ... \
\n\n.نزل <بالرد ؏ شخص>\n بالرد على الشخص لتنزيله من رتبة المشرف في جميع المجموعات"

    }
)

import asyncio
import random
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, User
from telethon.errors import UsernameNotOccupiedError, PeerIdInvalidError

@l313l.on(admin_cmd(pattern="رفع_البوتات_العشوائي ?(.*)"))
async def promote_random_bots(event):
    if not event.is_channel:
        await event.edit("▾∮ هذا الأمر يعمل فقط في القنوات!")
        return

    await event.edit("▾∮ يتم البحث عن البوتات ورفعهم كمشرفين...")

    # صلاحيات المشرف
    admin_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True
    )

    promoted_count = 0
    failed_count = 0
    not_bot_count = 0

    # إنشاء قائمة بجميع اليوزرات الممكنة (4 إلى 5 أحرف عشوائية + "bot")
    for _ in range(100):  # يمكنك تغيير العدد حسب الحاجة
        # إنشاء جزء عشوائي من 4 إلى 5 أحرف
        random_length = random.randint(4, 5)  # طول عشوائي بين 4 و5
        random_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random_length))
        username = f"{random_chars}bot"  # مثل aaaabot, abbbbot, abcccbot

        try:
            # التحقق من وجود اليوزر على Telegram
            bot_entity = await event.client.get_entity(username)
            
            # التأكد من أن اليوزر هو بوت وليس مستخدم عادي
            if not isinstance(bot_entity, User) or not bot_entity.bot:
                not_bot_count += 1
                continue  # تخطي المستخدمين العاديين
            
            # رفع البوت كمشرف
            await event.client(EditAdminRequest(event.chat_id, bot_entity, admin_rights, "Bot"))
            promoted_count += 1
            await event.edit(f"▾∮ تم رفع البوت @{username} كمشرف في القناة.")
        except (UsernameNotOccupiedError, PeerIdInvalidError):
            # تخطي اليوزرات غير الموجودة
            continue
        except Exception as e:
            failed_count += 1
            await event.edit(f"▾∮ فشل في رفع البوت @{username}: {str(e)}")
        
        # إضافة تأخير 10 ثواني بين كل عملية
        await asyncio.sleep(10)

    await event.edit(
        f"▾∮ تم الانتهاء من العملية!\n"
        f"▾∮ عدد البوتات التي تم رفعها: {promoted_count}\n"
        f"▾∮ عدد البوتات التي فشل رفعها: {failed_count}\n"
        f"▾∮ عدد المستخدمين العاديين الذين تم تخطيهم: {not_bot_count}"
    )
