import base64
import time

from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User

from JoKeRUB import l313l

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

# =========================================================== #
#                           الثـوابت                           #
# =========================================================== #
STAT_INDICATION = "**✧︙ جـاري جـمـع الإحصـائيـات انتـظـر ⏱ **"
CHANNELS_STR = "**✧︙ قائمة القنوات التي أنت فيها موجودة هنا\n\n"
CHANNELS_ADMINSTR = "**✧︙ قائمة القنوات التي انت مشـرف بهـا **\n\n"
CHANNELS_OWNERSTR = "**✧︙ قائمة القنوات التي تـكون انت مالكـها**\n\n"
GROUPS_STR = "**✧︙ قائمة المجموعات التي أنت فيها موجود فيـها**\n\n"
GROUPS_ADMINSTR = "**✧︙ قائمة المجموعات التي تكون مشـرف بهـا**\n\n"
GROUPS_OWNERSTR = "**✧︙ قائمة المجموعات التي تـكون انت مالكـها**\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


def inline_mention(user):
    full_name = user_full_name(user) or "بـدون اسـم"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


@l313l.ar_cmd(
    pattern="معلوماتي$",
    command=("معلوماتي", plugin_category),
    info={
        "header": "To get statistics of your telegram account.",
        "description": "Shows you the count of  your groups, channels, private chats...etc if no input is given.",
        "flags": {
            "g": "To get list of all group you in",
            "ga": "To get list of all groups where you are admin",
            "go": "To get list of all groups where you are owner/creator.",
            "c": "To get list of all channels you in",
            "ca": "To get list of all channels where you are admin",
            "co": "To get list of all channels where you are owner/creator.",
        },
        "usage": ["{tr}stat", "{tr}stat <flag>"],
        "examples": ["{tr}stat g", "{tr}stat ca"],
    },
)
async def stats(event):  # sourcery no-metrics
    "To get statistics of your telegram account."
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"✛━━━━━━━━━━━━━✛ \n"
    response += f"**✧︙ الدردشات الخاصة ️  :** {private_chats} \n"
    response += f"**✧︙ المستخـدمين : {private_chats - bots} \n"
    response += f"**✧︙ الـبوتـات :** {bots} \n"
    response += f"**✧︙ المجـموعـات :** {groups} \n"
    response += f"**✧︙ القنـوات  :** {broadcast_channels} \n"
    response += f"**✧︙ المجـموعات التـي تكـون فيها مشرف  :** {admin_in_groups} \n"
    response += f"**✧︙ المجموعات التـي تـكون انت مالكـها  **: {creator_in_groups} \n"
    response += f"**✧︙ القنوات التـي تكـون فيها مشـرف :** {admin_in_broadcast_channels} \n"
    response += (
        f"**✧︙ صلاحيات الاشـراف  :** {admin_in_broadcast_channels - creator_in_channels} \n"
    )
    response += f"**✧︙ المحـادثـات الغيـر مقـروء**: {unread} \n"
    response += f"**✧︙ الـتاكـات الغيـر مقـروء** : {unread_mentions} \n"
    response += f"✛━━━━━━━━━━━━━✛\n"
    await cat.edit(response)
        
@l313l.ar_cmd(
    pattern="قنواتي (الكل|ادمن|مالك)$",
)
async def stats(event):  # sourcery no-metrics
    catcmd = event.pattern_match.group(1)
    zedevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    
    if catcmd == "الكل":
        output = CHANNELS_STR
        for i in hi:
            output += f"⌔︙ [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        count = len(hi)
    elif catcmd == "ادمن":
        output = CHANNELS_ADMINSTR
        for i in hica:
            output += f"⌔︙ [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        count = len(hica)
    elif catcmd == "مالك":
        output = CHANNELS_OWNERSTR
        for i in hico:
            output += f"⌔︙ [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        count = len(hico)
    
    stop_time = time.time() - start_time
    output += f"\n**⌔︙ العدد الإجمالي: {count} قناة**"
    output += f"\n**- الوقت المستغرق: {stop_time:.02f} ثانية**"
    
    try:
        await zedevent.edit(output)
    except Exception:
        await edit_or_reply(
            zedevent,
            output,
            caption=caption,
        )

@l313l.ar_cmd(
    pattern="كروباتي (الكل|ادمن|مالك)$",
)
async def stats(event):  # sourcery no-metrics
    catcmd = event.pattern_match.group(1)
    zedevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    
    if catcmd == "الكل":
        output = GROUPS_STR
        for i in hi:
            output += f"⌔︙ [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        count = len(hi)
    elif catcmd == "ادمن":
        output = GROUPS_ADMINSTR
        for i in higa:
            output += f"⌔︙ [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        count = len(higa)
    elif catcmd == "مالك":
        output = GROUPS_OWNERSTR
        for i in higo:
            output += f"⌔︙ [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        count = len(higo)
    
    stop_time = time.time() - start_time
    output += f"\n**⌔︙ العدد الإجمالي: {count} مجموعة**"
    output += f"\n**- الوقت المستغرق: {stop_time:.02f} ثانية**"
    
    try:
        await zedevent.edit(output)
    except Exception:
        await edit_or_reply(
            zedevent,
            output,
            caption=caption,
    )
