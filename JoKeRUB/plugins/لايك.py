
from JoKeRUB import l313l, bot, tgbot
import time
import os
import requests
import logging
from telethon import Button, events
from ..Config import Config
from ..core import check_owner
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
import asyncio
import contextlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إعدادات نظام الهاك
REH = "**᯽︙ لأستخدام بوت اختراق الحساب عن طريق كود التيرمكس أضغط على الزر**"
JOKER_PIC = "https://graph.org/file/a467d3702fbc9ae391fe0-e6322ec96a2fd4c1f4.jpg"

# إعدادات نظام تعديل الصور
EDIT_TEXT = "**🖼️︙ لأستخدام بوت تعديل الصور أضغط على الزر**"
EDIT_PIC = "https://graph.org/file/c00c3a5e933e190dbe53e-fbcab545545de622ea.jpg"

Bot_Username = Config.TG_BOT_USERNAME

# ========== نظام اللايك ==========
# الكود المطلوب لنظام اللايك
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from . import BOTLOG, BOTLOG_CHATID, spamwatch, mention
from ..helpers import reply_id
from ..helpers.utils import _format
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.like_sql import (
    add_like,
    get_likes,
    remove_all_likes,
    remove_like,
)

zed_dev = (5427469031, 1985225531)
zelzal = (5427469031, 5280339206)
Zel_Uid = l313l.uid

# دالة الحصول على معلومات المستخدم
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

async def fetch_info(event):
    """Get details from the User object."""
    replied_user = await l313l.get_me()
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
    
    zmsg = await bot.get_messages(event.chat_id, 0, from_user=user_id)
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
    
    ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن سـورس آراس"
    ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ "
    ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ʟx5x5 ─┄─┄─┄─⋆"
    
    if gvarstatus("ZID_TEMPLATE") is None:
        caption = f"<b> {ZED_TEXT} </b>\n"
        caption += f"ٴ<b>{ZEDF}</b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> "
        caption += f'<a href="tg://user?id={user_id}">{full_name}</a>'
        caption += f"\n<b>{ZEDM}اليـوزر    ⤎  {username}</b>"
        caption += f"\n<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
        if zilzal == True or user_id in zelzal:
            caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
        caption += f"<b>{ZEDM}الاشتراك  ⤎  𝕍𝕀ℙ 💎</b>\n"
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

# ========== المعالج الموحد ==========
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "") if Bot_Username else ""
        query = event.text
        
        logger.info(f"Inline Query Received: {query} from user: {event.query.user_id}")
        
        if not query:
            return
        
        # ===== نظام الهاك =====
        if query.startswith("هاك"):
            if event.query.user_id != bot.uid:
                return
            buttons = Button.url("• اضغط هنا عزيزي •", f"https://t.me/{joker}")
            if JOKER_PIC and JOKER_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    JOKER_PIC, 
                    text=REH, 
                    buttons=buttons, 
                    link_preview=False
                )
            elif JOKER_PIC:
                result = builder.document(
                    JOKER_PIC,
                    title="Aljoker 🤡",
                    text=REH,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="Aljoker 🤡",
                    text=REH,
                    buttons=buttons,
                    link_preview=False,
                )
        
        # ===== نظام تعديل الصور =====
        elif query.startswith("صور"):
            if event.query.user_id != bot.uid:
                return
            buttons = Button.url("• اضغط هنا عزيزي •", f"https://t.me/{joker}")
            if EDIT_PIC and EDIT_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    EDIT_PIC, 
                    text=EDIT_TEXT, 
                    buttons=buttons, 
                    link_preview=False
                )
            elif EDIT_PIC:
                result = builder.document(
                    EDIT_PIC,
                    title="بوت تعديل الصور 🎨",
                    text=EDIT_TEXT,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="بوت تعديل الصور 🎨",
                    text=EDIT_TEXT,
                    buttons=buttons,
                    link_preview=False,
                )
        
        # ===== نظام اللايك =====
        elif query.startswith(("idid", "لايك")):
            if event.query.user_id != l313l.uid:
                return
            
            # التحقق من VIP إذا لزم الأمر
            # if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
            #     return await event.answer([])
            
            if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
                os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
            
            try:
                photo_path, caption = await fetch_info(event)
            except (AttributeError, TypeError):
                logger.error("Failed to fetch user info")
                return await event.answer([])
            
            message_id_to_reply = None
            if gvarstatus("ZID_TEMPLATE") is None:
                try:
                    uploaded_file = await event.client.upload_file(file=photo_path)
                    Like_id = gvarstatus("Like_Id")
                    Like_id = Like_id if Like_id else 0
                    buttons = [[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]]
                    result = builder.photo(
                        uploaded_file,
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
                    if not photo_path.startswith("http"):
                        os.remove(photo_path)
                except (TypeError, Exception) as e:
                    logger.error(f"Error uploading photo: {e}")
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
                        text=caption,
                        buttons=buttons,
                        link_preview=False,
                        parse_mode="html",
                    )
                    if not photo_path.startswith("http"):
                        os.remove(photo_path)
                except (TypeError, Exception) as e:
                    logger.error(f"Error uploading photo: {e}")
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
        
        # إرسال النتيجة
        if result:
            await event.answer([result])
            logger.info(f"Result sent for query: {query}")
        else:
            await event.answer([])
            logger.warning(f"No result for query: {query}")

# ========== الأوامر ==========
from ..utils import admin_cmd

@bot.on(admin_cmd(outgoing=True, pattern="هاك"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    await bot.send_message(lMl10l, "/hack")
    response = await bot.inline_query(lMl10l, "هاك")
    await response[0].click(event.chat_id)
    await event.delete()

@bot.on(admin_cmd(outgoing=True, pattern="صور"))
async def photo_edit_command(event):
    if event.fwd_from:
        return
    
    bot_user = Config.TG_BOT_USERNAME
    
    if event.reply_to_msg_id:
        await event.get_reply_message()
    
    await bot.send_message(bot_user, "/edit")
    response = await bot.inline_query(bot_user, "صور")
    
    if response:
        await response[0].click(event.chat_id)
    
    await event.delete()

@bot.on(admin_cmd(outgoing=True, pattern="لايك(?: |$)(.*)"))
async def who(event):
    # يمكنك إضافة شروط VIP هنا إذا لزم الأمر
    # if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
    #     return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\nتواصل : @Lx5x5**")
    
    input_str = event.pattern_match.group(1)
    reply = event.reply_to_msg_id
    if input_str and reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    if input_str or reply:
        return await edit_or_reply(event, "**- ارسـل الامـر بـدون رد**")
    
    zed = await edit_or_reply(event, "⇆")
    if event.reply_to_msg_id:
        await event.get_reply_message()
        return
    
    response = await bot.inline_query(Config.TG_BOT_USERNAME, "لايك")
    await response[0].click(event.chat_id)
    await zed.delete()

# ========== معالج زر اللايك ==========
import re
@tgbot.on(events.CallbackQuery(data=re.compile(rb"likes")))
async def _(event):
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
    
    if add_like(str(l313l.uid), str(user.id), user_name, user_username) is True:
        Like_id += 1
        addgvar("Like_Id", Like_id)
    else:
        return await event.answer("- انت معجب من قبل بهذا الشخص ❤️", cache_time=0, alert=True)
    
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
    
    try:
        await event.edit(buttons=[[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]])
        await event.answer("- تم إضافة إعجابك لـ هذا الشخص ♥️", cache_time=0, alert=True)
    except Exception:
        await event.answer("- تم إضافة إعجابك لـ هذا الشخص ♥️", cache_time=0, alert=True)
