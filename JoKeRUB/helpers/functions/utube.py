import os
import re
import glob  # <-- أضف هذا
import random  # <-- أضف هذا
import urllib.request
from collections import defaultdict

import ujson
import yt_dlp
from telethon import Button
from youtubesearchpython import VideosSearch
from yt_dlp.utils import DownloadError, ExtractorError, GeoRestrictedError

from ...Config import Config
from ...core import pool
from ...core.logger import logging
from ..aiohttp_helper import AioHttp
from ..progress import humanbytes
from .functions import sublists

LOGS = logging.getLogger(__name__)

def get_cookies_file():
    folder_path = f"{os.getcwd()}/karar"
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return cookie_txt_file


BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./JoKeRUB/cache/ytsearch.json"

song_dl = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"

thumb_dl = "yt-dlp --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' -f 'best[height<=480]' {video_link}"
name_dl = (
    "yt-dlp --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)


async def yt_search(JoKeRUB):
    try:
        JoKeRUB = urllib.parse.quote(JoKeRUB)
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={JoKeRUB}"
        )

        user_data = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_link = []
        k = 0
        for i in user_data:
            if user_data:
                video_link.append(f"https://www.youtube.com/watch?v={user_data[k]}")
            k += 1
            if k > 3:
                break
        if video_link:
            return video_link[0]
        return "Couldnt fetch results"
    except Exception:
        return "Couldnt fetch results"


async def ytsearch(query, limit):
    result = ""
    videolinks = VideosSearch(query.lower(), limit=limit)
    for v in videolinks.result()["result"]:
        textresult = f"[{v['title']}](https://www.youtube.com/watch?v={v['id']})\n"
        try:
            textresult += f"**الشرح : **`{v['descriptionSnippet'][-1]['text']}`\n"
        except Exception:
            textresult += "**الشرح : **`None`\n"
        textresult += (
            f"**المدة : **{v['duration']}  **المشاهدات : **{v['viewCount']['short']}\n"
        )
        result += f"☞ {textresult}\n"
    return result


class YT_Search_X:
    def __init__(self):
        if not os.path.exists(PATH):
            with open(PATH, "w") as f_x:
                ujson.dump({}, f_x)
        with open(PATH) as yt_db:
            self.db = ujson.load(yt_db)

    def store_(self, rnd_id: str, results: dict):
        self.db[rnd_id] = results
        self.save()

    def save(self):
        with open(PATH, "w") as outfile:
            ujson.dump(self.db, outfile, indent=4)


ytsearch_data = YT_Search_X()

"""
async def yt_data(JoKeRUB):
    params = {"format": "json", "url": JoKeRUB}
    url = "https://www.youtube.com/oembed"  # https://stackoverflow.com/questions/29069444/returning-the-urls-as-a-list-from-a-youtube-search-query
    query_string = urllib.parse.urlencode(params)
    url = f"{url}?{query_string}"
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = ujson.loads(response_text.decode())
    return data
"""


async def get_ytthumb(videoid: str):
    thumb_quality = [
        "maxresdefault.jpg",  # Best quality
        "hqdefault.jpg",
        "sddefault.jpg",
        "mqdefault.jpg",
        "default.jpg",  # Worst quality
    ]
    thumb_link = "https://i.imgur.com/4LwPLai.png"
    for qualiy in thumb_quality:
        link = f"https://i.ytimg.com/vi/{videoid}/{qualiy}"
        if await AioHttp().get_status(link) == 200:
            thumb_link = link
            break
    return thumb_link


def get_yt_video_id(url: str):
    if match := YOUTUBE_REGEX.search(url):
        return match.group(1)


# Based on https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f
def get_choice_by_id(choice_id, media_type: str):
    if choice_id == "mkv":
        # default format selection
        choice_str = "bestvideo+bestaudio/best"
        disp_str = "best(video+audio)"
    elif choice_id == "mp3":
        choice_str = "320"
        disp_str = "320 Kbps"
    elif choice_id == "mp4":
        # Download best Webm / Mp4 format available or any other best if no mp4
        # available
        choice_str = "bestvideo[ext=webm]+251/bestvideo[ext=mp4]+(258/256/140/bestaudio[ext=m4a])/bestvideo[ext=webm]+(250/249)/best"
        disp_str = "best(video+audio)[webm/mp4]"
    else:
        disp_str = str(choice_id)
        choice_str = (
            f"{disp_str}+(258/256/140/bestaudio[ext=m4a])/best"
            if media_type == "v"
            else disp_str
        )

    return choice_str, disp_str


async def result_formatter(results: list):
    output = {}
    for index, r in enumerate(results, start=1):
        v_deo_id = r.get("id")
        thumb = await get_ytthumb(v_deo_id)
        upld = r.get("channel")
        title = f'<a href={r.get("link")}><b>{r.get("title")}</b></a>\n'
        out = title
        if r.get("descriptionSnippet"):
            out += "<code>{}</code>\n\n".format(
                "".join(x.get("text") for x in r.get("descriptionSnippet"))
            )
        out += f'<b>❯ المـده :</b> {r.get("accessibility").get("duration")}\n'
        views = f'<b>❯ المشـاهـدات :</b> {r.get("viewCount").get("short")}\n'
        out += views
        out += f'<b>❯ تاريـخ الرفـع :</b> {r.get("publishedTime")}\n'
        if upld:
            out += "<b>❯ القنـاة :</b> "
            out += f'<a href={upld.get("link")}>{upld.get("name")}</a>'

        output[index] = dict(
            message=out,
            thumb=thumb,
            video_id=v_deo_id,
            list_view=f'<img src={thumb}><b><a href={r.get("link")}>{index}. {r.get("accessibility").get("title")}</a></b><br>',
        )

    return output


def yt_search_btns(
    data_key: str, page: int, vid: str, total: int, del_back: bool = False, chat_id: int = None, msg_id: int = None
):
    # تخزين chat_id و msg_id في البيانات
    extra_data = f"_{chat_id}_{msg_id}" if chat_id and msg_id else ""
    
    buttons = [
        [
            Button.inline(
                text="⬅️  رجوع",
                data=f"ytdl_back_{data_key}_{page}{extra_data}",
            ),
            Button.inline(
                text=f"{page} / {total}",
                data=f"ytdl_next_{data_key}_{page}{extra_data}",
            ),
        ],
        [
            Button.inline(
                text="📜  قائمة الكل",
                data=f"ytdl_listall_{data_key}_{page}{extra_data}",
            ),
            Button.inline(
                text="⬇️  تحميل",
                data=f"ytdl_download_{vid}_0{extra_data}",
            ),
        ],
    ]
    if del_back:
        buttons[0].pop(0)
    return buttons



@pool.run_in_thread
def download_button(vid: str, body: bool = False):
    try:
        # استخراج معلومات الفيديو من يوتيوب (بدون تحميل)
        ydl_opts = {
            "no-playlist": True,
            "quiet": True,
            "ignoreerrors": True,
            "extract_flat": True,  # استخراج المعلومات فقط
            "force_generic_extractor": False,
        }
        
        vid_data = yt_dlp.YoutubeDL(ydl_opts).extract_info(
            BASE_YT_URL + vid, download=False
        )
        
        if vid_data is None:
            buttons = [[Button.inline("❌ الفيديو غير متاح", data="noop")]]
            if body:
                return "لا يمكن تحميل الفيديو", buttons
            return buttons
            
    except Exception as e:
        LOGS.error(f"Error extracting video info: {str(e)}")
        buttons = [[Button.inline(f"❌ خطأ: {str(e)[:30]}", data="noop")]]
        if body:
            return "حدث خطأ أثناء جلب البيانات", buttons
        return buttons
    
    # إنشاء أزرار التحميل
    buttons = [
        [
            Button.inline("🎵 تحميل صوتي MP3", data=f"ytdl_download_audio_{vid}"),
            Button.inline("🎬 تحميل فيديو MP4", data=f"ytdl_download_video_{vid}"),
        ],
        [
            Button.inline("📜 قائمة البحث", data=f"ytdl_listall_{vid}_1"),
        ]
    ]
    
    if body:
        # تنسيق معلومات الفيديو
        title = vid_data.get('title', 'فيديو')
        duration = vid_data.get('duration', 0)
        # تحويل المدة إلى دقائق وثواني
        minutes = duration // 60
        seconds = duration % 60
        duration_str = f"{minutes} minutes, {seconds} seconds" if minutes > 0 else f"{seconds} seconds"
        
        views = vid_data.get('view_count', 0)
        views_str = f"{views/1000000:.0f}M views" if views >= 1000000 else f"{views/1000:.0f}K views"
        
        upload_date = vid_data.get('upload_date', '')
        if upload_date:
            year = upload_date[:4]
            ago_years = 2026 - int(year)
            upload_str = f"{ago_years} years ago" if ago_years > 0 else "this year"
        else:
            upload_str = "Unknown"
        
        channel = vid_data.get('channel', 'Unknown')
        
        vid_body = f'''<b><a href="{BASE_YT_URL + vid}">{title}</a></b>

❯ المـده : {duration_str}
❯ المشـاهـدات : {views_str}
❯ تاريـخ الرفـع : {upload_str}
❯ القنـاة : {channel}</b>'''
        
        return vid_body, buttons
    return buttons

@pool.run_in_thread
def _tubeDl(url: str, starttime, uid: str):
    ydl_opts = {
        "addmetadata": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": os.path.join(
            Config.TEMP_DIR, str(starttime), "%(title)s-%(format)s.%(ext)s"
        ),
        #         "logger": LOGS,
        "format": uid,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "postprocessors": [
            {"key": "FFmpegMetadata"}
            # ERROR R15: Memory quota vastly exceeded
            # {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
        "quiet": True,
        "no_warnings": True,
        "cookiefile" : get_cookies_file(),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            x = ydl.download([url])
    except DownloadError as e:
        LOGS.error(e)
    except GeoRestrictedError:
        LOGS.error("هذا الفيديو غير متاح  في بلدك")
    else:
        return x


@pool.run_in_thread
def _mp3Dl(url: str, starttime, uid: str):
    _opts = {
        "outtmpl": os.path.join(Config.TEMP_DIR, str(starttime), "%(title)s.%(ext)s"),
        #         "logger": LOGS,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": uid,
            },
            {"key": "EmbedThumbnail"},  # ERROR: Conversion failed!
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
        "no_warnings": True,
        "cookiefile" : get_cookies_file(),
    }
    try:
        with yt_dlp.YoutubeDL(_opts) as ytdl:
            dloader = ytdl.download([url])
    except Exception as y_e:
        LOGS.exception(y_e)
        return y_e
    else:
        return dloader
