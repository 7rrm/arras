import asyncio
import contextlib
import re
import random
import time
import psutil
import html
import shutil
import os
import base64
import requests
from requests import get
import psutil
from datetime import datetime
from platform import python_version

from telethon import Button, events, version
from telethon.events import CallbackQuery
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest
from telethon.utils import pack_bot_file_id
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError

from . import StartTime, l313l, mention
from ..core import check_owner, pool
from ..Config import Config
from ..utils import Zed_Vip, Zed_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from ..sql_helper.like_sql import (
    add_like,
    get_likes,
    remove_all_likes,
    remove_like,
)
from . import BOTLOG, BOTLOG_CHATID, spamwatch, mention

plugin_category = "العروض"
LOGS = logging.getLogger(__name__)
#Code by T.me/zzzzl1l
zed_dev = Zed_Dev
zel_dev = (5427469031, 8277718687, 1985225531)
zelzal = (5427469031, 5280339206)
Zel_Uid = l313l.uid

ZED_BLACKLIST = [
    -1001935599871,
    ]

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await l313l.get_me()
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
            user_object = await l313l.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

# Copyright (C) 2023 T.me/ZThon . All Rights Reserved
async def fetch_zelzal(user_id): #Write Code By Zelzal T.me/zzzzl1l
    headers = {
        'Host': 'restore-access.indream.app',
        'Connection': 'keep-alive',
        'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
        'Accept': '*/*',
        'Accept-Language': 'ar',
        'Content-Length': '25',
        'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"telegramId":' + str(user_id) + '}'
    response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
    zelzal_date = response['data']['date']
    return zelzal_date

async def fetch_info(event):
    """Get details from the User object."""
    replied_user = await l313l.get_me()
    #user = self_user.id
    FullUser = (await l313l(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await l313l(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
    dc_id = "Can't get dc id"
    with contextlib.suppress(AttributeError):
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
    user_id = replied_user.id
    zelzal_sinc = await fetch_zelzal(user_id)
    first_name = replied_user.first_name
    full_name = FullUser.private_forward_name
    common_chat = FullUser.common_chats_count
    username = replied_user.username
    user_bio = FullUser.about
    is_bot = replied_user.bot
    restricted = replied_user.restricted
    verified = replied_user.verified
    zilzal = (await l313l.get_entity(user_id)).premium
    if zilzal == True or user_id in zelzal: #Code by T.me/zzzzl1l
        zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
    else:
        zpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    #zid = int(gvarstatus("ZThon_Vip"))
    #if user_id in Zed_Dev: #Code by T.me/zzzzl1l
        #zvip = "𝕍𝕀ℙ 💎"
    #elif user_id == zid:
        #zvip = "𝕍𝕀ℙ 💎"
    #else:
        #zvip = "ℕ𝕆ℕ𝔼"
    photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg")
    photo = await l313l.download_profile_photo(
        user_id,
        photo_path,
        download_big=True,
    )
    print(f"مسار الصورة: {photo_path}")  # أضف هذا السطر
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    user_bio = "لا يـوجـد" if not user_bio else user_bio
    zzzsinc = zelzal_sinc if zelzal_sinc else ("غيـر معلـوم")
    zmsg = await bot.get_messages(event.chat_id, 0, from_user=user_id) #Code by T.me/zzzzl1l
    zzz = zmsg.total
    if zzz < 100: #Code by T.me/zzzzl1l
        zelzzz = "غير متفاعل  🗿"
    elif zzz > 200 and zzz < 500:
        zelzzz = "ضعيف  🗿"
    elif zzz > 500 and zzz < 700:
        zelzzz = "شد حيلك  🏇"
    elif zzz > 700 and zzz < 1000:
        zelzzz = "ماشي الحال  🏄🏻‍♂"
    elif zzz > 1000 and zzz < 2000:
        zelzzz = "ملك التفاعل  🎖"
    elif zzz > 2000 and zzz < 3000:
        zelzzz = "امبراطور التفاعل  🥇"
    elif zzz > 3000 and zzz < 4000:
        zelzzz = "غنبله  💣"
    else:
        zelzzz = "نار وشرر  🏆"
################# Dev ZilZal #################
    if user_id in zelzal: #Code by T.me/zzzzl1l
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id in zel_dev:
        rotbat = "مـطـور 𐏕" 
    elif user_id == (await l313l.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
################# Dev ZilZal #################
    ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن سـورس آراس"  #Code by T.me/zzzzl1l
    ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ " #Code by T.me/zzzzl1l
    ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ʟx5x5 ─┄─┄─┄─⋆" #Code by T.me/zzzzl1l
    if gvarstatus("ZID_TEMPLATE") is None:
        caption = f"<b> {ZED_TEXT} </b>\n"
        caption += f"ٴ<b>{ZEDF}</b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
        caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
        caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n" #Code by T.me/zzzzl1l
        if zilzal == True or user_id in zelzal: #Code by T.me/zzzzl1l
            caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
        #if user_id in Zed_Dev or user_id == zid: #Code by T.me/zzzzl1l
        caption += f"<b>{ZEDM}الاشتراك  ⤎  𝕍𝕀ℙ 💎</b>\n"
        caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
        caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n" #Code by T.me/zzzzl1l
        caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n" #Code by T.me/zzzzl1l
        if user_id != (await l313l.get_me()).id: #Code by T.me/zzzzl1l
            caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
        caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n" #Code by T.me/zzzzl1l
        caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
        caption += f"ٴ<b>{ZEDF}</b>"
    else:
        zzz_caption = gvarstatus("ZID_TEMPLATE")
        caption = zzz_caption.format(
            znam=full_name,
            zusr=username,
            zidd=user_id,
            zrtb=rotbat,
            zpre=zpre,
            zvip=zvip,
            zpic=replied_user_profile_photos_count,
            zmsg=zzz,
            ztmg=zelzzz,
            zcom=common_chat,
            zsnc=zzzsinc,
            zbio=user_bio,
        )
    return photo_path, caption

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await l313l.get_me()
        
        if query.startswith("idid") and event.query.user_id == l313l.uid:
            #if gvarstatus("ZThon_Vip") is None or Zel_Uid not in zed_dev:
                #return
            if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
                os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
            #replied_user = await get_user_from_event(event)
            try:
                photo_path, caption = await fetch_info(event)
            except (AttributeError, TypeError):
                return await edit_or_reply(zed, "**- لـم استطـع العثــور ع الشخــص ؟!**")
            message_id_to_reply = None
            if gvarstatus("ZID_TEMPLATE") is None:
                try:
                    uploaded_file = await event.client.upload_file(file=photo_path)
                    Like_id = gvarstatus("Like_Id")
                    Like_id = Like_id if Like_id else 0
                    buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]]
                    result = builder.photo(
                        uploaded_file,
                        #title="l313l",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
                    if not photo_path.startswith("http"):
                        os.remove(photo_path)
                    #await zed.delete()
                except (TypeError, ChatSendMediaForbiddenError, Exception):
                    Like_id = gvarstatus("Like_Id")
                    Like_id = Like_id if Like_id else 0
                    buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]]
                    result = builder.article(
                        title="l313l",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
            else:
                try:
                    uploaded_file = await event.client.upload_file(file=photo_path)
                    Like_id = gvarstatus("Like_Id")
                    Like_id = Like_id if Like_id else 0
                    buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]]
                    result = builder.photo(
                        uploaded_file,
                        #title="l313l",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
                    if not photo_path.startswith("http"):
                        os.remove(photo_path)
                    #await zed.delete()
                except (TypeError, ChatSendMediaForbiddenError, Exception):
                    Like_id = gvarstatus("Like_Id")
                    Like_id = Like_id if Like_id else 0
                    buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]]
                    result = builder.article(
                        title="l313l",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
            await event.answer([result] if result else None)
        else:
            return

# Copyright (C) 2021 Zed-Thon . All Rights Reserved
@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    input_str = event.pattern_match.group(1)
    reply = event.reply_to_msg_id
    if input_str and reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    if input_str or reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    zed = await edit_or_reply(event, "⇆")
    if event.reply_to_msg_id:
        await event.get_reply_message()
        return
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
    await response[0].click(event.chat_id)
    await zed.delete()

# Copyright (C) 2021 Zed-Thon . All Rights Reserved
@l313l.ar_cmd(pattern="like(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    input_str = event.pattern_match.group(1)
    reply = event.reply_to_msg_id
    if input_str and reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    if input_str or reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر .**")
    zed = await edit_or_reply(event, "⇆")
    if event.reply_to_msg_id:
        await event.get_reply_message()
        return
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
    await response[0].click(event.chat_id)
    await zed.delete()

# اوامـر لايك ايدي تبدأ من هنا
@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع **")
    count = 1
    likers = get_likes(l313l.uid)
    if likers:
        for mogab in likers:
            OUT_STR = f"𓆩 𝗮𝗥𝗥𝗮𝗦 𝗟𝗶𝗸𝗲 - **قائمـة المعجبيــن** ❤️𓆪\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n**• إجمالي عـدد المعجبيـن {count}**\n"
            OUT_STR += "\n**• الاسم:** [{}](tg://user?id={})\n**• الايـدي:** `{}`\n**• اليـوزر:** {}".format(mogab.f_name, mogab.lik_id, mogab.lik_id, mogab.f_user)
            count += 1
        await edit_or_reply(
            event,
            OUT_STR,
            caption="**⧗╎قائمـة المعجبيــن ❤️**",
            file_name="likers.text",
        )
    else:
        OUT_STR = "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**"
        await edit_or_reply(event, OUT_STR)

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    liikers = get_likes(l313l.uid)
    count = 1
    if liikers:
        zed = await edit_or_reply(event, "**⪼ جـارِ مسـح المعجبيـن .. انتظـر ⏳**")
        for mogab in liikers:
            count += 1
        remove_all_likes(l313l.uid)
        delgvar("Like_Id")
        await zed.edit("**⪼ تم حـذف جميـع المعجبيـن .. بنجـاح ✅**")
    else:
        OUT_STR = "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**"
        await edit_or_reply(event, OUT_STR)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
async def _(event):
    # الحصول على معلومات الشخص الذي قام بالضغط على الزر
    user_id = event.sender_id
    try:
        user = await l313l.get_entity(user_id)
        user_name = f"{user.first_name}{user.last_name}" if user.last_name else user.first_name
        user_username = f"@{user.username}" if user.username else "لا يوجد"
    except ValueError:
        user = await l313l(GetUsersRequest(user_id))
        user_name = f"{user.first_name}{user.last_name}" if user.last_name else user.first_name
        user_username = f"@{user.username}" if user.username else "لا يوجد"
    except Exception:
        user_name = "مستخدم محذوف"
        user_username = "لا يوجد"
    # إرسال إشعار لمجموعة السجل بمعلومات من قام بعمل لايك ( إعجاب )
    Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
    if add_like(str(l313l.uid), str(user.id), user_name, user_username) is True:
        Like_id += 1
        addgvar("Like_Id", Like_id)
    else:
        return await event.answer("- انت معجب من قبل بهذا الشخص ❤️", cache_time=0, alert=True)
        #remove_like(str(zedub.uid), str(user.id))
        #if add_like(str(zedub.uid), str(user.id), user_name, user_username) is True:
            #return await
    try:
        await l313l.send_message(
            BOTLOG_CHATID,
            "#الايـدي_بـ_لايــك 💝\n\n"
            f"**- المُستخـدِم :** {_format.mentionuser(user_name ,user.id)} \n"
            f"**- الايدي** `{user.id}`\n"
            f"**- اليـوزر :** {user_username} \n"
            f"**- قام بعمـل لايـك لـ الايـدي الخـاص بـك ♥️**\n"
            f"**- اصبح عـدد معجبينك هـو :** {Like_id} 🤳\n"
            f"**- لـ عـرض قائمـة المعجبيـن ارسـل:** ( `.المعجبين` ) 🎴\n"
            f"**- لـ مسح قائمـة المعجبيـن ارسـل:** ( `.مسح المعجبين` ) 🗑",
        )
    except Exception as e:
        await l313l.send_message(BOTLOG_CHATID, f"**- حدث خطأ أثناء إرسال إشعـار لايك ❌**\n**- الخطأ هـو 📑:**\n-{e}")
    # تحديث زر الإعجاب
    try:
        await event.edit(buttons=[[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]])
        await event.answer("- تم إضافة إعجابك لـ هذا الشخص ♥️", cache_time=0, alert=True)
    except Exception:
        await event.answer("- تم إضافة إعجابك لـ هذا الشخص ♥️", cache_time=0, alert=True)
