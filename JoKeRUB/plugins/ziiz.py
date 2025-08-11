import json
import os
from telethon import Button
from . import l313l
from ..sql_helper.globals import gvarstatus, delgvar, addgvar
from ..helpers import get_user_from_event
from ..Config import Config

async def zzz_info(zthon_user, event):
    FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
    first_name = zthon_user.first_name
    full_name = FullUser.private_forward_name
    user_id = zthon_user.id
    username = zthon_user.username
    first_name = first_name.replace("\u2060", "") if first_name else None
    full_name = full_name or first_name
    username = "@{}".format(username) if username else None
    return user_id, full_name, username

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def repozedub(event):
    if gvarstatus("ZThon_Vip") is None and l313l.uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @Lx5x5**")
    
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎يجب الرد على الشخص أو كتابة معرفه**")
    
    try:
        zthon_user = await get_user_from_event(event)
        user_id, full_name, username = await zzz_info(zthon_user, event)
    except Exception as e:
        return await edit_or_reply(event, f"**⎉╎حدث خطأ: {str(e)}**")
    
    # حذف المتغيرات القديمة
    delgvar("hmsa_id")
    delgvar("hmsa_name")
    delgvar("hmsa_user")
    
    # إضافة المتغيرات الجديدة
    addgvar("hmsa_id", str(user_id))
    addgvar("hmsa_name", full_name)
    addgvar("hmsa_user", username or f"[{full_name}](tg://user?id={user_id})")
    
    # إنشاء زر الهمسة
    button = [Button.switch_inline("اضـغـط هنـا", query=f"secret {user_id}", same_peer=True)]
    
    try:
        # إرسال الرسالة مع الزر
        await event.client.send_message(
            event.chat_id,
            f"**ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎اضغـط الزر بالاسفـل لارسال همسة لـ** {username or full_name}",
            buttons=button
        )
        await event.delete()
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ أثناء إرسال الهمسة: {str(e)}**")
