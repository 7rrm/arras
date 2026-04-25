import json
import math
import os
import random
import re
import time
from pathlib import Path
from uuid import uuid4

import yt_dlp
from telethon import Button, types
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery

from . import l313l
from ..Config import Config
from ..helpers.functions import rand_key
from ..helpers.functions.utube import (
    download_button,
    get_yt_video_id,
    get_ytthumb,
    ytsearch_data,
)
from ..sql_helper.globals import gvarstatus
from ..core.logger import logging

LOGS = logging.getLogger(__name__)
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
MEDIA_PATH_REGEX = re.compile(r"(:?\<\bmedia:(:?(?:.*?)+)\>)")
tr = Config.COMMAND_HAND_LER

def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb

@l313l.tgbot.on(InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:
        if str_y[0].lower() == "ytdl" and len(str_y) == 2:
            link = get_yt_video_id(str_y[1].strip())
            found_ = True
            if link is None:
                # استخدام yt_dlp للبحث بدلاً من youtubesearchpython
                ydl_opts = {
                    'extract_flat': True,
                    'quiet': True,
                    'no_warnings': True,
                }
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        search_query = f"ytsearch15:{str_y[1].strip()}"
                        resp = ydl.extract_info(search_query, download=False)
                        results_list = resp.get('entries', [])
                        
                        if len(results_list) == 0:
                            found_ = False
                        else:
                            # تحويل النتائج إلى الصيغة المطلوبة يدوياً
                            outdata = {}
                            for index, v in enumerate(results_list, start=1):
                                video_id = v.get('id')
                                thumb = await get_ytthumb(video_id)
                                
                                # تحويل المدة
                                duration_seconds = v.get('duration', 0)
                                if duration_seconds >= 3600:
                                    hours = duration_seconds // 3600
                                    minutes = (duration_seconds % 3600) // 60
                                    seconds = duration_seconds % 60
                                    duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
                                else:
                                    minutes = duration_seconds // 60
                                    seconds = duration_seconds % 60
                                    duration_str = f"{minutes}:{seconds:02d}"
                                
                                # تنسيق المشاهدات
                                views = v.get('view_count', 0)
                                if views >= 1000000:
                                    views_short = f"{views / 1000000:.1f}M"
                                elif views >= 1000:
                                    views_short = f"{views / 1000:.1f}K"
                                else:
                                    views_short = str(views)
                                
                                # الوصف
                                desc_snippet = ''
                                if v.get('description'):
                                    desc_snippet = v.get('description', '')[:100].replace('\n', ' ')
                                
                                title = f'<a href="https://youtube.com/watch?v={video_id}"><b>{v.get("title")}</b></a>\n'
                                message = title
                                if desc_snippet:
                                    message += f"<code>{desc_snippet}</code>\n\n"
                                message += f'<b>❯ المـده :</b> {duration_str}\n'
                                message += f'<b>❯ المشـاهـدات :</b> {views_short}\n'
                                message += f'<b>❯ تاريـخ الرفـع :</b> {v.get("upload_date", "غير معروف")}\n'
                                if v.get('uploader'):
                                    message += f'<b>❯ القنـاة :</b> <a href="https://youtube.com/@{v.get("uploader")}">{v.get("uploader")}</a>'
                                
                                list_view = f'<img src={thumb}><b><a href="https://youtube.com/watch?v={video_id}">{index}. {v.get("title")}</a></b><br>'
                                
                                outdata[index] = dict(
                                    message=message,
                                    thumb=thumb,
                                    video_id=video_id,
                                    list_view=list_view,
                                )
                            
                            key_ = rand_key()
                            ytsearch_data.store_(key_, outdata)
                            buttons = [
                                [
                                    Button.inline(
                                        f"1 / {len(outdata)}",
                                        data=f"ytdl_next_{key_}_1",
                                        style="primary"
                                    ),
                                ],
                                [
                                    Button.inline(
                                        "‹ : فَيديـو : ›",
                                        data=f'ytdl_download_{outdata[1]["video_id"]}_video',
                                        style="danger"
                                    ),
                                    Button.inline(
                                        "‹ : صَــوت : ›",
                                        data=f'ytdl_download_{outdata[1]["video_id"]}_audio',
                                        style="danger"
                                    ),
                                ],
                                [
                                    Button.inline(
                                        "📜 القائمـة",
                                        data=f"ytdl_listall_{key_}_1",
                                        style="primary"
                                    )
                                ],
                            ]
                            caption = outdata[1]["message"]
                            photo = await get_ytthumb(outdata[1]["video_id"])
                except Exception as e:
                    LOGS.error(f"بحث yt_dlp error: {e}")
                    found_ = False
            else:
                caption, buttons = await download_button(link, body=True)
                photo = await get_ytthumb(link)
            
            if found_:
                markup = event.client.build_reply_markup(buttons)
                photo_input = types.InputWebDocument(
                    url=photo, size=0, mime_type="image/jpeg", attributes=[]
                )
                text, msg_entities = await event.client._parse_message_text(
                    caption, "html"
                )
                result = types.InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=link if link else str_y[1],
                    description="⬇️ اضغـط للتحميـل",
                    thumb=photo_input,
                    content=photo_input,
                    send_message=types.InputBotInlineMessageMediaAuto(
                        reply_markup=markup, message=text, entities=msg_entities
                    ),
                )
            else:
                result = builder.article(
                    title="Not Found",
                    text=f"No Results found for `{str_y[1]}`",
                    description="INVALID",
                )
            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="Not Found",
                            text=f"No Results found for `{str_y[1]}`",
                            description="INVALID",
                        )
                    ]
                )
        elif string == "pmpermit":
            controlpmch = gvarstatus("pmchannel") or None
            if controlpmch is not None:
                zchannel = controlpmch.replace("@", "")
                buttons = [[Button.url("⌔ قنـاتـي ⌔", f"https://t.me/{zchannel}")]]
            else:
                buttons = [[Button.url("𝗭𝗧𝗵𝗼𝗻", "https://t.me/ZThon")]]
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                CAT = [x for x in PM_PIC.split()]
                PIC = list(CAT)
                ZZZ_IMG = random.choice(PIC)
            else:
                ZZZ_IMG = None
            query_ = gvarstatus("pmpermit_text")
            if ZZZ_IMG and ZZZ_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(
                    ZZZ_IMG,
                    text=query_,
                    buttons=buttons,
                )
            elif ZZZ_IMG:
                result = builder.document(
                    ZZZ_IMG,
                    title="Alive zzz",
                    text=query_,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="Alive zzz",
                    text=query_,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
