import asyncio
import math
import os
import shutil
import time
import urllib3
import base64
import requests
from datetime import datetime as dt
from pytz import timezone

from PIL import Image, ImageDraw, ImageFont
from telegraph import Telegraph, exceptions, upload_file
from urlextract import URLExtract
from pySmartDL import SmartDL
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from telethon.errors import FloodWaitError
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from ..Config import Config
from ..helpers.utils import _format
from ..core.managers import edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import edit_delete, l313l, logging, BOTLOG_CHATID, mention

plugin_category = "tools"
LOGS = logging.getLogger(__name__)
CHANGE_TIME = int(gvarstatus("CHANGE_TIME")) if gvarstatus("CHANGE_TIME") else 60
FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

normzltext = "1234567890"

autopic_path = os.path.join(os.getcwd(), "JoKeRUB", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "JoKeRUB", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "JoKeRUB", "photo_pfp.png")


NAUTO = gvarstatus("Z_NAUTO") or "(الاسم تلقائي|الاسم الوقتي|اسم وقتي|اسم تلقائي)"
NAAUTO = gvarstatus("Z_NAAUTO") or "(الاسم تلقائي2|الاسم الوقتي2|اسم وقتي2|اسم تلقائي2)"
PAUTO = gvarstatus("Z_PAUTO") or "(البروفايل تلقائي|الصوره الوقتيه|الصورة الوقتية|صوره وقتيه|البروفايل)"
BAUTO = gvarstatus("Z_BAUTO") or "(البايو تلقائي|البايو الوقتي|بايو وقتي|نبذه وقتيه|النبذه الوقتيه)"
CAUTO = gvarstatus("Z_CAUTO") or "(القناة تلقائي|قناة تلقائية|قناة وقتيه)"

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            digitalpfp = gvarstatus("DIGITAL_PIC")
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        zedfont = gvarstatus("DEFAULT_PIC") if gvarstatus("DEFAULT_PIC") else "zelz/helpers/styles/Papernotes.ttf"
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        ZTZone = dt.now(timezone(TIME_ZONE))
        ZTime = ZTZone.strftime('%H:%M')
        ZT = dt.strptime(ZTime, "%H:%M").strftime("%I:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(f"{zedfont}", 35)
        drawn_text.text((140, 70), ZT, font=fnt, fill=(280, 280, 280))
        img.save(autophoto_path)
        file = await l313l.upload_file(autophoto_path)
        try:
            if i > 0:
                await l313l(
                    functions.photos.DeletePhotosRequest(
                        await l313l.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await l313l(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"

async def autoname_loop():
    while AUTONAMESTART := gvarstatus("autoname") == "true":
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        ZTZone = dt.now(timezone(TIME_ZONE))
        ZTime = ZTZone.strftime('%H:%M')
        ZT = dt.strptime(ZTime, "%H:%M").strftime("%I:%M")
        for normal in ZT:
            if normal in normzltext:
              namerzfont = gvarstatus("ZI_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬" 
              namefont = namerzfont[normzltext.index(normal)]
              ZT = ZT.replace(normal, namefont)
        ZEDT = gvarstatus("CUSTOM_ALIVE_EMZED") or " 𓏺"
        name = f"{ZT}{ZEDT}"
        LOGS.info(name)
        try:
            await l313l(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"

async def auto2name_loop():
    while AUTO2NAMESTART := gvarstatus("auto2name") == "true":
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        ZTZone = dt.now(timezone(TIME_ZONE))
        ZTime = ZTZone.strftime('%H:%M')
        ZT = dt.strptime(ZTime, "%H:%M").strftime("%I:%M")
        for normal in ZT:
            if normal in normzltext:
              namerzfont = gvarstatus("ZI_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬" 
              namefont = namerzfont[normzltext.index(normal)]
              ZT = ZT.replace(normal, namefont)
        ZEDT = gvarstatus("CUSTOM_ALIVE_EMZED") or "𓏺 "
        name = f"{ZEDT}{ZT}"
        LOGS.info(name)
        try:
            await l313l(functions.account.UpdateProfileRequest(last_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTO2NAMESTART = gvarstatus("auto2name") == "true"

async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        TIME_ZONE = gvarstatus("T_Z") if gvarstatus("T_Z") else Config.TZ
        ZTZone = dt.now(timezone(TIME_ZONE))
        ZTime = ZTZone.strftime('%H:%M')
        ZT = dt.strptime(ZTime, "%H:%M").strftime("%I:%M")
        for normal in ZT:
            if normal in normzltext:
              namerzfont = gvarstatus("ZI_FN") or "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
              namefont = namerzfont[normzltext.index(normal)]
              ZT = ZT.replace(normal, namefont)
        DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "‏{وَتَوَكَّلْ عَلَى اللَّهِ ۚ وَكَفَىٰ بِاللَّهِ وَكِيلًا}"
        bio = f"{DEFAULTUSERBIO} ⏐ {ZT}" 
        LOGS.info(bio)
        try:
            await l313l(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


async def autochannel_loop():
while gvarstatus("autochannel") == "true":
TIME_ZONE = gvarstatus("T_Z") or "Asia/Riyadh"  # اختر المنطقة الزمنية
ZTZone = dt.now(timezone(TIME_ZONE))
ZTime = ZTZone.strftime('%H:%M')
ZT = dt.strptime(ZTime, "%H:%M").strftime("%I:%M")
ZEDT = gvarstatus("CUSTOM_ALIVE_EMZED") or " 𓏺"
channel_name = f"{ZT}{ZEDT}"

try:  
        channel_id = int(gvarstatus("AUTO_CHANNEL_ID"))  
        # تغيير اسم القناة  
        await l313l(functions.channels.EditTitleRequest(  
            channel=channel_id,  
            title=channel_name  
        ))  
        LOGS.info(f"تم تحديث اسم القناة إلى: {channel_name}")  
    except Exception as e:  
        LOGS.error(f"خطأ في تحديث اسم القناة: {str(e)}")  
      
    await asyncio.sleep(CHANGE_TIME)  # تكرار كل فترة زمنية محددة



@l313l.ar_cmd(pattern=f"{PAUTO}(?:\s+(.*))?$")
async def _(event):
    input_str = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**• جـارِ تفعيـل البروفايـل الوقتـي ⅏. . .**")
    
    if input_str:
        if input_str.startswith("http"):
            addgvar("DIGITAL_PIC", input_str)
        else:
            return await zed.edit("**⎉╎يجب إدخال رابط صورة صحيح!**")
    else:
        downloaded_file_name = await event.client.download_profile_photo(
            l313l.uid,
            Config.TMP_DOWNLOAD_DIRECTORY + str(l313l.uid) + ".jpg",
            download_big=True,
        )
        
        try:
            media_urls = upload_file(downloaded_file_name)
            if isinstance(media_urls, list) and len(media_urls) > 0:
                vinfo = "https://graph.org{}".format(media_urls[0])
            elif isinstance(media_urls, str):
                vinfo = media_urls
            else:
                return await zed.edit("**⎉╎فشل في رفع الصورة!**")
                
            addgvar("DIGITAL_PIC", vinfo)
        except Exception as exc:
            await zed.edit(f"**⎉╎خطا في رفع الصورة: {str(exc)}**")
            os.remove(downloaded_file_name)
            return
        finally:
            if os.path.exists(downloaded_file_name):
                os.remove(downloaded_file_name)

    digitalpfp = gvarstatus("DIGITAL_PIC")
    if not digitalpfp:
        return await edit_delete(event, "**- فار الصـورة الوقتيـه غيـر موجـود ؟!**\n**- يمكنك إرسال رابط صورة مع الأمر أو استخدام `.اضف صورة الوقتي`**")

    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
        
    if gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. تم تفعيلهـا سابقـاً**")
        
    addgvar("digitalpic", True)
    await zed.edit("<b>⎉╎تـم بـدء البروفايـل الوقتـي🝛 .. بنجـاح ✓</b>\n<b>⎉╎زخـارف البروفايـل الوقتـي ↶ <a href = https://t.me/zzzvrr/24>⦇  اضـغـط هنــا  ⦈</a> </b>", parse_mode="html", link_preview=False)
    await digitalpicloop()

@l313l.ar_cmd(pattern=f"{NAUTO}$")
async def _(event):
    if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
        delgvar("auto2name")
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_or_reply(event, "**⎉╎الاسـم الوقتـي .. تم تفعيلـه سابقـاً**")
    zzz = await edit_or_reply(event, "**• جـارِ تفعيـل الاسـم الوقتـي ⅏. . .**")
    user = await event.client.get_me()
    DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
    if ("𝟬" not in user.first_name) or ("𝟎" not in user.first_name) or ("٠" not in user.first_name) or ("₀" not in user.first_name) or ("⁰" not in user.first_name) or ("✪" not in user.first_name) or ("⓿" not in user.first_name) or ("⊙" not in user.first_name) or ("⓪" not in user.first_name) or ("𝟢" not in user.first_name) or ("𝟶" not in user.first_name) or ("𝟘" not in user.first_name) or ("０" not in user.first_name):
        zelzalll = user.first_name if user.first_name else "-"
        await event.client(functions.account.UpdateProfileRequest(last_name=zelzalll))
    elif ("𝟬" not in DEFAULTUSER) or ("𝟎" not in DEFAULTUSER) or ("٠" not in DEFAULTUSER) or ("₀" not in DEFAULTUSER) or ("⁰" not in DEFAULTUSER) or ("✪" not in DEFAULTUSER) or ("⓿" not in DEFAULTUSER) or ("⊙" not in DEFAULTUSER) or ("⓪" not in DEFAULTUSER) or ("𝟢" not in DEFAULTUSER) or ("𝟶" not in DEFAULTUSER) or ("𝟘" not in DEFAULTUSER) or ("０" not in DEFAULTUSER):
        zelzalll = user.first_name if user.first_name else "-"
        await event.client(functions.account.UpdateProfileRequest(last_name=zelzalll))
    else:
        zelzalll = DEFAULTUSER
        await event.client(functions.account.UpdateProfileRequest(last_name=zelzalll))
    addgvar("autoname", True)
    await zzz.edit("<b>⎉╎تـم بـدء الاسـم الوقتـي🝛 .. بنجـاح ✓</b>\n<b>⎉╎زخـارف الاسـم الوقتـي ↶ <a href = https://t.me/zzzvrr/23>⦇  اضـغـط هنــا  ⦈</a> </b>", parse_mode="html", link_preview=False)
    await autoname_loop()

@l313l.ar_cmd(pattern=f"{NAAUTO}$")
async def _(event):
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        delgvar("autoname")
    if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي² .. تم تفعيلـه سابقـاً**")
    zzz = await edit_or_reply(event, "**• جـارِ تفعيـل الاسـم الوقتـي² ⅏. . .**")
    addgvar("auto2name", True)
    await zzz.edit("<b>⎉╎تـم بـدء الاسـم الوقتـي²🝛 .. بنجـاح ✓</b>\n<b>⎉╎زخـارف الاسـم الوقتـي ↶ <a href = https://t.me/zzzvrr/23>⦇  اضـغـط هنــا  ⦈</a> </b>", parse_mode="html", link_preview=False)
    await auto2name_loop()

@l313l.ar_cmd(pattern=f"{BAUTO}$")
async def _(event):
    if gvarstatus("DEFAULT_BIO") is None:
        return await edit_delete(event, "**- فار النبـذة الوقتيـه غيـر موجـود ؟!**\n**- ارسـل نـص النبـذه ثم قم بالـرد عليهـا بالامـر :**\n\n`.اضف البايو`")
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "**⎉╎النبـذه الوقتـيه .. مفعلـه سابقـاً**")
    addgvar("autobio", True)
    await edit_delete(event, "**⎉╎تـم بـدء الـنبذة الوقتيـه .. بنجـاح ✓**")
    await autobio_loop()

@l313l.ar_cmd(pattern=f"{CAUTO}$")
async def _(event):
    if gvarstatus("autochannel") == "true":
        return await edit_delete(event, "**⎉╎القناة التلقائية مفعلة بالفعل!**")
    
    if not event.is_channel:
        return await edit_delete(event, "**⎉╎يجب استخدام هذا الأمر داخل القناة المراد التحكم بها!**")
    
    try:
        chat = await event.get_chat()
        if not chat:
            return await edit_delete(event, "**⎉╎حدث خطأ في جلب معلومات القناة!**")
            
        participant = await l313l.get_permissions(event.chat_id, 'me')
        if not participant.is_admin or not participant.change_info:
            return await edit_delete(event, "**⎉╎ليس لدي صلاحية تغيير معلومات القناة!**")
            
        addgvar("AUTO_CHANNEL_ID", str(event.chat_id))
        addgvar("autochannel", "true")
        
        await edit_delete(event, "**⎉╎تم تفعيل القناة التلقائية لهذه القناة بنجاح ✓**")
        await autochannel_loop()
        
    except Exception as e:
        await edit_delete(event, f"**⎉╎حدث خطأ: {str(e)}**")

@l313l.ar_cmd(
    pattern="الغاء(?: |$)(.*)",
    command=("الغاء", plugin_category),
    info={
        "header": "لإيقاف وظائف البروفايل التلقائي",
        "description": "لإيقاف وظائف البروفايل التلقائي",
        "options": {
            "digitalpfp": "لإيقاف البروفايل التلقائي",
            "autoname": "لإيقاف الاسم التلقائي",
            "autobio": "لإيقاف البايو التلقائي",
            "autochannel": "لإيقاف القناة التلقائية"
        },
        "usage": "{tr}الغاء <option>",
        "examples": ["{tr}الغاء البروفايل"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if input_str == "البروفايل تلقائي" or input_str == "البروفايل" or input_str == "البروفايل التلقائي" or input_str == "الصوره الوقتيه" or input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف البروفـايل الوقتـي .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي" or input_str == "الاسم" or input_str == "الاسم التلقائي" or input_str == "الاسم الوقتي" or input_str == "اسم الوقتي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER, last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "البايو تلقائي" or input_str == "البايو" or input_str == "البايو التلقائي" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه" or input_str == "النبذة الوقتية" or input_str == "بايو الوقتي" or input_str == "نبذه الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @ZedThon"
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف النبـذه الوقتيـه .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎النبـذه الوقتيـه .. غيـر مفعـله اصـلاً ؟!**")
    if input_str == "القناة تلقائي" or input_str == "قناة تلقائية" or input_str == "قناة وقتيه":
        if gvarstatus("autochannel") == "true":
            delgvar("autochannel")
            delgvar("AUTO_CHANNEL_ID")
            return await edit_delete(event, "**⎉╎تم إيقاف القناة التلقائية بنجاح ✓**")
        return await edit_delete(event, "**⎉╎القناة التلقائية غير مفعلة أصلاً!**")

@l313l.ar_cmd(
    pattern="ايقاف(?: |$)(.*)",
    command=("ايقاف", plugin_category),
    info={
        "header": "لإيقاف وظائف البروفايل التلقائي",
        "description": "لإيقاف وظائف البروفايل التلقائي",
        "options": {
            "digitalpfp": "لإيقاف البروفايل التلقائي",
            "autoname": "لإيقاف الاسم التلقائي",
            "autobio": "لإيقاف البايو التلقائي",
            "autochannel": "لإيقاف القناة التلقائية"
        },
        "usage": "{tr}ايقاف <option>",
        "examples": ["{tr}ايقاف البروفايل"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if input_str == "البروفايل تلقائي" or input_str == "البروفايل" or input_str == "البروفايل التلقائي" or input_str == "الصوره الوقتيه" or input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف البروفـايل الوقتـي .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي" or input_str == "الاسم" or input_str == "الاسم التلقائي" or input_str == "الاسم الوقتي" or input_str == "اسم الوقتي" or input_str == "اسم وقتي" or input_str == "اسم تلقائي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER, last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "البايو تلقائي" or input_str == "البايو" or input_str == "البايو التلقائي" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه" or input_str == "النبذة الوقتية" or input_str == "بايو الوقتي" or input_str == "نبذه الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @ZedThon"
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف النبـذه الوقتيـه .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎النبـذه الوقتيـه .. غيـر مفعـله اصـلاً ؟!**")
    if input_str == "القناة تلقائي" or input_str == "قناة تلقائية" or input_str == "قناة وقتيه":
        if gvarstatus("autochannel") == "true":
            delgvar("autochannel")
            delgvar("AUTO_CHANNEL_ID")
            return await edit_delete(event, "**⎉╎تم إيقاف القناة التلقائية بنجاح ✓**")
        return await edit_delete(event, "**⎉╎القناة التلقائية غير مفعلة أصلاً!**")

@l313l.ar_cmd(
    pattern="انهاء(?: |$)(.*)",
    command=("انهاء", plugin_category),
    info={
        "header": "لإيقاف وظائف البروفايل التلقائي",
        "description": "لإيقاف وظائف البروفايل التلقائي",
        "options": {
            "digitalpfp": "لإيقاف البروفايل التلقائي",
            "autoname": "لإيقاف الاسم التلقائي",
            "autobio": "لإيقاف البايو التلقائي",
            "autochannel": "لإيقاف القناة التلقائية"
        },
        "usage": "{tr}انهاء <option>",
        "examples": ["{tr}انهاء البروفايل"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if input_str == "البروفايل تلقائي" or input_str == "البروفايل" or input_str == "البروفايل التلقائي" or input_str == "الصوره الوقتيه" or input_str == "الصورة الوقتية":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف البروفـايل الوقتـي .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎البروفـايل الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي" or input_str == "الاسم" or input_str == "الاسم التلقائي" or input_str == "الاسم الوقتي" or input_str == "اسم الوقتي" or input_str == "اسم وقتي" or input_str == "اسم تلقائي":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            DEFAULTUSER = gvarstatus("ALIVE_NAME") if gvarstatus("ALIVE_NAME") else Config.ALIVE_NAME
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER, last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "الاسم تلقائي2" or input_str == "الاسم التلقائي2" or input_str == "الاسم الوقتي2" or input_str == "اسم الوقتي2" or input_str == "اسم وقتي2" or input_str == "اسم تلقائي2":
        if gvarstatus("auto2name") is not None and gvarstatus("auto2name") == "true":
            delgvar("auto2name")
            await event.client(
                functions.account.UpdateProfileRequest(last_name='.')
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف الاسـم الوقتـي² .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎الاسـم الوقتـي .. غيـر مفعـل اصـلاً ؟!**")
    if input_str == "البايو تلقائي" or input_str == "البايو" or input_str == "البايو التلقائي" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه" or input_str == "النبذة الوقتية" or input_str == "بايو الوقتي" or input_str == "نبذه الوقتي":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            DEFAULTUSERBIO = gvarstatus("DEFAULT_BIO") or "الحمد الله على كل شئ - @Lx5x5"
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "**⎉╎تم إيقـاف النبـذه الوقتيـه .. بنجـاح ✓**")
        return await edit_delete(event, "**⎉╎النبـذه الوقتيـه .. غيـر مفعـله اصـلاً ؟!**")
    if input_str == "القناة تلقائي" or input_str == "قناة تلقائية" or input_str == "قناة وقتيه":
        if gvarstatus("autochannel") == "true":
            delgvar("autochannel")
            delgvar("AUTO_CHANNEL_ID")
            return await edit_delete(event, "**⎉╎تم إيقاف القناة التلقائية بنجاح ✓**")
        return await edit_delete(event, "**⎉╎القناة التلقائية غير مفعلة أصلاً!**")

l313l.loop.create_task(digitalpicloop())
l313l.loop.create_task(autoname_loop())
l313l.loop.create_task(auto2name_loop())
l313l.loop.create_task(autobio_loop())
l313l.loop.create_task(autochannel_loop())

               



# ================================================================================================ #
# =========================================الوقتيه================================================= #
# ================================================================================================ #
# Zed-Thon
# Copyright (C) 2022 Zed-Thon . All Rights Reserved
#
# This file is a part of < https://github.com/Zed-Thon/ZelZal/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Zed-Thon/ZelZal/blob/master/LICENSE/>.

""" وصـف الملـف : اوامـر تغييـر زخـارف البروفايـل والاسـم الوقـتي باللغـة العربيـة كـاملة ولا حـرف انكلـش🤘 تخمـط اذكـر المصـدر يولـد
زخـارف ممطـروقـه بـ امـر واحـد فقـط
حقـوق للتـاريخ : @ZThon
@zzzzl1l - كتـابـة الملـف :  زلــزال الهيبــه"""
#زلـزال_الهيبـه يولـد هههههههههههههههههههههههههه

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


ZelzalVP_cmd = (
    "𓆩 [ ᥲRRᥲS . - اوامـر الفـارات](t.me/lx5x5) 𓆪\n\n"
    "**✾╎قائـمه اوامـر تغييـر زخـارف البروفايـل + الاسـم الوقـتي بأمـر واحـد فقـط - حقـوق لـ التـاريـخ 🦾 :** \n\n"
    "⪼ `.وقتيه 1` / `.الوقتي 1`\n\n"
    "⪼ `.وقتيه 2` / `.الوقتي 2`\n\n"
    "⪼ `.وقتيه 3` / `.الوقتي 3`\n\n"
    "⪼ `.وقتيه 4` / `.الوقتي 4`\n\n"
    "⪼ `.وقتيه 5` / `.الوقتي 5`\n\n"
    "⪼ `.وقتيه 6` / `.الوقتي 6`\n\n"
    "⪼ `.وقتيه 7` / `.الوقتي 7`\n\n"
    "⪼ `.وقتيه 8` / `.الوقتي 8`\n\n"
    "⪼ `.وقتيه 9` / `.الوقتي 9`\n\n"
    "⪼ `.وقتيه 10` / `.الوقتي 10`\n\n"
    "⪼ `.وقتيه 11` / `.الوقتي 11`\n\n"
    "⪼ `.وقتيه 12` / `.الوقتي 12`\n\n"
    "⪼ `.وقتيه 13` / `.الوقتي 13`\n\n"
    "⪼ `.وقتيه 14` / `.الوقتي 14`\n\n"
    "⪼ `.وقتيه 15`\n\n"
    "⪼ `.وقتيه 16`\n\n"
    "⪼ `.وقتيه 17`\n\n\n"
    "**✾╎لـ رؤيـة زغـارف البروفايـل الوقتـي ↶**  [⦇  اضـغـط هنــا  ⦈](t.me/lx5x5) \n\n"
    "**✾╎لـ رؤيـة زغـارف الاســم الوقتـي ↶**  [⦇  اضـغـط هنــا  ⦈](t.me/lx5x5) \n\n"
    "\n𓆩 [𓏺 ᥲRRᥲS . آراس](t.me/lx5x5) 𓆪"
)


# Copyright (C) 2022 @Zed-Thon . All Rights Reserved
@l313l.ar_cmd(pattern="وقتيه(?: |$)(.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**✾╎جـاري اضـافة زخـرفـة الوقتيـه لـ بوتـك 💞🦾 . . .**")
    # All Rights Reserved for "@Zed-Thon" "زلـزال الهيبـه"
    if input_str == "1":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/jepthon.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "2":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Starjedi.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "3":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Papernotes.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "4":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Terserah.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "5":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Photography Signature.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "6":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Austein.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "7":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Dream MMA.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "8":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/EASPORTS15.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "9":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/KGMissKindergarten.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "10":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/212 Orion Sans PERSONAL USE.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "11":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/PEPSI_pl.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "12":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Paskowy.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "13":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Cream Cake.otf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "14":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Hello Valentina.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "15":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Alien-Encounters-Regular.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "16":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/Linebeam.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)
    elif input_str == "17":
        variable = "DEFAULT_PIC"
        zinfo = "JoKeRUB/helpers/styles/EASPORTS15.ttf"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_PIC") is None:
            await zed.edit("**✾╎تم اضـافـة زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        else:
            await zed.edit("**✾╎تم تغييـر زغـرفـة البروفـايل الوقـتي {} بنجـاح ☑️**\n\n**✾╎الان قـم بـ ارسـال الامـر ↶** `.البروفايل` **لـ بـدء البروفـايل الوقتـي . .**".format(input_str))
        addgvar(variable, zinfo)


# Copyright (C) 2022 @Zed-Thon . All Rights Reserved
@l313l.ar_cmd(pattern="الوقتي(?: |$)(.*)")
async def hhhzelzal(event):
    input_str = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**✾╎جـاري اضـافة زخـرفـة الوقتيـه لـ بوتـك 💞🦾 . . .**")
    # All Rights Reserved for "@Zed-Thon" "زلـزال الهيبـه"
    if input_str == "1":
        zinfo = "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬")
    elif input_str == "2":
        zinfo = "𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎")
    elif input_str == "3":
        zinfo = "١٢٣٤٥٦٧٨٩٠"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "١٢٣٤٥٦٧٨٩٠")
    elif input_str == "4":
        zinfo = "₁₂₃₄₅₆₇₈₉₀"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "₁₂₃₄₅₆₇₈₉₀")
    elif input_str == "5":
        zinfo = "¹²³⁴⁵⁶⁷⁸⁹⁰"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "¹²³⁴⁵⁶⁷⁸⁹⁰")
    elif input_str == "6":
        zinfo = "➊➋➌➍➎➏➐➑➒✪"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "➊➋➌➍➎➏➐➑➒✪")
    elif input_str == "7":
        zinfo = "❶❷❸❹❺❻❼❽❾⓿"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "❶❷❸❹❺❻❼❽❾⓿")
    elif input_str == "8":
        zinfo = "➀➁➂➃➄➅➆➇➈⊙"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "➀➁➂➃➄➅➆➇➈⊙")
    elif input_str == "9":
        zinfo = "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓪"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓪")
    elif input_str == "10":
        zinfo = "①②③④⑤⑥⑦⑧⑨⓪"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "①②③④⑤⑥⑦⑧⑨⓪")
    elif input_str == "11":
        zinfo = "𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢")
    elif input_str == "12":
        zinfo = "𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶")
    elif input_str == "13":
        zinfo = "𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘")
    elif input_str == "14":
        zinfo = "１２３４５６７８９０"
        await asyncio.sleep(1.5)
        if gvarstatus("ZI_FN") is not None:
            await zed.edit("**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎الان ارسـل ↶** `.الاسم تلقائي`".format(zinfo))
        else:
            await zed.edit("**✾╎تم إضـافة زغـرفة الاسـم الوقتـي .. بنجـاح✓**\n**✾╎نـوع الزخـرفـه {} **\n**✾╎ارسـل الان ↶** `.الاسم تلقائي`".format(zinfo))
        addgvar("ZI_FN", "１２３４５６７８９０")


@l313l.ar_cmd(pattern="اوامر الاسم الوقتي")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalVP_cmd)
