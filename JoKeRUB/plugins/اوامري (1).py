import re
from telethon import Button, events
from telethon.events import CallbackQuery
from l313l.razan.resources.assistant import *
from l313l.razan.resources.mybot import *
from JoKeRUB import l313l
from ..core import check_owner
from ..Config import Config

# الصورة الرئيسية للقائمة
JEP_IC = "https://graph.org/file/a467d3702fbc9ae391fe0-e6322ec96a2fd4c1f4.jpg"
ROE = "**♰ هـذه هي قائمة اوامـر السـورس  ♰**"

hmm = "همسـة"
ymm = "يستطيـع"
fmm = "فتـح الهمسـه 🗳"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - **همسـة سـࢪيـه** 📠\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص).\nعبـر زدثــون"
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - همسـة سـࢪيـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔╎اضغـط الـزر بالاسفـل ⚓\n⌔╎لـ اࢪسـال همسـه سـࢪيـه الى"
ddd = "💌"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("اوامري") and event.query.user_id == bot.uid:
            buttons = [
                [Button.inline("اوامر الادمن 🧑‍💻", data="l313l0")],
                [
                    Button.inline("اوامر البوت 🤖", data="rozbot"),
                    Button.inline("الحساب 🆔", data="Jmrz"),
                    Button.inline("المجموعات 👥", data="gro"),
                ],
                [
                    Button.inline("الصيغ & الجهات ⚡", data="sejrz"),
                    Button.inline("الحماية & تلكراف ⚓", data="grrz"),
                ],
                [
                    Button.inline("اوامر التسلية 💫", data="tslrzj"),
                    Button.inline("الترحيبات & الردود 👋", data="r7brz"),
                ],
                [
                    Button.inline("اومر المساعدة ✨", data="krrznd"),
                    Button.inline("الملصقات وصور 🌃", data="jrzst"),
                ],
                [
                    Button.inline("التكرار والتنظيف 🚮", data="krrznd"),
                    Button.inline("الترفيـه ✨", data="rfhrz"),
                ],
                [
                    Button.inline("الأكستـرا ⚡", data="iiers"),
                    Button.inline("الانتحال والتقليد 🗣️", data="uscuxrz"),
                ],
            ]
            if JEP_IC and JEP_IC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    JEP_IC, text=ROE, buttons=buttons, link_preview=False
                )
            elif JEP_IC:
                result = builder.document(
                    JEP_IC,
                    title="JoKeRUB",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="JoKeRUB",
                    text=ROE,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)


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


# تعريف الأزرار والأوامر
@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"l313l0")))
@check_owner
async def _(event):
    buttons = [
        [Button.inline("التالي", data="jrzst")],
        [Button.inline("القائمة الرئيسية", data="ROE")],
    ]
    await event.edit(ROZADM, buttons=buttons)


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


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

async def user_info(user, event):
    FullUser = (await event.client(GetFullUserRequest(user.id))).full_user
    first_name = user.first_name
    full_name = FullUser.private_forward_name
    user_id = user.id
    username = user.username
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else None
    )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else "None"
    return user_id, full_name, username

@bot.on(admin_cmd(pattern="اهمس$"))
async def whisper_command(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        target_user = await get_user_from_event(event)
        try:
            user_id, full_name, username = await user_info(target_user, event)
        except (AttributeError, TypeError):
            return
        
        # إنشاء زر الإنلاين
        button = [[Button.inline("اضغط هنا لكتابة الهمسة", data=f"whisper_{user_id}")]]
        
        # إرسال الرسالة مع الزر
        await event.client.send_message(
            event.chat_id,
            f"{ttt} {full_name}",
            buttons=button,
            reply_to=replied.id
        )
        await event.delete()
    else:
        await event.edit("**يجب الرد على الشخص المراد إرسال الهمسة له باستخدام الأمر `.اهمس`**")
        await asyncio.sleep(3)
        await event.delete()

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"whisper_(\d+)")))
async def whisper_callback(event):
    target_user = int(event.data_match.group(1).decode('utf-8'))
    if event.sender_id != target_user:
        await event.answer("هذه الهمسة ليست لك!", alert=True)
        return
    
    # إرسال رسالة لكتابة الهمسة
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("**أرسل الهمسة السرية الآن:**")
        try:
            whisper_msg = await conv.get_response(timeout=60)
            await conv.send_message("**تم إرسال الهمسة بنجاح!**")
            
            # إرسال الهمسة للشخص المستهدف
            buttons = [[Button.inline("اضغط هنا لرؤية الهمسة", data=f"show_whisper_{event.sender_id}")]]
            await bot.send_message(
                target_user,
                f"**{hss} {event.sender.first_name}**",
                buttons=buttons
            )
            
        except asyncio.TimeoutError:
            await conv.send_message("**انتهى الوقت المحدد لإرسال الهمسة**")

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"show_whisper_(\d+)")))
async def show_whisper(event):
    sender_id = int(event.data_match.group(1).decode('utf-8'))
    if event.sender_id != sender_id:
        await event.answer("هذه الهمسة ليست لك!", alert=True)
        return
    
    # هنا يمكنك استرجاع الهمسة من قاعدة بيانات أو أي طريقة تخزين تفضلها
    await event.answer("هذه هي الهمسة السرية: [المحتوى السري]", alert=True)
