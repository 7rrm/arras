import json
import aiohttp
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from . import l313l, edit_delete, edit_or_reply
import asyncio
from datetime import datetime

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

# الأشهر الهجرية
HIJRI_MONTHS = {
    "1": "محرم",
    "2": "صفر",
    "3": "ربيع الأول",
    "4": "ربيع الثاني",
    "5": "جمادى الأولى",
    "6": "جمادى الآخرة",
    "7": "رجب",
    "8": "شعبان",
    "9": "رمضان",
    "10": "شوال",
    "11": "ذو القعدة",
    "12": "ذو الحجة"
}

@l313l.ar_cmd(
    pattern="صلاة(?:\s+(\S+))?$",
    command=("صلاة", plugin_category),
    info={
        "header": "يعرض أوقات الصلاة لمدينة عراقية",
        "usage": "{tr}صلاة [المدينة]\n{tr}صلاة كربلاء\n{tr}صلاة بغداد",
        "examples": [
            "{tr}صلاة - عرض المدينة الافتراضية",
            "{tr}صلاة كربلاء",
            "{tr}صلاة بغداد",
            "{tr}صلاة النجف"
        ],
    },
)
async def prayer_times(event):
    """أوقات الصلاة للمدن العراقية"""
    city = event.pattern_match.group(1)
    
    if not city:
        city = gvarstatus("prayer_default_city") or "بغداد"
    else:
        city = city.strip()
    
    if city not in IRAQ_CITIES:
        await edit_or_reply(
            event,
            f"**❌ المدينة غير مدعومة**\n\n"
            f"**🏙️ المدن المتاحة:**\n"
            f"{', '.join(IRAQ_CITIES.keys())}\n\n"
            f"**📝 الاستخدام:**\n"
            f"`{event.pattern_match.group(1)[0]}صلاة [اسم المدينة]`\n\n"
            f"**مثال:**\n"
            f"`{event.pattern_match.group(1)[0]}صلاة كربلاء`"
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
        
        # تحويل اسم الشهر الميلادي للعربية
        english_month = gregorian["month"]["en"]
        arabic_month = ARABIC_MONTHS.get(english_month, english_month)
        
        # تحويل اسم الشهر الهجري
        hijri_month_num = hijri["month"]["number"]
        hijri_month_ar = HIJRI_MONTHS.get(hijri_month_num, hijri["month"]["en"])
        
        # تنسيق الرسالة
        message = (
            f"<b>🕌 أوقات الصلاة في {city}</b>\n\n"
            f"<b>📅 التاريخ:</b>\n"
            f"الميلادي: <code>{gregorian['day']} {arabic_month} {gregorian['year']}</code>\n"
            f"الهجري: <code>{hijri['day']} {hijri_month_ar} {hijri['year']} هـ</code>\n\n"
            f"<b>⏰ الأوقات:</b>\n"
            f"• <b>🌄 الفجر:</b> <code>{timings['Fajr']}</code>\n"
            f"• <b>🌅 الشروق:</b> <code>{timings['Sunrise']}</code>\n"
            f"• <b>☀️ الظهر:</b> <code>{timings['Dhuhr']}</code>\n"
            f"• <b>⛅ العصر:</b> <code>{timings['Asr']}</code>\n"
            f"• <b>🌇 المغرب:</b> <code>{timings['Maghrib']}</code>\n"
            f"• <b>🌙 العشاء:</b> <code>{timings['Isha']}</code>\n"
        )
        
        # إضافة وقت الإمساك إذا موجود
        if 'Imsak' in timings:
            message += f"• <b>🕋 الإمساك:</b> <code>{timings['Imsak']}</code>\n"
        
        message += f"\n<b>📍 الموقع:</b> <code>{city}، العراق 🇮🇶</code>"
        
        await edit_or_reply(event, message, parse_mode="HTML")
        
    except aiohttp.ClientError as e:
        await edit_delete(event, f"**❌ خطأ في الاتصال بالإنترنت: {str(e)}**", 10)
    except asyncio.TimeoutError:
        await edit_delete(event, f"**⏱️ انتهت مهلة الاتصال بمدينة {city}**", 10)
    except KeyError as e:
        await edit_delete(event, f"**⚠️ خطأ في البيانات: المفتاح {str(e)} غير موجود**", 10)
    except Exception as e:
        await edit_delete(event, f"**❌ حدث خطأ غير متوقع: {str(e)}**", 10)

                    
        # تنسيق الرسالة
        message = (
            f"<b>🕌 أوقات الصلاة في {city}</b>\n\n"
            f"<b>⏰ الوقت الحالي:</b> <code>{current_time}</code>\n\n"
        )
        
        if current_prayer:
            message += f"<b>🕌 الصلاة الحالية:</b> <code>{current_prayer[0]} ({current_prayer[1]})</code>\n"
        
        if next_prayer and time_remaining:
            message += f"<b>⏳ الصلاة القادمة:</b> <code>{next_prayer[0]} ({next_prayer[1]})</code>\n"
            message += f"<b>🕐 الوقت المتبقي:</b> <code>{time_remaining}</code>\n\n"
        
        message += (
            f"<b>📅 اليوم:</b> <code>{gregorian['day']} {arabic_month} {gregorian['year']}</code>\n"
            f"<b>📅 هجري:</b> <code>{hijri['day']} {hijri_month_ar} {hijri['year']} هـ</code>\n\n"
            f"<b>📍 الموقع:</b> <code>{city}، العراق 🇮🇶</code>"
        )
        
        await edit_or_reply(event, message, parse_mode="HTML")
        
    except aiohttp.ClientError as e:
        await edit_delete(event, f"**❌ خطأ في الاتصال بالإنترنت: {str(e)}**", 10)
    except asyncio.TimeoutError:
        await edit_delete(event, f"**⏱️ انتهت مهلة الاتصال بمدينة {city}**", 10)
    except KeyError as e:
        await edit_delete(event, f"**⚠️ خطأ في البيانات: المفتاح {str(e)} غير موجود**", 10)
    except Exception as e:
        await edit_delete(event, f"**❌ حدث خطأ غير متوقع: {str(e)}**", 10)
