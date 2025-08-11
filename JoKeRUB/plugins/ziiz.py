import json
import os
from telethon import Button
from telethon.tl.functions.users import GetFullUserRequest
from . import l313l
from ..sql_helper.globals import gvarstatus, delgvar, addgvar
from ..helpers import get_user_from_event
from ..Config import Config
from ..core.managers import edit_or_reply

async def zzz_info(zthon_user, event):
    try:
        FullUser = (await event.client(GetFullUserRequest(zthon_user.id))).full_user
        first_name = zthon_user.first_name or "مستخدم"
        full_name = FullUser.private_forward_name or first_name
        user_id = zthon_user.id
        username = f"@{zthon_user.username}" if zthon_user.username else None
        return user_id, full_name, username
    except Exception as e:
        return None, None, None

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def repozedub(event):
    # الحصول على المستخدم المستهدف
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎يجب الرد على الشخص أو كتابة معرفه**")
    
    try:
        zthon_user = await get_user_from_event(event)
        user_id, full_name, username = await zzz_info(zthon_user, event)
        
        if not user_id:
            return await edit_or_reply(event, "**⎉╎لم يتم العثور على المستخدم**")
        
        # تحديث متغيرات الهمسة
        delgvar("hmsa_id")
        delgvar("hmsa_name")
        delgvar("hmsa_user")
        
        addgvar("hmsa_id", str(user_id))
        addgvar("hmsa_name", full_name)
        addgvar("hmsa_user", username or f"[{full_name}](tg://user?id={user_id})")
        
        # إنشاء زر الهمسة
        button = [[Button.switch_inline("اضـغـط هنـا", query=f"secret {user_id}", same_peer=True)]]
        
        # إرسال الرسالة
        await event.client.send_message(
            event.chat_id,
            f"**ᯓ 𝗮𝗥𝗥𝗮𝗦 𝗪𝗵𝗶𝘀𝗽𝗲𝗿 - همسـة سـريـه**\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎اضغـط الزر بالاسفـل لارسال همسة لـ** {username or full_name}",
            buttons=button
        )
        await event.delete()
        
    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ: {str(e)}**")
