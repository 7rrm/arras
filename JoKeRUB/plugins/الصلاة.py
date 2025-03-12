import json
import requests
from ..sql_helper.globals import gvarstatus
from . import l313l, edit_delete, edit_or_reply

plugin_category = "extra"

@l313l.ar_cmd(
    pattern="صلاة(?: |$)(.*)",
    command=("صلاة", plugin_category),
    info={
        "header": "يعرض أوقات الصلاة والإفطار والإمساك لمدينة معينة.",
        "note": "يمكنك تعيين المدينة الافتراضية باستخدام الأمر {tr}setcity.",
        "usage": "{tr}صلاة <المدينة>",
        "examples": "{tr}صلاة Baghdad",
    },
)
async def get_prayer_times(event):
    # جلب المدينة من الأمر
    city = event.pattern_match.group(1)
    if not city:
        city = gvarstatus("DEFCITY") or "Karbala"  # المدينة الافتراضية

    # إعداد طلب API
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {
        "city": city,
        "country": "IQ",  # يمكن تغيير الدولة حسب الحاجة
        "method": 2,  # طريقة الحساب (يمكن تغييرها حسب المذهب)
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            await edit_delete(event, f"**حدث خطأ أثناء جلب البيانات لمدينة {city}**", 5)
            return

        result = response.json()
        timings = result["data"]["timings"]
        date = result["data"]["date"]["gregorian"]

        # عرض النتائج
        output = (
            f"<b>اوقات الصلاة في {city}</b>\n\n"
            f"<b>التاريخ:</b> <i>{date['date']}</i>\n"
            f"<b>الفجر:</b> <i>{timings['Fajr']}</i>\n"
            f"<b>الشروق:</b> <i>{timings['Sunrise']}</i>\n"
            f"<b>الظهر:</b> <i>{timings['Dhuhr']}</i>\n"
            f"<b>العصر:</b> <i>{timings['Asr']}</i>\n"
            f"<b>المغرب:</b> <i>{timings['Maghrib']}</i>\n"
            f"<b>العشاء:</b> <i>{timings['Isha']}</i>\n"
            f"<b>الإمساك:</b> <i>{timings['Imsak']}</i>\n"
        )
        await edit_or_reply(event, output, parse_mode="html")

    except Exception as e:
        await edit_delete(event, f"**حدث خطأ: {str(e)}**", 5)
