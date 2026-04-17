from telethon import events, Button
from telethon.events import CallbackQuery
import asyncio
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from JoKeRUB.plugins import mention

# الكليشة مباشرة (بدون استدعاء)
ROZ = f"""╭───────• 𝗔𝗥𝗔𝗦 •───────╮
│ **● ʙᴏᴛ sᴛᴀᴛᴜs: ʀᴜɴɴɪɴɢ ✅**
├──────────────────────
│ **● ᴘʟᴀᴛғᴏʀᴍ ᴅᴇᴛᴀɪʟs:**
│ • ᴛᴇʟᴇᴛʜᴏɴ: `1.23.0`
│ • sᴏᴜʀᴄᴇ: `4.0.1`
│ • ʙᴏᴛ: `{Config.TG_BOT_USERNAME}`
│ • ᴘʏᴛʜᴏɴ: `3.9.10`
│ • ᴜsᴇʀ: {mention}
╰──────────────────────╯"""

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        query = event.text
        
        if query.startswith("السورس") and event.query.user_id == bot.uid:
            # ✅ أزرار ملونة مباشرة (بدون requests)
            buttons = [
                [Button.url("‹ : المـطـور : ›", "https://t.me/lx5x5", style="danger", icon="5368324170671202286")
                ],
            ]
            
            # إرسال مباشرة عبر Telethon
            await event.answer(
                [await builder.article(
                    title="🔥 JoKeRUB - السورس",
                    description="السورس الرسمي - اضغط للإرسال",
                    text=ROZ,
                    buttons=buttons,
                    link_preview=False,
                )],
                cache_time=0
            )

@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    
    # ✅ حل مشكلة PeerUser
    try:
        await event.get_sender()
        await event.get_chat()
    except Exception:
        pass
    
    TG_BOT = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(TG_BOT, "السورس")
    await response[0].click(event.chat_id)
    await event.delete()
