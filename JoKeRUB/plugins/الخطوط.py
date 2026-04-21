from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.managers import edit_delete
from telethon.extensions import html
import re

# ========== تخزين مؤقت للحالات (ذاكرة مؤقتة للسرعة) ==========
_status_cache = {
    "bold": False,
    "tshwesh": False,
    "ramz": False,
    "joker": False,
    "decorative_line": False
}

def update_cache():
    """تحديث الذاكرة المؤقتة من قاعدة البيانات (مرة واحدة فقط عند التغيير)"""
    _status_cache["bold"] = bool(gvarstatus("bold"))
    _status_cache["tshwesh"] = bool(gvarstatus("tshwesh"))
    _status_cache["ramz"] = bool(gvarstatus("ramz"))
    _status_cache["joker"] = bool(gvarstatus("joker"))
    _status_cache["decorative_line"] = bool(gvarstatus("decorative_line"))

# ========== أوامر التحكم في الخطوط ==========
@l313l.on(admin_cmd(pattern="(خط الغامق|خط غامق)"))
async def bold_toggle(event):
    key = "bold"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**", 1)
    update_cache()  # تحديث الكاش بعد التغيير

@l313l.on(admin_cmd(pattern="(خط المشطوب|خط مشطوب)"))
async def strikethrough_toggle(event):
    key = "tshwesh"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط المشطوب ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط المشطوب ✓**", 1)
    update_cache()

@l313l.on(admin_cmd(pattern="(خط رمز|خط الرمز)"))
async def monospace_toggle(event):
    key = "ramz"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الرمز ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الرمز ✓**", 1)
    update_cache()

@l313l.on(admin_cmd(pattern="(خط الجوكر|خط جوكر)"))
async def joker_toggle(event):
    key = "joker"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الجوكر ✓**", 1)
    else:
        delgvar(key)
        await edit_delete(event, "**᯽︙ تم إيقاف خط الجوكر ✓**", 1)
    update_cache()

@l313l.on(admin_cmd(pattern="(خط مزخرف|تفعيل خط مزخرف)"))
async def enable_decorative(event):
    key = "decorative_line"
    if not gvarstatus(key):
        addgvar(key, "on")
        await edit_delete(event, "**⎉╎تم تفعيل خط المزخرف مع التشويش ✓**", 1)
    else:
        await edit_delete(event, "**⎉╎خط المزخرف مفعل مسبقاً ✓**", 1)
    update_cache()

@l313l.on(admin_cmd(pattern="(تعطيل خط مزخرف|إيقاف خط مزخرف)"))
async def disable_decorative(event):
    key = "decorative_line"
    if gvarstatus(key):
        delgvar(key)
        await edit_delete(event, "**⎉╎تم تعطيل خط المزخرف ✓**", 1)
    else:
        await edit_delete(event, "**⎉╎خط المزخرف معطل مسبقاً ✓**", 1)
    update_cache()

# ========== دالة سريعة لفحص الإيموجي البريميوم ==========
def has_premium_emoji_fast(text):
    """فحص سريع - يوقف عند أول إيموجي بريميوم (أول 100 حرف فقط)"""
    for ch in text[:100]:
        if ord(ch) >= 0x10000:
            return True
    return False

# ========== المعالج الرئيسي الوحيد (الأسرع) ==========
@l313l.on(events.NewMessage(outgoing=True))
async def fast_formatting_handler(event):
    """معالج واحد سريع لجميع أنواع الخطوط"""
    msg = event.message
    
    # فحوصات سريعة أولاً
    if not msg.text or msg.media or msg.text.startswith('.'):
        return
    
    text = msg.text
    
    # فحص سريع للإيموجي البريميوم
    if has_premium_emoji_fast(text):
        return
    
    # استخدام الكاش السريع (بدون استدعاء قاعدة البيانات)
    if _status_cache["bold"]:
        await event.edit(f"**{text}**")
    
    elif _status_cache["tshwesh"]:
        await event.edit(f"~~{text}~~")
    
    elif _status_cache["ramz"]:
        await event.edit(f"`{text}`")
    
    elif _status_cache["joker"]:
        await event.edit(f"```{text}```")
    
    elif _status_cache["decorative_line"]:
        # خط مزخرف - يعمل بشكل صحيح مع السرعة
        decorated = f'<a href="emoji/5447181973544008180">✨</a> <a href="spoiler">{text}</a> <a href="emoji/5447389832781264371">✨</a>'
        try:
            parsed_text, entities = html.parse(decorated)
            
            # تحويل الكيانات إلى الأنواع الصحيحة
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url == 'spoiler':
                        entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                    elif e.url.startswith('emoji/'):
                        try:
                            emoji_id = int(e.url.split('/')[1])
                            entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, emoji_id)
                        except:
                            pass
            
            await event.edit(parsed_text, parse_mode=None, formatting_entities=entities)
        except Exception as e:
            # في حال فشل المزخرف، نرسل النص عادي
            print(f"خطأ في خط المزخرف: {e}")

# ========== تحديث الكاش عند بدء التشغيل ==========
update_cache()
