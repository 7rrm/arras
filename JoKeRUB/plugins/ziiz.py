import os
from telethon import Button
from telethon.tl.functions.users import GetFullUserRequest

from . import l313l
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_or_reply
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

@l313l.ar_cmd(pattern="اهمس(?: |$)(.*)")
async def set_whisper_target(event):
    try:
        # الحصول على المستخدم المستهدف
        target = await event.get_reply_message() if event.reply_to_msg_id else None
        user_input = event.pattern_match.group(1)
        
        if not target and not user_input:
            return await edit_or_reply(event, "❌ يجب الرد على شخص أو كتابة اسم المستخدم")
        
        try:
            # الحصول على معلومات المستخدم
            if target:
                user_entity = await event.client.get_entity(target.sender_id)
            else:
                user_entity = await event.client.get_entity(user_input)
                
            user_id = user_entity.id
            full_name = getattr(user_entity, 'first_name', '') or getattr(user_entity, 'title', '')
            username = f"@{user_entity.username}" if user_entity.username else ""
            
            # حفظ بيانات المستهدف
            delgvar("hmsa_id")
            delgvar("hmsa_name")
            delgvar("hmsa_user")
            
            addgvar("hmsa_id", str(user_id))
            addgvar("hmsa_name", full_name)
            addgvar("hmsa_user", username)

            # إنشاء زر الهمسة
            whisper_button = [
                [Button.inline("كتابة همسة", data="write_whisper")]
            ]
            
            # إرسال الرسالة مع الزر
            await event.client.send_message(
                event.chat_id,
                f"✓ تم تعيين {full_name} {username} كمستلم للهمسات\n"
                "اضغط على الزر أدناه لكتابة الهمسة",
                buttons=whisper_button
            )
            await event.delete()
            
        except Exception as e:
            LOGS.error(f"خطأ في تعيين المستلم: {e}")
            await edit_or_reply(event, "❌ حدث خطأ أثناء تعيين المستلم")
            
    except Exception as e:
        LOGS.error(f"خطأ في أمر الهمسة: {e}")
        await edit_or_reply(event, "❌ حدث خطأ في الأمر")

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"write_whisper")))
async def whisper_button_handler(event):
    try:
        # الحصول على بيانات المستلم
        target_id = gvarstatus("hmsa_id")
        target_name = gvarstatus("hmsa_name")
        target_user = gvarstatus("hmsa_user")
        
        if not target_id:
            return await event.answer("❌ لم يتم تعيين مستلم للهمسة", alert=True)
        
        # إرسال تعليمات كتابة الهمسة
        await event.answer("⚡ جاهز لكتابة الهمسة")
        
        # يمكنك هنا إضافة منطق لفتح واجهة كتابة الهمسة
        # أو استخدام زر إنلاين كما في الكود الأصلي
        
    except Exception as e:
        LOGS.error(f"خطأ في معالجة زر الهمسة: {e}")
        await event.answer("❌ حدث خطأ أثناء معالجة الطلب", alert=True)
