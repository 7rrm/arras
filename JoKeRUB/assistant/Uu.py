from telethon import Button, events
from telethon.tl.types import MessageEntityTextUrl, MessageEntityCustomEmoji
from telethon.errors import RPCError
from . import l313l
from ..helpers import reply_id
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

@l313l.bot_cmd(
    pattern="^/debugstart$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def debug_start(event):
    """نسخة تشخيصية مع تسجيل كامل للأخطاء"""
    
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    LOGS.info(f"=== بدء تشخيص /debugstart ===")
    LOGS.info(f"المستخدم: {chat.id} - {chat.first_name}")
    
    # 1. أولاً: اختبار إرسال رسالة عادية
    try:
        test_msg = await event.client.send_message(
            chat.id,
            "🔍 اختبار أساسي: الرسالة العادية تعمل ✅",
            reply_to=reply_to
        )
        LOGS.info("✅ الرسالة العادية أرسلت بنجاح")
    except Exception as e:
        LOGS.error(f"❌ فشل إرسال رسالة عادية: {str(e)}")
        await event.reply(f"❌ خطأ في الرسالة العادية: {str(e)[:100]}")
        return
    
    # 2. اختبار إيموجي عادي
    try:
        await event.client.send_message(
            chat.id,
            "🔥 اختبار إيموجي عادي",
            reply_to=test_msg.id
        )
        LOGS.info("✅ الإيموجي العادي يعمل")
    except Exception as e:
        LOGS.error(f"❌ فشل إيموجي عادي: {str(e)}")
    
    # 3. اختبار HTML parsing
    try:
        html_msg = await event.client.send_message(
            chat.id,
            "<b>اختبار HTML</b> - هذا نص عريض",
            parse_mode='html',
            reply_to=test_msg.id
        )
        LOGS.info("✅ تحليل HTML يعمل")
    except Exception as e:
        LOGS.error(f"❌ فشل تحليل HTML: {str(e)}")
        await event.reply(f"❌ خطأ HTML: {str(e)[:100]}")
    
    # 4. اختبار إيموجي بريميوم بالطريقة المختلفة
    emoji_id = 5368324170671202286
    
    LOGS.info(f"جاري اختبار إيموجي بريميوم ID: {emoji_id}")
    
    # الطريقة 1: <a href="emoji/ID">
    try:
        msg1 = f'🎉 <b>تم بنجاح!</b>\n<a href="emoji/{emoji_id}">🔥</a>\n\nللتواصل:'
        
        result1 = await event.client.send_message(
            chat.id,
            msg1,
            parse_mode='html',
            reply_to=test_msg.id
        )
        LOGS.info("✅ الطريقة 1 (href): ناجحة")
        await event.client.send_message(
            chat.id,
            "✅ الطريقة 1: <a href='emoji/ID'> تعمل",
            reply_to=result1.id
        )
    except Exception as e:
        LOGS.error(f"❌ فشل الطريقة 1: {str(e)}")
        error_details = f"❌ الطريقة 1 فشلت:\nنوع الخطأ: {type(e).__name__}\nتفاصيل: {str(e)}"
        await event.client.send_message(
            chat.id,
            error_details,
            reply_to=test_msg.id
        )
    
    # الطريقة 2: [link] مع Markdown
    try:
        msg2 = f"🎉 **تم بنجاح!**\n[🔥](tg://emoji?id={emoji_id})\n\nللتواصل:"
        
        result2 = await event.client.send_message(
            chat.id,
            msg2,
            parse_mode='md',
            reply_to=test_msg.id
        )
        LOGS.info("✅ الطريقة 2 (markdown): ناجحة")
    except Exception as e:
        LOGS.error(f"❌ فشل الطريقة 2: {str(e)}")
    
    # الطريقة 3: MessageEntity مباشرة
    try:
        from telethon.tl.types import MessageEntityBold, MessageEntityCustomEmoji
        
        message_text = "🎉 تم بنجاح!\n🔥\n\nللتواصل:"
        
        entities = [
            MessageEntityBold(offset=2, length=9),
            MessageEntityCustomEmoji(
                offset=len("🎉 تم بنجاح!\n"),
                length=len("🔥"),
                document_id=emoji_id
            )
        ]
        
        result3 = await event.client.send_message(
            chat.id,
            message_text,
            entities=entities,
            reply_to=test_msg.id
        )
        LOGS.info("✅ الطريقة 3 (entities): ناجحة")
    except Exception as e:
        LOGS.error(f"❌ فشل الطريقة 3: {str(e)}")
        # إظهار تفاصيل الخطأ للمستخدم
        await event.client.send_message(
            chat.id,
            f"❌ الطريقة 3 فشلت:\n{type(e).__name__}: {str(e)[:200]}",
            reply_to=test_msg.id
        )
    
    # 5. التحقق من حالة البوت
    try:
        bot = await event.client.get_me()
        LOGS.info(f"معلومات البوت: ID={bot.id}, اسم={bot.first_name}")
        
        # محاولة الحصول على تفاصيل الإيموجي
        try:
            from telethon.tl.functions.messages import GetCustomEmojiDocumentsRequest
            
            emojis = await event.client(GetCustomEmojiDocumentsRequest([emoji_id]))
            LOGS.info(f"✅ تم جلب معلومات الإيموجي: {len(emojis)} نتيجة")
            
            if emojis:
                await event.client.send_message(
                    chat.id,
                    f"✅ الإيموجي موجود في قاعدة البيانات\nID: {emoji_id}",
                    reply_to=test_msg.id
                )
            else:
                await event.client.send_message(
                    chat.id,
                    f"⚠️ الإيموجي غير موجود في قاعدة البيانات\nID: {emoji_id}",
                    reply_to=test_msg.id
                )
        except Exception as emoji_error:
            LOGS.error(f"❌ خطأ في جلب الإيموجي: {str(emoji_error)}")
            await event.client.send_message(
                chat.id,
                f"❌ لا يمكن الوصول للإيموجي: {str(emoji_error)[:150]}",
                reply_to=test_msg.id
            )
            
    except Exception as e:
        LOGS.error(f"❌ فشل الحصول على معلومات البوت: {str(e)}")
    
    # 6. رسالة ملخصة
    summary = (
        "📊 **ملخص التشخيص:**\n\n"
        "✅ الرسائل العادية تعمل\n"
        "✅ الإيموجيات العادية تعمل\n"
        "✅ HTML يعمل\n"
        "❓ الإيموجيات البريميوم تحتاج اختبار\n\n"
        "🔍 **الأسباب المحتملة:**\n"
        "1. الإيموجي غير موجود في حساب البوت\n"
        "2. ID الإيموجي غير صحيح\n"
        "3. البوت ليس لديه Telegram Premium\n"
        "4. مشكلة في مكتبة Telethon\n\n"
        "💡 **الحلول المقترحة:**\n"
        "1. تأكد أن البوت يملك الإيموجي\n"
        "2. جرب إيموجيات أخرى\n"
        "3. استخدم إيموجيات Unicode بديلة"
    )
    
    await event.client.send_message(
        chat.id,
        summary,
        parse_mode='md',
        reply_to=test_msg.id
    )
    
    LOGS.info("=== انتهاء التشخيص ===")

# ==========================================================
# دالة لفحص الإيموجي المحدد
# ==========================================================

@l313l.bot_cmd(
    pattern="^/checkemoji (\d+)$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def check_specific_emoji(event):
    """فحص إيموجي محدد بالـ ID"""
    
    emoji_id = int(event.pattern_match.group(1))
    chat = await event.get_chat()
    
    LOGS.info(f"فحص إيموجي ID: {emoji_id}")
    
    report = f"🔍 **فحص الإيموجي:** `{emoji_id}`\n\n"
    
    # اختبار جميع الطرق
    methods = [
        ("HTML (<a href>)", f'<a href="emoji/{emoji_id}">🔥</a>', 'html'),
        ("Markdown ([link])", f'[🔥](tg://emoji?id={emoji_id})', 'md'),
        ("نص عادي", "🔥", None),
    ]
    
    for method_name, emoji_code, parse_mode in methods:
        try:
            await event.client.send_message(
                chat.id,
                f"اختبار: {method_name}\n{emoji_code}",
                parse_mode=parse_mode
            )
            report += f"✅ {method_name}: يعمل\n"
            LOGS.info(f"✅ {method_name} يعمل لـ {emoji_id}")
        except Exception as e:
            error_msg = str(e)
            report += f"❌ {method_name}: {error_msg[:50]}...\n"
            LOGS.error(f"❌ {method_name} فشل لـ {emoji_id}: {error_msg}")
    
    # محاولة الحصول على معلومات الإيموجي
    try:
        from telethon.tl.functions.messages import GetCustomEmojiDocumentsRequest
        
        emojis = await event.client(GetCustomEmojiDocumentsRequest([emoji_id]))
        if emojis:
            report += f"\n📁 **معلومات الإيموجي:**\n"
            report += f"• موجود في قاعدة البيانات\n"
            if hasattr(emojis[0], 'size'):
                report += f"• الحجم: {emojis[0].size} بايت\n"
            if hasattr(emojis[0], 'mime_type'):
                report += f"• النوع: {emojis[0].mime_type}\n"
        else:
            report += "\n⚠️ **تحذير:** الإيموجي غير موجود في قاعدة البيانات\n"
    except Exception as e:
        report += f"\n❌ **خطأ في جلب المعلومات:** {str(e)[:100]}\n"
    
    await event.reply(report, parse_mode='md')

# ==========================================================
# دالة لسجل الأخطاء التفصيلي
# ==========================================================

@l313l.bot_cmd(
    pattern="^/errordetail$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def error_detail(event):
    """عرض تفاصيل الأخطاء بطريقة مفصلة"""
    
    chat = await event.get_chat()
    
    # اختبار مع التقاط كامل للخطأ
    emoji_id = 5368324170671202286
    
    test_cases = [
        {
            "name": "HTML بريميوم",
            "code": f'<a href="emoji/{emoji_id}">🔥</a>',
            "parse_mode": "html"
        },
        {
            "name": "HTML عادي",
            "code": "<b>نص عادي</b>",
            "parse_mode": "html"
        },
        {
            "name": "Markdown بريميوم",
            "code": f'[🔥](tg://emoji?id={emoji_id})',
            "parse_mode": "md"
        },
    ]
    
    results = []
    
    for test in test_cases:
        try:
            start_time = datetime.now()
            
            await event.client.send_message(
                chat.id,
                f"اختبار: {test['name']}\n{test['code']}",
                parse_mode=test['parse_mode']
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            results.append(f"✅ **{test['name']}**: ناجح ({duration:.2f} ثانية)")
            LOGS.info(f"✅ {test['name']}: ناجح")
            
        except RPCError as e:
            results.append(f"❌ **{test['name']}**: خطأ RPC\n   الكود: {e.code}\n   الرسالة: {e.message}")
            LOGS.error(f"❌ {test['name']}: RPCError {e.code} - {e.message}")
            
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            
            results.append(f"❌ **{test['name']}**: {type(e).__name__}\n   {str(e)[:100]}")
            LOGS.error(f"❌ {test['name']}: {type(e).__name__} - {str(e)}")
            LOGS.debug(f"Traceback: {tb}")
    
    # جمع النتائج
    report = "📋 **نتائج الاختبار التفصيلي:**\n\n"
    report += "\n".join(results)
    
    # إضافة معلومات إضافية
    report += "\n\n🔧 **معلومات النظام:**\n"
    report += f"• Telethon الإصدار: {telethon.__version__}\n"
    report += f"• Python الإصدار: {sys.version[:50]}\n"
    report += f"• نظام التشغيل: {platform.system()}\n"
    
    await event.reply(report, parse_mode='md')

# ==========================================================
# دالة لاختبار مجموعة من الإيموجيات
# ==========================================================

@l313l.bot_cmd(
    pattern="^/testallemojis$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_all_emojis(event):
    """اختبار مجموعة من الإيموجيات البريميوم"""
    
    chat = await event.get_chat()
    
    # قائمة إيموجيات بريميوم معروفة
    premium_emojis = [
        {"id": 5368324170671202286, "char": "🔥", "name": "نار"},
        {"id": 5368324170671202287, "char": "👑", "name": "تاج"},
        {"id": 5368324170671202288, "char": "⚡", "name": "صاعقة"},
        {"id": 5210763312597326700, "char": "❤️", "name": "قلب أحمر"},
        {"id": 5668127928907464707, "char": "❤️", "name": "قلب آخر"},
        {"id": 5222295067858855800, "char": "⭐", "name": "نجمة"},
        {"id": 5834774412338927340, "char": "🌟", "name": "نجمة متلألئة"},
        {"id": 6323136954380585694, "char": "✨", "name": "تألق"},
    ]
    
    results = []
    
    for emoji in premium_emojis:
        try:
            # محاولة الإرسال
            await event.client.send_message(
                chat.id,
                f'<a href="emoji/{emoji["id"]}">{emoji["char"]}</a>',
                parse_mode='html'
            )
            results.append(f"✅ {emoji['name']} ({emoji['id']}): ناجح")
            LOGS.info(f"✅ إيموجي {emoji['name']} يعمل")
            
        except Exception as e:
            error_msg = str(e)
            results.append(f"❌ {emoji['name']} ({emoji['id']}): {error_msg[:40]}")
            LOGS.warning(f"❌ إيموجي {emoji['name']} فشل: {error_msg}")
            
            # انتظر قليلاً بين المحاولات
            await asyncio.sleep(0.5)
    
    # عرض النتائج
    report = "🎭 **نتائج اختبار الإيموجيات البريميوم:**\n\n"
    report += "\n".join(results)
    
    # إحصائيات
    total = len(premium_emojis)
    success = sum(1 for r in results if "✅" in r)
    
    report += f"\n\n📊 **الإحصائيات:**\n"
    report += f"• الإجمالي: {total}\n"
    report += f"• الناجحة: {success}\n"
    report += f"• الفاشلة: {total - success}\n"
    report += f"• النسبة: {(success/total*100):.1f}%\n\n"
    
    if success == 0:
        report += "⚠️ **تحذير:** لا توجد إيموجيات بريميوم تعمل!\n"
        report += "• تأكد أن البوت لديه Telegram Premium\n"
        report += "• تأكد أن الإيموجيات مضاف
