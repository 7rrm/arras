import json
import aiohttp
from . import l313l, edit_delete, edit_or_reply
import asyncio
from datetime import datetime, timedelta

plugin_category = "extra"

# قاعدة بيانات المدن العراقية
IRAQ_CITIES = {
    "بغداد": "Baghdad",
    "كربلاء": "Karbala", 
    "النجف": "Najaf",
    "الموصل": "Mosul",
    "البصرة": "Basrah",
    "اربيل": "Erbil",
    "كركوك": "Kirkuk",
    "ديالى": "Diyala",
    "الأنبار": "Anbar",
    "بابل": "Babil",
    "واسط": "Wasit",
    "ذي قار": "Dhi Qar",
    "ميسان": "Maysan",
    "صلاح الدين": "Salah ad Din",
    "القادسية": "Al Qadisiyah",
    "دهوك": "Dohuk",
    "السليمانية": "Sulaymaniyah"
}

# أسماء الأشهر العربية
ARABIC_MONTHS = {
    "January": "يناير",
    "February": "فبراير", 
    "March": "مارس",
    "April": "أبريل",
    "May": "مايو",
    "June": "يونيو",
    "July": "يوليو",
    "August": "أغسطس",
    "September": "سبتمبر",
    "October": "أكتوبر",
    "November": "نوفمبر",
    "December": "ديسمبر"
}

# أسماء الأيام العربية
ARABIC_DAYS = {
    "Monday": "الاثنين",
    "Tuesday": "الثلاثاء", 
    "Wednesday": "الأربعاء",
    "Thursday": "الخميس",
    "Friday": "الجمعة",
    "Saturday": "السبت",
    "Sunday": "الأحد"
}

@l313l.ar_cmd(
    pattern="صلاة(?:\s+(\S+))?$",
    command=("صلاة", plugin_category),
    info={
        "header": "يعرض أوقات الصلاة لمدينة عراقية",
        "usage": "{tr}صلاة <المدينة>",
        "examples": [
            "{tr}صلاة كربلاء",
            "{tr}صلاة بغداد",
            "{tr}صلاة النجف"
        ],
    },
)
async def prayer_times(event):
    """أوقات الصلاة للمدن العراقية"""
    # الحصول على المدينة من الأمر
    city_input = event.pattern_match.group(1)
    
    # الحصول على البادئة من الكوماند (مثل . أو !)
    cmd_prefix = event.pattern_match.group(1)[0] if event.pattern_match.group(1) else "."
    
    # إذا لم يحدد المستخدم مدينة
    if not city_input:
        await edit_or_reply(
            event,
            "**❌ يجب تحديد المدينة**\n\n"
            "**📝 الاستخدام الصحيح:**\n"
            f"`{cmd_prefix}صلاة <اسم المدينة>`\n\n"
            "**مثال:**\n"
            f"`{cmd_prefix}صلاة كربلاء`\n"
            f"`{cmd_prefix}صلاة بغداد`\n"
            f"`{cmd_prefix}صلاة النجف`"
        )
        return
    
    city = city_input.strip()
    
    # إذا كانت المدينة غير مدعومة
    if city not in IRAQ_CITIES:
        await edit_or_reply(
            event,
            f"**❌ المدينة غير مدعومة**\n\n"
            f"**🏙️ المدن المتاحة:**\n"
            f"{', '.join(IRAQ_CITIES.keys())}"
        )
        return
    
    english_city = IRAQ_CITIES[city]
    
    try:
        # استخدام aiohttp مباشرة
        url = f"https://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": english_city,
            "country": "IQ",
            "method": 2,  # طريقة أم القرى - مناسبة للعراق
        }
        
        # إنشاء جلسة جديدة
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status != 200:
                    await edit_delete(event, f"**❌ خطأ في الاتصال: {response.status}**", 10)
                    return
                    
                data = await response.json()
        
        # استخراج البيانات
        timings = data["data"]["timings"]
        gregorian = data["data"]["date"]["gregorian"]
        hijri = data["data"]["date"]["hijri"]
        
        # تعديل التاريخ الهجري (إنقاص يوم واحد)
        hijri_day = int(hijri['day'])
        hijri_month = hijri['month']['number']
        hijri_year = hijri['year']
        
        # إذا كان اليوم 1 يبقى 1، وإذا كان أكبر من 1 ينقص 1
        if hijri_day > 1:
            hijri_day = hijri_day - 1
        # ملاحظة: لا نتعامل مع حالة أول الشهر لأن API يعطي التاريخ الصحيح للسعودية
        # والعراق يتأخر بيوم واحد فقط
        
        # تنسيق التاريخ الميلادي بالعربية
        english_month = gregorian["month"]["en"]
        arabic_month = ARABIC_MONTHS.get(english_month, english_month)
        
        # الحصول على اسم اليوم بالعربية
        english_day = gregorian["weekday"]["en"]
        arabic_day = ARABIC_DAYS.get(english_day, english_day)
        
        # تنسيق الرسالة - بطريقة أبسط
        message = (
            f" <b>أوقات الصلاة في {city}</b>\n\n"
            f"📅 <b>التاريخ الميلادي:</b> {arabic_day}، {gregorian['day']} {arabic_month} {gregorian['year']}\n"
            f"📅 <b>التاريخ الهجري:</b> {hijri_day} {hijri['month']['ar']} {hijri_year} هـ\n\n"
            
            f"- <b>الفجر:</b> {timings['Fajr']}\n"
            f"- <b>الشروق:</b> {timings['Sunrise']}\n"
            f"- <b>الظهر:</b> {timings['Dhuhr']}\n"
            f"- <b>العصر:</b> {timings['Asr']}\n"
            f"- <b>المغرب:</b> {timings['Maghrib']}\n"
            f"- <b>العشاء:</b> {timings['Isha']}\n"
        )
        
        # إضافة وقت الإمساك إذا موجود
        if 'Imsak' in timings:
            message += f"- <b>الإمساك:</b> {timings['Imsak']}\n"
        
        message += f"\n📍 <b>الموقع:</b> {city}، العراق 🇮🇶"
        
        await edit_or_reply(event, message, parse_mode="HTML")
        
    except aiohttp.ClientError as e:
        await edit_delete(event, f"**❌ خطأ في الاتصال بالإنترنت: {str(e)}**", 10)
    except asyncio.TimeoutError:
        await edit_delete(event, f"**⏱️ انتهت مهلة الاتصال**", 10)
    except KeyError as e:
        await edit_delete(event, f"**⚠️ خطأ في البيانات: المفتاح {str(e)} غير موجود**", 10)
    except Exception as e:
        await edit_delete(event, f"**❌ حدث خطأ غير متوقع: {str(e)}**", 10)
