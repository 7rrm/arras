import asyncio
import contextlib
import re
import random
import time
import os
import requests
from datetime import datetime

from telethon import Button, events
from telethon.events import CallbackQuery
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest

from . import StartTime, l313l, mention
from ..core import check_owner
from ..Config import Config
from ..utils import Zed_Dev
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.like_sql import (
    add_like,
    get_likes,
    remove_all_likes,
    remove_like,
)
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "العروض"
LOGS = logging.getLogger(__name__)

zed_dev = Zed_Dev
zelzal = (5427469031, 5280339206)
Zel_Uid = l313l.uid

ZED_BLACKLIST = [-1001935599871]

# متغير لتخزين الصفحات
template_pages = {}

# =========================================================== #
# الحصول على معلومات الحساب تلقائياً
# =========================================================== #

async def get_my_account_info():
    """استخراج معلومات الحساب الحالي تلقائياً"""
    me = await l313l.get_me()
    my_username = me.username if me.username else None
    my_name = me.first_name
    my_id = me.id
    return my_username, my_name, my_id

# =========================================================== #
# كليشات الايدي (ID Templates)
# =========================================================== #

# الكليشة الأساسية (الطويلة)
DEFAULT_TEMPLATE = (
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

# الكليشات الأخرى
ID_TEMPLATES = {
    "elegant": {
        "name": "أنيق",
        "template": (
            "╭━━━━━━━━━━━━━━━╮\n"
            "┃ ✦ <b>الاســم</b> : {znam}\n"
            "┃ ✦ <b>اليـوزر</b> : {zusr}\n"
            "┃ ✦ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "┃ ✦ <b>الرتبــه</b> : {zrtb}\n"
            "┃ ✦ <b>الحساب</b> : {zpre}\n"
            "╰━━━━━━━━━━━━━━━╯"
        )
    },
    "simple": {
        "name": "بسيط",
        "template": (
            "👤 <b>{znam}</b>\n"
            "🆔 <code>{zidd}</code>\n"
            "📝 {zusr}\n"
            "⭐ {zpre}"
        )
    },
    "minimal": {
        "name": "صغير",
        "template": (
            "<code>{zidd}</code> | {znam}\n"
            "{zusr}"
        )
    },
    "box": {
        "name": "صندوق",
        "template": (
            "┌─────────────────┐\n"
            "│ ✦ {znam}\n"
            "│ ✦ <code>{zidd}</code>\n"
            "│ ✦ {zusr}\n"
            "│ ✦ {zrtb}\n"
            "└─────────────────┘"
        )
    },
    "star": {
        "name": "نجوم",
        "template": (
            "★━━━━━━━━━━━━━━━━━━★\n"
            "✧ <b>الاســم</b> : {znam}\n"
            "✧ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "✧ <b>اليـوزر</b> : {zusr}\n"
            "✧ <b>الرتبــه</b> : {zrtb}\n"
            "★━━━━━━━━━━━━━━━━━━★"
        )
    },
    "arrow": {
        "name": "سهام",
        "template": (
            "➜ <b>الاســم</b> : {znam}\n"
            "➜ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "➜ <b>اليـوزر</b> : {zusr}\n"
            "➜ <b>الرتبــه</b> : {zrtb}"
        )
    },
    "heart": {
        "name": "قلوب",
        "template": (
            "♥️ <b>الاســم</b> : {znam}\n"
            "♥️ <b>الايـدي</b> : <code>{zidd}</code>\n"
            "♥️ <b>اليـوزر</b> : {zusr}\n"
            "♥️ <b>الرتبــه</b> : {zrtb}\n"
            "♥️ <b>الحساب</b> : {zpre}"
        )
    }
}

# =========================================================== #
# دوال مساعدة
# =========================================================== #

async def fetch_zelzal(user_id):
    headers = {
        'Host': 'restore-access.indream.app',
        'Connection': 'keep-alive',
        'x-api-key': 'e758fb28-79be-4d1c-af6b-066633ded128',
        'Accept': '*/*',
        'Accept-Language': 'ar',
        'User-Agent': 'Nicegram/101 CFNetwork/1404.0.5 Darwin/22.3.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"telegramId":' + str(user_id) + '}'
    try:
        response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
        return response['data']['date']
    except Exception:
        return "غير معلوم"

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
    replied_user_profile_photos_count = replied_user_profile_photos.count if replied_user_profile_photos else "لا يوجد"
    
    zelzal_sinc = await fetch_zelzal(user_id)
    first_name = replied_user.first_name
    full_name = FullUser.private_forward_name or first_name
    common_chat = FullUser.common_chats_count
    username = f"@{replied_user.username}" if replied_user.username else "لا يوجد"
    user_bio = FullUser.about or "لا يوجد"
    
    zilzal = (await l313l.get_entity(user_id)).premium
    zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟" if zilzal or user_id in zelzal else "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    
    photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, str(user_id) + ".jpg")
    await l313l.download_profile_photo(user_id, photo_path, download_big=True)
    
    first_name = first_name.replace("\u2060", "") if first_name else "مستخدم"
    zzzsinc = zelzal_sinc if zelzal_sinc else "غير معلوم"
    
    # حساب عدد الرسائل
    try:
        zmsg = await l313l.get_messages(event.chat_id, 0, from_user=user_id)
        zzz = zmsg.total if zmsg else 0
    except Exception:
        zzz = 0
    
    if zzz < 100:
        zelzzz = "غير متفاعل 🗿"
    elif zzz < 500:
        zelzzz = "ضعيف 🗿"
    elif zzz < 700:
        zelzzz = "شد حيلك 🏇"
    elif zzz < 1000:
        zelzzz = "ماشي الحال 🏄🏻‍♂"
    elif zzz < 2000:
        zelzzz = "ملك التفاعل 🎖"
    elif zzz < 3000:
        zelzzz = "امبراطور التفاعل 🥇"
    elif zzz < 4000:
        zelzzz = "غنبله 💣"
    else:
        zelzzz = "نار وشرر 🏆"
    
    # تحديد الرتبة
    if user_id in zelzal:
        rotbat = "مطـور السـورس 𓄂" 
    elif user_id in zed_dev:
        rotbat = "مـطـور 𐏕" 
    elif user_id == (await l313l.get_me()).id:
        rotbat = "مـالك الحساب 𓀫" 
    else:
        rotbat = "العضـو 𓅫"
    
    # الكليشة المختارة (إذا لم تكن مختارة، استخدم الأساسية)
    selected_template = gvarstatus("SELECTED_ID_TEMPLATE")
    if selected_template and selected_template in ID_TEMPLATES:
        template_data = ID_TEMPLATES[selected_template]
        template = template_data["template"]
    else:
        template = DEFAULT_TEMPLATE
    
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

# =========================================================== #
# الاستعلامات المضمنة
# =========================================================== #

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler_like(event):
        builder = event.builder
        query = event.text
        await l313l.get_me()
        
        # ✅ استعلام idid - بطاقة المعلومات
        if query.startswith("idid") and event.query.user_id == l313l.uid:
            try:
                photo_path, caption = await fetch_info(event)
            except Exception as e:
                return
            
            like_button_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
            my_username, my_name, my_id = await get_my_account_info()
            my_link = f"https://t.me/{my_username}" if my_username else f"tg://user?id={my_id}"
            
            # زر واحد فقط حسب النمط المختار
            if like_button_mode == "likes":
                Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
                buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes", style="primary")]]
            else:
                buttons = [[Button.url(f"👤 {my_name}", my_link, style="primary")]]
            
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
                        title="l313l",
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
            except Exception:
                result = builder.article(
                    title="l313l",
                    text=caption,
                    buttons=buttons,
                    link_preview=False,
                    parse_mode="html",
                )
            
            await event.answer([result] if result else None)
        
        # ✅ استعلام كليشات الايدي
        elif query.startswith("id_templates") and event.query.user_id == l313l.uid:
            user_id = event.query.user_id
            template_keys = list(ID_TEMPLATES.keys())
            total_pages = len(template_keys)
            
            current_page = template_pages.get(user_id, 0)
            if current_page >= total_pages:
                current_page = 0
            current_key = template_keys[current_page]
            current_template = ID_TEMPLATES[current_key]
            
            text = f"**🎨 الكليشة {current_page + 1}/{total_pages}**\n\n"
            text += f"```\n{current_template['template'][:500]}\n```\n"
            text += f"• **الاسم:** {current_template['name']}"
            
            buttons = []
            nav_buttons = []
            if current_page > 0:
                nav_buttons.append(Button.inline("◀️ رجوع", data="template_prev", style="primary"))
            if current_page < total_pages - 1:
                nav_buttons.append(Button.inline("التالي ▶️", data="template_next", style="primary"))
            
            if nav_buttons:
                buttons.append(nav_buttons)
            
            buttons.append([
                Button.inline("💾 حفظ الكليشة", data=f"template_save_{current_key}", style="success"),
                Button.inline("❌ إغلاق", data="close_panel", style="danger")
            ])
            
            result = builder.article(
                title="🎨 كليشات الايدي",
                description=f"الكليشة {current_page + 1}/{total_pages}: {current_template['name']}",
                text=text,
                buttons=buttons,
                link_preview=False,
                parse_mode="Markdown",
            )
            await event.answer([result], cache_time=0)
        
        # ✅ استعلام نمط اللايك
        elif query.startswith("like_mode") and event.query.user_id == l313l.uid:
            current_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
            my_username, my_name, my_id = await get_my_account_info()
            
            text = f"**⚙️ إعدادات زر اللايك**\n\n"
            text += f"• النمط الحالي: **{'❤️ نمط القلوب' if current_mode == 'likes' else '👤 نمط الحساب'}**\n\n"
            text += f"• شكل الزر:\n"
            
            if current_mode == "likes":
                text += f"`ʟɪᴋᴇ ♥️ ⤑ (العدد)`\n"
                text += f"• زر الإعجاب فقط"
            else:
                text += f"`👤 {my_name}`\n"
                text += f"• رابط حسابك فقط"
            
            text += f"\n\n• استخدم الأمر `.نمط اللايك` مرة أخرى للتبديل"
            
            buttons = [[Button.inline("🔄 تبديل النمط", data="toggle_like_mode", style="primary")]]
            buttons.append([Button.inline("❌ إغلاق", data="close_panel", style="danger")])
            
            result = builder.article(
                title="⚙️ إعدادات اللايك",
                description=f"النمط الحالي: {'قلوب' if current_mode == 'likes' else 'حساب'}",
                text=text,
                buttons=buttons,
                link_preview=False,
                parse_mode="Markdown",
            )
            await event.answer([result], cache_time=0)

# =========================================================== #
# أوامر المستخدم
# =========================================================== #

@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷**")
    
    zed = await edit_or_reply(event, "⇆")
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
    await response[0].click(event.chat_id)
    await zed.delete()

@l313l.ar_cmd(pattern="كليشات الايدي$")
async def id_templates_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "id_templates")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="نمط اللايك$")
async def like_mode_cmd(event):
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "like_mode")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    likers = get_likes(l313l.uid)
    if likers:
        OUT_STR = "𓆩 𝗮𝗥𝗥𝗮𝗦 𝗟𝗶𝗸𝗲 - **قائمـة المعجبيــن** ❤️𓆪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
        for mogab in likers:
            OUT_STR += f"\n• **الاسم:** [{mogab.f_name}](tg://user?id={mogab.lik_id})\n• **الايـدي:** `{mogab.lik_id}`\n• **اليـوزر:** {mogab.f_user}\n"
        OUT_STR += f"\n• **إجمالي عـدد المعجبيـن {len(likers)}**"
        await edit_or_reply(event, OUT_STR)
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵**")
    
    likers = get_likes(l313l.uid)
    if likers:
        zed = await edit_or_reply(event, "⪼ جـارِ مسـح المعجبيـن .. انتظـر ⏳")
        remove_all_likes(l313l.uid)
        delgvar("Like_Id")
        await zed.edit("⪼ تم حـذف جميـع المعجبيـن .. بنجـاح ✅")
    else:
        await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯**\n**- ماعنـدك معجبيـن حالياً ❤️‍🩹**")

@l313l.ar_cmd(pattern="مسح الاعدادات$")
async def reset_settings(event):
    delgvar("SELECTED_ID_TEMPLATE")
    delgvar("LIKE_BUTTON_MODE")
    delgvar("Like_Id")
    remove_all_likes(l313l.uid)
    await edit_or_reply(event, "✅ تم مسح جميع الإعدادات والتغييرات بنجاح!\n\n• عادت الكليشة إلى الأساسية\n• عاد نمط اللايك إلى القلوب\n• تم مسح جميع المعجبين")

# =========================================================== #
# أزرار التفاعل (CallbackQuery) - النسخة المصححة
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
async def like_callback(event):
    user_id = event.sender_id
    
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
    
    # إرسال إشعار للمطور
    try:
        await l313l.send_message(
            BOTLOG_CHATID,
            f"#لايك_جديد 💝\n\n"
            f"**- المستخدم :** [{user_name}](tg://user?id={user_id})\n"
            f"**- الايدي :** `{user_id}`\n"
            f"**- اليوزر :** {user_username}\n"
            f"**- أصبح عدد المعجبين :** {Like_id}",
        )
    except Exception:
        pass
    
    # تحديث الزر حسب النمط
    if like_button_mode == "likes":
        button_text = f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}"
        button_data = "likes"
        buttons = [[Button.inline(button_text, data=button_data, style="primary")]]
    else:
        my_username, my_name, my_id = await get_my_account_info()
        my_link = f"https://t.me/{my_username}" if my_username else f"tg://user?id={my_id}"
        buttons = [[Button.url(f"👤 {my_name}", my_link, style="primary")]]
    
    try:
        await event.edit(buttons=buttons)
        await event.answer(f"✅ تم إضافة إعجابك لـ {user_name}!", alert=True)
    except Exception:
        await event.answer(f"✅ تم إضافة إعجابك لـ {user_name}!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"template_prev")))
async def template_prev(event):
    user_id = event.query.user_id
    current_page = template_pages.get(user_id, 0)
    if current_page > 0:
        template_pages[user_id] = current_page - 1
    
    # إصلاح: استخدام input_chat
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "id_templates")
    if response:
        await response[0].click(event.input_chat)
    await event.delete()

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"template_next")))
async def template_next(event):
    user_id = event.query.user_id
    current_page = template_pages.get(user_id, 0)
    total_pages = len(ID_TEMPLATES)
    
    # منع تجاوز الحد الأقصى
    if current_page + 1 < total_pages:
        template_pages[user_id] = current_page + 1
    
    # إصلاح: استخدام input_chat
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "id_templates")
    if response:
        await response[0].click(event.input_chat)
    await event.delete()

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"template_save_(.+)")))
async def template_save(event):
    match = re.match(r"template_save_(.+)", event.data.decode())
    if not match:
        return
    
    template_key = match.group(1)
    if template_key in ID_TEMPLATES:
        addgvar("SELECTED_ID_TEMPLATE", template_key)
        await event.edit(f"✅ تم حفظ كليشة **{ID_TEMPLATES[template_key]['name']}** بنجاح!\n\n• ستظهر في جميع بطاقات الـ .لايك")
    else:
        await event.answer("❌ كليشة غير موجودة!", alert=True)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"toggle_like_mode")))
async def toggle_like_mode(event):
    current_mode = gvarstatus("LIKE_BUTTON_MODE") or "likes"
    new_mode = "profile" if current_mode == "likes" else "likes"
    addgvar("LIKE_BUTTON_MODE", new_mode)
    
    mode_name = "نمط الحساب" if new_mode == "profile" else "نمط القلوب"
    
    # تعديل الرسالة بدلاً من حذفها (لأنها رسالة مضمنة)
    await event.edit(f"✅ تم التبديل إلى **{mode_name}** بنجاح!")
    await asyncio.sleep(2)
    # إغلاق القائمة
    await event.edit("❌ تم إغلاق القائمة!", buttons=None, parse_mode="Markdown")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"close_panel")))
async def close_panel(event):
    """إغلاق القائمة"""
    await event.edit("❌ تم إغلاق القائمة!", buttons=None, parse_mode="Markdown")
