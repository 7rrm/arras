import os
import random
import string
import asyncio
import re
import requests
from datetime import datetime
from PIL import Image
from telegraph import Telegraph, exceptions
from telethon.utils import get_display_name
from telethon.errors import YouBlockedUserError
from JoKeRUB import l313l
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "utils"

telegraph = Telegraph()
telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)

# ==================== أمر تلكراف نص ====================
@l313l.ar_cmd(
    pattern="تلكراف نص(?:\s|$)([\s\S]*)",
    command=("تلكراف نص", plugin_category),
    info={
        "header": "إنشاء صفحة Telegraph من نص",
        "description": "الرد على رسالة نصية لإنشاء صفحة في Telegraph",
        "usage": ["{tr}تلكراف نص <عنوان اختياري>"],
    },
)
async def telegraph_text(event):
    """إنشاء صفحة Telegraph من نص"""
    jokevent = await edit_or_reply(event, "⌔︙جـار إنشاء صفحة تلكراف نصية...")
    
    optional_title = event.pattern_match.group(1)
    
    if not event.reply_to_msg_id:
        return await jokevent.edit("`⌔︙قـم بالـرد عـلى رسالة نصية`")

    start = datetime.now()
    r_message = await event.get_reply_message()
    
    # الحصول على اسم المرسل كعنوان
    user_object = await event.client.get_entity(r_message.sender_id)
    title_of_page = get_display_name(user_object)
    
    if optional_title and optional_title.strip():
        title_of_page = optional_title.strip()
    
    # محتوى الصفحة
    page_content = r_message.message
    
    if not page_content:
        return await jokevent.edit("`⌔︙الرسالة التي رد عليها لا تحتوي على نص`")
    
    # تحويل السطور الجديدة إلى <br>
    page_content = page_content.replace("\n", "<br>")
    
    try:
        response = telegraph.create_page(title_of_page, html_content=page_content)
    except Exception as e:
        # إذا فشل بسبب عنوان مكرر أو طويل
        title_of_page = "".join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase)
            for _ in range(12)
        )
        response = telegraph.create_page(title_of_page, html_content=page_content)
    
    end = datetime.now()
    ms = (end - start).seconds
    telegraph_link = f"https://telegra.ph/{response['path']}"
    
    await jokevent.edit(
        f"**⌔︙الـرابـط :** [اضغـط هنـا]({telegraph_link})\n"
        f"**⌔︙العنوان :** `{title_of_page}`\n"
        f"**⌔︙الـوقـت :** `{ms} ثـانيـة`",
        link_preview=False,
    )


# ==================== أمر تلكراف ميديا ====================
@l313l.ar_cmd(
    pattern="تلكراف ميديا$",
    command=("تلكراف ميديا", plugin_category),
)
async def telegraph_media(event):
    """رفع الصورة إلى Telegraph عبر @vTelegraphBot بدون تحميل"""
    jokevent = await edit_or_reply(event, "⌔︙جـار رفع الصورة إلى تلكراف...")
    
    if not event.reply_to_msg_id:
        return await jokevent.edit("`⌔︙قـم بالـرد عـلى صورة`")
    
    start = datetime.now()
    r_message = await event.get_reply_message()
    
    if not r_message.photo:
        return await jokevent.edit("`⌔︙الرد يجب أن يكون على صورة`")
    
    bot_username = "@vTelegraphBot"
    
    try:
        async with event.client.conversation(bot_username, timeout=30) as conv:
            try:
                # إرسال الصورة مباشرة باستخدام photo (وليس media)
                await conv.send_message(r_message.photo)
                
                # انتظار الرد الأول (الرسالة التي فيها الزر)
                response1 = await conv.get_response()
                
                # الضغط على الزر
                if response1.buttons:
                    await response1.click(0)
                    
                    # انتظار الرد بعد الضغط (رابط Telegraph)
                    response2 = await conv.get_response()
                    
                    # استخراج رابط Telegraph
                    if response2.text and "telegra.ph" in response2.text:
                        import re
                        urls = re.findall(r'https?://telegra\.ph/\S+', response2.text)
                        if urls:
                            telegraph_link = urls[0]
                            
                            end = datetime.now()
                            ms = (end - start).seconds
                            
                            await jokevent.edit(
                                f"**⌔︙الـرابـط :** [اضغـط هنـا]({telegraph_link})\n"
                                f"**⌔︙الـوقـت :** `{ms} ثـانيـة`",
                                link_preview=False,
                            )
                            return
                    
                    await jokevent.edit(f"**⌔︙لم أجد رابطاً في رد البوت**")
                else:
                    await jokevent.edit("**⌔︙لم أجد زراً في رد البوت**")
                    
            except YouBlockedUserError:
                await jokevent.edit(f"**⌔︙قم بإلغاء حظر {bot_username} أولاً**")
                return
            except asyncio.TimeoutError:
                await jokevent.edit("**⌔︙انتهى الوقت، البوت لم يرد**")
                return
                
    except Exception as e:
        await jokevent.edit(f"**⌔︙حدث خطأ:**\n`{str(e)}`")
