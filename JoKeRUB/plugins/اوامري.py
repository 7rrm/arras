import re
from telethon import Button, events
from telethon.events import CallbackQuery
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from l313l.razan.resources.assistant import *
from l313l.razan.resources.mybot import *
from JoKeRUB import l313l
from ..core import check_owner
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# الصور والنصوص الثابتة
JEP_IC = "https://graph.org/file/a467d3702fbc9ae391fe0-e6322ec96a2fd4c1f4.jpg"
ROE = "**♰ هـذه هي قائمة اوامـر السـورس  ♰**"
HMSA_ICON = "https://graph.org/file/a467d3702fbc9ae391fe0.jpg"
HMSA_TEXT = "**♰ هـذه همسة سرية من سورس زدثون ♰**"
ddd = "💌"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        
        # قسم الأوامر
        if query.startswith("اوامري") and event.query.user_id == bot.uid:
            buttons = [
                [Button.inline("اوامر الادمن 🧑‍💻", data="l313l0")],
                [Button.inline("اوامر البوت 🤖", data="rozbot"),
                 Button.inline("الحساب 🆔", data="Jmrz"),
                 Button.inline("المجموعات 👥", data="gro")],
                [Button.inline("الصيغ & الجهات ⚡", data="sejrz"),
                 Button.inline("الحماية & تلكراف ⚓", data="grrz")],
                [Button.inline("اوامر التسلية 💫", data="tslrzj"),
                 Button.inline("الترحيبات & الردود 👋", data="r7brz")],
                [Button.inline("اومر المساعدة ✨", data="krrznd"),
                 Button.inline("الملصقات وصور 🌃", data="jrzst")],
                [Button.inline("التكرار والتنظيف 🚮", data="krrznd"),
                 Button.inline("الترفيـه ✨", data="rfhrz")],
                [Button.inline("الأكستـرا ⚡", data="iiers"),
                 Button.inline("الانتحال والتقليد 🗣️", data="uscuxrz")],
            ]
            if JEP_IC and JEP_IC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(JEP_IC, text=ROE, buttons=buttons, link_preview=False)
            elif JEP_IC:
                result = builder.document(JEP_IC, title="JoKeRUB", text=ROE, buttons=buttons, link_preview=False)
            else:
                result = builder.article(title="JoKeRUB", text=ROE, buttons=buttons, link_preview=False)
        
        # قسم الهمسة السرية
        elif query.startswith("همسة") and event.query.user_id == bot.uid:
            user_id = gvarstatus("hmsa_id")
            full_name = gvarstatus("hmsa_name") or "مجهول"
            username = gvarstatus("hmsa_user") or "None"
            
            buttons = [[Button.inline("اضغط لرؤية الهمسة", data=f"hmsa_{user_id}")]]
            text = f"{HMSA_TEXT}\n\nلـ {full_name} ({username})\n{ddd}"
            
            if HMSA_ICON and HMSA_ICON.endswith((".jpg", ".png")):
                result = builder.photo(HMSA_ICON, text=text, buttons=buttons, link_preview=False)
            else:
                result = builder.article(title="همسة سرية", text=text, buttons=buttons, link_preview=False)
        
        await event.answer([result] if result else None)

    @tgbot.on(events.CallbackQuery(pattern=re.compile(rb"hmsa_(\d+)")))
    async def hmsa_callback(event):
        user_id = int(event.pattern_match.group(1).decode('utf-8'))
        if event.query.user_id != user_id:
            return await event.answer("هذه الهمسة ليست لك!", alert=True)
        await event.answer("ها هي همستك السرية: ...", alert=True)

# الأوامر الأساسية
@bot.on(admin_cmd(outgoing=True, pattern="اوامري"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "اوامري")
    await response[0].click(event.chat_id)
    await event.delete()

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)"))
async def repozedub(event):
    user = event.pattern_match.group(1)
    if not user and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎يجب الرد على مستخدم أو كتابة اسم المستخدم**")

    try:
        zthon_user = await get_user_from_event(event)
        if not zthon_user:
            return await edit_or_reply(event, "**⎉╎لم يتم العثور على المستخدم**")

        user_id, full_name, username = await zzz_info(zthon_user, event)
        
        delgvar("hmsa_id")
        delgvar("hmsa_name")
        delgvar("hmsa_user")
        addgvar("hmsa_id", str(user_id))
        addgvar("hmsa_name", full_name or "غير معروف")
        addgvar("hmsa_user", username or "None")

        response = await l313l.inline_query(Config.TG_BOT_USERNAME, "همسة")
        if response:
            await response[0].click(event.chat_id)
            await event.delete()
        else:
            await edit_or_reply(event, "**⎉╎حدث خطأ في إنشاء الرسالة المضمنة**")

    except Exception as e:
        await edit_or_reply(event, f"**⎉╎حدث خطأ: {str(e)}**")

# باقي الأكواد الأصلية (لازالت كما هي)
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"l313l0")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="jrzst")],
        [Button.inline("القائمة الرئيسية", data="ROE")],
    ]
    await event.edit(ROZADM, buttons=buttons)

# ... (بقية الأكواد الأصلية تبقى كما هي دون تغيير)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"jrzst")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="tslrzj")],
        [Button.inline("رجوع", data="l313l0")],
    ]
    await event.edit(GRTSTI, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"tslrzj")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="krrznd")],
        [Button.inline("رجوع", data="jrzst")],
    ]
    await event.edit(JMAN, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"krrznd")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="rozbot")],
        [Button.inline("رجوع", data="tslrzj")],
    ]
    await event.edit(TKPRZ, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"rozbot")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="Jmrz")],
        [Button.inline("رجوع", data="krrznd")],
    ]
    await event.edit(ROZBOT, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"Jmrz")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="r7brz")],
        [Button.inline("رجوع", data="rozbot")],
    ]
    await event.edit(JROZT, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"r7brz")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="sejrz")],
        [Button.inline("رجوع", data="Jmrz")],
    ]
    await event.edit(JMTRD, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"sejrz")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="gro")],
        [Button.inline("رجوع", data="r7brz")],
    ]
    await event.edit(ROZSEG, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"gro")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="grrz")],
        [Button.inline("رجوع", data="sejrz")],
    ]
    await event.edit(JMGR1, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"grrz")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="iiers")],
        [Button.inline("رجوع", data="gro")],
    ]
    await event.edit(ROZPRV, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"iiers")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="rfhrz")],
        [Button.inline("رجوع", data="grrz")],
    ]
    await event.edit(HERP, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"rfhrz")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="uscuxrz")],
        [Button.inline("رجوع", data="iiers")],
    ]
    await event.edit(T7SHIZ, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"uscuxrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع", data="l313l0")]]
    await event.edit(CLORN, buttons=buttons)
