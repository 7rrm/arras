from telethon import events, Button
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"

# نص السورس
ROZ = (
    f"╭───────• 𝗔𝗥𝗔𝗦 •───────╮\n"
    f"│ **● ʙᴏᴛ sᴛᴀᴛᴜs: ʀᴜɴɴɪɴɢ ✅**\n"
    f"├──────────────────────\n"
    f"│ **● ᴘʟᴀᴛғᴏʀᴍ ᴅᴇᴛᴀɪʟs:**\n"
    f"│ • ᴛᴇʟᴇᴛʜᴏɴ: `1.23.0`\n"
    f"│ • sᴏᴜʀᴄᴇ: `4.0.1`\n"
    f"│ • ʙᴏᴛ: `@{Config.TG_BOT_USERNAME}`\n"
    f"│ • ᴘʏᴛʜᴏɴ: `3.9.6`\n"
    f"│ • ᴜsᴇʀ: {mention}\n"
    f"╰──────────────────────╯"
)

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        query = event.text
        user_id = event.query.user_id
        
        await bot.get_me()
        
        if query.startswith("السورس") and user_id == bot.uid:
            # ✅ استخدام Button فقط - هذا هو الحل الصحيح
            buttons = [
                [Button.url("∙ المـطور ∙", "https://t.me/lx5x5")],
                [Button.url("∙ قناة السورس ∙", "https://t.me/your_channel")],
                [Button.url("∙ الدعم الفني ∙", "https://t.me/your_support")]
            ]
            
            if ROZ_PIC and ROZ_PIC.endswith((".jpg", ".png", ".gif", ".mp4")):
                result = builder.photo(
                    ROZ_PIC, 
                    text=ROZ, 
                    buttons=buttons, 
                    link_preview=False
                )
            elif ROZ_PIC:
                result = builder.document(
                    ROZ_PIC, 
                    title="JoKeRUB", 
                    text=ROZ, 
                    buttons=buttons, 
                    link_preview=False
                )
            else:
                result = builder.article(
                    title="JoKeRUB", 
                    text=ROZ, 
                    buttons=buttons, 
                    link_preview=False
                )
            
            await event.answer([result] if result else None)

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
