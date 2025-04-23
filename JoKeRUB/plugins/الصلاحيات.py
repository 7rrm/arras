import logging
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

# إعداد تسجيل الأخطاء
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot_errors.log'
)
logger = logging.getLogger(__name__)

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
    except Exception as e:
        logger.error(f"Error in is_admin: {str(e)}", exc_info=True)
        is_mod = False
    return is_mod

@l313l.ar_cmd(
    pattern="قفل(?: |$)(.*)",
    command=("قفل", plugin_category),
    info={
        "header": "اوامــر قفـل الحمـاية الخـاصه بـ المجمـوعـات",
        "الوصـف": "اوامـر ذكيـه لـ قفـل / فتـح حمـاية المجمـوعـات بالمسـح والطـرد والتقييـد لـ اول مـره فقـط ع سـورس زدثــون",
        "الاوامـر": {
            "الدردشه": "- لـ قفـل ارسـال الرسـائل فقـط",
            "الميديا": "- لـ قفـل ارسـال الوسـائط",
            "الدخول": "- لـ قفـل دخـول الاعضـاء",
            "الفارسيه": "- لـ قفـل الفـارسيـه",
            "الفشار": "- لـ قفـل الفشـار والسـب",
            "المعرفات": "- لـ قفـل ارسـال المعـرفات",
            "الانلاين": "- لـ قفـل انـلاين البـوتـات",
            "البوتات": "- لـ قفـل اضـافة البـوتـات",
            "الاضافه": "- لـ قفـل اضـافة الاعضـاء",
            "التوجيه": "- لـ قفـل التـوجيـه",
            "الروابط": "- لـ قفـل ارسـال الروابـط",
            "الكل": "- لـ قفـل كـل الاوامـر",
        },
        "الاسـتخـدام": "{tr}قفل + الامــر",
    },
    #groups_only=True,
    require_admin=True,
)
async def _(event):
    try:
        if not event.is_group:
            return
        if event.fwd_from:
            return
        input_str = event.pattern_match.group(1)
        peer_id = event.chat_id
        zed_id = event.chat_id
        chat_per = (await event.get_chat()).default_banned_rights
        if input_str in ("الدردشه", "الدردشة", "الصور", "الملصقات", "المتحركه", "المتحركة", "المتحركات" "الفيديو", "الصوت", "البصمات", "الكل"):
            msg = chat_per.send_messages
            media = chat_per.send_media
            sticker = chat_per.send_stickers
            gif = chat_per.send_gifs
            gamee = chat_per.send_games
            ainline = chat_per.send_inline
            embed_link = chat_per.embed_links
            gpoll = chat_per.send_polls
            adduser = chat_per.invite_users
            cpin = chat_per.pin_messages
            changeinfo = chat_per.change_info
            if input_str == "الدردشة" or input_str == "الدردشه":
                if msg:
                    return await edit_or_reply(event, "**◆╎تـم قفـل الدردشـه بنجـاح ✅ .**")
                msg = True
                what = "الدردشـه"
            elif input_str == "الصور" or input_str == "الفيديو" or input_str == "الصوت" or input_str == "البصمات":
                if media:
                    return await edit_or_reply(event, "**◆╎الوسائـط مغلقـه بالفعـل سابقـاً ☑️ .**")
                media = True
                what = "الصـور والفيديـو والصـوت"
            elif input_str == "الملصقات":
                if sticker:
                    return await edit_or_reply(event, "**◆╎الملصقـات مغلقـه بالفعـل سابقـاً ☑️ .**")
                sticker = True
                what = "الملصقـات"
            elif input_str == "المتحركه":
                if gif:
                    return await edit_or_reply(event, "**◆╎المتحركـات مغلقـه بالفعـل سابقـاً ☑️ .**")
                gif = True
                what = "المتحركـات"
            elif input_str == "الكل":
                msg = None
                media = True
                sticker = True
                gif = True
                what = "الكـل"
                update_lock(zed_id, "bots", True)
                update_lock(zed_id, "game", True)
                update_lock(zed_id, "forward", True)
                update_lock(zed_id, "egame", True)
                update_lock(zed_id, "rtl", True)
                update_lock(zed_id, "url", True)
                update_lock(zed_id, "contact", True)
                update_lock(zed_id, "location", True)
                update_lock(zed_id, "button", True)
                update_lock(zed_id, "inline", True)
                update_lock(zed_id, "video", True)
                update_lock(zed_id, "sticker", True)
                update_lock(zed_id, "voice", True)
                update_lock(zed_id, "audio", True)
            lock_rights = ChatBannedRights(
                until_date=None,
                send_messages=msg,
                send_media=media,
                send_stickers=sticker,
                send_gifs=gif,
                send_games=gamee,
                send_inline=ainline,
                send_polls=gpoll,
                embed_links=embed_link,
                invite_users=adduser,
                pin_messages=cpin,
                change_info=changeinfo,
            )
            try:
                await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights))
                return await edit_or_reply(event, f"**◆╎تـم قفـل {what} بنجـاح ✅ .**")
            except BaseException as e:
                logger.error(f"Error in locking chat: {str(e)}", exc_info=True)
                return await edit_or_reply(event, f"**◆╎عـذࢪاً  عـزيـزي ..**\n**⤶╎لا املك صـلاحيات هنـا .**")
        if input_str == "البوتات":
            update_lock(zed_id, "bots", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة الطـرد والتحذيـر .**".format(input_str))
        if input_str == "المعرفات":
            update_lock(zed_id, "button", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر .**".format(input_str))
        if input_str == "الدخول":
            update_lock(zed_id, "location", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة الطـرد والتحذيـر .**".format(input_str))
        if input_str == "الفارسيه" or input_str == "دخول الايران":
            update_lock(zed_id, "egame", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر .**".format(input_str))
        if input_str == "الاضافه":
            update_lock(zed_id, "contact", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة الطـرد والتحذيـر .**".format(input_str))
        if input_str == "التوجيه":
            update_lock(zed_id, "forward", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر .**".format(input_str))
        if input_str == "الميديا":
            update_lock(zed_id, "game", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح بالتقييـد والتحذيـر .**".format(input_str))
        if input_str == "تعديل الميديا":
            update_lock(zed_id, "document", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح بالتقييـد والتحذيـر •**".format(input_str))
        if input_str == "الانلاين":
            update_lock(zed_id, "inline", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
        if input_str == "الفشار":
            update_lock(zed_id, "rtl", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
        if input_str == "الروابط":
            update_lock(zed_id, "url", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة المسـح والتحذيـر •**".format(input_str))
        if input_str == "التفليش" or input_str == "الخيانه" or input_str == "الخيانة":
            update_lock(zed_id, "audio", True)
            return await edit_or_reply(event, "**◆╎تـم قفـل {} بنجـاح ✅ •**\n\n**⎉╎خاصيـة تنزيـل المشـرف الخـائن •**".format(input_str))
        if input_str == "المميز":
            return
        else:
            if input_str:
                return await edit_or_reply(event, f"**◆╎عذراً لايـوجـد امـر بـ اسـم :** `{input_str}`\n**⤶╎لعـرض اوامـر القفـل والفتـح ارسـل** `.م7`")

            return await edit_or_reply(event, "**◆╎عـذࢪاً عـزيـزي .. لايمكنك قفـل اي شي هنـا ... **")
    except Exception as e:
        logger.error(f"Error in قفل command: {str(e)}", exc_info=True)
        await edit_or_reply(event, "**◆╎حدث خطأ أثناء تنفيذ الأمر، يرجى المحاولة لاحقاً**")

# ... (يجب إضافة نفس التعديلات لبقية الدوال)

@l313l.on(events.NewMessage(incoming=True))
async def check_incoming_messages(event):
    try:
        if not event.is_group:
            return
        try:
            chat = await event.get_chat()
            admin = chat.admin_rights
            creator = chat.creator
            if not admin and not creator:
                return
        except Exception as e:
            logger.error(f"Error in getting chat info: {str(e)}", exc_info=True)
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
        except Exception as e:
            logger.error(f"Error in getting sender info: {str(e)}", exc_info=True)
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
                    logger.error(f"Error in anti-thift: {str(e)}", exc_info=True)
                    return
                if BOTLOG:
                    try:
                        await event.client.send_message(BOTLOG_CHATID,
                            "**◆╎سيـدي المـالك**\n\n**◆╎قـام هـذا** [الشخـص](tg://user?id={})  \n**◆╎بانتحـال اسمـك**\n**◆╎تم تحذيـر الشخـص وكتمـه .. بنجـاح ✓ .**".format(
                                zelzal
                            )
                        )
                    except Exception as e:
                        logger.error(f"Error sending to BOTLOG: {str(e)}", exc_info=True)
        if is_locked(zed_id, "rtl") and ("خرا" in hhh or "كسها" in hhh or "كسمك" in hhh or "كسختك" in hhh or "عيري" in hhh or "كسخالتك" in hhh or "خرا بالله" in hhh or "عير بالله" in hhh or "كسخواتكم" in hhh or "اختك" in hhh or "بڪسسخخت" in hhh or "كحاب" in hhh or "مناويج" in hhh or "كحبه" in hhh or " كواد " in hhh or "كواده" in hhh or "تبياته" in hhh or "تبياتة" in hhh or "فرخ" in hhh or "كحبة" in hhh or "فروخ" in hhh or "طيز" in hhh or "آإيري" in hhh or "اختج" in hhh or "سالب" in hhh or "موجب" in hhh or "فحل" in hhh or "كسي" in hhh or "كسك" in hhh or "كسج" in hhh or "مكوم" in hhh or "نيج" in hhh or "نتنايج" in hhh or "مقاطع" in hhh or "ديوث" in hhh or "دياث" in hhh or "اديث" in hhh or "محارم" in hhh or "سكس" in hhh or "مصي" in hhh or "اعرب" in hhh or "أعرب" in hhh or "قحب" in hhh or "قحاب" in hhh or "عراب" in hhh or "مكود" in hhh or "عربك" in hhh or "مخنث" in hhh or "مخنوث" in hhh or "فتال" in hhh or "زاني" in hhh or "زنا" in hhh or "لقيط" in hhh or "بنات شوارع" in hhh or "بنت شوارع" in hhh or "نيك" in hhh or "منيوك" in hhh or "منيوج" in hhh or "نايك" in hhh or "قواد" in hhh or "زبي" in hhh or "ايري" in hhh or "ممحو" in hhh or "بنت شارع" in hhh or " است " in hhh or "اسات" in hhh or "زوب" in hhh or "عيير" in hhh or "املس" in hhh or "مربرب" in hhh or " خول " in hhh or "عرص" in hhh or "قواد" in hhh or "اهلاتك" in hhh or "جلخ" in hhh or "شرمو" in hhh or "فرك" in hhh or "رهط" in hhh):
            if zelzal == malath or await is_admin(event, zelzal) or zelzal in zed_dev:
                return
            else:
                try:
                    await event.delete()
                    await event.reply(f"[ᯓ 𝗮𝗥𝗥𝗮𝗦 - حمـاية المجموعـة ](t.me/lx5x5)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**عـذࢪاً** [{user.first_name}](tg://user?id={user.id})  \n⌔╎**يُمنـع الفشـار والسب هنـا ⚠️•**", link_preview=False)
                except Exception as e:
                    logger.error(f"Error in handling rtl lock: {str(e)}", exc_info=True)
                    await event.reply(
                        "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(str(e))
                    )
                    update_lock(zed_id, "rtl", False)
        # ... (يجب إضافة نفس التعديلات لبقية الشروط)
    except Exception as e:
        logger.error(f"Error in check_incoming_messages: {str(e)}", exc_info=True)

# ... (يجب إضافة نفس التعديلات لبقية الدوال)

@l313l.on(events.ChatAction())
async def _(event):
    try:
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
                            logger.error(f"Error in banning bot: {str(e)}", exc_info=True)
                            await event.reply(
                                "**◆╎عـذࢪاً  عـزيـزي .. لا املك صـلاحيات المشـرف هنـا .** \n`{}`".format(
                                    str(e)
                                )
                            )
                            update_lock(event.chat_id, "bots", False)
                            break
            if BOTLOG and is_ban_able:
                try:
                    await event.client.send_message(BOTLOG_CHATID,
                        "**◆╎سيـدي المـالك**\n\n**⎉╎قـام هـذا** [الشخـص](tg://user?id={})  \n**◆╎باضـافة بـوت للمجمـوعـة**\n**◆╎تم تحذيـر الشخـص وطـرد البـوت .. بنجـاح ✓ .**".format(
                            zelzal_by
                        )
                    )
                except Exception as e:
                    logger.error(f"Error sending to BOTLOG: {str(e)}", exc_info=True)
    except Exception as e:
        logger.error(f"Error in ChatAction handler: {str(e)}", exc_info=True)
