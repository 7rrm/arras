from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
import re
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_or_reply
from . import l313l

TARGET_BOT = "@e556bot"

# قائمة الخطوط (بالترتيب)
FONTS = ["Amiri", "Cairo", "Lalezar", "Ghayaty", "Shahab", "Arial"]

@l313l.ar_cmd(pattern="اختبار_خط (.*)")
async def test_font(event):
    """اختبار اختيار الخط - الأمر: .اختبار_خط Amiri"""
    font_name = event.pattern_match.group(1)
    
    if font_name not in FONTS:
        return await event.edit(f"❌ الخط غير موجود\nالخطوط المتاحة: {', '.join(FONTS)}")
    
    font_index = FONTS.index(font_name)
    
    await event.edit(f"🧪 **جاري اختبار الخط: {font_name}**\nرقم الزر: {font_index + 1}\n\n⌔︙جـار الاتصال بالبوت...")
    
    try:
        async with l313l.conversation(TARGET_BOT, timeout=45) as conv:
            # إرسال /start
            await conv.send_message("/start")
            await asyncio.sleep(2)
            
            # القائمة الرئيسية
            main_menu = await conv.get_response()
            await event.edit(f"✅ تم استلام القائمة الرئيسية\n\n🧪 **جاري الضغط على زر 'نوع الخط' (الزر الأول)...**")
            
            # الضغط على زر "نوع الخط"
            await main_menu.click(0)
            await asyncio.sleep(2)
            
            # قائمة الخطوط
            font_list = await conv.get_response()
            await event.edit(f"✅ تم استلام قائمة الخطوط\n\n🧪 **جاري الضغط على الزر رقم {font_index + 1} ({font_name})...**")
            
            # الضغط على الزر المطلوب
            btn_counter = 0
            clicked = False
            for row in font_list.buttons:
                for btn in row:
                    if btn_counter == font_index:
                        await btn.click()
                        clicked = True
                        await event.edit(f"✅ **تم الضغط على الزر {font_index + 1} ({font_name})**\n\n📝 نص الزر: {btn.text}\n📊 بيانات الزر: {btn.data}")
                        break
                    btn_counter += 1
                if clicked:
                    break
            
            if not clicked:
                await event.edit(f"❌ لم يتم العثور على الزر رقم {font_index + 1}")
                return
            
            await asyncio.sleep(2)
            
            # استقبال الرد بعد الضغط
            response = await conv.get_response()
            
            result_text = f"**✅ نتائج الاختبار:**\n\n"
            result_text += f"• **الخط المختار:** {font_name}\n"
            result_text += f"• **رقم الزر:** {font_index + 1}\n"
            result_text += f"• **تم الضغط على الزر:** ✅\n"
            result_text += f"• **رد البوت:** {response.text[:200] if response.text else 'لا يوجد رد نصي'}\n"
            
            if response.buttons:
                result_text += f"• **الأزرار في الرد:** {len(response.buttons)} صف\n"
            
            await event.edit(result_text)
            
    except asyncio.TimeoutError:
        await event.edit("❌ **انتهى الوقت - البوت لم يرد**")
    except Exception as e:
        await event.edit(f"❌ **حدث خطأ:**\n`{str(e)}`")
