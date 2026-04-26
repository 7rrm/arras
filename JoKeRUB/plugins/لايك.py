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

zed_dev = Zed_Dev
zel_dev = (5427469031, 1985225531)
zelzal = (5427469031, 5280339206)
Zel_Uid = l313l.uid

ZED_BLACKLIST = [-1001935599871]

# =========================================================== #
# كليشات الايدي (ID Templates)
# =========================================================== #

ID_TEMPLATES = {
    "default": {
        "name": "الافتراضي",
        "template": (
            "<b> •⎚• مـعلومـات المسـتخـدم مـن سـورس آراس </b>\n"
            "ٴ<b>⋆─┄─┄─┄─ ʟx5x5 ─┄─┄─┄─⋆</b>\n"
            "<b>✦ الاســم    ⤎ </b> <a href='tg://user?id={zidd}'>{znam}</a>\n"
            "<b>✦ اليـوزر    ⤎  {zusr}</b>\n"
            "<b>✦ الايـدي    ⤎ </b> <code>{zidd}</code>\n"
            "<b>✦ الرتبــه    ⤎ {zrtb} </b>\n"
            "<b>✦ الحساب  ⤎  {zpre}</b>\n"
            "<b>✦ الاشتراك  ⤎  {zvip}</b>\n"
            "<b>✦ الصـور    ⤎</b>  {zpic}\n"
            "<b>✦ الرسائل  ⤎</b>  {zmsg}  💌\n"
            "<b>✦ التفاعل  ⤎</b>  {ztmg}\n"
            "<b>✦ الإنشـاء  ⤎</b>  {zsnc}  🗓\n"
            "<b>✦ البايـو     ⤎  {zbio}</b>\n"
            "ٴ<b>⋆─┄─┄─┄─ ʟx5x5 ─┄─┄─┄─⋆</b>"
        )
    },
    "simple": {
        "name": "بسيط",
        "template": (
            "<b>👤 {znam}</b>\n"
            "<b>🆔 {zidd}</b>\n"
            "<b>📝 {zusr}</b>\n"
            "<b>⭐ {zpre}</b>"
        )
    },
    "elegant": {
        "name": "أنيق",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ **الاســم** : {znam}\n"
            "┃ ✦ **اليـوزر** : {zusr}\n"
            "┃ ✦ **الايـدي** : <code>{zidd}</code>\n"
            "┃ ✦ **الرتبــه** : {zrtb}\n"
            "┃ ✦ **الحساب** : {zpre}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    "minimal": {
        "name": "صغير",
        "template": (
            "<b>{znam}</b> | <code>{zidd}</code> | {zusr}\n"
            "<b>{zrtb}</b> | {zpre}"
        )
    },
    "box": {
        "name": "صندوق",
        "template": (
            "┌─────────────────┐\n"
            "│ ✦ {znam}\n"
            "│ ✦ {zidd}\n"
            "│ ✦ {zusr}\n"
            "│ ✦ {zrtb}\n"
            "└─────────────────┘"
        )
    },
    "star": {
        "name": "نجوم",
        "template": (
            "★━━━━━━━━━━━━━━━━━━★\n"
            "✧ **الاســم** : {znam}\n"
            "✧ **الايـدي** : <code>{zidd}</code>\n"
            "✧ **اليـوزر** : {zusr}\n"
            "✧ **الرتبــه** : {zrtb}\n"
            "★━━━━━━━━━━━━━━━━━━★"
        )
    },
    "arrow": {
        "name": "سهام",
        "template": (
            "➜ **الاســم** : {znam}\n"
            "➜ **الايـدي** : <code>{zidd}</code>\n"
            "➜ **اليـوزر** : {zusr}\n"
            "➜ **الرتبــه** : {zrtb}"
        )
    },
    "heart": {
        "name": "قلوب",
        "template": (
            "♥️ **الاســم** : {znam}\n"
            "♥️ **الايـدي** : <code>{zidd}</code>\n"
            "♥️ **اليـوزر** : {zusr}\n"
            "♥️ **الرتبــه** : {zrtb}\n"
            "♥️ **الحساب** : {zpre}"
        )
    }
}

# =========================================================== #
# دوال مساعدة
# =========================================================== #

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

async def fetch_zelzal(user_id):
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

async def fetch_info(event, user_id=None):
    """Get details from the User object."""
    if user_id is None:
        replied_user = await l313l.get_me()
        user_id = replied_user.id
    else:
        replied_user = await l313l.get_entity(user_id)
    
    FullUser = (await l313l(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await l313l(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    )
    replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
    dc_id = "Can't get dc id"
    with contextlib.suppress(AttributeError):
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
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
    if zilzal == True or user_id in zelzal:
        zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
    else:
        zpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    
    photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg")
    photo = await l313l.download_profile_photo(
        user_id,
        photo_path,
        download_big=True,
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يـوجـد")
    user_bio = "لا يـوجـد" if not user_bio else user_bio
    zzzsinc = zelzal_sinc if zelzal_sinc else ("غيـر معلـوم")
    zmsg = await l313l.get_messages(event.chat_id, 0, from_user=user_id)
    zzz = zmsg.total
    if zzz < 100:
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
    
    if user_id in zelzal:
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id in zed_dev:
        rotbat = "مـطـور 𐏕" 
    elif user_id == (await l313l.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
    
    # الحصول على الكليشة المختارة
    selected_template = gvarstatus("SELECTED_ID_TEMPLATE") or "default"
    like_button_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"  # likes أو profile
    
    template_data = ID_TEMPLATES.get(selected_template, ID_TEMPLATES["default"])
    template = template_data["template"]
    
    zvip = "𝕍𝕀ℙ 💎" if user_id in Zed_Dev else "ℕ𝕆ℕ𝔼"
    
    caption = template.format(
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
    async def inline_handler_like(event):
        builder = event.builder
        result = None
        query = event.text
        await l313l.get_me()
        
        if query.startswith("idid") and event.query.user_id == l313l.uid:
            try:
                photo_path, caption = await fetch_info(event)
            except (AttributeError, TypeError):
                return
            
            # الحصول على وضع زر اللايك
            like_button_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
            
            if like_button_mode == "likes":
                Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
                buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes", style="primary")]]
            else:
                buttons = [[Button.inline("❤️ اضغط للإعجاب", data="likes", style="primary")]]
            
            try:
                uploaded_file = await event.client.upload_file(file=photo_path)
                result = builder.photo(
                    uploaded_file,
                    text=caption,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="html",
                )
                if not photo_path.startswith("http"):
                    os.remove(photo_path)
            except Exception:
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


@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات**")
    
    zed = await edit_or_reply(event, "⇆")
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
    await response[0].click(event.chat_id)
    await zed.delete()

@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    count = 1
    likers = get_likes(l313l.uid)
    if likers:
        OUT_STR = f"𓆩 𝗮𝗥𝗥𝗮𝗦 𝗟𝗶𝗸𝗲 - **قائمـة المعجبيــن** ❤️𓆪\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
        for mogab in likers:
            OUT_STR += f"\n**• الاسم:** [{mogab.f_name}](tg://user?id={mogab.lik_id})\n**• الايـدي:** `{mogab.lik_id}`\n**• اليـوزر:** {mogab.f_user}\n"
            count += 1
        OUT_STR += f"\n**• إجمالي عـدد المعجبيـن {count-1}**"
        await edit_or_reply(event, OUT_STR)
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    likers = get_likes(l313l.uid)
    if likers:
        zed = await edit_or_reply(event, "**⪼ جـارِ مسـح المعجبيـن .. انتظـر ⏳**")
        remove_all_likes(l313l.uid)
        delgvar("Like_Id")
        await zed.edit("**⪼ تم حـذف جميـع المعجبيـن .. بنجـاح ✅**")
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**")


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
async def like_callback(event):
    user_id = event.sender_id
    
    # منع الإعجاب بالنفس
    if user_id == l313l.uid:
        return await event.answer("❌ لا يمكنك الإعجاب بنفسك!", alert=True)
    
    try:
        user = await l313l.get_entity(user_id)
        user_name = f"{user.first_name}{' ' + user.last_name if user.last_name else ''}"
        user_username = f"@{user.username}" if user.username else "لا يوجد"
    except Exception:
        user_name = "مستخدم محذوف"
        user_username = "لا يوجد"
    
    Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
    like_button_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
    
    if add_like(str(l313l.uid), str(user_id), user_name, user_username) is True:
        Like_id += 1
        addgvar("Like_Id", Like_id)
    else:
        return await event.answer("❤️ انت معجب من قبل بهذا الشخص!", cache_time=0, alert=True)
    
    # إرسال إشعار
    try:
        await l313l.send_message(
            BOTLOG_CHATID,
            f"#الايـدي_بـ_لايــك 💝\n\n"
            f"**- المُستخدِم :** {_format.mentionuser(user_name ,user_id)} \n"
            f"**- الايدي** `{user_id}`\n"
            f"**- اليـوزر :** {user_username} \n"
            f"**- قام بعمـل لايـك لـ الايـدي الخـاص بـك ♥️**\n"
            f"**- اصبح عـدد معجبينك هـو :** {Like_id} 🤳",
        )
    except Exception as e:
        pass
    
    # تحديث الزر
    if like_button_mode == "likes":
        button_text = f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}"
        button_data = "likes"
    else:
        button_text = f"❤️ {user_name} ⤑ {Like_id}"
        button_data = f"like_profile_{user_id}"
    
    try:
        await event.edit(buttons=[[Button.inline(button_text, data=button_data, style="primary")]])
        await event.answer(f"✅ تم إضافة إعجابك لـ {user_name}!", alert=True)
    except Exception:
        await event.answer(f"✅ تم إضافة إعجابك لـ {user_name}!", alert=True)


@l313l.ar_cmd(pattern="كليشات الايدي$")
async def id_templates_menu(event):
    """عرض قائمة كليشات الايدي"""
    text = "**🎨 قائمة كليشات الايدي المتاحة:**\n\n"
    buttons = []
    row = []
    
    for key, template in ID_TEMPLATES.items():
        selected = "✅ " if gvarstatus("SELECTED_ID_TEMPLATE") == key else ""
        row.append(Button.inline(f"{selected}{template['name']}", data=f"select_template_{key}", style="primary"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
    
    buttons.append([Button.inline("❌ إغلاق", data="close_templates", style="danger")])
    
    await edit_or_reply(event, text, buttons=buttons)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"select_template_(.+)")))
async def select_template(event):
    match = re.match(r"select_template_(.+)", event.data.decode())
    if not match:
        return
    
    template_key = match.group(1)
    if template_key in ID_TEMPLATES:
        addgvar("SELECTED_ID_TEMPLATE", template_key)
        await event.edit(f"✅ تم اختيار كليشة **{ID_TEMPLATES[template_key]['name']}** بنجاح!")
    else:
        await event.answer("❌ كليشة غير موجودة!", alert=True)

@l313l.ar_cmd(pattern="نمط اللايك$")
async def like_mode_menu(event):
    """اختيار نمط زر اللايك"""
    current_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
    
    text = f"**⚙️ إعدادات زر اللايك:**\n\n"
    text += f"• النمط الحالي: **{'قلوب' if current_mode == 'likes' else 'اسم المستخدم'}**\n\n"
    text += f"• اختر النمط الذي تريده:"
    
    buttons = [
        [Button.inline(f"{'✅ ' if current_mode == 'likes' else ''}❤️ نمط القلوب", data="set_like_mode_likes", style="primary")],
        [Button.inline(f"{'✅ ' if current_mode == 'profile' else ''}👤 نمط اسم المستخدم", data="set_like_mode_profile", style="primary")],
        [Button.inline("❌ إغلاق", data="close_templates", style="danger")]
    ]
    
    await edit_or_reply(event, text, buttons=buttons)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"set_like_mode_(.+)")))
async def set_like_mode(event):
    match = re.match(r"set_like_mode_(.+)", event.data.decode())
    if not match:
        return
    
    mode = match.group(1)  # likes أو profile
    addgvar("LIKE_BUTTON_MODE", mode)
    
    mode_name = "نمط القلوب" if mode == "likes" else "نمط اسم المستخدم"
    await event.edit(f"✅ تم تغيير نمط اللايك إلى **{mode_name}** بنجاح!")

@l313l.ar_cmd(pattern="مسح الاعدادات$")
async def reset_settings(event):
    """مسح جميع التغييرات (الكليشات ونمط اللايك)"""
    delgvar("SELECTED_ID_TEMPLATE")
    delgvar("LIKE_BUTTON_MODE")
    delgvar("Like_Id")
    remove_all_likes(l313l.uid)
    
    await edit_or_reply(event, "✅ تم مسح جميع الإعدادات والتغييرات بنجاح!\n\n• عادت الكليشة إلى الافتراضية\n• عاد نمط اللايك إلى القلوب\n• تم مسح جميع المعجبين")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"close_templates")))
async def close_templates(event):
    await event.delete()
