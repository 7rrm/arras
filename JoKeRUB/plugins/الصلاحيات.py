import contextlib
import base64
import asyncio
import io
import re
import time
from asyncio import sleep
from datetime import datetime
from math import sqrt

from telethon.events import InlineQuery, callbackquery
from telethon import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest, EditBannedRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest

from telethon import events, functions, types
from telethon.tl.types import Channel, Chat, User, ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantsKicked,
    ChatBannedRights,
    MessageActionChannelMigrateFrom,
    MessageEntityCustomEmoji,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
    InputPeerChat,
)
from telethon.errors import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
    FloodWaitError,
    MessageNotModifiedError,
)
from . import l313l
from ..utils import is_admin
from ..sql_helper.locks_sql import get_locks, is_locked, update_lock
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import reply_id, _format
from ..sql_helper.fsub_sql import *
from ..helpers import readable_time
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

ANTI_DDDD_ZEDTHON_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_media=True, send_stickers=True, send_gifs=True
)
from ..Config import Config
zed_dev = (5427469031, 5280339206)
kicked_count = 0
The_Premium = False
activated = []
admins_out = {}
plugin_category = "admin"

async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        if sed.is_admin:
            is_mod = True
        else:
            is_mod = False
    except:
        is_mod = False
    return is_mod

from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

@l313l.ar_cmd(
    pattern=r"(قفل|فتح)(?: |$)(.*)",
    command=("حماية", plugin_category),
    info={
        "header": "أوامر الحماية في المجموعات (قفل/فتح للأعضاء أو المشرفين)",
        "الوصـف": "يمكنك استخدام أوامر قفل/فتح المجموعات بأوضاع مخصصة باستخدام كلمة 'عام' لتطبيق الحظر على المشرفين أيضًا.",
        "الاوامـر": {
            "قفل الدردشه": "- قفل إمكانية إرسال الرسائل في المجموعة",
            "فتح الدردشه": "- فتح إمكانية إرسال الرسائل في المجموعة",
            "قفل الميديا": "- قفل الوسائط (الصور، الفيديوهات، المستندات)",
            "فتح الميديا": "- فتح الوسائط",
            "قفل الروابط": "- قفل إرسال الروابط",
            "فتح الروابط": "- فتح إرسال الروابط",
            "قفل الملصقات": "- قفل إرسال الملصقات",
            "فتح الملصقات": "- فتح إرسال الملصقات",
            "قفل التوجيه": "- قفل التوجيه من مجموعات أو قنوات أخرى",
            "فتح التوجيه": "- فتح إمكانية التوجيه",
            "قفل الانلاين": "- قفل استخدام البوتات الانلاين",
            "فتح الانلاين": "- فتح استخدام البوتات الانلاين",
            "قفل الكل": "- لقفل كل الأوامر دفعة واحدة",
            "فتح الكل": "- فتح كل الأوامر دفعة واحدة",
        },
        "الاسـتخـدام": "{tr}قفل + الأمر + [عام] / {tr}فتح + الأمر",
    },
    require_admin=True,
)
async def lock_unlock_cmd(event):
    if not event.is_group:
        return await edit_or_reply(event, "**◆╎هذا الأمر فقط للمجموعات.**")  # التحقق أن الأمر في مجموعة
    if event.fwd_from:
        return
   
    # تحديد الأمر
    input_full = event.pattern_match.group(2).strip()
    if not input_full:
        return await edit_or_reply(event, "**◆╎يرجى تحديد نوع القفل أو الفتح.**")

    # استخراج الأمر والكلمة المفتاحية
    args = input_full.split()
    action = event.pattern_match.group(1)  # قفل أو فتح
    lock_type = args[0]
    global_action = False
    if len(args) > 1 and args[1].lower() == "عام":
        global_action = True  # تحديد ما إذا كان على الجميع (المشرفين + الأعضاء)

    peer_id = event.chat_id
    lock_rights = None
    unlock_rights = None

    try:
        # ضبط إعدادات الصلاحيات الافتراضية
        chat_per = (await event.get_chat()).default_banned_rights
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        ainline = chat_per.send_inline
        embed_link = chat_per.embed_links
        adduser = chat_per.invite_users

        # بناء إعدادات الحظر/الإلغاء حسب نوع القفل/الفتح
        if lock_type in ("الدردشه", "الدردشة"):
            lock_rights = ChatBannedRights(until_date=None, send_messages=True)
            unlock_rights = ChatBannedRights(until_date=None, send_messages=False)
            what = "الدردشة"
        elif lock_type in ("الميديا", "الصور", "الفيديو", "الصوت"):
            lock_rights = ChatBannedRights(until_date=None, send_media=True)
            unlock_rights = ChatBannedRights(until_date=None, send_media=False)
            what = "الوسائط"
        elif lock_type == "الروابط":
            lock_rights = ChatBannedRights(until_date=None, embed_links=True)
            unlock_rights = ChatBannedRights(until_date=None, embed_links=False)
            what = "الروابط"
        elif lock_type == "الملصقات":
            lock_rights = ChatBannedRights(until_date=None, send_stickers=True)
            unlock_rights = ChatBannedRights(until_date=None, send_stickers=False)
            what = "الملصقات"
        elif lock_type == "التوجيه":
            lock_rights = ChatBannedRights(until_date=None, forward_messages=True)
            unlock_rights = ChatBannedRights(until_date=None, forward_messages=False)
            what = "التوجيه"
        elif lock_type == "الانلاين":
            lock_rights = ChatBannedRights(until_date=None, send_inline=True)
            unlock_rights = ChatBannedRights(until_date=None, send_inline=False)
            what = "الانلاين"
        elif lock_type == "الكل":
            lock_rights = ChatBannedRights(
                until_date=None,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_inline=True,
                embed_links=True,
            )
            unlock_rights = ChatBannedRights(
                until_date=None,
                send_messages=False,
                send_media=False,
                send_stickers=False,
                send_gifs=False,
                send_inline=False,
                embed_links=False,
            )
            what = "كل الأوامر"

        # تنفيذ القفل أو الفتح
        if action == "قفل":
            await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights))
            if global_action:
                # لمنع رسائل المشرفين أيضًا إذا كان "عام"
                async for message in event.client.iter_messages(peer_id, limit=100):
                    if await is_admin(event, message.sender_id):  # تحقق من كونه مشرفًا
                        await message.delete()
            await edit_or_reply(event, f"**◆╎تم قفل {what}{' لكل الأعضاء والمشرفين' if global_action else ''} بنجاح ✅ .**")

        elif action == "فتح":
            await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=unlock_rights))
            await edit_or_reply(event, f"**◆╎تم فتح {what} بنجاح ✅ .**")

    except Exception as e:
        await edit_or_reply(event, f"**◆╎حدث خطأ أثناء تنفيذ الأمر:**\n`{e}`")
	    


@l313l.ar_cmd(pattern="(المميز تفعيل|قفل المميز)")
async def lock_premium(event):
    global The_Premium
    The_Premium = True
    activated.append(event.chat_id)
    return await edit_or_reply(event, "**⎉╎تم قفـل الايمـوجي المميـز .. بنجاح ✅ .**")

@l313l.ar_cmd(pattern="(المميز تعطيل|فتح المميز)")
async def unlock_premium(event):
    global The_Premium
    The_Premium = False
    activated.remove(event.chat_id)
    return await edit_or_reply(event, "**◆╎تم فتـح الايمـوجي المميـز .. بنجاح ✅ .**")

@l313l.ar_cmd(
    pattern="الاعدادات$",
    command=("الاعدادات", plugin_category),
    info={
        "header": "لـ عـرض اعـدادات حمـاية المجمـوعـة الخـاصـه ببـوت زدثــون",
        "الاسـتخـدام": "{tr}الاعدادات",
    },
    #groups_only=True,
)
async def _(event):
    if not event.is_group:
        return #await edit_or_reply(event, "**ايا مطـي! ، هـذه ليست مجموعـة لقفـل الأشيـاء**")
    if event.fwd_from:
        return
    res = "**- فيمـا يلـي إعـدادات حمـاية المجمـوعـة :**\n**- الخاصـه بـ سـورس أراس**\n\n"
    ubots = "✅" if is_locked(event.chat_id, "bots") else "❌"
    uegame = "✅" if is_locked(event.chat_id, "egame") else "❌"
    urtl = "✅" if is_locked(event.chat_id, "rtl") else "❌"
    uforward = "✅" if is_locked(event.chat_id, "forward") else "❌"
    ubutton = "✅" if is_locked(event.chat_id, "button") else "❌"
    uurl = "✅" if is_locked(event.chat_id, "url") else "❌"
    ugame = "✅" if is_locked(event.chat_id, "game") else "❌"
    udocument = "✅" if is_locked(event.chat_id, "document") else "❌"
    ulocation = "✅" if is_locked(event.chat_id, "location") else "❌"
    ucontact = "✅" if is_locked(event.chat_id, "contact") else "❌"
    ubutton = "✅" if is_locked(event.chat_id, "button") else "❌"
    uinline = "✅" if is_locked(event.chat_id, "inline") else "❌"
    uaudio = "✅" if is_locked(event.chat_id, "audio") else "❌"
    res += f"**◆╎ البوتات :** {ubots}\n"
    res += f"**◆╎ الدخول :** {ulocation}\n"
    res += f"**◆╎ دخول الايران :** {uegame}\n"
    res += f"**◆╎ الاضافه :** {ucontact}\n"
    res += f"**◆╎ التوجيه :** {uforward}\n"
    res += f"**◆╎ الميديا :** {ugame}\n"
    res += f"**◆╎ تعديـل الميديـا :** {udocument}\n"
    res += f"**◆╎ المعرفات :** {ubutton}\n"
    res += f"**◆╎ الفارسيه :** {uegame}\n"
    res += f"**◆╎ الفشار :** {urtl}\n"
    res += f"**◆╎ الروابط :** {uurl}\n"
    res += f"**◆╎ الانلاين :** {uinline}\n"
    res += f"**◆╎ التفليش :** {uaudio}\n"
    await edit_or_reply(event, res)


@l313l.ar_cmd(incoming=True, forword=None)
async def check_incoming_messages(event):
    if not event.is_group:
        return
    try:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    except Exception:
        return
    zed_dev = (5427469031, 5280339206)
    zelzal = event.sender_id
    zelzal_by = event.sender_id
    malath = l313l.uid
    hhh = event.message.text
    ttt = gvarstatus("ANTI_THIFT")
    zed_id = event.chat_id
    user = await event.get_sender()
    try:
        zelzal_by = user.id
    except AttributeError:
        zelzal_by = event.sender_id
    except Exception:
        return
    if ttt is not None:
        first = zelzal.first_name
        last = zelzal.last_name
        if ttt in first:
            if zelzal == malath or await is_admin(event, zelzal) or not await is_admin(event, malath):
                return
            try:
                await event.delete()
                await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - كاشـف الانتحـال ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**الحيـوان** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**ليه منتحـل اسمـي  😡⚠️.**", link_preview=False)
            except Exception as e:
                return
            if BOTLOG:
                await event.client.send_message(BOTLOG_CHATID,
                    "**◆╎سيـدي المـالك**\n\n**◆╎قـام هـذا** [الشخـص](tg://user?id={})  \n**◆╎بانتحـال اسمـك**\n**◆╎تم تحذيـر الشخـص وكتمـه .. بنجـاح ✓ .**".format(
                        zelzal
                    )
                )
    if is_locked(zed_id, "rtl") and ("خرا" in hhh or "كسها" in hhh or "كسمك" in hhh or "كسختك" in hhh or "عيري" in hhh or "كسخالتك" in hhh or "خرا بالله" in hhh or "عير بالله" in hhh or "كسخواتكم" in hhh or "اختك" in hhh or "بڪسسخخت" in hhh or "كحاب" in hhh or "مناويج" in hhh or "كحبه" in hhh or " كواد " in hhh or "كواده" in hhh or "تبياته" in hhh or "تبياتة" in hhh or "فرخ" in hhh or "كحبة" in hhh or "فروخ" in hhh or "طيز" in hhh or "آإيري" in hhh or "اختج" in hhh or "سالب" in hhh or "موجب" in hhh or "فحل" in hhh or "كسي" in hhh or "كسك" in hhh or "كسج" in hhh or "مكوم" in hhh or "نيج" in hhh or "نتنايج" in hhh or "مقاطع" in hhh or "ديوث" in hhh or "دياث" in hhh or "اديث" in hhh or "محارم" in hhh or "سكس" in hhh or "مصي" in hhh or "اعرب" in hhh or "أعرب" in hhh or "قحب" in hhh or "قحاب" in hhh or "عراب" in hhh or "مكود" in hhh or "عربك" in hhh or "مخنث" in hhh or "مخنوث" in hhh or "فتال" in hhh or "زاني" in hhh or "زنا" in hhh or "لقيط" in hhh or "بنات شوارع" in hhh or "بنت شوارع" in hhh or "نيك" in hhh or "منيوك" in hhh or "منيوج" in hhh or "نايك" in hhh or "قواد" in hhh or "زبي" in hhh or "ايري" in hhh or "ممحو" in hhh or "بنت شارع" in hhh or " است " in hhh or "اسات" in hhh or "زوب" in hhh or "عيير" in hhh or "املس" in hhh or "مربرب" in hhh or " خول " in hhh or "عرص" in hhh or "قواد" in hhh or "اهلاتك" in hhh or "جلخ" in hhh or "شرمو" in hhh or "فرك" in hhh or "رهط" in hhh):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع الفشـار والسب هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "rtl", False)
    if is_locked(zed_id, "game") and event.message.media:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع ارسـال الوسائـط هنـا 🚸•**\n\n⌔╎**تـم تقييدك مـن ارسـال الوسائط 📵**\n⌔╎**التـزم الهـدوء .. تستطـيع ارسـال الرسـائل فقـط..**", link_preview=False)
	            await event.client(
	                EditBannedRequest(
	                    event.chat_id, event.sender_id, ANTI_DDDD_ZEDTHON_MODE
	                )
	            )
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "game", False)
    if is_locked(zed_id, "forward") and event.fwd_from:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع التوجيـه هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "forward", False)
    if is_locked(zed_id, "button") and "@" in hhh:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع ارسـال المعـرفـات هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "button", False)
    if is_locked(zed_id, "egame") and ("فارسى" in hhh or "خوببی" in hhh or "میخوام" in hhh or "کی" in hhh or "پی" in hhh or "گ" in hhh or "خسته" in hhh or "صكص" in hhh or "راحتی" in hhh or "بیام" in hhh or "بپوشم" in hhh or "گرمه" in hhh or "چ" in hhh or "چه" in hhh or "ڬ" in hhh or "ٺ" in hhh or "چ" in hhh or "ڿ" in hhh or "ڇ" in hhh or "ڀ" in hhh or "ڎ" in hhh or "ݫ" in hhh or "ژ" in hhh or "ڟ" in hhh or "۴" in hhh or "زدن" in hhh or "دخترا" in hhh or "كسى" in hhh or "مک" in hhh or "خالى" in hhh or "ݜ" in hhh or "ڸ" in hhh or "پ" in hhh or "بند" in hhh or "عزيزم" in hhh or "برادر" in hhh or "باشى" in hhh or "ميخوام" in hhh or "خوبى" in hhh or "ميدم" in hhh or "كى اومدى" in hhh or "خوابيدين" in hhh):
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع التحـدث بالفارسيـه هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "egame", False)
    if is_locked(zed_id, "url") and "http" in hhh:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع ارسـال الروابـط هنـا ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "url", False)
    if is_locked(zed_id, "inline") and event.message.via_bot:
        if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع استخـدام الانلايـن في هذه المجموعـة ⚠️•**", link_preview=False)
	        except Exception as e:
	            await event.reply(
	                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
	            )
	            update_lock(zed_id, "inline", False)

@l313l.on(events.NewMessage(incoming=True))
async def Premiumz(event):
    if not The_Premium:
        return
    if not event.is_group:
        return
    if event.is_private or event.chat_id not in activated:
        return
    sender_id = event.sender_id
    malath = l313l.uid
    if sender_id == malath or await is_admin(event, sender_id) or not await is_admin(event, malath):
        return
    if sender_id not in zed_dev:
        if isinstance(event.message.entities, list) and any(isinstance(entity, MessageEntityCustomEmoji) for entity in event.message.entities):
            try:
                await event.delete()
                sender = await event.get_sender()
                usr_entity = await l313l.get_entity(sender.id)
                usr_profile = f"[{usr_entity.first_name}](tg://user?id={usr_entity.id})"
                await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** {usr_profile} .\n⌔╎**يُمنـع ارسـال الايمـوجي المميـز هنـا ⚠️•**", link_preview=False)
            except Exception as e:
                return


@l313l.on(events.MessageEdited)
async def check_edit_media(event):
    if not is_locked(event.chat_id, "document"):
        return
    if not event.is_group:
        return
    if event.is_group:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (5427469031, 5280339206) 
    zelzal = event.sender_id
    malath = l313l.uid
    hhh = event.message.text
    zed_id = event.chat_id
    user = await event.get_sender()
    if is_locked(zed_id, "document") and event.message.media:
        if zelzal == malath or zelzal in zed_dev:
            return
        else:
	        try:
	            await event.delete()
	            await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع تعديـل الميديـا هنـا 🚫**\n⌔╎**تم حـذف التعديـل .. بنجـاح ☑️**", link_preview=False)
	            await event.client(
	                EditBannedRequest(
	                    event.chat_id, event.sender_id, ANTI_DDDD_ZEDTHON_MODE
	                )
	            )
	        except Exception: 
	            update_lock(zed_id, "document", False)


@l313l.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "contact"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (5427469031, 5280339206)
    malath = l313l.uid
    if event.user_added:
        zedy = await event.client.get_entity(event.user_id)
        zelzal_by = event.action_message.sender_id
        zed = await event.client.get_permissions(event.chat_id, zelzal_by)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if event.user_added:
                is_ban_able = True
                if zelzal_by == malath or zed.is_admin or zelzal_by in zed_dev:
                    return
                else:
	                try:
	                    await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, user_obj, rights
	                        )
	                    )
	                    await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع اضـافة الاعضـاء لـ هـذه المجموعـة ⚠️•**\n\n⌔╎**تـم حظـࢪ العضـو المضـاف .. بنجـاح ☑️**", link_preview=False)
	                except Exception as e:
	                    await event.reply(
	                        "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(
	                            str(e)
	                        )
	                    )
	                    update_lock(event.chat_id, "contact", False)
	                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**◆╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**⎉╎باضافـة اشخـاص للمجمـوعـة**\n**◆╎تم تحذيـر الشخـص وطـرد الاعضـاء المضافيـن .. بنجـاح ✓𓆰**".format(
                    zelzal_by
                )
            )

@l313l.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "egame"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (5427469031, 925972505)
    if event.user_joined: 
        a_user = await event.get_user()
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        zedy = await event.client.get_entity(event.user_id)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        if event.user_joined and ("ژ" in first or "چ" in first or "۴" in first or "مهسا" in first or "sara" in first or "گ" in first or "نازنین" in first or "آسمان" in first or "ڄ" in first or "پ" in first or "Sanaz" in first or "𝓈𝒶𝓇𝒶" in first or "سارة" in first or "GIRL" in first or " Lady " in first or "فتاة" in first or "👅" in first or "سمانه" in first or "بهار" in first or "maryam" in first or "👙" in first or "هانیه" in first or "هستی" in first or "💋" in first or "ندا" in first or "Mina" in first or "خانم" in first or "ایناز" in first or "مبینا" in first or "امینی" in first or "سرنا" in first or "اندیشه" in first or "لنتكلم" in first or "دریا" in first or "زاده" in first or "نااز" in first or "ناز" in first or "بیتا" in first or "سكس" in first or "💄" in first or "اعرب" in first or "أعرب" in first or "قحب" in first or "قحاب" in first or "عراب" in first or "مكود" in first or "عربك" in first or "مخنث" in first or "مخنوث" in first or "فتال" in first or "زاني" in first or "زنا" in first or "لقيط" in first or "بنات شوارع" in first or "بنت شوارع" in first or "نيك" in first or "منيوك" in first or "منيوج" in first or "نايك" in first or "قواد" in first or "زبي" in first or "ايري" in first or "ممحو" in first or "بنت شارع" in first or " است " in first or "اسات" in first or "زوب" in first or "عيير" in first or "املس" in first or "مربرب" in first or " خول " in first or "عرص" in first or "قواد" in first or "اهلاتك" in first or "جلخ" in first or "شرمو" in first or "فرك" in first or "رهط" in first):
            is_ban_able = True
            if zedy.id in zed_dev:
                return
            else:
	            try:
	                await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, zedy.id, rights
	                        )
	                    )
	                await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً**  [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع انضمـام الايـࢪان هنـا 🚷•**\n\n⌔╎**تـم حظـࢪه .. بنجـاح ☑️**", link_preview=False)
	            except Exception as e:
	                await event.reply(
	                    "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(
	                        str(e)
	                    )
	                )
	                update_lock(event.chat_id, "egame", False)
	                return
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**◆╎** [عـزيـزي](tg://user?id={}) **يمنـع دخـول الايـران لهـذه المجمـوعـة .**".format(
                    zedy.id
                )
            )

@l313l.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "location"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (5427469031, 5280339206)
    if event.user_joined: 
        zedy = await event.client.get_entity(event.user_id)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        if event.user_joined:
            is_ban_able = True
            if zedy.id in zed_dev:
                return
            else:
	            try:
	                await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, zedy.id, rights
	                        )
	                    )
	                await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع الانضمـام لـ هـذه المجموعـة 🚷•**\n⌔╎**تـم حظـࢪه .. بنجـاح ☑️**", link_preview=False)
	            except Exception as e:
	                await event.reply(
	                    "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(
	                        str(e)
	                    )
	                )
	                update_lock(event.chat_id, "location", False)
	                return
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**◆╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**◆╎بالانضمـام للمجمـوعـة**\n**◆╎تم تحذيـر الشخـص وطـرده .. بنجـاح ✓𓆰**".format(
                    zedy.id
                )
            )


@l313l.on(events.ChatAction())
async def _(event):
    if not is_locked(event.chat_id, "bots"):
        return
    if not event.is_group:
        return
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    zed_dev = (5427469031, 5280339206)
    malath = l313l.uid
    if event.user_added:
        zedy = await event.client.get_entity(event.user_id)
        zelzal_by = event.action_message.sender_id
        zed = await event.client.get_permissions(event.chat_id, zelzal_by)
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                if zelzal_by == malath or zelzal_by in zed_dev:
                    return
                else:
	                try:
	                    await event.client(
	                        functions.channels.EditBannedRequest(
	                            event.chat_id, user_obj, rights
	                        )
	                    )
	                    await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{zedy.first_name}](tg://user?id={zedy.id})  \n⌔╎**يُمنـع اضـافة البـوتـات لـ هـذه المجمـوعـة 🚫•**", link_preview=False)
	                except Exception as e:
	                    await event.reply(
	                        "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(
	                            str(e)
	                        )
	                    )
	                    update_lock(event.chat_id, "bots", False)
	                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.client.send_message(BOTLOG_CHATID,
                "**◆╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**◆╎باضـافة بـوت للمجمـوعـة**\n**◆╎تم تحذيـر الشخـص وطـرد البـوت .. بنجـاح ✓ .**".format(
                    zelzal_by
                )
            )


@l313l.on(events.ChatAction())
async def handle_event(event):
    global kicked_count
    if not is_locked(event.chat_id, "bots"):
        return
    if not event.is_group:
        return
    zedy = await event.client.get_entity(event.user_id)
    if event.user_id in await l313l.get_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        if "kicked" in event.raw_text:
            zedy = await event.client.get_entity(event.user_id)
            kicked_count += 1
            if kicked_count == 3:
                await zedub(EditAdminRequest(event.chat_id, zedy.id, change_info=False,
                                              post_messages=False, edit_messages=False,
                                              delete_messages=False, ban_users=False,
                                              invite_users=False, pin_messages=False,
                                              add_admins=False))
                await zedub(EditAdminRequest(event.chat_id, zedy.id, rank=''))
                kicked_count = 0
                await edit_or_reply(event, f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - حمـاية المجموعـة ](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**مشرف خاين** [{zedy.first_name}](tg://user?id={zedy.id}) .\n⌔╎**حاول تفليش المجموعـة•**\n⌔╎**تم تنزيلـه .. بنجـاح ✅**", link_preview=False)


@l313l.ar_cmd(pattern=f"البوتات ?(.*)")
async def zelzal(zed):
    con = zed.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**⎉╎مجمـوعتك/قناتـك في أمـان ✅.. لاتوجـد بوتـات في هذه المجمـوعـة ༗**"
    if con != "طرد":
        event = await edit_or_reply(zed, "**⎉╎جـاري البحـث عن بوتات في هـذه المجمـوعـة ...🝰**")
        async for user in zed.client.iter_participants(zed.chat_id):
            if user.bot:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"🛂**┊كشـف البـوتات -** 𝗮𝗥𝗥𝗮𝗦\
                           \n\n**⎉╎تم العثور على** **{del_u}**  **بـوت**\
                           \n**⎉╎لطـرد البوتات استخدم الامـر التالي ⩥** `.البوتات طرد`"
        await event.edit(del_status)
        return
    chat = await zed.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(zed, "**◆╎عـذࢪاً .. احتـاج الى صلاحيـات المشـرف هنـا .**")
        return
    event = await edit_or_reply(zed, "**◆╎جـارِ طـرد البوتـات من هنـا ...**")
    del_u = 0
    del_a = 0
    async for user in zed.client.iter_participants(zed.chat_id):
        if user.bot:
            try:
                await zed.client.kick_participant(zed.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_or_reply(event, "**◆╎اووبس .. ليس لدي صلاحيـات حظـر هنـا**")
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**⎉╎تم طـرد  {del_u}  بـوت .. بنجـاح🚮**"
    if del_a > 0:
        del_status = f"❇️**┊طـرد البـوتات -** 𝗮𝗥𝗥𝗮𝗦\
                           \n\n**⎉╎تم طـرد  {del_u}  بـوت بنجـاح ✓** 🚮 \
                           \n**⎉╎لـم يتـم طـرد  {del_a}  بـوت لانـها اشـراف ..⅏** \
                           \n\n**⎉╎الان لـ الحفـاظ علـى كروبك/قناتك من التصفيـر ارسـل ⩥** `.قفل البوتات`"
    await edit_or_reply(event, del_status)
    if BOTLOG:
        await zed.client.send_message(
            BOTLOG_CHATID,
            f"#طـرد_البوتـات\
            \n ⎉╎{del_status}\
            \n ⎉╎الدردشه: {zed.chat.title}(`{zed.chat_id}`)",
        )
