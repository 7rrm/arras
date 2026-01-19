from telethon import events
from JoKeRUB import l313l
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon import functions
from telethon.errors.rpcerrorlist import MessageIdInvalidError

# جميع أوامر الخطوط مع التعديل الجديد للخط الغامق
@l313l.on(admin_cmd(pattern="(خط الغامق|خط غامق)"))
async def bold_toggle(event):
    if not gvarstatus("bold"):
        addgvar("bold", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الغامق بنجاح ✓**")
    else:
        delgvar("bold")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الغامق ✓**")

@l313l.on(admin_cmd(pattern="(خط المشطوب|خط مشطوب)"))
async def strikethrough_toggle(event):
    if not gvarstatus("tshwesh"):
        addgvar("tshwesh", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط المشطوب ✓**")
    else:
        delgvar("tshwesh")
        await edit_delete(event, "**᯽︙ تم إيقاف خط المشطوب ✓**")

@l313l.on(admin_cmd(pattern="(خط رمز|خط الرمز)"))
async def monospace_toggle(event):
    if not gvarstatus("ramz"):
        addgvar("ramz", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الرمز ✓**")
    else:
        delgvar("ramz")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الرمز ✓**")

@l313l.on(admin_cmd(pattern="(خط الجوكر|خط جوكر)"))
async def joker_toggle(event):
    if not gvarstatus("joker"):
        addgvar("joker", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط الجوكر ✓**")
    else:
        delgvar("joker")
        await edit_delete(event, "**᯽︙ تم إيقاف خط الجوكر ✓**")

@l313l.on(events.NewMessage(outgoing=True))
async def handle_text_formatting(event):
    if not event.message.text or event.message.media:
        return
        
    text = event.message.text
    modified = False
    
    # التحقق من جميع أنواع الخطوط
    if gvarstatus("bold"):
        if not text.startswith('.') and '.' not in text[:-1]:
            text = f"**{text}**"
            modified = True
            
    if gvarstatus("tshwesh") and not modified:
        text = f"~~{text}~~"
        modified = True
        
    if gvarstatus("ramz") and not modified:
        text = f"`{text}`"
        modified = True
        
    if gvarstatus("joker") and not modified:
        text = f"```{text}```"
        modified = True
        
    if modified:
        try:
            await event.edit(text)
        except:
            pass
            
#########################
from telethon import events, types
from JoKeRUB import l313l
from ..sql_helper.globals import gvarstatus, addgvar, delgvar
from ..core.managers import edit_delete
from telethon.extensions import html
from telethon.extensions import markdown

DECORATIVE_EMOJI_ID = "5447181973544008180"  # إيموجي قبل النص
DECORATIVE_EMOJII_ID = "5447389832781264371"  # إيموجي بعد النص

# ========== كلاس الإيموجي المخصص ==========
class CustomParseMode:
    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == 'html':
            text, entities = html.parse(text)
            # معالجة إيموجيات البريميوم
            for i, e in enumerate(entities):
                if isinstance(e, types.MessageEntityTextUrl):
                    if e.url.startswith('emoji/'):
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(
                            offset=e.offset,
                            length=e.length,
                            document_id=document_id
                        )
            return text, entities
        elif self.parse_mode == 'markdown':
            return markdown.parse(text)
        raise ValueError("Unsupported parse mode")

    @staticmethod
    def unparse(text, entities):
        return html.unparse(text, entities)

# ========== أوامر خط مزخرف (التشويش + الإيموجيات) ==========
@l313l.on(admin_cmd(pattern="(خط مزخرف|تفعيل خط مزخرف)"))
async def enable_decorative_line(event):
    """تفعيل خط مزخرف مع تشويش"""
    is_decorative = gvarstatus("decorative_line")
    if not is_decorative:
        addgvar("decorative_line", "on")
        await edit_delete(event, "**⎉╎تم تفعيـل خـط المـزخرف بالتشويش ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل خط مزخرف)**")
        return
    if is_decorative:
        await edit_delete(event, "**⎉╎خـط المـزخرف مفعـل .. مسبقـاً ✓**\n**⎉╎لـ تعطيله اكتب (.تعطيل خط مزخرف)**")
        return

@l313l.on(admin_cmd(pattern="(تعطيل خط مزخرف|إيقاف خط مزخرف)"))
async def disable_decorative_line(event):
    """تعطيل خط مزخرف مع تشويش"""
    is_decorative = gvarstatus("decorative_line")
    if is_decorative:
        delgvar("decorative_line")
        await edit_delete(event, "**⎉╎تم تعطيـل خـط المـزخرف .. بنجـاح ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل خط مزخرف)**")
        return
    if not is_decorative:
        await edit_delete(event, "**⎉╎خـط المـزخرف معطـل .. مسبقـاً ✓**\n**⎉╎لـ تفعيله اكتب (.تفعيل خط مزخرف)**")
        return

# ========== المعالج الرئيسي ==========
@l313l.on(events.NewMessage(outgoing=True))
async def handle_decorative_spoiler(event):
    """معالجة الرسائل مع التشويش والإيموجيات"""
    # التحقق من وجود نص وليس وسائط
    if not event.message.text or event.message.media:
        return
    
    # تخطي الأوامر التي تبدأ بنقطة
    if event.message.text.startswith('.'):
        return
    
    # التحقق من تفعيل خط مزخرف
    is_decorative = gvarstatus("decorative_line")
    if not is_decorative:
        return
    
    text = event.message.text
    
    try:
        # الطريقة 1: HTML مع الإيموجيات المخصصة (الأفضل)
        formatted_html = (
            f'<a href="emoji/{DECORATIVE_EMOJI_ID}">💫</a> '
            f'<tg-spoiler>{text}</tg-spoiler> '
            f'<a href="emoji/{DECORATIVE_EMOJII_ID}">💫</a>'
        )
        
        # استخدام CustomParseMode لتحويل HTML
        parse_mode = CustomParseMode("html")
        parsed_text, entities = parse_mode.parse(formatted_html)
        
        # تعديل الرسالة
        await event.edit(
            parsed_text,
            parse_mode=None,
            formatting_entities=entities
        )
        
    except Exception as e:
        # إذا فشلت طريقة HTML، جرب Markdown
        try:
            # الطريقة 2: Markdown مع التشويش
            formatted_markdown = f"💫 **[{text}](spoiler)** 💫"
            await event.edit(formatted_markdown, parse_mode=CustomParseMode("markdown"))
        except:
            # إذا فشلت جميع الطرق، استخدم HTML عادي
            try:
                formatted_simple = f'💫 <tg-spoiler>{text}</tg-spoiler> 💫'
                await event.edit(formatted_simple, parse_mode="html")
            except:
                # تجاهل أي خطأ نهائي
                pass
