
import os
import random
import string
import requests
from datetime import datetime
from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
from telethon.utils import get_display_name
from JoKeRUB import l313l
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "utils"

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

# --- دالة الرفع البسيطة والفعالة ---
def upload_to_cloud(file_path):
    # فقط الطريقة التي تعمل: Catbox.moe
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": f},
                timeout=20
            )
        if response.status_code == 200:
            return response.text.strip()  # يرجع رابط مباشر
    except Exception as e:
        LOGS.error(f"Upload to Catbox Failed: {e}")
    
    return None

@l313l.ar_cmd(
    pattern="(ت(ل)?ك(راف)?) ?(m|t|ميديا|نص)(?:\s|$)([\s\S]*)",
    command=("تلكراف", plugin_category),
    info={
        "header": "للحصول على روابط Telegraph",
        "description": "الرد على نص للحصول على صفحة Telegraph، أو على ميديا للحصول على رابط مباشر",
        "options": {
            "ميديا أو m": "للحصول على رابط صورة/فيديو",
            "نص أو t": "للحصول على صفحة نصية في Telegraph",
        },
        "usage": [
            "{tr}تلكراف ميديا",
            "{tr}تلكراف نص <عنوان اختياري>",
        ],
    },
)
async def _(event):
    "للحصول على روابط Telegraph"
    jokevent = await edit_or_reply(event, "⌔︙جـار انشـاء رابـط تلكـراف .")
    optional_title = event.pattern_match.group(5)
    
    if not event.reply_to_msg_id:
        return await jokevent.edit("` ⌔︙قـم بالـرد عـلى رسالة`")

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()
    
    if input_str in ["ميديا", "m"]:
        # --- تلكراف ميديا ---
        if not r_message.media:
            return await jokevent.edit("` ⌔︙الرد يجب أن يكون على صورة أو فيديو.`")

        downloaded_file_name = await event.client.download_media(
            r_message, Config.TEMP_DIR
        )
        await jokevent.edit(f"`⌔︙تـم التحـميل...`")
        
        if downloaded_file_name.endswith(".webp"):
            resize_image(downloaded_file_name)
        
        media_url = upload_to_cloud(downloaded_file_name)
        
        if media_url:
            end = datetime.now()
            ms = (end - start).seconds
            await jokevent.edit(
                f"** ⌔︙الـرابـط : **[إضـغط هنـا]({media_url})\n"
                f"** ⌔︙الرابط الخام : ** `{media_url}`\n"
                f"** ⌔︙الوقـت : **`{ms} ثـانيـة.`",
                link_preview=False,
            )
        else:
            await jokevent.edit("** ⌔︙فشل الرفع!**\nجرب مرة أخرى.")
        
        # تنظيف الملف المؤقت
        if os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)
            
    elif input_str in ["نص", "t"]:
        # --- تلكراف نص ---
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        
        if optional_title:
            title_of_page = optional_title
            
        page_content = r_message.message
        
        if r_message.media:
            if page_content != "":
                title_of_page = page_content if len(page_content) < 100 else title_of_page
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8", errors="ignore") + "\n"
            os.remove(downloaded_file_name)
            
        page_content = page_content.replace("\n", "<br>")
        
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
        except Exception as e:
            LOGS.info(f"Telegraph text error: {e}")
            title_of_page = "".join(
                random.choice(string.ascii_lowercase + string.ascii_uppercase)
                for _ in range(12)
            )
            response = telegraph.create_page(title_of_page, html_content=page_content)
            
        end = datetime.now()
        ms = (end - start).seconds
        joker = f"https://telegra.ph/{response['path']}"
        
        await jokevent.edit(
            f"** ⌔︙الـرابـط : ** [اضغـط هنـا]({joker})\n"
            f"** ⌔︙العنوان : ** `{title_of_page}`\n"
            f"** ⌔︙الـوقـت : **`{ms} ثـانيـة.`",
            link_preview=False,
        )
