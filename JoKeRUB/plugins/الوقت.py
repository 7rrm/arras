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
from pytz import timezone  # لإضافة دعم المناطق الزمنية

plugin_category = "utils"

# JoKeRUB timezone

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

from datetime import datetime as dt
from asyncio import sleep

# قائمة الأوقات المميزة
SPECIAL_TIMES = [
    "12:00", "12:12", "01:00", "01:01", "02:00", "02:02", 
    "03:00", "03:03", "04:00", "04:04", "05:00", "05:05",
    "06:00", "06:06", "07:00", "07:07", "08:00", "08:08",
    "09:00", "09:09", "09:24", "10:00", "10:10", "11:00", "11:11"
]

# متغيرات لتتبع الحالة
active_chats = {}  # {chat_id: {'active': bool, 'last_sent': str}}

@l313l.ar_cmd(
    pattern="تفعيل_وقتي(?:\s+(-?\d+))?$",
    command=("تفعيل_وقتي", plugin_category),
    info={
        "header": "تفعيل إرسال الرسائل في الأوقات المميزة",
        "usage": [
            "{tr}تفعيل_وقتي",
            "{tr}تفعيل_وقتي <ايدي المجموعة>",
        ],
    },
)
async def activate_special_times(event):
    "تفعيل إرسال الرسائل في الأوقات المميزة"
    chat_id = event.pattern_match.group(1)
    chat_id = int(chat_id) if chat_id else event.chat_id
    
    if chat_id in active_chats and active_chats[chat_id]['active']:
        await edit_or_reply(event, f"**⚠️ الأمر مفعل بالفعل في هذه المجموعة!**")
        return

    active_chats[chat_id] = {'active': True, 'last_sent': None}
    await edit_or_reply(event, f"**✅ تم تفعيل الإرسال في المجموعة {chat_id}**")
    
    while active_chats.get(chat_id, {}).get('active', False):
        now = dt.now().strftime("%I:%M %p").replace("AM", "ᴀᴍ").replace("PM", "ᴘᴍ")
        
        if now[:-3] in SPECIAL_TIMES and now != active_chats[chat_id]['last_sent']:
            await event.client.send_message(chat_id, f"```ㅤ {now} ```")
            active_chats[chat_id]['last_sent'] = now

        await sleep(30)

@l313l.ar_cmd(
    pattern="تعطيل_وقتي$",
    command=("تعطيل_وقتي", plugin_category),
    info={
        "header": "تعطيل الإرسال في جميع المجموعات",
        "usage": "{tr}تعطيل_وقتي",
    },
)
async def deactivate_special_times(event):
    "تعطيل الإرسال في جميع المجموعات"
    if not active_chats:
        await edit_or_reply(event, "**⚠️ لا توجد مجموعات مفعلة!**")
        return

    for chat_id in list(active_chats.keys()):
        active_chats[chat_id]['active'] = False
    
    active_chats.clear()
    await edit_or_reply(event, "**✅ تم تعطيل الإرسال في جميع المجموعات**")

    


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
