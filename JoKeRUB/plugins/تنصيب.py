from telethon import events, Button
from telethon.tl.types import InlineQuery, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"
FIRE_EMOJI = "5368324170671202286"  # ايدي الإيموجي الناري 🔥

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        
        if query.startswith("السورس") and event.query.user_id == bot.uid:
            # 🎨 أزرار ملونة مع إيموجي مخصص
            buttons = [
                [
                    InlineKeyboardButton(
                        text="🔥✦ المـطور ✦🔥",
                        url="https://t.me/lx5x5",
                        style="primary",  # 🔵 أزرق
                        icon_custom_emoji_id=FIRE_EMOJI
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅✦ القناة ✦✅",
                        url="https://t.me/your_channel",
                        style="success",  # 🟢 أخضر
                        icon_custom_emoji_id=FIRE_EMOJI
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🛡✦ الدعم ✦🛡",
                        url="https://t.me/your_support",
                        style="primary",  # 🔵 أزرق
                        icon_custom_emoji_id=FIRE_EMOJI
                    )
                ]
            ]
            
            # تحويل الأزرار إلى تنسيق Telethon
            markup = event.builder.article(
                title="JoKeRUB - السورس",
                description="اضغط لفتح السورس",
                text=ROZ,
                buttons=buttons,
                link_preview=False
            )
            
            await event.answer([markup] if markup else None)
    
    @tgbot.on(events.CallbackQuery)
    async def callback_handler(event):
        """معالج الضغط على الأزرار"""
        await event.answer("✨ تم الضغط على الزر!", alert=False)

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    TG_BOT = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(TG_BOT, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()
