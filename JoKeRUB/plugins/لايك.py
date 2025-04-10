import os
import re
import contextlib
import requests
from datetime import datetime
from platform import python_version
from telethon import Button, version
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetUsersRequest, GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.errors.rpcerrorlist import ChatSendMediaForbiddenError
from ..sql_helper.like_sql import (
    add_like,
    get_likes,
    remove_all_likes,
    remove_like,
)
from ..core import check_owner
from ..Config import Config
from ..helpers import _format, mention
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import StartTime, l313l, BOTLOG_CHATID
from ..utils import Zed_Vip, Zed_Dev

plugin_category = "tools"
LOGS = logging.getLogger(__name__)
#Code by T.me/zzzzl1l
zed_dev = Zed_Dev
zel_dev = (5176749470, 5427469031, 6269975462, 1985225531)
zelzal = (925972505, 5427469031, 5280339206)
Zel_Uid = l313l.uid

ZED_BLACKLIST = [
    -1001935599871,
]

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
    try:
        response = requests.post('https://restore-access.indream.app/regdate', headers=headers, data=data).json()
        zelzal_date = response['data']['date']
        return zelzal_date
    except:
        return None

async def fetch_info(event):
    """الحصول على معلومات المستخدم"""
    replied_user = await event.client.get_me()
    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
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
    
    if zilzal == True or user_id in zelzal:
        zpre = "ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟"
    else:
        zpre = "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨"
    
    photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, f"user_{user_id}.jpg")
    try:
        photo = await l313l.download_profile_photo(
            user_id,
            photo_path,
            download_big=True,
        )
    except:
        photo_path = None
    
    first_name = first_name.replace("\u2060", "") if first_name else "هذا المستخدم ليس له اسم أول"
    full_name = full_name or first_name
    username = f"@{username}" if username else "لا يـوجـد"
    user_bio = "لا يـوجـد" if not user_bio else user_bio
    zzzsinc = zelzal_sinc if zelzal_sinc else "غيـر معلـوم"
    
    zmsg = await bot.get_messages(event.chat_id, 0, from_user=user_id)
    zzz = zmsg.total
    
    if zzz < 100:
        zelzzz = "غير متفاعل 🗿"
    elif 200 < zzz < 500:
        zelzzz = "ضعيف 🗿"
    elif 500 < zzz < 700:
        zelzzz = "شد حيلك 🏇"
    elif 700 < zzz < 1000:
        zelzzz = "ماشي الحال 🏄🏻‍♂"
    elif 1000 < zzz < 2000:
        zelzzz = "ملك التفاعل 🎖"
    elif 2000 < zzz < 3000:
        zelzzz = "امبراطور التفاعل 🥇"
    elif 3000 < zzz < 4000:
        zelzzz = "غنبله 💣"
    else:
        zelzzz = "نار وشرر 🏆"
    
    if user_id in zelzal:
        rotbat = "مطـور السـورس 𓄂"
    elif user_id in zed_dev:
        rotbat = "مـطـور 𐏕"
    elif user_id == (await event.client.get_me()).id:
        rotbat = "مـالك الحساب 𓀫"
    else:
        rotbat = "العضـو 𓅫"
    
    ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن بـوت زدثــون"
    ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ "
    ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ᶻᵗʰᵒᶰ ─┄─┄─┄─⋆"
    
    if gvarstatus("ZID_TEMPLATE") is None:
        caption = f"<b>{ZED_TEXT}</b>\n"
        caption += f"ٴ<b>{ZEDF}</b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
        caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
        caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
        if zilzal == True or user_id in zelzal:
            caption += f"<b>{ZEDM}الحساب  ⤎  {zpre}</b>\n"
        caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
        caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
        caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n"
        if user_id != (await l313l.get_me()).id:
            caption += f"<b>{ZEDM}الـمجموعات المشتـركة ⤎  {common_chat}</b>\n"
        caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zzzsinc}  🗓\n"
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
            zpic=replied_user_profile_photos_count,
            zmsg=zzz,
            ztmg=zelzzz,
            zcom=common_chat,
            zsnc=zzzsinc,
            zbio=user_bio,
        )
    
    return photo_path, caption

@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def who(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    input_str = event.pattern_match.group(1)
    reply = event.reply_to_msg_id
    
    if input_str and reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    if input_str or reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    
    zed = await edit_or_reply(event, "**⏳ جاري جلب المعلومات...**")
    
    try:
        photo_path, caption = await fetch_info(event)
        Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
        buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]]
        
        try:
            if photo_path and os.path.exists(photo_path):
                await event.client.send_file(
                    event.chat_id,
                    photo_path,
                    caption=caption,
                    buttons=buttons,
                    parse_mode="html"
                )
                os.remove(photo_path)
            else:
                await event.client.send_message(
                    event.chat_id,
                    caption,
                    buttons=buttons,
                    parse_mode="html"
                )
        except Exception as e:
            await zed.edit(f"**- حدث خطأ ❌:**\n`{str(e)}`")
            return
    except Exception as e:
        await zed.edit(f"**- حدث خطأ أثناء جلب المعلومات ❌:**\n`{str(e)}`")
        return
    
    await zed.delete()

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
async def _(event):
    user_id = event.sender_id
    try:
        user = await l313l.get_entity(user_id)
        user_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        user_username = f"@{user.username}" if user.username else "لا يوجد"
    except Exception:
        user_name = "مستخدم محذوف"
        user_username = "لا يوجد"
    
    Like_id = int(gvarstatus("Like_Id")) if gvarstatus("Like_Id") else 0
    
    if add_like(str(l313l.uid), str(user.id), user_name, user_username):
        Like_id += 1
        addgvar("Like_Id", Like_id)
        
        try:
            await event.edit(buttons=[[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]])
            await event.answer(f"تم إضافة إعجابك ♥️ (الإجمالي: {Like_id})", alert=False)
            
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#إعجاب_جديد\n\n"
                    f"👤 المستخدم: [{user_name}](tg://user?id={user_id})\n"
                    f"🆔 الايدي: `{user_id}`\n"
                    f"🔗 اليوزر: {user_username}\n"
                    f"📊 الإجمالي: {Like_id} إعجاب"
                )
        except Exception as e:
            await event.answer(f"تم تسجيل إعجابك لكن حدث خطأ في التحديث: {str(e)}", alert=True)
    else:
        await event.answer("لقد قمت بالإعجاب من قبل! ❤️", alert=True)

@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    likers = get_likes(l313l.uid)
    if not likers:
        return await edit_or_reply(event, "**- لا يوجد معجبين حتى الآن!**")
    
    output = "**𓆩 قائمة المعجبين ♥️𓆪**\n**━━━━━━━━━━━━━━━━━━**\n"
    for i, liker in enumerate(likers, start=1):
        output += f"{i}. [{liker.f_name}](tg://user?id={liker.lik_id}) - `{liker.lik_id}`\n"
    
    output += f"\n**𓆩 الإجمالي: {len(likers)} معجب𓆪**"
    await edit_or_reply(event, output)

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    likers = get_likes(l313l.uid)
    if not likers:
        return await edit_or_reply(event, "**- لا يوجد معجبين ليتم مسحهم!**")
    
    remove_all_likes(l313l.uid)
    delgvar("Like_Id")
    await edit_or_reply(event, "**✓ تم مسح جميع المعجبين بنجاح**")
