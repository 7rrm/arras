from telethon import Button, events
from telethon.tl.types import MessageEntityCustomEmoji, MessageEntityBold
from . import l313l
from ..helpers import reply_id


# كلاس التحليل المخصص
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
        
# تعريف إيموجي بريميوم للتجربة
PREMIUM_EMOJI_ID = 5368324170671202286  # إيموجي النار 🔥

@l313l.bot_cmd(
    pattern="^/test$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def test_command(event):
    """نسخة مبسطة مع زر واحد - مطابقة لـ python-telegram-bot"""
    
    # الحصول على الدردشة والرد
    chat = await event.get_chat()
    reply_to = await reply_id(event)
    
    # بناء الرسالة بنفس الطريقة تماماً
    message = "🎉 <b>تم بنجاح!</b>\n"
    
    # إضافة الإيموجي البريميوم بنفس الطريقة
    # في Telethon نستخدم <emoji> بدل <tg-emoji>
    message += f'<emoji id="{PREMIUM_EMOJI_ID}">🔥</emoji>\n\n'
    message += "للتواصل مع المطور:"
    
    # زر واحد للمطور - مطابق للكود الأصلي
    buttons = [
        [Button.url("👤 تواصل مع المطور", "https://t.me/lx5x5")]
    ]
    
    # إرسال الرسالة بنفس الطريقة
    try:
        await event.client.send_message(
            chat.id,
            message,
            parse_mode='html',  # نفس parse_mode
            buttons=buttons,
            reply_to=reply_to,
            link_preview=False
        )
        
    except Exception as e:
        # في حالة فشل الإيموجي البريميوم، نستخدم إيموجي عادي
        fallback_message = "🎉 <b>تم بنجاح!</b>\n🔥\n\nللتواصل مع المطور:"
        
        await event.client.send_message(
            chat.id,
            fallback_message,
            parse_mode='html',
            buttons=buttons,
            reply_to=reply_to,
            link_preview=False
        )
        
        # تسجيل الخطأ
        from ..core.logger import logging
        LOGS = logging.getLogger(__name__)
        LOGS.error(f"خطأ في إرسال الإيموجي البريميوم: {str(e)}")
      
