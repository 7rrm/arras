from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.managers import edit_delete

# ========== أوامر التحكم السريعة ==========
@l313l.on(admin_cmd(pattern="(خط الغامق|خط غامق)"))
async def bold_toggle(event):
    key = "bold"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط المشطوب|خط مشطوب)"))
async def strikethrough_toggle(event):
    key = "tshwesh"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط المشطوب ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط المشطوب ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط رمز|خط الرمز)"))
async def monospace_toggle(event):
    key = "ramz"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الرمز ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الرمز ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط الجوكر|خط جوكر)"))
async def joker_toggle(event):
    key = "joker"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الجوكر ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الجوكر ✓**", 1)

@l313l.on(admin_cmd(pattern="(خط مزخرف|تفعيل خط مزخرف)"))
async def enable_decorative(event):
    key = "decorative_line"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**⎉╎تم تفعيل خط المزخرف مع التشويش ✓**", 1)
    else:
        await edit_delete(event, "**⎉╎خط المزخرف مفعل مسبقاً ✓**", 1)

@l313l.on(admin_cmd(pattern="(تعطيل خط مزخرف|إيقاف خط مزخرف)"))
async def disable_decorative(event):
    key = "decorative_line"
    if gvarstatus(key):
        delgvar(key)
        await edit_delete(event, "**⎉╎تم تعطيل خط المزخرف ✓**", 1)
    else:
        await edit_delete(event, "**⎉╎خط المزخرف معطل مسبقاً ✓**", 1)

# ========== المعالج السريع للخطوط العادية (مع الحفاظ على الإيموجي البريميوم) ==========
@l313l.on(events.NewMessage(outgoing=True))
async def fast_text_formatting(event):
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    text = event.message.text
    original_entities = event.message.entities or []
    
    # الخطوط العادية (سريعة) مع الحفاظ على الكيانات الأصلية
    if gvarstatus("bold"):
        # إضافة entity الغامق للنص بالكامل مع الحفاظ على الكيانات الأصلية
        new_entities = [types.MessageEntityBold(0, len(text))] + original_entities
        await event.edit(text, formatting_entities=new_entities)
        
    elif gvarstatus("tshwesh"):
        # إضافة entity المشطوب للنص بالكامل مع الحفاظ على الكيانات الأصلية
        new_entities = [types.MessageEntityStrike(0, len(text))] + original_entities
        await event.edit(text, formatting_entities=new_entities)
        
    elif gvarstatus("ramz"):
        # إضافة entity الرمز للنص بالكامل مع الحفاظ على الكيانات الأصلية
        new_entities = [types.MessageEntityCode(0, len(text))] + original_entities
        await event.edit(text, formatting_entities=new_entities)
        
    elif gvarstatus("joker"):
        # إضافة entity الجوكر (pre) للنص بالكامل مع الحفاظ على الكيانات الأصلية
        new_entities = [types.MessageEntityPre(0, len(text), '')] + original_entities
        await event.edit(text, formatting_entities=new_entities)

# ========== معالج منفصل للخط المزخرف (مع الحفاظ على الإيموجي البريميوم) ==========
@l313l.on(events.NewMessage(outgoing=True))
async def decorative_line_handler(event):
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    if not gvarstatus("decorative_line"):
        return
    
    # إذا كان أحد الخطوط العادية مفعل، لا تشتغل
    if gvarstatus("bold") or gvarstatus("tshwesh") or gvarstatus("ramz") or gvarstatus("joker"):
        return
    
    text = event.message.text
    original_entities = event.message.entities or []
    
    # إيموجيات الزينة (يمكنك تغييرها)
    emoji_left_id = 5447181973544008180   # المعرف الأيسر
    emoji_right_id = 5447389832781264371  # المعرف الأيمن
    
    # إنشاء الكيانات الجديدة
    left_emoji_len = 1  # طول الإيموجي
    right_emoji_len = 1
    
    # كيان الإيموجي الأيسر
    left_emoji_entity = types.MessageEntityCustomEmoji(0, left_emoji_len, emoji_left_id)
    
    # كيان التمويه (spoiler) للنص الأصلي
    spoiler_start = left_emoji_len + 1  # +1 للمسافة
    spoiler_entity = types.MessageEntitySpoiler(spoiler_start, len(text))
    
    # كيان الإيموجي الأيمن
    right_emoji_start = spoiler_start + len(text) + 1  # +1 للمسافة
    right_emoji_entity = types.MessageEntityCustomEmoji(right_emoji_start, right_emoji_len, emoji_right_id)
    
    # دمج جميع الكيانات مع الحفاظ على الكيانات الأصلية (مع تعديل المواقع)
    adjusted_original_entities = []
    offset = left_emoji_len + 1 + len(text) + 1 + right_emoji_len  # الإزاحة الكلية
    
    for entity in original_entities:
        # تعديل موقع الكيان الأصلي ليتناسب مع النص الجديد
        if hasattr(entity, 'offset') and hasattr(entity, 'length'):
            adjusted_entity = entity
            # إزاحة الكيان الأصلي ليتناسب مع النص بعد الإضافة
            adjusted_entity.offset = entity.offset + left_emoji_len + 1
            adjusted_original_entities.append(adjusted_entity)
    
    # النص النهائي: [إيموجي أيسر] + مسافة + [النص الأصلي] + مسافة + [إيموجي أيمن]
    final_text = f"  {text}  "  # مسافتين قبل وبعد للنص
    
    # تجميع جميع الكيانات
    all_entities = [left_emoji_entity, spoiler_entity, right_emoji_entity] + adjusted_original_entities
    
    try:
        await event.edit(final_text, formatting_entities=all_entities)
    except Exception as e:
        print(f"خطأ في المزخرف: {e}")
        # في حال فشل، استخدم الطريقة القديمة كاحتياطي
        decorated = f'<a href="emoji/{emoji_left_id}">✨</a> <a href="spoiler">{text}</a> <a href="emoji/{emoji_right_id}">✨</a>'
        try:
            parsed_text, entities = html.parse(decorated)
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url == 'spoiler':
                        entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                    elif e.url.startswith('emoji/'):
                        emoji_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, emoji_id)
            await event.edit(parsed_text, parse_mode=None, formatting_entities=entities)
        except Exception as e2:
            print(f"خطأ في الاحتياطي: {e2}")
