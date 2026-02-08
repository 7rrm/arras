import json
import requests
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
        # استخدام aiohttp مباشرة
        url = f"http://api.aladhan.com/v1/timingsByCity"
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
        
        # إضافة منتصف الليل إذا موجود
        if 'Midnight' in timings:
            message += f"• <b>🌃 منتصف الليل:</b> <code>{timings['Midnight']}</code>\n"
        
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
        # استخدام aiohttp مباشرة
        url = f"http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": english_city,
            "country": "IQ",
            "method": 2,
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
        
        # البحث عن الصلاة الحالية والقادمة
        for i, (prayer_name, prayer_time) in enumerate(prayer_times):
            if current_time < prayer_time:
                next_prayer = (prayer_name, prayer_time)
                if i > 0:
                    current_prayer = prayer_times[i-1]
                break
        
        # إذا لم توجد صلاة قادمة (أي الوقت بعد العشاء)
        if not next_prayer:
            current_prayer = prayer_times[-1]  # العشاء
            next_prayer = prayer_times[0]      # الفجر (غداً)
        
        # حساب الوقت المتبقي
        if next_prayer:
            next_time_str = next_prayer[1]
            next_time = datetime.strptime(next_time_str, "%H:%M")
            current_time_dt = datetime.strptime(current_time, "%H:%M")
            
            # إذا كانت الصلاة القادمة في اليوم التالي (بعد منتصف الليل)
            if next_time < current_time_dt:
                next_time = datetime.strptime("23:59", "%H:%M")
                time_diff = (next_time - current_time_dt).seconds
                time_diff += 60  # إضافة دقيقة للانتقال للغد
                time_diff += (datetime.strptime(next_prayer[1], "%H:%M") - datetime.strptime("00:00", "%H:%M")).seconds
            else:
                time_diff = (next_time - current_time_dt).seconds
            
            hours, remainder = divmod(time_diff, 3600)
            minutes = remainder // 60
            
            if hours == 0:
                time_remaining = f"{minutes} دقيقة"
            elif minutes == 0:
                time_remaining = f"{hours} ساعة"
            else:
                time_remaining = f"{hours} ساعة {minutes} دقيقة"
        
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

@l313l.ar_cmd(
    pattern="صلاة (\S+)(?:\s+(\d+))?$",
    command=("صلاة", plugin_category),
    info={
        "header": "عرض أوقات الصلاة لمدينة مع طريقة حساب معينة",
        "usage": "{tr}صلاة <المدينة> [رقم الطريقة]",
        "examples": [
            "{tr}صلاة بغداد",
            "{tr}صلاة كربلاء 1",
            "{tr}صلاة النجف 2"
        ],
        "methods": "1: الأزهر، 2: أم القرى، 3: ISNA، 4: رابطة العالم الإسلامي"
    },
)
async def prayer_with_method(event):
    """أوقات الصلاة بطريقة حساب محددة"""
    args = event.pattern_match.groups()
    city = args[0].strip()
    method = args[1] if args[1] else "2"  # الافتراضي أم القرى
    
    if not city:
        city = gvarstatus("prayer_default_city") or "بغداد"
    
    if city not in IRAQ_CITIES:
        await edit_or_reply(
            event,
            f"**❌ المدينة غير مدعومة**\n"
            f"**المدن المتاحة:** {', '.join(IRAQ_CITIES.keys())}"
        )
        return
    
    # طرق الحساب وأسماؤها
    method_names = {
        "1": "جامعة الأزهر (مصر)",
        "2": "أم القرى (السعودية)",
        "3": "ISNA (أمريكا الشمالية)",
        "4": "رابطة العالم الإسلامي",
        "5": "الكويت",
        "7": "سنغافورة",
        "8": "فرنسا",
        "9": "تركيا",
        "10": "الجزائر"
    }
    
    method_name = method_names.get(method, f"الطريقة {method}")
    
    english_city = IRAQ_CITIES[city]
    
    try:
        # استخدام aiohttp مباشرة
        url = f"http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": english_city,
            "country": "IQ",
            "method": method,
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
            f"<b>🕌 أوقات الصلاة في {city}</b>\n"
            f"<b>📊 طريقة الحساب:</b> <code>{method_name}</code>\n\n"
            f"<b>📅 التاريخ:</b>\n"
            f"الميلادي: <code>{gregorian['day']} {arabic_month} {gregorian['year']}</code>\n"
            f"الهجري: <code>{hijri['day']} {hijri_month_ar} {hijri['year']} هـ</code>\n\n"
            f"<b>⏰ الأوقات:</b>\n"
            f"• <b>🌄 الفجر:</b> <code>{timings['Fajr']}</code>\n"
            f"• <b>🌅 الشروق:</b> <code>{timings['Sunrise']}</code>\n"
            f"• <b>☀️ الظهر:</b> <code>{timings['Dhuhr']}</code>\n"
            f"• <b>⛅ العصر:</b> <code>{timings['Asr']}</code>\n"
            f"• <b>🌇 المغرب:</b> <code>{timings['Maghrib']}</code>\n"
            f"• <b>🌙 العشاء:</b> <code>{timings['Isha']}</code>\n\n"
            f"<b>📍 الموقع:</b> <code>{city}، العراق 🇮🇶</code>"
        )
        
        await edit_or_reply(event, message, parse_mode="HTML")
        
    except aiohttp.ClientError as e:
        await edit_delete(event, f"**❌ خطأ في الاتصال بالإنترنت: {str(e)}**", 10)
    except asyncio.TimeoutError:
        await edit_delete(event, f"**⏱️ انتهت مهلة الاتصال**", 10)
    except KeyError as e:
        await edit_delete(event, f"**⚠️ خطأ في البيانات: {str(e)}**", 10)
    except Exception as e:
        await edit_delete(event, f"**❌ حدث خطأ: {str(e)}**", 10)
