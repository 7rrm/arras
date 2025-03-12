import json
import requests
from ..sql_helper.globals import gvarstatus
from . import l313l, edit_delete, edit_or_reply

plugin_category = "extra"

# قاموس لتحويل أسماء المدن من العربية إلى الإنجليزية
city_translations = {
    "كربلاء": "Karbala",
    "بغداد": "Baghdad",
    "النجف": "Najaf",
    # يمكنك إضافة المزيد من المدن هنا
}

@l313l.ar_cmd(
    pattern="صلاة(?: |$)(.*)",
    command=("صلاة", plugin_category),
    info={
        "header": "يعرض أوقات الصلاة والإفطار والإمساك لمدينة معينة.",
        "note": "يمكنك تعيين المدينة الافتراضية باستخدام الأمر {tr}setcity.",
        "usage": "{tr}صلاة <المدينة>",
        "examples": "{tr}صلاة كربلاء",
    },
)
async def get_prayer_times(event):
    # جلب المدينة من الأمر
    city_arabic = event.pattern_match.group(1).strip()
    if not city_arabic:
        city_arabic = gvarstatus("DEFCITY") or "بغداد"  # المدينة الافتراضية

    # تحويل اسم المدينة من العربية إلى الإنجليزية
    city = city_translations.get(city_arabic, city_arabic)

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
            await edit_delete(event, f"**حدث خطأ أثناء جلب البيانات لمدينة {city_arabic}**", 5)
            return

        result = response.json()
        timings = result["data"]["timings"]
        date = result["data"]["date"]["gregorian"]

        # عرض النتائج باللغة العربية
        output = (
            f"<b>⏰ أوقات الصلاة في {city_arabic}</b>\n\n"
            f"<b>📅 التاريخ:</b> <i>{date['date']}</i>\n\n"
            f"<b>🌄 الفجر:</b> <i>{timings['Fajr']}</i>\n"
            f"<b>🌅 الشروق:</b> <i>{timings['Sunrise']}</i>\n"
            f"<b>☀️ الظهر:</b> <i>{timings['Dhuhr']}</i>\n"
            f"<b>🌤️ العصر:</b> <i>{timings['Asr']}</i>\n"
            f"<b>🌥️ المغرب (الإفطار):</b> <i>{timings['Maghrib']}</i>\n"
            f"<b>🌙 العشاء:</b> <i>{timings['Isha']}</i>\n"
            f"<b>⛅ الإمساك:</b> <i>{timings['Imsak']}</i>\n"
        )
        await edit_or_reply(event, output, parse_mode="html")

    except Exception as e:
        await edit_delete(event, f"**حدث خطأ: {str(e)}**", 5)
