from telethon import events
from telethon.tl.types import InputBotInlineMessageText

@l313l.tgbot.on(events.InlineQuery)
async def test_handler(event):
    builder = event.builder
    
    # تجربة 1: باستخدام HTML مع إيموجي مميز
    test_result_1 = builder.article(
        title="تجربة 1 - إيموجي بريميوم",
        description="هذا اختبار للإيموجي المميز",
        text='<tg-emoji emoji-id="5210740682414644888">✅</tg-emoji> هذا إيموجي مميز <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>',
        parse_mode='html'
    )
    
    # تجربة 2: نص عادي مع إيموجي عادي
    test_result_2 = builder.article(
        title="تجربة 2 - إيموجي عادي",
        description="هذا اختبار للإيموجي العادي",
        text='✅ هذا إيموجي عادي ✅',
    )
    
    # تجربة 3: باستخدام InputBotInlineMessageText مباشرة
    try:
        test_result_3 = InputBotInlineMessageText(
            message='<tg-emoji emoji-id="5210740682414644888">✅</tg-emoji> إيموجي مميز مباشر <tg-emoji emoji-id="5210740682414644888">✅</tg-emoji>',
            entities=None,
            no_webpage=True
        )
    except:
        test_result_3 = None
    
    await event.answer([test_result_1, test_result_2, test_result_3] if test_result_3 else [test_result_1, test_result_2])
