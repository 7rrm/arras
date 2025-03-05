import os
from datetime import datetime as dt
from asyncio import sleep

from PIL import Image, ImageDraw, ImageFont
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from JoKeRUB import l313l

from ..Config import Config
from ..core.managers import edit_or_reply
from . import reply_id

plugin_category = "utils"

# JoKeRUB timezone

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# الأوقات المميزة
SPECIAL_TIMES = [
    "12:00", "12:12", 
    "1:00", "1:01", "1:11", 
    "2:00", "2:02", "2:22", 
    "3:00", "3:03", "3:33", 
    "4:00", "4:04", "4:44", 
    "5:00", "5:05", "5:55", 
    "6:00", "6:06", 
    "7:00", "7:07", 
    "8:00", "8:08", 
    "9:00", "9:09", 
    "10:00", "10:10", 
    "11:00", "11:11"
]

async def get_tz(con):
    """Get time zone of the given country."""
    if "(Uk)" in con:
        con = con.replace("Uk", "UK")
    if "(Us)" in con:
        con = con.replace("Us", "US")
    if " Of " in con:
        con = con.replace(" Of ", " of ")
    if "(Western)" in con:
        con = con.replace("(Western)", "(western)")
    if "Minor Outlying Islands" in con:
        con = con.replace("Minor Outlying Islands", "minor outlying islands")
    if "Nl" in con:
        con = con.replace("Nl", "NL")
    for c_code in c_n:
        if con == c_n[c_code]:
            return c_tz[c_code]
    try:
        if c_n[con]:
            return c_tz[con]
    except KeyError:
        return
@l313l.ar_cmd(
    pattern="تفعيل_وقتي$",
    command=("تفعيل_وقتي", plugin_category),
    info={
        "header": "تفعيل إرسال الرسائل في الأوقات المميزة",
        "usage": "{tr}تفعيل_وقتي",
    },
)
async def activate_special_times(event):
    "تفعيل إرسال الرسائل في الأوقات المميزة"
    await edit_or_reply(event, "**تم تفعيل إرسال الرسائل في الأوقات المميزة**")
    last_sent_time = None  # لتخزين الوقت المميز الأخير الذي تم إرسال رسالة عنه
    while True:
        now = dt.now().strftime("%I:%M %p")  # الحصول على الوقت الحالي بتنسيق 12 ساعة مع AM/PM
        print(f"الوقت الحالي: {now}")  # طباعة الوقت للتحقق
        if now[:-3] in SPECIAL_TIMES and now != last_sent_time:  # التحقق من الوقت المميز وتجنب التكرار
            print(f"تم التعرف على الوقت المميز: {now}")  # طباعة للتحقق
            await event.client.send_message(
                event.chat_id,
                f"naw {now} naw",  # إرسال الوقت مع AM/PM
            )
            last_sent_time = now  # تحديث الوقت المميز الأخير
        await sleep(30)  # التحقق كل 30 ثانية لزيادة الدقة


@l313l.ar_cmd(
    pattern="توقيت(?:\s|$)([\s\S]*)(?<![0-9])(?: |$)([0-9]+)?",
    command=("توقيت", plugin_category),
    info={
        "header": "To get current time of a paticular country",
        "note": "For country names check [this link](https://telegra.ph/country-names-10-24)",
        "usage": "{tr}ctime <country name/code> <timezone number>",
        "examples": "{tr}ctime Brazil 2",
    },
)
async def time_func(tdata):
    """To get current time of a paticular country"""
    con = tdata.pattern_match.group(1).title()
    tz_num = tdata.pattern_match.group(2)
    t_form = "%I:%M"
    d_form = "%d/%m/%y - %A"
    c_name = ""
    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif Config.COUNTRY:
        c_name = Config.COUNTRY
        tz_num = Config.TZ_NUMBER
        timezones = await get_tz(Config.COUNTRY)
    else:
        return await edit_or_reply(
            tdata,
            f"᯽︙ الـساعة الآن {dt.now().strftime(t_form)}\n᯽︙ تـاريـخ اليوم{dt.now().strftime(d_form)}",
        )
    if not timezones:
        return await edit_or_reply(tdata,  "᯽︙ الـبلد غير صالح")
    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} has multiple timezones:`\n\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Choose one by typing the number "
            return_str += "in the command.`\n"
            return_str += f"`Example: .ctime {c_name} 2`"

            return await edit_or_reply(tdata, return_str)

    dtnow1 = dt.now(tz(time_zone)).strftime(t_form)
    dtnow2 = dt.now(tz(time_zone)).strftime(d_form)
    if c_name != Config.COUNTRY:
        await edit_or_reply(
            tdata,
            f"`It's`  **{dtnow1}**` on `**{dtnow2}**  `in {c_name} ({time_zone} timezone).`",
        )
    if Config.COUNTRY:
        await edit_or_reply(
            tdata,
            f"`It's`  **{dtnow1}**` on `**{dtnow2}**  `here, in {Config.COUNTRY}"
            f"({time_zone} timezone).`",
        )

@l313l.ar_cmd(
    pattern="الوقت(?:\s|$)([\s\S]*)",
    command=("الوقت", plugin_category),
    info={
        "header": "To show current time.",
        "description": "shows current default time you can change by changing TZ in heroku vars.",
        "usage": "{tr}time",
    },
)
async def _(event):
    "To show current time"
    reply_msg_id = await reply_id(event)
    current_time = dt.now().strftime(
        f"⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n⚡JoKeRUB⚡\n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n   {os.path.basename(Config.TZ)}\n  Time: %I:%M:%S \n  Date: %d.%m.%y \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
    )
    input_str = event.pattern_match.group(1)
    if input_str:
        current_time = input_str
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    required_file_name = Config.TEMP_DIR + " " + str(dt.now()) + ".webp"
    img = Image.new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await event.client.send_file(
        event.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
    )
    os.remove(required_file_name)
    await event.delete()
