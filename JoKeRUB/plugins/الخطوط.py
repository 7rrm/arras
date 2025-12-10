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
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete
from telethon.extensions import html

# كلاس التحليل المخصص (كما في كود الأوامر)
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

# الإيموجي الثابت للزخرفة
DECORATIVE_EMOJI_ID = "5447181973544008180"
DECORATIVE_EMOJII_ID = "5447389832781264371"

# الأمر الرئيسي لتفعيل خط مزخرف
@l313l.on(admin_cmd(pattern="(خط مزخرف|خط المزخرف)"))
async def decorative_toggle(event):
    if not gvarstatus("decorative"):
        addgvar("decorative", "on")
        await edit_delete(event, "**᯽︙ تم تفعيل خط مزخرف بنجاح ✓**")
    else:
        delgvar("decorative")
        await edit_delete(event, "**᯽︙ تم إيقاف خط مزخرف ✓**")

@l313l.on(events.NewMessage(outgoing=True))
async def handle_decorative_formatting(event):
    if not event.message.text or event.message.media:
        return
    
    # التحقق من تفعيل خط مزخرف
    if gvarstatus("decorative"):
        text = event.message.text
        
        # تخطي إذا كان النص يبدأ بنقطة (أوامر)
        if text.startswith('.'):
            return
        
        # تنسيق النص مع الإيموجي من الجانبين
        formatted_text = f'<a href="emoji/{DECORATIVE_EMOJI_ID}">❤️</a>{text}<a href="emoji/{DECORATIVE_EMOJII_ID}">❤️</a>'
        
        try:
            # استخدام CustomParseMode مع event.edit()
            # ننشئ الكيانيات يدوياً
            parse_mode = CustomParseMode("html")
            parsed_text, entities = parse_mode.parse(formatted_text)
            
            # نعدل الرسالة الأصلية
            await event.edit(
                parsed_text,
                parse_mode=None,  # نستخدم الكيانيات مباشرة
                formatting_entities=entities
            )
        except Exception as e:
            # في حال فشل، نستخدم الطريقة العادية
            try:
                await event.edit(formatted_text)
            except:
                pass
