import asyncio
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
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
                    # تخزين الرسالة المحولة للرد عليها لاحقاً عند التعديل
                    LOG_CHATS_.STORED_MESSAGES[event.message.id] = forwarded_msg.id
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.error(f"Error: {e}")

@l313l.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=True, forword=None)
async def handle_edited_messages(event):
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            # البحث عن الرسالة الأصلية في مجموعة التخزين
            original_msg_id = event.message.id
            if original_msg_id in LOG_CHATS_.STORED_MESSAGES:
                storage_msg_id = LOG_CHATS_.STORED_MESSAGES[original_msg_id]
                try:
                    # الرد على الرسالة الأصلية في مجموعة التخزين
                    reply_msg = await event.client.send_message(
                        Config.PM_LOGGER_GROUP_ID,
                        f"**🛂┊المسـتخـدم :** {_format.mentionuser(sender.first_name , sender.id)}\n"
                        f"**🎟┊الايـدي :** `{sender.id}`\n"
                        f"**📝┊اليـوزر :** @{sender.username if sender.username else 'لا يوجد'}\n\n"
                        f"**قام بتعديل رسالة إلى:**\n"
                        f"{event.message.message}",
                        reply_to=storage_msg_id
                    )
                    # تحويل الرسالة المعدلة إلى مجموعة التخزين
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                except Exception as e:
                    LOGS.error(f"Error handling edited message: {e}")

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

# باقي الأوامر (تفعيل التخزين، تعطيل التخزين، تخزين الخاص، تخزين الكروبات)
# تبقى كما هي دون تغيير
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

# قائمة لتخزين المستخدمين تحت المراقبة
monitored_users = []

# متغير لتخزين معرف مجموعة المراقبة
monitoring_group_id = None

@l313l.ar_cmd(pattern="مراقبة (?:(.*))")
async def monitor_user(event):
    global monitoring_group_id  # استخدام المتغير العام

    # الحصول على المستخدم أو الـ ID المطلوب مراقبته
    target = event.pattern_match.group(1)
    if not target:
        return await event.edit("**⌔┊يجب عليك تحديد المستخدم أو الـ ID للمراقبة**")

    # إنشاء مجموعة جديدة للمراقبة (إذا لم يتم إنشاؤها مسبقًا)
    if monitoring_group_id is None:
        try:
            result = await event.client(CreateChannelRequest(
                title="كروب المراقبة",
                about="مجموعة لمراقبة الرسائل التي يرسلها المستخدمون في المجموعات المشتركة.",
                megagroup=True
            ))
            monitoring_group_id = result.chats[0].id
            invite_link = await event.client(ExportChatInviteRequest(monitoring_group_id))
            await event.edit(f"**⌔┊تم إنشاء مجموعة المراقبة بنجاح: [اضغط هنا للدخول]({invite_link.link})**")
        except Exception as e:
            print(f"حدث خطأ أثناء إنشاء المجموعة: {str(e)}")  # Debugging
            return await event.edit(f"**⌔┊حدث خطأ أثناء إنشاء المجموعة: {str(e)}**")

    # إضافة المستخدم إلى قائمة المراقبة
    if target not in monitored_users:
        monitored_users.append(target)
        await event.edit(f"**⌔┊تم بدء مراقبة المستخدم {target} في جميع المجموعات المشتركة.**")
    else:
        await event.edit(f"**⌔┊المستخدم {target} تحت المراقبة بالفعل.**")

@l313l.ar_cmd(pattern="الغاء مراقبة (?:(.*))")
async def unmonitor_user(event):
    # الحصول على المستخدم أو الـ ID المطلوب إيقاف مراقبته
    target = event.pattern_match.group(1)
    if not target:
        return await event.edit("**⌔┊يجب عليك تحديد المستخدم أو الـ ID لإيقاف المراقبة**")

    # إزالة المستخدم من قائمة المراقبة
    if target in monitored_users:
        monitored_users.remove(target)
        await event.edit(f"**⌔┊تم إيقاف مراقبة المستخدم {target}.**")
    else:
        await event.edit(f"**⌔┊المستخدم {target} غير موجود في قائمة المراقبة.**")

@l313l.ar_cmd(incoming=True, func=lambda e: e.is_group, edited=False, forword=None)
async def monitor_messages(event):
    try:
        sender = await event.get_sender()
        # التحقق من أن المستخدم تحت المراقبة
        if str(sender.id) in monitored_users or sender.username in monitored_users:
            # إعداد الكليشة (الرسالة المخصصة)
            group_title = event.chat.title if event.chat.title else "مجموعة غير معروفة"
            message_link = f"https://t.me/c/{event.chat.id}/{event.message.id}"
            message_text = (
                "#المـراقبـه\n\n"
                f"↜︙الكــروب : {group_title}\n\n"
                f"↜︙المـرسـل : {_format.mentionuser(sender.first_name, sender.id)}\n\n"
                f"↜︙الرســالـه : {event.message.message}\n\n"
                f"↜︙رابـط الرسـاله : [اضغط هنا]({message_link})\n"
            )

            # إرسال الكليشة إلى مجموعة المراقبة
            await event.client.send_message(monitoring_group_id, message_text, parse_mode="markdown")
    except Exception as e:
        print(f"حدث خطأ أثناء مراقبة الرسائل: {str(e)}")  # Debugging

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
