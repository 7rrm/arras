from telethon import events, Button
from ..Config import Config
from ..sql_helper.globals import gvarstatus
from l313l.razan.resources.mybot import *

ROZ_PIC = "https://graph.org/file/2e51431a290028d612377-07abd6e9a86fde6949.jpg"
FIRE_EMOJI = "5368324170671202286"  # 🔥 ايموجي بريميوم

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

# ✅ هذا الجزء خاص بالإنلاين (للبوت فقط)
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        query = event.text
        user_id = event.query.user_id
        
        await bot.get_me()
        
        if query.startswith("السورس") and user_id == bot.uid:
            # أزرار الإنلاين (هذا شغال عندك)
            buttons = [
                [Button.url("🔥 المطور @lx5x5 🔥", "https://t.me/lx5x5")],
                [Button.url("✅ قناة السورس ✅", "https://t.me/your_channel")],
                [Button.url("🛡 الدعم الفني 🛡", "https://t.me/your_support")]
            ]
            
            result = builder.article(
                title="🔥 JoKeRUB - السورس",
                text=ROZ,
                buttons=buttons,
                link_preview=False
            )
            await event.answer([result])

# ✅ هذا الأمر يرسل رسالة عادية من الحساب مع أزرار
@bot.on(admin_cmd(outgoing=True, pattern="السورس"))
async def repo(event):
    if event.fwd_from:
        return
    
    # حذف الأمر
    await event.delete()
    
    # ✅ إنشاء الأزرار بشكل صحيح - المهم هنا
    buttons = [
        [Button.url("🔥 المطور @lx5x5 🔥", "https://t.me/lx5x5")],
        [Button.url("✅ قناة السورس ✅", "https://t.me/your_channel")],
        [Button.url("🛡 الدعم الفني 🛡", "https://t.me/your_support")]
    ]
    
    # ✅ إرسال الرسالة مع الأزرار - هذا هو الحل
    await bot.send_message(
        event.chat_id,
        ROZ,
        buttons=buttons,      # هنا المشكلة كانت
        parse_mode='markdown',
        link_preview=False
    )
    
    print(f"✅ تم إرسال السورس مع الأزرار للمحادثة {event.chat_id}")
