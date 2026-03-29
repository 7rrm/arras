# تحديث فريق زدثــون
# ZThon T.me/ZedThon
# Devolper ZelZal T.me/zzzzl1l
import asyncio
import logging

from youtube_search import YoutubeSearch
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import User
from . import l313l
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

from ..vc_karar.stream_helper import Stream
from ..vc_karar.tg_downloader import tg_dl
from ..vc_karar.vcp_helper import ZedVC

plugin_category = "المكالمات"

logging.getLogger("pytgcalls").setLevel(logging.ERROR)

OWNER_ID = l313l.uid

vc_session = Config.VC_SESSION

if vc_session:
    vc_client = TelegramClient(
        StringSession(vc_session), Config.APP_ID, Config.API_HASH
    )
else:
    vc_client = l313l

vc_client.__class__.__module__ = "telethon.client.telegramclient"
vc_player = ZedVC(vc_client)

asyncio.create_task(vc_player.start())


@vc_player.app.on_stream_end()
async def handler(_, update):
    await vc_player.handle_next(update)


ALLOWED_USERS = set()


@l313l.ar_cmd(
    pattern="انضمام ?(\S+)? ?(?:ك)? ?(\S+)?",
    command=("انضمام", plugin_category),
    info={
        "header": "لـ الانضمـام الى المحـادثه الصـوتيـه",
        "ملاحظـه": "يمكنك اضافة الامر (ك) للامر الاساسي للانضمام الى المحادثه ك قنـاة مع اخفاء هويتك",
        "امـر اضافـي": {
            "ك": "للانضمام الى المحادثه ك قنـاة",
        },
        "الاستخـدام": [
            "{tr}انضمام",
            "{tr}انضمام + ايـدي المجمـوعـه",
            "{tr}انضمام ك (peer_id)",
            "{tr}انضمام (chat_id) ك (peer_id)",
        ],
        "مثــال :": [
            "{tr}انضمام",
            "{tr}انضمام -1005895485",
            "{tr}انضمام ك -1005895485",
            "{tr}انضمام -1005895485 ك -1005895485",
        ],
    },
)
async def joinVoicechat(event):
    "لـ الانضمـام الى المحـادثه الصـوتيـه"
    chat = event.pattern_match.group(1)
    joinas = event.pattern_match.group(2)

    await edit_or_reply(event, "⚈ **جـارِ الانضمـام الى المكالمـة الصـوتيـه ...**")

    if chat and chat != "ك":
        if chat.strip("-").isnumeric():
            chat = int(chat)
    else:
        chat = event.chat_id

    if vc_player.app.active_calls:
        return await edit_delete(
            event, f"⚈ **انت منضـم مسبقـاً الـى**  {vc_player.CHAT_NAME}"
        )

    try:
        vc_chat = await l313l.get_entity(chat)
    except Exception as e:
        return await edit_delete(event, f'⚈ **خطـأ** : \n{e or "UNKNOWN CHAT"}')

    if isinstance(vc_chat, User):
        return await edit_delete(event, "⚈ **عـذراً عـزيـزي ✗**\n⚈ **المكالمـة الصـوتيـه مغلقـه هنـا ؟!**\n⚈ **قم بفتح المكالمـه اولاً 🗣**")

    if joinas and not vc_chat.username:
        await edit_or_reply(event, "⚈ **عـذراً عـزيـزي**\n⚈**لم استطـع الانضمـام الى المكالمـة ✗**\n⚈ **قم بالانضمـام يدويـاً**")
        joinas = False

    out = await vc_player.join_vc(vc_chat, joinas)
    await edit_delete(event, out)


@l313l.ar_cmd(
    pattern="خروج",
    command=("خروج", plugin_category),
    info={
        "header": "لـ المغـادره من المحـادثه الصـوتيـه",
        "الاستخـدام": [
            "{tr}خروج",
        ],
    },
)
async def leaveVoicechat(event):
    "لـ المغـادره من المحـادثه الصـوتيـه"
    if vc_player.CHAT_ID:
        await edit_or_reply(event, "⚈ **جـارِ مغـادرة المحـادثـة الصـوتيـه ...**")
        chat_name = vc_player.CHAT_NAME
        await vc_player.leave_vc()
        await edit_delete(event, f"⚈ **تم مغـادرة المكـالمـه** {chat_name}")
    else:
        await edit_delete(event, "⚈ **لم تنضم بعـد للمكالمـه ؟!**")
    
