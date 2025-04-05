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


# أمر الهمسة السرية
# أمر الهمسة السرية المعدل
@bot.on(admin_cmd(pattern="اهمس$"))
async def whisper_command(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        target_user = replied.sender_id
        
        # إنشاء زر الإنلاين
        button = [
            [Button.inline("اضغط هنا لكتابة الهمسة", data=f"whisper_{target_user}")]
        ]
        
        # إرسال الرسالة مع الزر
        await event.client.send_message(
            event.chat_id,
            "**لإرسال همسة سرية:**",
            buttons=button,
            reply_to=replied.id
        )
        await event.delete()  # حذف الأمر الأصلي
    else:
        await event.edit("يجب الرد على الشخص المراد إرسال الهمسة له باستخدام الأمر `.اهمس`")
        await asyncio.sleep(3)
        await event.delete()

# باقي الكود كما هو...

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"whisper_(\d+)")))
async def whisper_callback(event):
    target_user = int(event.data_match.group(1).decode('utf-8'))
    if event.sender_id != target_user:
        await event.answer("هذه الهمسة ليست لك!", alert=True)
        return
    
    # إرسال رسالة لكتابة الهمسة
    async with bot.conversation(event.sender_id) as conv:
        await conv.send_message("أرسل الهمسة السرية الآن:")
        try:
            whisper_msg = await conv.get_response(timeout=60)
            await conv.send_message("تم إرسال الهمسة بنجاح!")
            
            # إرسال الهمسة للشخص المستهدف
            buttons = [
                [Button.inline("اضغط هنا لرؤية الهمسة", data=f"show_whisper_{event.sender_id}")]
            ]
            await bot.send_message(
                target_user,
                f"لديك همسة سرية من {event.sender.first_name}",
                buttons=buttons
            )
            
        except asyncio.TimeoutError:
            await conv.send_message("انتهى الوقت المحدد لإرسال الهمسة")


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"show_whisper_(\d+)")))
async def show_whisper(event):
    sender_id = int(event.data_match.group(1).decode('utf-8'))
    if event.sender_id != sender_id:
        await event.answer("هذه الهمسة ليست لك!", alert=True)
        return
    
    # هنا يمكنك استرجاع الهمسة من قاعدة بيانات أو أي طريقة تخزين تفضلها
    # في هذا المثال سنستخدم محادثة بسيطة
    async with bot.conversation(sender_id) as conv:
        await conv.send_message("الهمسة السرية هي: ...")  # استبدل هذا بالهمسة الفعلية
