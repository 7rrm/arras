from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.managers import edit_delete
from telethon.extensions import html

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

# ========== المعالج السريع للخطوط العادية ==========
@l313l.on(events.NewMessage(outgoing=True))
async def fast_text_formatting(event):
    if not event.message.text or event.message.media or event.message.text.startswith('.'):
        return
    
    text = event.message.text
    
    # الخطوط العادية (سريعة)
    if gvarstatus("bold"):
        await event.edit(f"**{text}**")
    elif gvarstatus("tshwesh"):
        await event.edit(f"~~{text}~~")
    elif gvarstatus("ramz"):
        await event.edit(f"`{text}`")
    elif gvarstatus("joker"):
        await event.edit(f"```{text}```")

# ========== معالج منفصل للخط المزخرف (لتفادي الأخطاء) ==========
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
    
    # خط مزخرف سريع
    decorated = f'<a href="emoji/5447181973544008180">✨</a> <a href="spoiler">{text}</a> <a href="emoji/5447389832781264371">✨</a>'
    
    try:
        parsed_text, entities = html.parse(decorated)
        
        # تحويل entities
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    emoji_id = int(e.url.split('/')[1])
                    entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, emoji_id)
        
        await event.edit(parsed_text, parse_mode=None, formatting_entities=entities)
    except Exception as e:
        print(f"خطأ في المزخرف: {e}")
