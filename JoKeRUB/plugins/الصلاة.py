import json
import requests
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

@l313l.ar_cmd(
    pattern="صلاة(?: |$)(.*)",
    command=("صلاة", plugin_category),
    info={
        "header": "يعرض أوقات الصلاة لمدينة عراقية",
        "usage": "{tr}صلاة <المدينة>",
        "examples": "{tr}صلاة كربلاء",
    },
)
async def prayer_times(event):
    """أوقات الصلاة للمدن العراقية"""
    city = event.pattern_match.group(1).strip()
    
    if not city:
        city = gvarstatus("prayer_default_city") or "بغداد"
    
    if city not in IRAQ_CITIES:
        await edit_or_reply(
            event,
            f"**❌ المدينة غير مدعومة**\n"
            f"**المدن المتاحة:** {', '.join(IRAQ_CITIES.keys())}"
        )
        return
    
    english_city = IRAQ_CITIES[city]
    
    try:
        # جلب البيانات من API
        url = f"http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": english_city,
            "country": "IQ",  # العراق فقط
            "method": 2,  # طريقة الحساب
        }
        
        async with event.client._session.get(url, params=params) as response:
            if response.status != 200:
                await edit_delete(event, f"**❌ خطأ في الاتصال: {response.status}**", 10)
                return
                
            data = await response.json()
            
        # استخراج البيانات
        timings = data["data"]["timings"]
        gregorian = data["data"]["date"]["gregorian"]
        hijri = data["data"]["date"]["hijri"]
        
        # تنسيق الرسالة
        message = (
            f"<b>🕌 أوقات الصلاة في {city}</b>\n\n"
            f"<b>📅 التاريخ:</b>\n"
            f"الميلادي: {gregorian['day']} {gregorian['month']['ar']} {gregorian['year']}\n"
            f"الهجري: {hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ\n\n"
            f"<b>⏰ الأوقات:</b>\n"
            f"• <b>الفجر:</b> {timings['Fajr']}\n"
            f"• <b>الشروق:</b> {timings['Sunrise']}\n"
            f"• <b>الظهر:</b> {timings['Dhuhr']}\n"
            f"• <b>العصر:</b> {timings['Asr']}\n"
            f"• <b>المغرب:</b> {timings['Maghrib']}\n"
            f"• <b>العشاء:</b> {timings['Isha']}\n"
        )
        
        # إضافة وقت الإمساك إذا موجود
        if 'Imsak' in timings:
            message += f"• <b>الإمساك:</b> {timings['Imsak']}\n"
        
        # إضافة منتصف الليل إذا موجود
        if 'Midnight' in timings:
            message += f"• <b>منتصف الليل:</b> {timings['Midnight']}\n"
        
        message += f"\n<b>📍 الموقع:</b> {city}، العراق 🇮🇶"
        
        await edit_or_reply(event, message, parse_mode="HTML")
        
    except Exception as e:
        await edit_delete(event, f"**❌ حدث خطأ: {str(e)}**", 10)

@l313l.ar_cmd(
    pattern="مدن صلاة$",
    command=("مدن صلاة", plugin_category),
    info={
        "header": "عرض قائمة المدن العراقية المدعومة",
        "usage": "{tr}مدن صلاة",
    },
)
async def list_cities(event):
    """عرض المدن العراقية المدعومة"""
    cities_list = []
    for arabic_name, english_name in IRAQ_CITIES.items():
        cities_list.append(f"• <b>{arabic_name}</b>")
    
    message = (
        f"<b>🏙️ المدن العراقية المدعومة:</b>\n\n"
        f"{chr(10).join(cities_list)}\n\n"
        f"<b>📝 الاستخدام:</b>\n"
        f"<code>{event.pattern_match.group(1)[0]}صلاة [اسم المدينة]</code>\n\n"
        f"<b>مثال:</b>\n"
        f"<code>{event.pattern_match.group(1)[0]}صلاة كربلاء</code>\n"
        f"<code>{event.pattern_match.group(1)[0]}صلاة بغداد</code>"
    )
    
    await edit_or_reply(event, message, parse_mode="HTML")

@l313l.ar_cmd(
    pattern="تعيين مدينة صلاة(?: |$)(.*)",
    command=("تعيين مدينة صلاة", plugin_category),
    info={
        "header": "تعيين المدينة الافتراضية لأوقات الصلاة",
        "usage": "{tr}تعيين مدينة صلاة <المدينة>",
        "examples": "{tr}تعيين مدينة صلاة كربلاء",
    },
)
async def set_default_city(event):
    """تعيين المدينة الافتراضية"""
    city = event.pattern_match.group(1).strip()
    
    if not city:
        current = gvarstatus("prayer_default_city") or "غير معين"
        await edit_or_reply(
            event,
            f"<b>المدينة الافتراضية الحالية:</b> {current}\n\n"
            f"<b>لتعيين مدينة جديدة:</b>\n"
            f"<code>{event.pattern_match.group(1)[0]}تعيين مدينة صلاة [اسم المدينة]</code>",
            parse_mode="HTML"
        )
        return
    
    if city not in IRAQ_CITIES:
        await edit_or_reply(
            event,
            f"**❌ المدينة غير مدعومة**\n\n"
            f"<b>المدن المتاحة:</b>\n"
            f"{chr(10).join([f'• {c}' for c in IRAQ_CITIES.keys()])}",
            parse_mode="HTML"
        )
        return
    
    addgvar("prayer_default_city", city)
    await edit_or_reply(
        event,
        f"<b>✅ تم تعيين المدينة الافتراضية إلى:</b> {city}",
        parse_mode="HTML"
    )

@l313l.ar_cmd(
    pattern="حذف مدينة صلاة$",
    command=("حذف مدينة صلاة", plugin_category),
    info={
        "header": "حذف المدينة الافتراضية لأوقات الصلاة",
        "usage": "{tr}حذف مدينة صلاة",
    },
)
async def delete_default_city(event):
    """حذف المدينة الافتراضية"""
    if gvarstatus("prayer_default_city"):
        delgvar("prayer_default_city")
        await edit_or_reply(
            event,
            "<b>✅ تم حذف المدينة الافتراضية</b>",
            parse_mode="HTML"
        )
    else:
        await edit_or_reply(
            event,
            "<b>⚠️ لا توجد مدينة افتراضية معينة</b>",
            parse_mode="HTML"
        )

@l313l.ar_cmd(
    pattern="صلاة الان(?: |$)(.*)",
    command=("صلاة الان", plugin_category),
    info={
        "header": "عرض أوقات الصلاة الحالية مع الوقت المتبقي",
        "usage": "{tr}صلاة الان <المدينة>",
        "examples": "{tr}صلاة الان كربلاء",
    },
)
async def prayer_now(event):
    """أوقات الصلاة مع الوقت المتبقي"""
    city = event.pattern_match.group(1).strip()
    
    if not city:
        city = gvarstatus("prayer_default_city") or "بغداد"
    
    if city not in IRAQ_CITIES:
        await edit_or_reply(
            event,
            f"**❌ المدينة غير مدعومة**\n"
            f"**المدن المتاحة:** {', '.join(IRAQ_CITIES.keys())}"
        )
        return
    
    english_city = IRAQ_CITIES[city]
    
    try:
        # جلب البيانات من API
        url = f"http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": english_city,
            "country": "IQ",
            "method": 2,
        }
        
        async with event.client._session.get(url, params=params) as response:
            if response.status != 200:
                await edit_delete(event, f"**❌ خطأ في الاتصال: {response.status}**", 10)
                return
                
            data = await response.json()
        
        # استخراج البيانات
        timings = data["data"]["timings"]
        gregorian = data["data"]["date"]["gregorian"]
        hijri = data["data"]["date"]["hijri"]
        
        # الحصول على الوقت الحالي
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        # تحديد الصلاة الحالية واللاحقة
        prayer_times = [
            ("الفجر", timings['Fajr']),
            ("الشروق", timings['Sunrise']),
            ("الظهر", timings['Dhuhr']),
            ("العصر", timings['Asr']),
            ("المغرب", timings['Maghrib']),
            ("العشاء", timings['Isha']),
        ]
        
        current_prayer = None
        next_prayer = None
        time_remaining = None
        
        for i, (prayer_name, prayer_time) in enumerate(prayer_times):
            prayer_hour, prayer_minute = map(int, prayer_time.split(':'))
            
            if current_time < prayer_time:
                next_prayer = (prayer_name, prayer_time)
                if i > 0:
                    current_prayer = prayer_times[i-1]
                break
        
        # حساب الوقت المتبقي
        if next_prayer:
            next_time = datetime.strptime(next_prayer[1], "%H:%M")
            time_diff = next_time - datetime.strptime(current_time, "%H:%M")
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes = remainder // 60
            time_remaining = f"{hours} ساعة {minutes} دقيقة"
        
        # تنسيق الرسالة
        message = (
            f"<b>🕌 أوقات الصلاة في {city}</b>\n\n"
            f"<b>⏰ الوقت الحالي:</b> {current_time}\n\n"
        )
        
        if current_prayer:
            message += f"<b>🕌 الصلاة الحالية:</b> {current_prayer[0]} ({current_prayer[1]})\n"
        
        if next_prayer and time_remaining:
            message += f"<b>⏳ الصلاة القادمة:</b> {next_prayer[0]} ({next_prayer[1]})\n"
            message += f"<b>🕐 الوقت المتبقي:</b> {time_remaining}\n\n"
        
        message += (
            f"<b>📅 اليوم:</b> {gregorian['day']} {gregorian['month']['ar']} {gregorian['year']}\n"
            f"<b>📅 هجري:</b> {hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ\n\n"
            f"<b>📍 الموقع:</b> {city}، العراق 🇮🇶"
        )
        
        await edit_or_reply(event, message, parse_mode="HTML")
        
    except Exception as e:
        await edit_delete(event, f"**❌ حدث خطأ: {str(e)}**", 10)
