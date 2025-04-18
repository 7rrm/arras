import asyncio
import glob
import base64
import io
import urllib.parse
import os
import random
from pathlib import Path
from YoutubeSearch import YoutubeSearch
from yt_dlp import YoutubeDL
from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError, ChatSendMediaForbiddenError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv, name_dl, song_dl, video_dl, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id
from . import l313l

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "**╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰**"
SONG_NOT_FOUND = "**- فشـل في العثور على النتائج**"
SONG_SENDING_STRING = "**╮ جـارِ الرفـع ▬▬ . . .🎧♥️╰**"
# =========================================================== #
#                                                             #
# =========================================================== #
def get_cookies_file():
    folder_path = os.path.join(os.getcwd(), "karar")  # المسار إلى مجلد zion
    if not os.path.exists(folder_path):
        raise FileNotFoundError("Folder 'karar' not found in current directory")
        
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))  # البحث عن ملفات txt
    if not txt_files:
        raise FileNotFoundError("No .txt cookies files found in 'karar' folder")
        
    return random.choice(txt_files)  # اختيار ملف كوكيز عشوائي

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)

@l313l.ar_cmd(
    pattern="بحث(?: |$)(.*)",
    command=("بحث", plugin_category),
    info={
        "header": "للبحث عن الأغاني من يوتيوب",
        "description": "يبحث عن المقطع الصوتي الأول من يوتيوب ويرسله",
        "usage": "{tr}بحث <اسم المقطع>",
        "examples": "{tr}بحث أغنية",
    },
)
async def _(event):
    "للبحث عن الأغاني"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**⎉╎قم باضافـة إسـم للامـر ..**\n**⎉╎بحث + اسـم المقطـع الصـوتي**")
    
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING)
    
    ydl_ops = {
        "format": "bestaudio[ext=m4a]",
        "keepvideo": False,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "cookiefile": get_cookies_file(),
    }
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
    except Exception as e:
        await catevent.edit(f"**- فشـل التحميـل** \n**- الخطأ :** `{str(e)}`")
        return
    
    await catevent.edit("**╮ جـارِ التحميل ▬▭ . . .🎧♥️╰**")
    
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        
        await catevent.edit(SONG_SENDING_STRING)
        await event.client.send_file(
            event.chat_id,
            audio_file,
            force_document=False,
            caption=f"**⎉╎البحث :** `{title}`",
            thumb=thumb_name,
            reply_to=reply_to_id,
        )
        await catevent.delete()
    except Exception as e:
        await catevent.edit(f"**- فشـل التحميـل** \n**- الخطأ :** `{str(e)}`")
    finally:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)


@l313l.ar_cmd(
    pattern="فيديو(?:\s|$)([\s\S]*)",
    command=("فيديو", plugin_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def _(event):
    "To search video songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على ما تريد البحث عنه")
    cat = base64.b64decode("YnkybDJvRG04WEpsT1RBeQ==")
    catevent = await edit_or_reply(event, "⌔∮ جاري البحث عن المطلوب انتظر")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`"
        )
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    try:
        stderr = (await _catutils.runcmd(video_cmd))[1]
        # if stderr:
        # return await catevent.edit(f"**Error :** `{stderr}`")
        catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
        if stderr:
            return await catevent.edit(f"**Error :** `{stderr}`")
        catname = os.path.splitext(catname)[0]
        vsong_file = Path(f"{catname}.mp4")
    except:
        pass
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`"
        )
    await catevent.edit("**⌔∮ جاري الارسال انتظر قليلا**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    title = catname.replace("./temp/", "").replace("_", "|")
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        caption=f"**Title:** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@l313l.ar_cmd(pattern="اسم الاغنية$")
async def shazamcmd(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "⌔∮ يرجى الرد على مقطع صوتي او بصمه للبحث عنها"
        )
    catevent = await edit_or_reply(event, "**⌔∮ يتم معالجه المقطع الصوتي  .**")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            catevent, f"**⌔∮ لقد حدث خطأ ما اثناء البحث عن اسم الاغنيه:**\n__{e}__"
        )

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**الاغنية:** `{song}`", reply_to=reply
    )
    await catevent.delete()


@l313l.ar_cmd(
    pattern="بحث2(?:\s|$)([\s\S]*)",
    command=("بحث2", plugin_category),
    info={
        "header": "To search songs and upload to telegram",
        "description": "Searches the song you entered in query and sends it quality of it is 320k",
        "usage": "{tr}song2 <song name>",
        "examples": "{tr}song2 memories song",
    },
)
async def _(event):
    "To search songs"
    song = event.pattern_match.group(1)
    chat = "@songdl_bot"
    reply_id_ = await reply_id(event)
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
        except YouBlockedUserError:
            await edit_or_reply(
                catevent, "**Error:** Trying to unblock & retry, wait a sec..."
            )
            await catub(unblock("songdl_bot"))
            purgeflag = await conv.send_message("/start")
        await conv.get_response()
        await conv.send_message(song)
        hmm = await conv.get_response()
        while hmm.edit_hide is not True:
            await asyncio.sleep(0.1)
            hmm = await event.client.get_messages(chat, ids=hmm.id)
        baka = await event.client.get_messages(chat)
        if baka[0].message.startswith(
            ("I don't like to say this but I failed to find any such song.")
        ):
            await delete_conv(event, chat, purgeflag)
            return await edit_delete(
                catevent, SONG_NOT_FOUND, parse_mode="html", time=5
            )
        await catevent.edit(SONG_SENDING_STRING, parse_mode="html")
        await baka[0].click(0)
        await conv.get_response()
        await conv.get_response()
        music = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>Title :- <code>{song}</code></b>",
            parse_mode="html",
            reply_to=reply_id_,
        )
        await catevent.delete()
        await delete_conv(event, chat, purgeflag)

