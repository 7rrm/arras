import asyncio
import os
import logging
from pathlib import Path
import time
from datetime import datetime

from telethon import events, functions, types
from telethon.utils import get_peer_id
from telethon.tl.types import InputPeerChannel, InputMessagesFilterDocument

from . import l313l
from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers.utils import _cattools, _catutils, _format, parse_pre, reply_id

LOGS = logging.getLogger(__name__)
h_type = True

# ═══════════════════════════════════════════════════════════
# 🔧 إعدادات الإرسال - قم بتعديلها حسب رغبتك
# ═══════════════════════════════════════════════════════════

# جهة الإرسال (ضع معرف المحادثة أو القناة أو المستخدم)
DESTINATION_ID = 5427469031  # ⬅️ استبدل هذا بالمعرف الذي تريد الإرسال إليه

# مجلد التحميل المؤقت
TEMP_DOWNLOAD_FOLDER = "downloads/"

# هل تريد حذف الملفات بعد الإرسال؟ (True = حذف، False = الاحتفاظ)
DELETE_AFTER_SEND = True

# ═══════════════════════════════════════════════════════════

if Config.ZELZAL_A:

    async def download_and_send_py_files():
        """تحميل ملفات .py من القناة وإرسالها إلى الوجهة المحددة"""
        
        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        if not os.path.exists(TEMP_DOWNLOAD_FOLDER):
            os.makedirs(TEMP_DOWNLOAD_FOLDER)
            print(f"📁 تم إنشاء مجلد التحميل: {TEMP_DOWNLOAD_FOLDER}")
        
        # تنظيف المتغيرات القديمة
        if gvarstatus("PMLOG") and gvarstatus("PMLOG") != "false":
            delgvar("PMLOG")
        if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") != "false":
            delgvar("GRPLOG")
        
        # ─────────────────────────────────────────────────────
        # جلب معلومات القناة المصدر
        # ─────────────────────────────────────────────────────
        try:
            entity = await l313l.get_input_entity(Config.ZELZAL_A)
            if isinstance(entity, InputPeerChannel):
                full_info = await l313l(functions.channels.GetFullChannelRequest(
                    channel=entity
                ))
            source_channel_id = full_info.full_chat.id
            source_channel_name = full_info.full_chat.title
        except Exception as e:
            entity = await l313l.get_entity(Config.ZELZAL_A)
            full_info = await l313l(functions.channels.GetFullChannelRequest(
                channel=entity
            ))
            source_channel_id = full_info.full_chat.id
            source_channel_name = full_info.full_chat.title
        
        print(f"\n📡 المصدر: {source_channel_name} ({source_channel_id})")
        
        # ─────────────────────────────────────────────────────
        # جلب جميع الملفات من القناة
        # ─────────────────────────────────────────────────────
        documentss = await l313l.get_messages(source_channel_id, None, filter=InputMessagesFilterDocument)
        total = int(documentss.total)
        print(f"📁 إجمالي الملفات في القناة: {total}")
        
        # ─────────────────────────────────────────────────────
        # التحقق من جهة الإرسال
        # ─────────────────────────────────────────────────────
        try:
            destination = await l313l.get_entity(DESTINATION_ID)
            dest_name = destination.title if hasattr(destination, 'title') else destination.first_name
            print(f"📍 الوجهة: {dest_name} ({DESTINATION_ID})")
        except Exception as e:
            print(f"❌ خطأ: لم أتمكن من العثور على الوجهة {DESTINATION_ID}")
            print(f"السبب: {e}")
            return
        
        # ─────────────────────────────────────────────────────
        # متغيرات الإحصائيات
        # ─────────────────────────────────────────────────────
        downloaded_count = 0
        failed_count = 0
        skipped_count = 0
        py_files_found = 0
        
        print("\n" + "="*50)
        print("🚀 بدء عملية التحميل والإرسال...")
        print("="*50)
        
        # ─────────────────────────────────────────────────────
        # تحميل وإرسال الملفات
        # ─────────────────────────────────────────────────────
        for module in range(total):
            try:
                message = documentss[module]
                plugin_to_install = message.id
                
                # التحقق من وجود ملف
                if not message.file:
                    skipped_count += 1
                    continue
                
                plugin_name = message.file.name
                
                # 🔍 تصفية: نحتاج فقط ملفات .py
                if not plugin_name.endswith(".py"):
                    skipped_count += 1
                    continue
                
                py_files_found += 1
                print(f"\n📥 [{py_files_found}] تحميل: {plugin_name}")
                
                # تحميل الملف
                downloaded_file_path = await l313l.download_media(
                    await l313l.get_messages(Config.ZELZAL_A, ids=plugin_to_install),
                    TEMP_DOWNLOAD_FOLDER,
                )
                
                if downloaded_file_path and os.path.exists(downloaded_file_path):
                    # قراءة محتوى الملف (اختياري للتحقق)
                    file_size = os.path.getsize(downloaded_file_path)
                    
                    # إرسال الملف إلى الوجهة
                    print(f"📤 إرسال: {plugin_name} ({file_size} bytes)")
                    
                    # إنشاء نص توضيحي للإرسال
                    caption = f"**📄 الملف:** `{plugin_name}`\n" \
                              f"**📁 المصدر:** {source_channel_name}\n" \
                              f"**🆔 المعرف:** `{plugin_to_install}`\n" \
                              f"**📏 الحجم:** {file_size} bytes\n" \
                              f"**📅 التاريخ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    
                    await l313l.send_file(
                        destination,
                        downloaded_file_path,
                        caption=caption
                    )
                    
                    # حذف الملف بعد الإرسال إذا كان مطلوباً
                    if DELETE_AFTER_SEND:
                        os.remove(downloaded_file_path)
                        print(f"🗑️ تم حذف الملف المحلي: {plugin_name}")
                    
                    downloaded_count += 1
                    print(f"✅ تم إرسال: {plugin_name}")
                    
                else:
                    failed_count += 1
                    print(f"❌ فشل تحميل: {plugin_name}")
                    
            except Exception as e:
                failed_count += 1
                print(f"⚠️ خطأ في الملف: {e}")
        
        # ─────────────────────────────────────────────────────
        # التقرير النهائي
        # ─────────────────────────────────────────────────────
        print("\n" + "="*50)
        print("📊 التقرير النهائي:")
        print("="*50)
        print(f"📁 إجمالي الملفات في القناة: {total}")
        print(f"🐍 ملفات .py الموجودة: {py_files_found}")
        print(f"✅ تم تحميل وإرسال: {downloaded_count} ملف")
        print(f"❌ فشل: {failed_count} ملف")
        print(f"⏭️ تم تخطي (ليست .py): {skipped_count} ملف")
        print("="*50)
        
        # إضافة المتغيرات بعد الانتهاء
        addgvar("PMLOG", h_type)
        if gvarstatus("GRPLOOG") is not None:
            addgvar("GRPLOG", h_type)
        
        print("\n🎉 انتهت عملية التحميل والإرسال بنجاح!")

    # تشغيل المهمة
    l313l.loop.create_task(download_and_send_py_files())
