# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import urllib

from telethon.tl.functions.users import GetFullUserRequest

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import deEmojify, higlighted_text
from ..helpers.tools import media_type
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, l313l, reply_id

plugin_category = "tools"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pages = {
    "Note Book": "note",
    "Raugh Book": "rough",
    "Spiral Book": "spiral",
    "White Book": "white",
    "Notepad": "notepad",
    "A4 Page": "a4",
}

Fonts = ["BrownBag", "Caveat", "HomemadeApple", "JottFLF", "WriteSong", "aras"]

Colors = [
    "black",
    "brown",
    "crimson",
    "darkblue",
    "darkcyan",
    "darkgreen",
    "darkmagenta",
    "darkred",
    "darkslateblue",
    "darkslategray",
    "darkviolet",
    "indigo",
    "magenta",
    "maroon",
    "mediumblue",
    "midnightblue",
    "navy",
    "orangered",
    "purple",
    "red",
    "teal",
]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def notebook_values(page, font):  # sourcery skip: low-code-quality
    if page == "a4":
        position = (75, 10)
        lines = 28
        if font == "BrownBag":
            text_wrap = 1.1
            font_size = 50
            linespace = "-55"
            lines = 26
        elif font == "Caveat":
            text_wrap = 0.766
            font_size = 35
            linespace = "-35"
        elif font == "HomemadeApple":
            text_wrap = 1.2
            font_size = 30
            linespace = "-62"
            lines = 26
        elif font == "JottFLF":
            text_wrap = 1.15
            font_size = 40
            linespace = "-37"
        elif font == "WriteSong":
            text_wrap = 0.6
            font_size = 30
            linespace = "-15"
        elif font == "aras":
            text_wrap = 1.0
            font_size = 45
            linespace = "-35"
    # اضبط القيم حسب تجربتك
    elif page == "spiral":
        position = (130, 10)
        lines = 26
        if font == "BrownBag":
            text_wrap = 1.2
            font_size = 55
            linespace = "-67"
        elif font == "Caveat":
            text_wrap = 0.766
            font_size = 35
            linespace = "-35"
            lines = 28
        elif font == "HomemadeApple":
            text_wrap = 1.1
            font_size = 30
            linespace = "-64"
        elif font == "JottFLF":
            text_wrap = 1.05
            font_size = 40
            linespace = "-37"
            lines = 28
        elif font == "WriteSong":
            text_wrap = 0.6
            font_size = 30
            linespace = "-15"
    elif page == "white":
        position = (130, 35)
        lines = 27
        if font == "BrownBag":
            text_wrap = 1.12
            font_size = 50
            linespace = "-58"
            lines = 26
        elif font == "Caveat":
            text_wrap = 0.77
            font_size = 35
            linespace = "-36"
        elif font == "HomemadeApple":
            text_wrap = 1.1
            font_size = 28
            linespace = "-60"
        elif font == "JottFLF":
            text_wrap = 1
            font_size = 35
            linespace = "-30"
        elif font == "WriteSong":
            text_wrap = 0.65
            font_size = 30
            linespace = "-20"
            lines = 30
    elif page == "notepad":
        position = (20, 100)
        lines = 28
        if font == "BrownBag":
            text_wrap = 1.17
            font_size = 47
            linespace = "-57"
        elif font == "Caveat":
            text_wrap = 0.85
            font_size = 33
            linespace = "-35"
        elif font == "HomemadeApple":
            text_wrap = 1.1
            font_size = 26
            linespace = "-56"
        elif font == "JottFLF":
            text_wrap = 1
            font_size = 33
            linespace = "-30"
        elif font == "WriteSong":
            text_wrap = 0.7
            font_size = 30
            linespace = "-23"
            lines = 30
            position = (20, 110)
    elif page == "note":
        position = (40, 115)
        lines = 22
        if font == "BrownBag":
            text_wrap = 1.1
            font_size = 45
            linespace = "-46"
            position = (40, 110)
        elif font == "Caveat":
            text_wrap = 0.85
            font_size = 35
            linespace = "-33"
        elif font == "HomemadeApple":
            text_wrap = 1.17
            font_size = 28
            linespace = "-57"
            position = (40, 110)
        elif font == "JottFLF":
            text_wrap = 1.1
            font_size = 36
            linespace = "-29"
        elif font == "WriteSong":
            text_wrap = 0.7
            font_size = 30
            linespace = "-14"
    elif page == "rough":
        lines = 25
        position = (70, 60)
        if font == "BrownBag":
            text_wrap = 1.1
            font_size = 45
            linespace = "-47"
            position = (70, 50)
        elif font == "Caveat":
            text_wrap = 0.9
            font_size = 35
            linespace = "-35"
        elif font == "HomemadeApple":
            text_wrap = 1.1
            font_size = 27
            linespace = "-55"
        elif font == "JottFLF":
            text_wrap = 0.95
            font_size = 33
            linespace = "-25"
        elif font == "WriteSong":
            text_wrap = 0.666
            font_size = 30
            linespace = "-16"
            position = (70, 65)
    return lines, text_wrap, font_size, linespace, position


# الأمر الأول: كتابة نص (الأمر الإنجليزي .write والأمر العربي .اكتب)
@l313l.ar_cmd(
    pattern="(write|اكتب)(?:\s|$)([\s\S]*)",
    command=("write", plugin_category),
    info={
        "header": "للكتابة في دفتر الملاحظات",
        "description": "اكتب نصاً أو رد على رسالة لتحويلها إلى صورة دفتر ملاحظات",
        "usage": [
            "{tr}write <نص> أو {tr}اكتب <نص>",
            "{tr}write -f <رد على ملف نصي>",
        ],
    },
)
async def write_page(event):
    """كتابة النص في دفتر ملاحظات"""
    cmd = event.pattern_match.group(1)
    font = gvarstatus("NOTEBOOK_FONT") or "Caveat"
    page = gvarstatus("NOTEBOOK_PAGE") or "spiral"
    log = gvarstatus("NOTEBOOK_LOG") or "Off"
    foreground = gvarstatus("NOTEBOOK_PEN_COLOR") or "black"
    if cmd == "write" or cmd == "اكتب":
        text = event.pattern_match.group(2)
        rtext = await event.get_reply_message()
        if text == "-f":
            if not rtext.media:
                return await edit_delete(event, "**⚠️ يرجى الرد على ملف نصي فقط**")
            if await media_type(rtext) == "Document":
                file_name = await rtext.download_media(Config.TEMP_DIR)
                with open(file_name, "r") as f:
                    text = f.read()
                if os.path.exists(file_name):
                    os.remove(file_name)
        if not text and rtext:
            text = rtext.message
        if not text:
            return await edit_delete(event, "**⚠️ من فضلك، قم بإدخال النص أو الرد على رسالة**")
        cap = None
    if cmd == "notebook":
        text = (
            (await l313l(GetFullUserRequest(l313l.uid))).full_user
        ).about or "هذا مجرد نص تجريبي\n              - بواسطة البوت"
        cap = f"**📒 إعدادات الدفتر:**\n\n**✍️ الخط:** `{font}`\n**📄 الصفحة:** `{list(Pages.keys())[list(Pages.values()).index(page)]}`\n**🎨 اللون:** `{foreground.title()}`\n**💾 التسجيل:** `{log}`"
    reply_to_id = await reply_id(event)
    text = deEmojify(text)
    catevent = await edit_or_reply(event, "**✍️ جاري الكتابة...**")
    temp_name = "./temp/nbpage.jpg"
    font_name = "./temp/nbfont.ttf"
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if not os.path.exists(temp_name):
        urllib.request.urlretrieve(
            f"https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Notebook/Images/{page}.jpg",
            temp_name,
        )
    if not os.path.exists(font_name):
        urllib.request.urlretrieve(
            f"https://github.com/7rrm/ArasUserbot-Resources/blob/master/Resources/Notebook/Fonts/{font}.ttf?raw=true",
            font_name,
        )
    lines, text_wrap, font_size, linespace, position = notebook_values(page, font)
    image, _ = higlighted_text(
        temp_name,
        text,
        text_wrap=text_wrap,
        font_name=font_name,
        font_size=font_size,
        linespace=linespace,
        position=position,
        foreground=foreground,
        lines=lines,
        align="left",
        transparency=0,
        album=True,
    )
    await event.client.send_file(
        event.chat_id, image, caption=cap, reply_to=reply_to_id
    )
    await catevent.delete()
    if log == "On" and cmd != "notebook" and BOTLOG_CHATID != event.chat_id:
        await event.client.send_file(
            BOTLOG_CHATID, image, caption=f"#NOTE_BOOK\n\n{cap}"
        )
    for i in image:
        os.remove(i)


# الأمر الثاني: عرض إعدادات الدفتر (الأمر الإنجليزي .notebook والأمر العربي .اعدادات)
@l313l.ar_cmd(
    pattern="notebook|اعدادات$",
    command=("notebook", plugin_category),
    info={
        "header": "لعرض إعدادات الدفتر الحالية",
        "description": "يعرض إعدادات الدفتر الحالية مثل الخط، الصفحة، اللون، التسجيل",
        "usage": "{tr}notebook أو {tr}اعدادات",
    },
)
async def notebook(event):
    """عرض إعدادات الدفتر الحالية"""
    font = gvarstatus("NOTEBOOK_FONT") or "Caveat"
    page = gvarstatus("NOTEBOOK_PAGE") or "spiral"
    log = gvarstatus("NOTEBOOK_LOG") or "Off"
    foreground = gvarstatus("NOTEBOOK_PEN_COLOR") or "black"
    cap = f"**📒 إعدادات الدفتر:**\n\n**✍️ الخط:** `{font}`\n**📄 الصفحة:** `{list(Pages.keys())[list(Pages.values()).index(page)]}`\n**🎨 اللون:** `{foreground.title()}`\n**💾 التسجيل:** `{log}`"
    await edit_or_reply(event, cap)


# الأمر الثالث: تغيير الإعدادات
# الأمر الثالث: تغيير الإعدادات (الأمر الإنجليزي nb والأمر العربي اعدادات)
@l313l.ar_cmd(
    pattern="(?:nb|اعدادات)(page|font|pen|log)(?:\s|$)([\s\S]*)",
    command=("nb", plugin_category),
    info={
        "header": "تغيير إعدادات الدفتر",
        "description": "تخصيص خط الدفتر، الصفحة، لون القلم، التسجيل",
        "flags": {
            "page": "تغيير صفحة الدفتر",
            "font": "تغيير خط الدفتر", 
            "pen": "تغيير لون القلم",
            "log": "تفعيل/إيقاف حفظ السجل",
        },
        "usage": [
            "{tr}اعدادات page <اسم الصفحة>  أو  {tr}nbpage <اسم الصفحة>",
            "{tr}اعدادات font <اسم الخط>     أو  {tr}nbfont <اسم الخط>",
            "{tr}اعدادات pen <اللون>         أو  {tr}nbpen <اللون>",
            "{tr}اعدادات log <On/Off>        أو  {tr}nblog <On/Off>",
        ],
        "examples": [
            "{tr}اعدادات page Spiral Book",
            "{tr}اعدادات font Caveat",
            "{tr}اعدادات pen red",
            "{tr}اعدادات log On",
        ],
    },
)
async def notebook_conf(event):
    """تغيير إعدادات الدفتر"""
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    
    if cmd == "page":
        cap = "**📄 صفحات الدفتر المتاحة:**\n\n"
        for i, each in enumerate(Pages.keys(), start=1):
            cap += f"**{i}.**  `{each}`\n"
        if input_str and input_str in Pages.keys():
            addgvar("NOTEBOOK_PAGE", Pages[input_str])
            if os.path.exists("temp/nbpage.jpg"):
                os.remove("temp/nbpage.jpg")
            return await edit_delete(
                event, f"**✅ تم تغيير صفحة الدفتر بنجاح إلى:** `{input_str}`", 20
            )
        temp_page = "Pages"
        
    elif cmd == "font":
        cap = "**✍️ الخطوط المتاحة:**\n\n"
        for i, each in enumerate(Fonts, start=1):
            cap += f"**{i}.**  `{each}`\n"
        if input_str and input_str in Fonts:
            addgvar("NOTEBOOK_FONT", input_str)
            if os.path.exists("temp/nbfont.ttf"):
                os.remove("temp/nbfont.ttf")
            return await edit_delete(
                event, f"**✅ تم تغيير خط الدفتر بنجاح إلى:** `{input_str}`", 20
            )
        temp_page = "Fonts"
        
    elif cmd == "pen":
        cap = "**🎨 الألوان المتاحة:**\n\n"
        for i, each in enumerate(Colors, start=1):
            cap += f"**{i}.**  `{each}`\n"
        if input_str and input_str in Colors:
            addgvar("NOTEBOOK_PEN_COLOR", input_str)
            if os.path.exists("temp/nbfont.ttf"):
                os.remove("temp/nbfont.ttf")
            return await edit_delete(
                event,
                f"**✅ تم تغيير لون قلم الدفتر بنجاح إلى:** `{input_str}`",
                20,
            )
        temp_page = "Colors"
        
    elif cmd == "log":
        if not BOTLOG:
            return await edit_delete(
                event, "⚠️ يجب عليك تعيين `PRIVATE_GROUP_BOT_API_ID` في الإعدادات أولاً.", 20
            )
        cap = "**💾 خيارات حفظ السجل:**\n\n1. `On` (تشغيل)\n2. `Off` (إيقاف)"
        if input_str and input_str in ["On", "Off"]:
            addgvar("NOTEBOOK_LOG", input_str)
            status = "تشغيل" if input_str == "On" else "إيقاف"
            return await edit_delete(
                event,
                f"**✅ تم تغيير خيار حفظ السجل بنجاح إلى:** `{status}`",
                50,
            )
        return await edit_delete(event, cap)
    
    await event.delete()
    file = f"{temp_page}.jpg"
    urllib.request.urlretrieve(
        f"https://github.com/TgCatUB/CatUserbot-Resources/raw/master/Resources/Notebook/Images/{temp_page}.jpg",
        file,
    )
    await event.client.send_file(event.chat_id, file, caption=cap, reply_to=reply_to_id)
    os.remove(file)
