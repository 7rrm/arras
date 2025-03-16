from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
from telethon import events
import itertools
import asyncio
from ..Config import Config
from JoKeRUB import l313l

# الحقوق محفوظة
marculs = 9

# صلاحيات المشرف
admin_rights = ChatAdminRights(
    add_admins=True,
    invite_users=True,
    change_info=True,
    ban_users=True,
    delete_messages=True,
    pin_messages=True,
    manage_call=True
)

# أمر رفع البوتات كمشرفين
@l313l.on(events.NewMessage(pattern=r"\.رفع بوتات"))
async def promote_bots(event):
    await event.edit("▾∮ جاري رفع البوتات كمشرفين...")
    
    # إنشاء أسماء البوتات (a-z مع 'bot' في النهاية)
    for combo in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=3):
        username = ''.join(combo) + 'bot'
        
        try:
            # محاولة رفع البوت كمشرف
            await event.client(EditAdminRequest(
                event.chat_id,
                username,
                admin_rights,
                "Bot Admin"
            ))
            await asyncio.sleep(2)  # تأخير 2 ثانية بين كل عملية
        except UserIdInvalidError:
            pass  # تجاهل الأسماء غير الصالحة
        except Exception:
            pass  # تجاهل جميع الأخطاء الأخرى

    await event.edit("▾∮ تم الانتهاء من رفع البوتات كمشرفين.")

# أمر رفع مشرف عادي (مثل الكود الأصلي)
@l313l.on(events.NewMessage(pattern=r"\.ارفع"))
async def promote_user(event):
    await event.edit("▾∮ جاري رفع المستخدم كمشرف...")
    reply = await event.get_reply_message()
    
    if not reply:
        await event.edit("▾∮ يجب الرد على المستخدم أولاً.")
        return
    
    user = reply.sender_id
    try:
        await event.client(EditAdminRequest(
            event.chat_id,
            user,
            admin_rights,
            "Admin"
        ))
        await event.edit(f"▾∮ تم رفع المستخدم {user} كمشرف.")
    except Exception:
        await event.edit("▾∮ فشل في رفع المستخدم.")

# أمر تنزيل مشرف (مثل الكود الأصلي)
@l313l.on(events.NewMessage(pattern=r"\.نزل"))
async def demote_user(event):
    await event.edit("▾∮ جاري تنزيل المستخدم...")
    reply = await event.get_reply_message()
    
    if not reply:
        await event.edit("▾∮ يجب الرد على المستخدم أولاً.")
        return
    
    user = reply.sender_id
    try:
        await event.client(EditAdminRequest(
            event.chat_id,
            user,
            ChatAdminRights(),  # إزالة جميع الصلاحيات
            ""
        ))
        await event.edit(f"▾∮ تم تنزيل المستخدم {user}.")
    except Exception:
        await event.edit("▾∮ فشل في تنزيل المستخدم.")

# تحديث CMD_HELP
CMD_HELP.update(
    {
        "اشراف عام": ".ارفع <بالرد ؏ شخص>\n لرفع المستخدم مشرف في المجموعة.\n\n.نزل <بالرد ؏ شخص>\n لتنزيل المستخدم من رتبة المشرف.\n\n.رفع بوتات\n لرفع جميع البوتات التي تنتهي أسماؤها بـ 'bot' كمشرفين."
    }
)
