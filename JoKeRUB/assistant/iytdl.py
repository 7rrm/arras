""" Download Youtube Video / Audio in a User friendly interface """
# --------------------------- #
#   Modded ytdl by code-rgb   #
# --------------------------- #

import asyncio
import glob
import io
import os
import re
from pathlib import Path
from time import time

import ujson
from telethon import Button, types
from telethon.errors import BotResponseTimeoutError
from telethon.events import CallbackQuery
from telethon.utils import get_attributes
from wget import download

from JoKeRUB import l313l

from ..Config import Config
from ..core import check_owner, pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import post_to_telegraph, progress, reply_id
from ..helpers.functions.utube import (
    _mp3Dl,
    _tubeDl,
    download_button,
    get_choice_by_id,
    get_ytthumb,
    yt_search_btns,
)
from ..plugins import BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./JoKeRUB/cache/ytsearch.json"
plugin_category = "البوت"


@l313l.ar_cmd(
    pattern="بحث(?:\s|$)([\s\S]*)",
    command=("يوت", plugin_category),
    info={
        "header": "ytdl with inline buttons.",
        "description": "To search and download youtube videos by inline buttons.",
        "usage": "{tr}iytdl [URL / Text] or [Reply to URL / Text]",
    },
)
async def iytdl_inline(event):
    "ytdl with inline buttons."
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    input_url = None
    if input_str:
        input_url = (input_str).strip()
    elif reply and reply.text:
        input_url = (reply.text).strip()
    if not input_url:
        return await edit_delete(event, "**- بالـرد ع رابـط او كتـابة نص مـع الامـر**")
    zedevent = await edit_or_reply(event, f"**⌔╎جـارِ البحث في اليوتيوب عـن:** `'{input_url}'`")
    flag = True
    cout = 0
    results = None
    while flag:
        try:
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, f"ytdl {input_url}"
            )
            flag = False
        except BotResponseTimeoutError:
            await asyncio.sleep(2)
        cout += 1
        if cout > 5:
            flag = False
    if results:
        await zedevent.delete()
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    else:
        await zedevent.edit("**⌔╎عـذراً .. لم اجد اي نتائـج**")

@l313l.tgbot.on(
    CallbackQuery(
        data=re.compile(b"^ytdl_download_(.*)_([\d]+|mkv|mp4|mp3)(?:_(a|v))?")
    )
)
@check_owner
async def ytdl_download_callback(c_q: CallbackQuery):
    yt_code = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    choice_id = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    downtype = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    
    yt_url = BASE_YT_URL + yt_code
    media_type = "فيديو" if downtype == "v" else "مقطع صوتي"
    
    # إعلام المستخدم بأنه جاري التحميل
    await c_q.answer(f"⌔╎جـارِ جلب {media_type} من البوت ...", alert=True)
    
    bot_username = "W60yBot"
    
    # حفظ معرف الرسالة الأصلية لحذفها لاحقاً
    original_msg_id = c_q.query.msg_id
    
    try:
        # إرسال الأمر للبوت الخارجي بالشكل الصحيح: "يوت" + الرابط
        await l313l.send_message(bot_username, f"يوت {yt_url}")
        
        # ننتظر قليلاً حتى يقوم البوت بالرد
        await asyncio.sleep(8)
        
        # نبحث عن آخر رسالة من البوت تحتوي على ملف
        async for msg in l313l.iter_messages(bot_username, limit=5):
            if msg.media and msg.date:
                caption = (
                    f"<b>⌔╎الـرابـط 📎:</b> <a href='{yt_url}'>⏯️ اضغط للمشاهدة</a>\n"
                    f"<b>⌔╎نـوع الوسائـط :</b> {media_type}\n"
                    f"<b>⌔╎الصيغـه :</b> {choice_id}\n"
                    f"<b>⌔╎تم الجلـب من :</b> @{bot_username}"
                )
                
                # حذف الرسالة الأصلية (التي تحتوي على الأزرار)
                await c_q.client.delete_messages(c_q.chat_id, original_msg_id)
                
                # إرسال رسالة جديدة بالملف
                await c_q.client.send_file(
                    c_q.chat_id,
                    msg.media,
                    caption=caption,
                    parse_mode="html",
                    reply_to=original_msg_id
                )
                return
        
        # إذا لم نجد أي ملف خلال 8 ثواني، ننتظر أكثر قليلاً
        await asyncio.sleep(5)
        
        async for msg in l313l.iter_messages(bot_username, limit=3):
            if msg.media and msg.date:
                caption = (
                    f"<b>⌔╎الـرابـط 📎:</b> <a href='{yt_url}'>⏯️ اضغط للمشاهدة</a>\n"
                    f"<b>⌔╎نـوع الوسائـط :</b> {media_type}\n"
                    f"<b>⌔╎الصيغـه :</b> {choice_id}\n"
                    f"<b>⌔╎تم الجلـب من :</b> @{bot_username}"
                )
                
                # حذف الرسالة الأصلية
                await c_q.client.delete_messages(c_q.chat_id, original_msg_id)
                
                # إرسال رسالة جديدة بالملف
                await c_q.client.send_file(
                    c_q.chat_id,
                    msg.media,
                    caption=caption,
                    parse_mode="html",
                    reply_to=original_msg_id
                )
                return
        
        # إذا لم نجد أي ملف نهائياً
        # حذف الرسالة الأصلية
        await c_q.client.delete_messages(c_q.chat_id, original_msg_id)
        
        # إرسال رسالة جديدة بدون ملف
        await c_q.client.send_message(
            c_q.chat_id,
            f"<b>⌔╎عـذراً .. لم يتم العثور على الملف من البوت</b>\n\n"
            f"<b>⌔╎الرابـط المطلـوب :</b>\n<a href='{yt_url}'>⏯️ {yt_url}</a>\n\n"
            f"<b>⌔╎جـرب إرسال الأمر يدويًا :</b>\n<code>يوت {yt_url}</code>\n"
            f"<b>⌔╎للبوت :</b> @{bot_username}",
            parse_mode="html"
        )
        
    except Exception as e:
        # حذف الرسالة الأصلية في حالة الخطأ
        try:
            await c_q.client.delete_messages(c_q.chat_id, original_msg_id)
        except:
            pass
            
        # إرسال رسالة الخطأ
        await c_q.client.send_message(
            c_q.chat_id,
            f"<b>⌔╎حدث خطـأ :</b>\n<code>{str(e)}</code>\n\n"
            f"<b>⌔╎الرابـط المطلـوب :</b>\n<a href='{yt_url}'>اضغط هنا للمشاهدة</a>\n\n"
            f"<b>⌔╎جـرب إرسال الأمر يدويًا :</b>\n<code>يوت {yt_url}</code>\n"
            f"<b>⌔╎للبوت :</b> @{bot_username}",
            parse_mode="html"
        )


@l313l.tgbot.on(
    CallbackQuery(data=re.compile(b"^ytdl_(listall|back|next|detail)_([a-z0-9]+)_(.*)"))
)
@check_owner
async def ytdl_callback(c_q: CallbackQuery):
    choosen_btn = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    data_key = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    page = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    if not os.path.exists(PATH):
        return await c_q.answer(
            "عملية البحث غير دقيقة يرجى اختيار عنوان صحيح وحاول مجددا",
            alert=True,
        )
    with open(PATH) as f:
        view_data = ujson.load(f)
    search_data = view_data.get(data_key)
    total = len(search_data) if search_data is not None else 0
    if total == 0:
        return await c_q.answer(
            "يرجى البحث مرة اخرى لم يتم العثور على نتائج دقيقة", alert=True
        )
    if choosen_btn == "back":
        index = int(page) - 1
        del_back = index == 1
        await c_q.answer()
        back_vid = search_data.get(str(index))
        await c_q.edit(
            text=back_vid.get("message"),
            file=await get_ytthumb(back_vid.get("video_id")),
            buttons=yt_search_btns(
                del_back=del_back,
                data_key=data_key,
                page=index,
                vid=back_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "next":
        index = int(page) + 1
        if index > total:
            return await c_q.answer("هذا كل ما يمكنني عرضه", alert=True)
        await c_q.answer()
        front_vid = search_data.get(str(index))
        await c_q.edit(
            text=front_vid.get("message"),
            file=await get_ytthumb(front_vid.get("video_id")),
            buttons=yt_search_btns(
                data_key=data_key,
                page=index,
                vid=front_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "listall":
        await c_q.answer("العرض تغير الى :  📜  اللستة", alert=False)
        list_res = "".join(
            search_data.get(vid_s).get("list_view") for vid_s in search_data
        )

        telegraph = await post_to_telegraph(
            f"يتم عرض {total} من الفيديوهات على اليوتيوب حسب طلبك ...",
            list_res,
        )
        await c_q.edit(
            file=await get_ytthumb(search_data.get("1").get("video_id")),
            buttons=[
                (
                    Button.url(
                        "↗️  اضغط للتحميل",
                        url=telegraph,
                    )
                ),
                (
                    Button.inline(
                        "📰  عرض التفاصيل",
                        data=f"ytdl_detail_{data_key}_{page}",
                    )
                ),
            ],
        )
    else:  # Detailed
        index = 1
        await c_q.answer("تم تغيير العرض الى:  📰  التفاصيل", alert=False)
        first = search_data.get(str(index))
        await c_q.edit(
            text=first.get("message"),
            file=await get_ytthumb(first.get("video_id")),
            buttons=yt_search_btns(
                del_back=True,
                data_key=data_key,
                page=index,
                vid=first.get("video_id"),
                total=total,
            ),
            parse_mode="html",
           )
