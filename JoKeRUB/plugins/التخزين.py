import asyncio
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon import events
from JoKeRUB import l313l
from JoKeRUB.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete
from ..helpers.tools import media_type
from ..helpers.utils import _format
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "البوت"

class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0
        self.STORED_MESSAGES = {}  # لتخزين الرسائل المحولة
        self.ORIGINAL_MESSAGES = {}  # لتخزين محتوى الرسائل الأصلية

LOG_CHATS_ = LOG_CHATS()

@l313l.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event):
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        try:
                            await LOG_CHATS_.NEWPM.edit(
                                LOG_CHATS_.NEWPM.text.replace(
                                    " **📮┊رسـاله جـديده**", f"{LOG_CHATS_.COUNT} **رسـائل**"
                                )
                            )
                        except Exception as er:
                            LOGS.error(f"Error: {er}")
                    else:
                        await event.client.send_message(
                            Config.PM_LOGGER_GROUP_ID,
                            LOG_CHATS_.NEWPM.text.replace(
                                " **📮┊رسـاله جـديده**", f"{LOG_CHATS_.COUNT} **رسـائل**"
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"**🛂┊المسـتخـدم :** {_format.mentionuser(sender.first_name , sender.id)} **- قام بـ إرسـال رسـالة جـديـده** \n**🎟┊الايـدي :** `{chat.id}`",
                )
            try:
                if event.message:
                    forwarded_msg = await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                    # تخزين الرسالة المحولة والرسالة الأصلية
                    LOG_CHATS_.STORED_MESSAGES[event.message.id] = forwarded_msg.id
                    LOG_CHATS_.ORIGINAL_MESSAGES[event.message.id] = event.message.text
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.error(f"Error: {e}")

@l313l.ar_cmd(incoming=True, func=lambda e: e.mentioned, edited=False, forword=None)
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    from .afk import AFK_

    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (Config.PM_LOGGER_GROUP_ID == -100)
        or ("on" in AFK_.USERAFK_ON)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = None
    try:
        messaget = await media_type(event)
    except BaseException:
        messaget = None
    resalt = f"#التــاكــات\n\n<b>⌔┊الكــروب : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += (
            f"\n\n<b>⌔┊المـرسـل : </b> {_format.htmlmentionuser(full.first_name , full.id)}"
        )
    if messaget is not None:
        resalt += f"\n\n<b>⌔┊رسـالـة ميـديـا : </b><code>{messaget}</code>"
    else:
        resalt += f"\n\n<b>⌔┊الرســالـه : </b>{event.message.message}"
    resalt += f"\n\n<b>⌔┊رابـط الرسـاله : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>"
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )

@l313l.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=True, forword=None)
async def handle_edited_messages(event):
    if Config.PM_LOGGER_GROUP_ID == -100 and not BOTLOG:
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            # التحقق مما إذا كانت الرسالة قد تم تعديلها فعلاً
            original_text = LOG_CHATS_.ORIGINAL_MESSAGES.get(event.message.id, "")
            if original_text and original_text != event.message.text:
                # إرسال إلى مجموعة التخزين أولاً (إذا كانت مفعلة)
                if Config.PM_LOGGER_GROUP_ID != -100:
                    if event.message.id in LOG_CHATS_.STORED_MESSAGES:
                        storage_msg_id = LOG_CHATS_.STORED_MESSAGES[event.message.id]
                        try:
                            await event.client.send_message(
                                Config.PM_LOGGER_GROUP_ID,
                                f"#الـتـعديـل\n\n"
                                f"**🛂┊المسـتخـدم :** {_format.mentionuser(sender.first_name , sender.id)}\n"
                                f"**🎟┊الايـدي :** `{sender.id}`\n"
                                f"**📝┊اليـوزر :** @{sender.username if sender.username else 'لا يوجد'}\n\n"
                                f"**✏┊قام بـتعديل رسالة مـن :**\n"
                                f"`{original_text}`\n\n"
                                f"**إلـى:**\n"
                                f"`{event.message.text}`",
                                reply_to=storage_msg_id
                            )
                            await event.client.forward_messages(
                                Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                            )
                        except Exception as e:
                            LOGS.error(f"Error sending to storage group: {e}")

                # ثم إرسال إلى مجموعة السجل (إذا كانت مفعلة)
                if BOTLOG and BOTLOG_CHATID:
                    try:
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            f"#الـتـعديـل\n\n"
                            f"**🛂┊المسـتخـدم :** {_format.mentionuser(sender.first_name , sender.id)}\n"
                            f"**🎟┊الايـدي :** `{sender.id}`\n"
                            f"**📝┊اليـوزر :** @{sender.username if sender.username else 'لا يوجد'}\n\n"
                            f"**✏┊قام بـتعديل رسالة مـن :**\n"
                            f"`{original_text}`\n\n"
                            f"**إلـى:**\n"
                            f"`{event.message.text}`"
                        )
                    except Exception as e:
                        LOGS.error(f"Error sending to log group: {e}")

@l313l.ar_cmd(
    pattern="خزن(?:\s|$)([\s\S]*)",
    command=("خزن", plugin_category),
    info={
        "header": "لحفظ الرسالة في مجموعة التخزين",
        "الاسـتخـدام": [
            "{tr}خزن",
        ],
    },
)
async def log(log_text):
    "لحفظ الرسالة في مجموعة التخزين"
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            forwarded_msg = await reply_msg.forward_to(BOTLOG_CHATID)
            # تخزين معرف الرسالة المحولة
            LOG_CHATS_.STORED_MESSAGES[reply_msg.id] = forwarded_msg.id
        elif log_text.pattern_match.group(1):
            user = f"#التخــزين / ايـدي الدردشــه : {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await log_text.client.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("**⌔┊بالــرد على اي رسـاله لحفظهـا في كـروب التخــزين**")
            return
        await log_text.edit("**⌔┊تـم الحفـظ في كـروب التخـزين .. بنجـاح ✓**")
    else:
        await log_text.edit("**⌔┊عـذراً .. هـذا الامـر يتطلـب تفعيـل فـار التخـزين اولاً**")
    await asyncio.sleep(2)
    await log_text.delete()


from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from . import _format

async def create_monitoring_group(client):
    try:
        result = await client(CreateChannelRequest(
            title="كروب المراقبة",
            about="مجموعة لمراقبة الرسائل التي يرسلها المستخدمون في المجموعات المشتركة.",
            megagroup=True
        ))
        monitoring_group_id = str(result.chats[0].id)
        addgvar("monitoring_group_id", monitoring_group_id)
        invite_link = await client(ExportChatInviteRequest(int(monitoring_group_id)))
        return monitoring_group_id, invite_link.link
    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء المجموعة: {str(e)}")
        return None, None

@l313l.ar_cmd(pattern="مراقبة (?:(.*))")
async def monitor_user(event):
    target = event.pattern_match.group(1)
    if not target:
        return await event.edit("**⌔┊يجب عليك تحديد المستخدم أو الـ ID للمراقبة**")

    monitored_users = gvarstatus("monitored_users") or ""
    monitored_list = monitored_users.split(",") if monitored_users else []

    monitoring_group_id = gvarstatus("monitoring_group_id")
    if not monitoring_group_id:
        monitoring_group_id, invite_link = await create_monitoring_group(event.client)
        if not monitoring_group_id:
            return await event.edit("**⌔┊حدث خطأ أثناء إنشاء مجموعة المراقبة**")
        await event.edit(f"**⌔┊تم إنشاء مجموعة المراقبة بنجاح: [اضغط هنا للدخول]({invite_link})**")

    if target not in monitored_list:
        monitored_list.append(target)
        addgvar("monitored_users", ",".join(monitored_list))
        await event.edit(f"**⌔┊تم بدء مراقبة المستخدم {target} في جميع المجموعات المشتركة.**")
    else:
        await event.edit(f"**⌔┊المستخدم {target} تحت المراقبة بالفعل.**")

@l313l.ar_cmd(pattern="الغاء مراقبة (?:(.*))")
async def unmonitor_user(event):
    target = event.pattern_match.group(1)
    if not target:
        return await event.edit("**⌔┊يجب عليك تحديد المستخدم أو الـ ID لإيقاف المراقبة**")

    monitored_users = gvarstatus("monitored_users") or ""
    monitored_list = monitored_users.split(",") if monitored_users else []

    if target in monitored_list:
        monitored_list.remove(target)
        addgvar("monitored_users", ",".join(monitored_list))
        await event.edit(f"**⌔┊تم إيقاف مراقبة المستخدم {target}.**")
    else:
        await event.edit(f"**⌔┊المستخدم {target} غير موجود في قائمة المراقبة.**")

@l313l.ar_cmd(incoming=True, func=lambda e: e.is_group, edited=False, forword=None)
async def monitor_messages(event):
    try:
        monitored_users = gvarstatus("monitored_users") or ""
        monitored_list = monitored_users.split(",") if monitored_users else []
        monitoring_group_id = gvarstatus("monitoring_group_id")
        
        if not monitored_list or not monitoring_group_id:
            return

        sender = await event.get_sender()
        if str(sender.id) in monitored_list or (sender.username and sender.username in monitored_list):
            group_title = event.chat.title if event.chat.title else "مجموعة غير معروفة"
            message_link = f"https://t.me/c/{event.chat.id}/{event.message.id}"
            message_text = (
                "#المـراقبـه\n\n"
                f"↜︙الكــروب : {group_title}\n\n"
                f"↜︙المـرسـل : {_format.mentionuser(sender.first_name, sender.id)}\n\n"
                f"↜︙الرســالـه : {event.message.message}\n\n"
                f"↜︙رابـط الرسـاله : [اضغط هنا]({message_link})\n"
            )

            await event.client.send_message(int(monitoring_group_id), message_text, parse_mode="markdown")
    except Exception as e:
        print(f"حدث خطأ أثناء مراقبة الرسائل: {str(e)}")


@l313l.ar_cmd(
    pattern="تفعيل التخزين$",
    command=("تفعيل التخزين", plugin_category),
    info={
        "header": "To turn on logging of messages from that chat.",
        "الاسـتخـدام": [
            "{tr}log",
        ],
    },
)
async def set_no_log_p_m(event):
    "To turn on logging of messages from that chat."
    if Config.PM_LOGGER_GROUP_ID != -100:
        chat = await event.get_chat()
        if no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.disapprove(chat.id)
            await edit_delete(
                event, "**⌔┊تـم تفعيـل التخـزين لهـذه الدردشـه .. بنجـاح ✓**", 5
            )

@l313l.ar_cmd(
    pattern="تعطيل التخزين$",
    command=("تعطيل التخزين", plugin_category),
    info={
        "header": "To turn off logging of messages from that chat.",
        "الاسـتخـدام": [
            "{tr}nolog",
        ],
    },
)
async def set_no_log_p_m(event):
    "To turn off logging of messages from that chat."
    if Config.PM_LOGGER_GROUP_ID != -100:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.approve(chat.id)
            await edit_delete(
                event, "**⌔┊تـم تعطيـل التخـزين لهـذه الدردشـه .. بنجـاح ✓**", 5
            )

@l313l.ar_cmd(
    pattern="تخزين الخاص (تفعيل|تعطيل)$",
    command=("تخزين الخاص", plugin_category),
    info={
        "header": "To turn on or turn off logging of Private messages in pmlogger group.",
        "الاسـتخـدام": [
            "{tr}pmlog on",
            "{tr}pmlog off",
        ],
    },
)
async def set_pmlog(event):
    "To turn on or turn off logging of Private messages"
    if Config.PM_LOGGER_GROUP_ID == -100:
        return await edit_delete(
            event,
            "__For functioning of this you need to set PM_LOGGER_GROUP_ID in config vars__",
            10,
        )
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        h_type = False
    elif input_str == "تفعيل":
        h_type = True
    PMLOG = not gvarstatus("PMLOG") or gvarstatus("PMLOG") != "false"
    if PMLOG:
        if h_type:
            await event.edit("**- تخزين الخاص بالفعـل ممكـن ✓**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**- تـم تعطيـل تخـزين رسـائل الخـاص .. بنجـاح✓**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("**- تـم تفعيـل تخـزين رسـائل الخـاص .. بنجـاح✓**")
    else:
        await event.edit("**- تخزين الخاص بالفعـل معطـل ✓**")

@l313l.ar_cmd(
    pattern="تخزين الكروبات (تفعيل|تعطيل)$",
    command=("تخزين الكروبات", plugin_category),
    info={
        "header": "To turn on or turn off group tags logging in pmlogger group.",
        "الاسـتخـدام": [
            "{tr}grplog on",
            "{tr}grplog off",
        ],
    },
)
async def set_grplog(event):
    "To turn on or turn off group tags logging"
    if Config.PM_LOGGER_GROUP_ID == -100:
        return await edit_delete(
            event,
            "__For functioning of this you need to set PM_LOGGER_GROUP_ID in config vars__",
            10,
        )
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        h_type = False
    elif input_str == "تفعيل":
        h_type = True
    GRPLOG = not gvarstatus("GRPLOG") or gvarstatus("GRPLOG") != "false"
    if GRPLOG:
        if h_type:
            await event.edit("**- تخزين الكـروبات بالفعـل ممكـن ✓**")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("**- تـم تعطيـل تخـزين تاكـات الكـروبات .. بنجـاح✓**")
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("**- تـم تفعيـل تخـزين تاكـات الكـروبات .. بنجـاح✓**")
    else:
        await event.edit("**- تخزين الكـروبات بالفعـل معطـل ✓**")
