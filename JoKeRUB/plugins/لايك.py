import os
import re
import requests
from telethon import Button, events
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.errors.rpcerrorlist import ChatSendMediaForbiddenError

from . import l313l
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..sql_helper.like_sql import (
    add_like,
    get_likes,
    remove_all_likes,
    remove_like,
)
from . import BOTLOG_CHATID
from ..helpers import _format
from ..core.managers import edit_or_reply

plugin_category = "العروض"

# الكائنات الثابتة
zel_dev = (5176749470, 5427469031, 6269975462, 1985225531)
zelzal = (925972505, 5427469031, 5280339206)
Zel_Uid = l313l.uid
ZED_BLACKLIST = [-1001935599871]

async def fetch_zelzal(user_id):
    """تاريخ الإنشاء الثابت 2022"""
    return "2022"

async def fetch_info(event):
    """جلب معلومات المستخدم"""
    replied_user = await l313l.get_me()
    FullUser = (await l313l(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await l313l(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)
    
    replied_user_profile_photos_count = "لا يـوجـد بروفـايـل"
    with contextlib.suppress(AttributeError):
        replied_user_profile_photos_count = replied_user_profile_photos.count

    user_id = replied_user.id
    zelzal_sinc = await fetch_zelzal(user_id)
    first_name = replied_user.first_name
    full_name = FullUser.private_forward_name or first_name
    common_chat = FullUser.common_chats_count
    username = "@{}".format(replied_user.username) if replied_user.username else "لا يـوجـد"
    user_bio = FullUser.about or "لا يـوجـد"
    zilzal = (await l313l.get_entity(user_id)).premium

    # تحديد الرتبة
    if user_id in zelzal:
        rotbat = "مطـور السـورس 𓄂"
    elif user_id in zel_dev:
        rotbat = "مـطـور 𐏕"
    elif user_id == (await l313l.get_me()).id:
        rotbat = "مـالك الحساب 𓀫"
    else:
        rotbat = "العضـو 𓅫"

    # حساب التفاعل
    zmsg = await l313l.get_messages(event.chat_id, 0, from_user=user_id)
    zzz = zmsg.total
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

    # إنشاء النص
    ZED_TEXT = gvarstatus("CUSTOM_ALIVE_TEXT") or "•⎚• مـعلومـات المسـتخـدم مـن بـوت زدثــون"
    ZEDM = gvarstatus("CUSTOM_ALIVE_EMOJI") or "✦ "
    ZEDF = gvarstatus("CUSTOM_ALIVE_FONT") or "⋆─┄─┄─┄─ ᶻᵗʰᵒᶰ ─┄─┄─┄─⋆"

    if gvarstatus("ZID_TEMPLATE") is None:
        caption = f"<b>{ZED_TEXT}</b>\n"
        caption += f"ٴ<b>{ZEDF}</b>\n"
        caption += f"<b>{ZEDM}الاســم    ⤎ </b> <a href='tg://user?id={user_id}'>{full_name}</a>\n"
        caption += f"<b>{ZEDM}اليـوزر    ⤎  {username}</b>\n"
        caption += f"<b>{ZEDM}الايـدي    ⤎ </b> <code>{user_id}</code>\n"
        caption += f"<b>{ZEDM}الرتبــه    ⤎ {rotbat} </b>\n"
        
        if zilzal or user_id in zelzal:
            caption += f"<b>{ZEDM}الحساب  ⤎  بـريميـوم 🌟</b>\n"
        
        caption += f"<b>{ZEDM}الصـور    ⤎</b>  {replied_user_profile_photos_count}\n"
        caption += f"<b>{ZEDM}الرسائل  ⤎</b>  {zzz}  💌\n"
        caption += f"<b>{ZEDM}التفاعل  ⤎</b>  {zelzzz}\n"
        
        if user_id != (await l313l.get_me()).id:
            caption += f"<b>{ZEDM}المجموعات المشتركة ⤎  {common_chat}</b>\n"
            
        caption += f"<b>{ZEDM}الإنشـاء  ⤎</b>  {zelzal_sinc}  🗓\n"
        caption += f"<b>{ZEDM}البايـو     ⤎  {user_bio}</b>\n"
        caption += f"ٴ<b>{ZEDF}</b>"
    else:
        zzz_caption = gvarstatus("ZID_TEMPLATE")
        caption = zzz_caption.format(
            znam=full_name,
            zusr=username,
            zidd=user_id,
            zrtb=rotbat,
            zpre="ℙℝ𝔼𝕄𝕀𝕌𝕄 🌟" if zilzal or user_id in zelzal else "𝕍𝕀ℝ𝕋𝕌𝔸𝕃 ✨",
            zvip="𝕍𝕀ℙ 💎",
            zpic=replied_user_profile_photos_count,
            zmsg=zzz,
            ztmg=zelzzz,
            zcom=common_chat,
            zsnc=zelzal_sinc,
            zbio=user_bio,
        )

    # تحميل الصورة
    photo_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, f"{user_id}.jpg")
    await l313l.download_profile_photo(user_id, photo_path, download_big=True)
    
    return photo_path, caption

@l313l.ar_cmd(pattern="لايك(?: |$)(.*)")
async def like_cmd(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    if (event.chat_id in ZED_BLACKLIST) and (Zel_Uid not in zed_dev):
        return await edit_or_reply(event, "**- عـذراً .. عـزيـزي 🚷\n- لا تستطيـع استخـدام هـذا الامـر 🚫\n- فـي مجموعـة استفسـارات زدثــون ؟!**")
    
    zed = await edit_or_reply(event, "⇆")
    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "idid")
    await response[0].click(event.chat_id)
    await zed.delete()

@l313l.ar_cmd(pattern="like(?: |$)(.*)")
async def like_en_cmd(event):
    await like_cmd(event)

@l313l.ar_cmd(pattern="المعجبين$")
async def on_like_list(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    likers = get_likes(l313l.uid)
    if not likers:
        return await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯\n- ماعنـدك معجبيـن حالياً ❤️‍🩹**")
    
    out_str = "𓆩 𝗦𝗼𝘂𝗿𝗰𝗲 𝗭𝗧𝗵𝗼𝗻 - **قائمـة المعجبيــن** ❤️𓆪\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
    out_str += f"**• إجمالي عـدد المعجبيـن {len(likers)}**\n\n"
    
    for count, mogab in enumerate(likers, start=1):
        out_str += f"**{count}. الاسم:** [{mogab.f_name}](tg://user?id={mogab.lik_id})\n"
        out_str += f"**• الايـدي:** `{mogab.lik_id}`\n"
        out_str += f"**• اليـوزر:** {mogab.f_user}\n\n"
    
    await edit_or_reply(event, out_str)

@l313l.ar_cmd(pattern="مسح المعجبين$")
async def on_all_liked_delete(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in zed_dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    
    if not get_likes(l313l.uid):
        return await edit_or_reply(event, "**- مسكيـن ع باب الله 🧑🏻‍🦯\n- ماعنـدك معجبيـن حالياً ❤️‍🩹**")
    
    zed = await edit_or_reply(event, "**⪼ جـارِ مسـح المعجبيـن .. انتظـر ⏳**")
    remove_all_likes(l313l.uid)
    delgvar("Like_Id")
    await zed.edit("**⪼ تم حـذف جميـع المعجبيـن .. بنجـاح ✅**")

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"likes")))
async def like_callback(event):
    user_id = event.sender_id
    try:
        user = await l313l.get_entity(user_id)
        user_name = user.first_name + (f" {user.last_name}" if user.last_name else "")
        user_username = f"@{user.username}" if user.username else "لا يوجد"
    except Exception:
        user_name = "مستخدم محذوف"
        user_username = "لا يوجد"
    
    Like_id = int(gvarstatus("Like_Id") or 0)
    
    if add_like(str(l313l.uid), str(user.id), user_name, user_username):
        Like_id += 1
        addgvar("Like_Id", Like_id)
        
        try:
            await l313l.send_message(
                BOTLOG_CHATID,
                "#الايـدي_بـ_لايــك 💝\n\n"
                f"**- المُستخـدِم:** {_format.mentionuser(user_name, user.id)}\n"
                f"**- الايدي:** `{user.id}`\n"
                f"**- اليـوزر:** {user_username}\n"
                f"**- قام بعمـل لايـك لـ الايـدي الخـاص بـك ♥️**\n"
                f"**- اصبح عـدد معجبينك:** {Like_id} 🤳\n"
            )
        except Exception as e:
            LOGS.error(f"فشل إرسال إشعار لايك: {e}")
        
        try:
            await event.edit(buttons=[[Button.inline(f"ʟɪᴋᴇ ♥️ ⤑ {Like_id}", data="likes")]])
            await event.answer("- تم إضافة إعجابك ♥️", alert=False)
        except:
            await event.answer("- تم إضافة إعجابك ♥️", alert=False)
    else:
        await event.answer("- أنت معجب بالفعل ❤️", alert=False)
