import asyncio

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..sql_helper import antiflood_sql as sql
from ..utils import is_admin
from . import edit_or_reply, l313l

CHAT_FLOOD = sql.__load_flood_settings()

ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@l313l.ar_cmd(incoming=True, groups_only=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    zthonadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not zthonadmin:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 - **مانع التكرار**\n━━━━━━━━━━━━━━━━\n**✧╎ قام↫** [المستخدم](tg://user?id={event.message.sender_id})\n**✧╎بتكرار رسائله في المجموعة**\x1f`{e}`",
            reply_to=event.message.id,
        )

        await asyncio.sleep(4)
        await no_admin_privilege_message.edit(
            "**✧╎هذا هو الشخص الذي قام بالتكرار \n✧╎توقف لكي لا تًطرد 📵**"
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 - **مانع التكرار**\n━━━━━━━━━━━━━━━━━\n**✧╎قام ↫**[المستخدم ](tg://user?id={event.message.sender_id})\n**✧╎بتجاوز عدد الـتكرار لـذلك تـم تقيـيده**",
            reply_to=event.message.id,
        )

@l313l.ar_cmd(
    pattern="ضع تكرار(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def _(event):
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "جاري معالجة الطلب ..")
    await asyncio.sleep(1)
    try:
        if int(input_str) >= 99999:
            try:
                sql.set_flood(event.chat_id, "0")
            except:
                pass
            global CHAT_FLOOD
            CHAT_FLOOD = sql.__load_flood_settings()
            await event.edit("تم إيقاف وحذف مكافح التكرار من هذه المجموعة ✓")
        else:
            sql.set_flood(event.chat_id, input_str)
            sql.__load_flood_settings()
            await event.edit(f"تم تحديث التكرار الى {input_str} في الدردشة الحالية")
    except ValueError:
        await event.edit("الرجاء إدخال رقم صحيح")
    except Exception as e:
        await event.edit(f"حدث خطأ: {str(e)}")
