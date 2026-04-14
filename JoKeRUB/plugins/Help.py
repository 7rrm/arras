
import re
from telethon import Button, events
from telethon.events import CallbackQuery
import json
import requests
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = '''**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**
**🛂┊في قائمـة المسـاعـده والشـروحـات
🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**

[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)

'''

# إيموجي بريميوم
EMOJI_AWAMER = "5667948420749328402"   # قبل كل امر
EMOJI_OWNER = "5046707123942066452"    # عند اسم المطور
EMOJI_HEART = "5220157149103023925"    # قلب

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        query = event.text
        
        if query.startswith("مساعدة"):
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "‹ : أوامـر البحـث والتحميل : ›",
                            "callback_data": "main_menu",
                            "style": "danger"
                        }
                    ],
                    [
                        {
                            "text": "‹ : السـورس : ›",
                            "callback_data": "source_menu",
                            "style": "primary"
                        },
                        {
                            "text": "‹ : الحـساب : ›",
                            "callback_data": "account_menu",
                            "style": "primary"
                        }
                    ]
                ]
            }
            
            url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/answerInlineQuery"
            inline_data = {
                "inline_query_id": event.id,
                "results": json.dumps([
                    {
                        "type": "article",
                        "id": "help_menu_1",
                        "title": "📚 قائمة المساعدة - آراس",
                        "description": "اضغط لعرض الأوامر",
                        "input_message_content": {
                            "message_text": HELP,
                            "parse_mode": "Markdown",
                            "disable_web_page_preview": True
                        },
                        "reply_markup": keyboard
                    }
                ]),
                "cache_time": 0,
                "is_personal": True
            }
            
            try:
                requests.post(url, json=inline_data)
            except Exception as e:
                print(f"❌ خطأ: {e}")

@l313l.ar_cmd(pattern="مساعدة$")
async def help(event):
    if event.reply_to_msg_id:
        await event.get_reply_message()

    try:
        await event.get_sender()
        await event.get_chat()
    except Exception as e:
        print(f"تم التحميل: {e}")

    response = await l313l.inline_query(Config.TG_BOT_USERNAME, "مساعدة")
    await response[0].click(event.chat_id)
    await event.delete()

# =========================================================== #
# القائمة الرئيسية (أوامر البحث والتحميل)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"main_menu")))
@check_owner
async def main_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة البحـث والتحَميـل
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر البحـث والتحَمـيل 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : أوامـر اليوت والفيديـو( البوت ) : ›", data="youtube_commands")],
        [
            Button.inline("‹ : أوامـر البحـث والفيـديو ( الأنلاين ) : ›", data="inline_search_commands"),
            Button.inline("‹ : أوامـر السوشيال مَيـديا : ›", data="social_commands")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة السورس (التحديث والتشغيل)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"source_menu")))
@check_owner
async def source_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة التحديث والتشغيل
‹ : من هنـا يمكنـك إيجـاد شـرح لكـل أوامـر التحديثات 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [
        [Button.inline("‹ : التحَـديث : ›", data="update_commands")],
        [
            Button.inline("‹ : أعَـادة التشغيل : ›", data="restart_commands"),
            Button.inline("‹ : أيـقاف البوت : ›", data="stop_commands")
        ],
        [Button.inline("‹ : الفحَـص و سَرعة الأنترنت : ›", data="speed_commands")],
        [
            Button.inline("‹ : السَليب : ›", data="sleep_commands"),
            Button.inline("‹ : المـطور المَساعـد : ›", data="assistant_dev_commands")
        ],
        [Button.inline("رجــوع ↩️", data="ZEDHELP")]
    ]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر التحديث
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"update_commands")))
@check_owner
async def update_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التشغيل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تحديث</code> <b>⦘</b>
❐ التحقق من التحديثات
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تحديث الان</code> <b>⦘</b>
❐ لتحديث السورس
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.التحديثات تشغيل</code> <b>⦘</b>
❐ تشغيل الرسالة التجريبية
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.التحديثات ايقاف</code> <b>⦘</b>
❐ إيقاف الرسالة التجريبية
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر إعادة التشغيل
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"restart_commands")))
@check_owner
async def restart_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التشغيل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.اعادة التشغيل</code> <b>⦘</b>
❐ إعادة تشغيل البوت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر إيقاف البوت
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"stop_commands")))
@check_owner
async def stop_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر الاطفاء 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.اطفاء</code> <b>⦘</b>
❐ إيقاف تشغيل البوت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر الفحص وسرعة الإنترنت
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"speed_commands")))
@check_owner
async def speed_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر المساعدة 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.سرعة النت</code> <b>⦘</b>
❐ قياس سرعة الانترنت
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.بنك</code> <b>⦘</b>
❐ قياس سرعة البنك
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.فحص</code> <b>⦘</b>
❐ لعرض معلومات التشغيل
❐ <b>طريقة الاستخدام:</b> إرسال الأمر فقط

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر السليب
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"sleep_commands")))
@check_owner
async def sleep_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السليب 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.سليب</code> <b>⦘</b>
❐ وضعك في وضع غير المتصل
❐ <b>طريقة الاستخدام:</b> <code>.سليب السبب</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.سليب_ميديا</code> <b>⦘</b>
❐ سليب مع صورة أو متحركة
❐ <b>طريقة الاستخدام:</b> <code>.سليب_ميديا السبب بالرد</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر المطور المساعد
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"assistant_dev_commands")))
@check_owner
async def assistant_dev_commands(event):
    text = f'''<b>ᯓ اوامــر المطـور المســاعد .</b>

⎉╎قائـمـه اوامـر رفـع المطـور المسـاعـد 🧑🏻‍💻✅ 🦾 : 
- اضغـط ع الامـر للنسـخ ثـم استخـدمهـا بالتـرتيـب 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.رفع مطور</code> <b>⦘</b>
- لـ رفـع الشخـص مطـور مسـاعـد معـك بالبـوت 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تنزيل مطور</code> <b>⦘</b>
- لـ تنزيـل الشخـص مطـور مسـاعـد مـن البـوت 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.المطورين</code> <b>⦘</b>
- لـ عـرض قائمـة بمطـورين البـوت الخـاص بـك 🧑🏻‍💻📑 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.امر المطور تفعيل</code> <b>⦘</b>
- لـ تفعيـل وضـع المطـورين المسـاعدين 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.امر المطور تعطيل</code> <b>⦘</b>
- لـ تعطيـل وضـع المطـورين المسـاعدين 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تحكم كامل</code> <b>⦘</b>
- اعطـاء المطـورين المرفـوعيـن صلاحيـة التحكـم الكـاملـه بالاوامــر ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تحكم آمن</code> <b>⦘</b>
- اعطـاء المطـورين المرفـوعيـن صلاحيـة التحكـم الآمـن لـ الاوامــر الامنـه فقـط ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تحكم + اسم الامـر</code> <b>⦘</b>
- اعطـاء المطـورين المرفـوعيـن صلاحيـة التحكـم بأمـر واحـد فقـط او عـدة اوامـر معينـه ✓ .. مثـال (<code>.تحكم ايدي</code>) او (<code>.تحكم ايدي فحص كتم</code>)

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.ايقاف تحكم كامل</code> <b>⦘</b>
- ايقـاف صلاحيـة التحكـم الكـاملـه بالاوامــر للمطـورين المرفـوعيـن ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.ايقاف تحكم آمن</code> <b>⦘</b>
- ايقـاف صلاحيـة التحكـم الآمـن لـ الاوامــر الآمنـه للمطـورين المرفـوعيـن ✓ 

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.ايقاف تحكم + اسم الامـر</code> <b>⦘</b>
- ايقـاف صلاحيـة التحكـم المعطـاه لـ امـر واحـد فقـط او عـدة اوامـر للمطـورين المرفـوعيـن ✓ .. مثـال (<code>.ايقاف تحكم ايدي</code>) او (<code>.ايقاف تحكم ايدي فحص كتم</code>)

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.التحكم</code> / <code>.التحكم المعطل</code> <b>⦘</b>
- لـ عـرض قائمـة بالاوامـر المسمـوحـه والغيـر مسمـوحـه للمطـوريـن التحكـم فيهـا 🛃🚷 

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="source_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# قائمة الحساب (مؤقت - سيتم إكمالها لاحقاً)
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"account_menu")))
@check_owner
async def account_menu(event):
    text = f'''‹ : مـࢪحبـاً عـزيـزي <tg-emoji emoji-id="{EMOJI_HEART}">❤️</tg-emoji>
‹ : في قائمـة الحسـاب
‹ : سيتم إضافة الأوامر قريباً 

ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️'''
    
    buttons = [[Button.inline("رجــوع ↩️", data="ZEDHELP")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# أوامر البحث والتحميل (الأنلاين) - موجودة مسبقاً
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"youtube_commands")))
@check_owner
async def youtube_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر التحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.يوت</code> <b>⦘</b>
❐ البحث عن أغنية
❐ <b>طريقة الاستخدام:</b> <code>.بحث اسم الاغنية</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تفعيل يوت</code> <b>⦘</b>
❐ لتسمح ب استخدام امر يوت للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل يوت</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تعطيل يوت</code> <b>⦘</b>
❐ لتعطيل استخدام امر يوت
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل يوت</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.فيديو</code> <b>⦘</b>
❐ البحث عن فيديو
❐ <b>طريقة الاستخدام:</b> <code>.بحث اسم الفيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تفعيل فيديو</code> <b>⦘</b>
❐ لتسمح ب استخدام امر فيديو للأشخاص الآخرين
❐ <b>طريقة الاستخدام:</b> <code>.تفعيل فيديو</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تعطيل فيديو</code> <b>⦘</b>
❐ لتعطيل استخدام امر فيديو
❐ <b>طريقة الاستخدام:</b> <code>.تعطيل فيديو</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"inline_search_commands")))
@check_owner
async def inline_search_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر البحث والتحميل 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.بحث</code> <b>⦘</b>
❐ تحميل( صوت / فيديو ) من يوتيوب 
❐ <b>طريقة الاستخدام:</b> <code>.بحث الكلمة أو الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"social_commands")))
@check_owner
async def social_commands(event):
    text = f'''<b>𓆩 𝐒𝐎𝐔𝐑𝐂𝐄 𝐀𝐑𝐀𝐒 - أوامر السوشيال ميديا 𓆪</b>
━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.فيس</code> <b>⦘</b>
❐ تحميل من الفيس بوك
❐ <b>طريقة الاستخدام:</b> <code>.فيس الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.تيك</code> <b>⦘</b>
❐ تحميل من تيك توك
❐ <b>طريقة الاستخدام:</b> <code>.تيك الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.ستوري</code> <b>⦘</b>
❐ تحميل ستوري من التلكرام
❐ <b>طريقة الاستخدام:</b> <code>.ستوري الرابط</code>

<tg-emoji emoji-id="{EMOJI_AWAMER}">📨</tg-emoji> <b>⦗</b> <code>.داون</code> <b>⦘</b>
❐ تحميل من جميع مواقع التواصل
❐ <b>طريقة الاستخدام:</b> <code>.داون الرابط</code>

•ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ•
⌔︙🅳🅴🆅 @Lx5x5 .<tg-emoji emoji-id="{EMOJI_OWNER}">🦅</tg-emoji>'''
    
    buttons = [[Button.inline("↩️ رجوع", data="main_menu")]]
    await event.edit(text, buttons=buttons, parse_mode="HTML", link_preview=False)

# =========================================================== #
# زر الرجوع النهائي
# =========================================================== #

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"ZEDHELP")))
@check_owner
async def back_to_main(event):
    buttons = [
        [Button.inline("‹ : أوامـر البحـث والتحميل : ›", data="main_menu")],
        [
            Button.inline("‹ : السـورس : ›", data="source_menu"),
            Button.inline("‹ : الحـساب : ›", data="account_menu")
        ]
    ]
    await event.edit(HELP, buttons=buttons, link_preview=False)
