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

ZED_BLACKLIST = [
    -1001935599871,
]

# ====================== قاموس الكليشات ======================
ZID_TEMPLATES = {
    "1": {
        "name": "🎭 الكليشة الافتراضية",
        "template": "<b> {ZED_TEXT} </b>\nٴ<b>{ZEDF}</b>\n<b>{ZEDM}الاســم    ⤎ </b> <a href='tg://user?id={zidd}'>{znam}</a>\n<b>{ZEDM}اليـوزر    ⤎  {zusr}</b>\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{zidd}</code>\n<b>{ZEDM}الرتبــه    ⤎ {zrtb} </b>\n<b>{ZEDM}الحساب  ⤎  {zpre}</b>\n<b>{ZEDM}الصـور    ⤎</b>  {zpic}\n<b>{ZEDM}الرسائل  ⤎</b>  {zmsg}  💌\n<b>{ZEDM}التفاعل  ⤎</b>  {ztmg}\n<b>{ZEDM}الـمجموعات المشتـركة ⤎  {zcom}</b>\n<b>{ZEDM}الإنشـاء  ⤎</b>  {zsnc}  🗓\n<b>{ZEDM}البايـو     ⤎  {zbio}</b>\nٴ<b>{ZEDF}</b>"
    },
    "2": {
        "name": "✨ كليشة عصرية",
        "template": "「 𓄂 𝑰𝑵𝑭𝑶𝑹𝑴𝑨𝑻𝑰𝑶𝑵 」\n•⎚•\n⎊ الاسم : {znam}\n⎊ اليوزر : {zusr}\n⎊ الايدي : <code>{zidd}</code>\n⎊ الرتبة : {zrtb}\n⎊ الحساب : {zpre}\n⎊ عدد الصور : {zpic}\n⎊ عدد الرسائل : {zmsg}\n⎊ التفاعل : {ztmg}\n⎊ تاريخ الانشاء : {zsnc}\n⎊ البايو : {zbio}\n•⎚•\n『 𝗔𝗥𝗥𝗔𝗦 𝗦𝗢𝗨𝗥𝗖𝗘 』"
    },
    "3": {
        "name": "⭐ كليشة أنيقة",
        "template": "╭━━━━━━━━━━━━╮\n┃ • ⌯ {znam}\n┃ • ⌯ {zusr}\n┃ • ⌯ <code>{zidd}</code>\n┃ • ⌯ {zrtb}\n┃ • ⌯ {zpre}\n┃ • ⌯ {zpic} صورة\n┃ • ⌯ {zmsg} رسالة\n┃ • ⌯ {ztmg}\n┃ • ⌯ {zsnc}\n┃ • ⌯ {zbio}\n╰━━━━━━━━━━━━╯"
    },
    "4": {
        "name": "🎨 كليشة ملونة",
        "template": "🎭 <b>{znam}</b>\n📝 <code>{zusr}</code>\n🆔 <code>{zidd}</code>\n👑 {zrtb}\n💎 {zpre}\n📸 {zpic} صور\n💬 {zmsg} رسائل\n🔥 {ztmg}\n📅 {zsnc}\n📝 {zbio}"
    },
    "5": {
        "name": "🔮 كليشة مطورة",
        "template": "⋆⋅☆⋅⋆ ── 𝙄𝙉𝙁𝙊 ── ⋆⋅☆⋅⋆\n\n➥ الاسم : {znam}\n➥ اليوزر : {zusr}\n➥ الايدي : <code>{zidd}</code>\n➥ الرتبة : {zrtb}\n➥ الحساب : {zpre}\n➥ الصور : {zpic}\n➥ الرسائل : {zmsg}\n➥ التفاعل : {ztmg}\n➥ الانشاء : {zsnc}\n➥ البايو : {zbio}\n\n⋆⋅☆⋅⋆ ── 𝗔𝗥𝗥𝗔𝗦 ── ⋆⋅☆⋅⋆"
    }
}

# متغيرات لتخزين اختيارات المستخدم
user_selected_template = {}
user_selected_button = {}

# ====================== دوال مساعدة معدلة ======================

async def fetch_zelzal(user_id):
    """جلب تاريخ إنشاء الحساب - مع معالجة الأخطاء"""
    try:
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
        response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data, timeout=10)
        
        if response.status_code != 200:
            return None
            
        result = response.json()
        
        if result and 'data' in result and result['data'] and 'date' in result['data']:
            return result['data']['date']
        else:
            return None
    except Exception as e:
        LOGS.error(f"خطأ في جلب تاريخ الإنشاء: {e}")
        return None

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

# ====================== أوامر تغيير الكليشة والزر ======================

@l313l.ar_cmd(pattern="تغيير الكليشة$")
async def change_template(event):
    """تغيير كليشة عرض معلومات المستخدم"""
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    zed = await edit_or_reply(event, "⇆")
    if Config.TG_BOT_USERNAME:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "تغيير_الكليشة")
        await response[0].click(event.chat_id)
        await zed.delete()
    else:
        await zed.edit("**- يرجى تعيين متغير TG_BOT_USERNAME اولا**")

@l313l.ar_cmd(pattern="تغيير الزر$")
async def change_button(event):
    """تغيير نوع الزر أسفل الكليشة"""
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    zed = await edit_or_reply(event, "⇆")
    if Config.TG_BOT_USERNAME:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "تغيير_الزر")
        await response[0].click(event.chat_id)
        await zed.delete()
    else:
        await zed.edit("**- يرجى تعيين متغير TG_BOT_USERNAME اولا**")

@l313l.ar_cmd(pattern="مسح التعديلات$")
async def reset_settings(event):
    """مسح جميع التعديلات والعودة للاعدادات الافتراضية"""
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    user_id = event.sender_id
    if user_id in user_selected_template:
        del user_selected_template[user_id]
    if user_id in user_selected_button:
        del user_selected_button[user_id]
    
    delgvar("Like_Id")
    remove_all_likes(l313l.uid)
    
    await edit_or_reply(event, "**✅ تم مسح جميع التعديلات والعودة للاعدادات الافتراضية بنجاح!**")

# ====================== أوامر اللايك ======================

@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫**")
    
    zed = await edit_or_reply(event, "⇆")
    if Config.TG_BOT_USERNAME:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
        await response[0].click(event.chat_id)
        await zed.delete()
    else:
        await zed.edit("**- يرجى تعيين متغير TG_BOT_USERNAME اولا**")

@l313l.ar_cmd(pattern="like(?: |$)(.*)")
async def who_like(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر .**")
    
    zed = await edit_or_reply(event, "⇆")
    if Config.TG_BOT_USERNAME:
        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
        await response[0].click(event.chat_id)
        await zed.delete()
    else:
        await zed.edit("**- يرجى تعيين متغير TG_BOT_USERNAME اولا**")

# ====================== قائمة المعجبين ======================

@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس**")
    
    likers = get_likes(l313l.uid)
    if likers:
        OUT_STR = f"𓆩 𝗮𝗥𝗥𝗮𝗦 𝗟𝗶𝗸𝗲 - **قائمـة المعجبيــن** ❤️𓆪\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n**• إجمالي عـدد المعجبيـن {len(likers)}**\n\n"
        for mogab in likers:
            OUT_STR += "**• الاسم:** [{}](tg://user?id={})\n**• الايـدي:** `{}`\n**• اليـوزر:** {}\n\n".format(mogab.f_name, mogab.lik_id, mogab.lik_id, mogab.f_user)
        await edit_or_reply(event, OUT_STR)
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯\n- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة**")
    
    likers = get_likes(l313l.uid)
    if likers:
        zed = await edit_or_reply(event, "**⪼ جـارِ مسـح المعجبيـن .. انتظـر ⏳**")
        remove_all_likes(l313l.uid)
        delgvar("Like_Id")
        await zed.edit("**⪼ تم حـذف جميـع المعجبيـن .. بنجـاح ✅**")
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯\n- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

# ====================== نظام الاستعلام المضمن ======================

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler_main(event):
        builder = event.builder
        query = event.text
        
        # نظام اختيار الكليشات
        if query.startswith("تغيير_الكليشة"):
            buttons = []
            for tid, tdata in ZID_TEMPLATES.items():
                buttons.append([Button.inline(f"📝 {tdata['name']}", data=f"select_temp_{tid}")])
            buttons.append([Button.inline("✖️ إلغاء", data="cancel_template")])
            
            result = builder.article(
                title="🎨 اختيار كليشة الأيدي",
                text="**اختر الكليشة التي تريد استخدامها لعرض معلومات المستخدم:**\n\n",
                buttons=buttons,
                parse_mode="md"
            )
            await event.answer([result])
            return
        
        # نظام اختيار نوع الزر
        elif query.startswith("تغيير_الزر"):
            buttons = [
                [Button.inline("❤️ نظام التفاعل (القلوب)", data="select_button_likes")],
                [Button.inline("👤 رابط الحساب (اسم المستخدم)", data="select_button_profile")],
                [Button.inline("✖️ إلغاء", data="cancel_template")]
            ]
            
            result = builder.article(
                title="🎛️ اختيار نوع الزر",
                text="**اختر نوع الزر الذي يظهر أسفل كليشة الأيدي:**\n\n- ❤️ نظام التفاعل: يسمح للآخرين بعمل لايك لك\n- 👤 رابط الحساب: يظهر زر باسم المستخدم رابط لملفك الشخصي",
                buttons=buttons,
                parse_mode="md"
            )
            await event.answer([result])
            return
        
        # نظام الـ idid الرئيسي
        elif query.startswith("idid") and event.query.user_id == l313l.uid:
            if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
                os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
            
            try:
                # جلب معلومات المستخدم
                replied_user = await l313l.get_me()
                if not replied_user:
                    return
                
                FullUser = (await l313l(GetFullUserRequest(replied_user.id))).full_user
                
                replied_user_profile_photos = await l313l(
                    GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
                )
                
                replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
                with contextlib.suppress(AttributeError):
                    if replied_user_profile_photos and hasattr(replied_user_profile_photos, 'count'):
                        replied_user_profile_photos_count = replied_user_profile_photos.count
                
                user_id = replied_user.id
                
                # جلب تاريخ الإنشاء
                zelzal_sinc = await fetch_zelzal(user_id)
                if not zelzal_sinc:
                    zelzal_sinc = "غيـر معلـوم"
                
                first_name = replied_user.first_name or "لا يوجد"
                full_name = FullUser.private_forward_name if FullUser.private_forward_name else first_name
                common_chat = FullUser.common_chats_count if FullUser.common_chats_count else 0
                username = f"@{replied_user.username}" if replied_user.username else "لا يـوجـد"
                user_bio = FullUser.about if FullUser.about else "لا يـوجـد"
                
                # التحقق من premium
                zilzal = False
                try:
                    user_entity = await l313l.get_entity(user_id)
                    zilzal = user_entity.premium if user_entity else False
                except:
                    zilzal = False
                
                if zilzal == True or user_id in zelzal:
                    zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
                else:
                    zpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
                
                # الرتبة
                if user_id in zelzal:
                    rotbat = "مطـور السـورس 𓄂" 
                elif user_id in zel_dev:
                    rotbat = "مـطـور 𐏕" 
                elif user_id == (await l313l.get_me()).id:
                    rotbat = "مـالك الحساب 𓀫" 
                else:
                    rotbat = "العضـو 𓅫"
                
                # عدد الرسائل
                try:
                    zmsg = await l313l.get_messages(event.chat_id, 0, from_user=user_id)
                    zzz = zmsg.total if zmsg else 0
                except:
                    zzz = 0
                
                # تقييم التفاعل
                if zzz < 100:
                    zelzzz = "غير متفاعل  🗿"
                elif 200 < zzz < 500:
                    zelzzz = "ضعيف  🗿"
                elif 500 < zzz < 700:
                    zelzzz = "شد حيلك  🏇"
                elif 700 < zzz < 1000:
                    zelzzz = "ماشي الحال  🏄🏻‍♂"
                elif 1000 < zzz < 2000:
                    zelzzz = "ملك التفاعل  🎖"
                elif 2000 < zzz < 3000:
                    zelzzz = "امبراطور التفاعل  🥇"
                elif 3000 < zzz < 4000:
                    zelzzz = "غنبله  💣"
                else:
                    zelzzz = "نار وشرر  🏆"
                
                ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن سـورس آراس"
                ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ "
                ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ʟx5x5 ─┄─┄─┄─⋆"
                
                # تحميل الصورة
                photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, str(user_id) + ".jpg")
                try:
                    await l313l.download_profile_photo(user_id, photo_path, download_big=True)
                except:
                    photo_path = None
                
                # جلب اختيارات المستخدم
                user_id_query = event.query.user_id
                template_id = user_selected_template.get(user_id_query, "1")
                button_type = user_selected_button.get(user_id_query, "likes")
                
                # تطبيق الكليشة المختارة
                if template_id in ZID_TEMPLATES:
                    caption = ZID_TEMPLATES[template_id]["template"].format(
                        znam=full_name,
                        zusr=username,
                        zidd=user_id,
                        zrtb=rotbat,
                        zpre=zpre,
                        zpic=replied_user_profile_photos_count,
                        zmsg=zzz,
                        ztmg=zelzzz,
                        zcom=common_chat,
                        zsnc=zelzal_sinc,
                        zbio=user_bio,
                        ZED_TEXT=ZED_TEXT,
                        ZEDM=ZEDM,
                        ZEDF=ZEDF
                    )
                else:
                    caption = f"<b> {ZED_TEXT} </b>\nٴ<b>{ZEDF}</b>\n<b>{ZEDM}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n<b>{ZEDM}الحساب  ⤎  {zpre}</b>\n<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n<b>{ZEDM}الإنشـاء  ⤎</b>  {zelzal_sinc}  🗓\n<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\nٴ<b>{ZEDF}</b>"
                
                # إنشاء الزر حسب الاختيار
                Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
                
                if button_type == "likes":
                    button_text = f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}"
                    buttons = [[Button.inline(button_text, data="likes", style="primary")]]
                else:
                    user_name = first_name if first_name and first_name != "لا يوجد" else "حسابي"
                    buttons = [[Button.url(f"👤 {user_name}", f"tg://user?id={user_id}")]]
                
                try:
                    if photo_path and os.path.exists(photo_path):
                        uploaded_file = await event.client.upload_file(file=photo_path)
                        result = builder.photo(
                            uploaded_file,
                            text=caption,
                            buttons=buttons,
                            link_preview=False,
                            parse_mode="html",
                        )
                        os.remove(photo_path)
                    else:
                        result = builder.article(
                            title=f"معلومات {full_name}",
                            text=caption,
                            buttons=buttons,
                            link_preview=False,
                            parse_mode="html",
                        )
                    await event.answer([result])
                except Exception as e:
                    LOGS.error(f"Error sending result: {e}")
                    result = builder.article(
                        title=f"معلومات {full_name}",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
                    await event.answer([result])
                    
            except Exception as e:
                LOGS.error(f"Error in idid: {e}")
            return

    # ====================== معالجة أزرار الكليشات ======================
    
    @tgbot.on(CallbackQuery(data=re.compile(rb"select_temp_(\d+)")))
    async def on_select_template(event):
        template_id = event.pattern_match.group(1).decode()
        user_id = event.sender_id
        
        if template_id in ZID_TEMPLATES:
            user_selected_template[user_id] = template_id
            await event.edit(f"✅ **تم اختيار الكليشة بنجاح!**\n\n**الكليشة المختارة:** {ZID_TEMPLATES[template_id]['name']}\n\nيمكنك الآن استخدام امر `.لايك` لرؤية الكليشة الجديدة.")
        else:
            await event.edit("❌ **حدث خطأ في اختيار الكليشة**")
        await event.answer()

    @tgbot.on(CallbackQuery(data=re.compile(rb"select_button_(likes|profile)")))
    async def on_select_button(event):
        button_type = event.pattern_match.group(1).decode()
        user_id = event.sender_id
        
        user_selected_button[user_id] = button_type
        
        if button_type == "likes":
            await event.edit("✅ **تم اختيار نظام التفاعل (القلوب)!**\n\nسوف يظهر زر اللايك أسفل الكليشة ليتمكن الآخرون من الاعجاب بك.")
        else:
            await event.edit("✅ **تم اختيار رابط الحساب!**\n\nسوف يظهر زر باسم المستخدم أسفل الكليشة، عند الضغط عليه يتم فتح ملفك الشخصي.")
        await event.answer()

    @tgbot.on(CallbackQuery(data=re.compile(rb"cancel_template")))
    async def on_cancel_template(event):
        await event.edit("❌ **تم الغاء العملية**")
        await event.answer()

    # ====================== نظام اللايك ======================
    
    @tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
    async def on_like_click(event):
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
        
        Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
        
        if add_like(str(l313l.uid), str(user_id), user_name, user_username) is True:
            Like_id += 1
            addgvar("Like_Id", Like_id)
        else:
            return await event.answer("- انت معجب من قبل بهذا الشخص ❤️", cache_time=0, alert=True)
        
        try:
            await l313l.send_message(
                BOTLOG_CHATID,
                "#الايـدي_بـ_لايــك 💝\n\n"
                f"**- المُستخـدِم :** {_format.mentionuser(user_name ,user_id)} \n"
                f"**- الايدي** `{user_id}`\n"
                f"**- اليـوزر :** {user_username} \n"
                f"**- قام بعمـل لايـك لـ الايـدي الخـاص بـك ♥️**\n"
                f"**- اصبح عـدد معجبينك هـو :** {Like_id} 🤳\n"
                f"**- لـ عـرض قائمـة المعجبيـن ارسـل:** ( `.المعجبين` ) 🎴\n"
                f"**- لـ مسح قائمـة المعجبيـن ارسـل:** ( `.مسح المعجبين` ) 🗑",
            )
        except Exception as e:
            LOGS.error(f"Error sending like notification: {e}")
        
        try:
            await event.edit(buttons=[[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes", style="primary")]])
            await event.answer("- تم إضافة إعجابك لـ هذا الشخص ♥️", cache_time=0, alert=True)
        except Exception:
            await event.answer("- تم إضافة إعجابك لـ هذا الشخص ♥️", cache_time=0, alert=True)
