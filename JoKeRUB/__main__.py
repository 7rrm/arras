import sys
import contextlib
import JoKeRUB
from JoKeRUB import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from .Config import Config
from .core.logger import logging
from .core.session import l313l
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    load_plugins,
    setup_bot,
    mybot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("JoKeRUB")

print(JoKeRUB.__copyright__)
print("Licensed under the terms of the " + JoKeRUB.__license__)

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("جارِ بدء سورس آراس ✓")
    l313l.loop.run_until_complete(setup_bot())
    LOGS.info("تم اكتمال تنصيب البوت ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()

try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    l313l.loop.run_until_complete(mybot())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as jep:
    LOGS.error(f"- {jep}")
    sys.exit()    

async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("᯽︙بـوت آراس يعـمل بـنجاح ")
    print(
        f"تم تشغيل الانلاين تلقائياً ارسل {cmdhr}الاوامر لـرؤيـة اوامر السورس\
        \nللمسـاعدة تواصـل  https://t.me/Lx5x5"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return

async def externalrepo():
    if Config.VCMODE:
        await install_externalrepo("https://github.com/Ksidhdnkddbos/JepVc", "jepvc", "jepthonvc")

l313l.loop.run_until_complete(externalrepo())
l313l.loop.run_until_complete(startup_process())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        l313l.run_until_disconnected()
else:
    l313l.disconnect()


@l313l.ar_cmd(
    pattern="تحديث ميوزك$",
    command=("تحديث ميوزك", plugin_category),
    info={
        "header": "لتحديث مستودع الميوزك",
        "description": "يقوم بتحديث مستودع الميوزك إلى أحدث إصدار",
        "usage": ["{tr}تحديث ميوزك"],
    },
)
async def update_music(event):
    "أمر تحديث مستودع الميوزك"
    event = await edit_or_reply(event, "**✧︙ جـارِ تـحـديـث مـيـوزك اراس انـتـظـر**")
    
    # نسبة 20%
    zzz1 = await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 🝢 **تـحـديـث مـيـوزك**\n**•─────────────────•**\n**⇜ جـارِ تـحـديـث مـيـوزك اراس . . .🌐**\n\n%𝟸𝟶 ▬▬▭▭▭▭▭▭▭▭")
    await asyncio.sleep(1)
    
    # نسبة 50%
    zzz2 = await zzz1.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 🝢 **تـحـديـث مـيـوزك**\n**•─────────────────•**\n**⇜ جـارِ تـحـديـث مـيـوزك اراس . . .🌐**\n\n%𝟻𝟶 ▬▬▬▬▬▭▭▭▭▭")
    await asyncio.sleep(1)
    
    # نسبة 80%
    zzz3 = await zzz2.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 🝢 **تـحـديـث مـيـوزك**\n**•─────────────────•**\n**⇜ جـارِ تـحـديـث مـيـوزك اراس . . .🌐**\n\n%𝟾𝟶 ▬▬▬▬▬▬▬▬▭▭")
    await asyncio.sleep(1)
    
    # نسبة 100%
    zzz4 = await zzz3.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 🝢 **تـحـديـث مـيـوزك**\n**•─────────────────•**\n**⇜ جـارِ تـحـديـث مـيـوزك اراس . . .🌐**\n\n%𝟷𝟶𝟶 ▬▬▬▬▬▬▬▬▬▬💯")
    await asyncio.sleep(1)
    
    # تنفيذ التحديث
    try:
        await install_externalrepo("https://github.com/jepthoniq/JepVc", "jepvc", "jepthonvc")
        await zzz4.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗔𝗥𝗥𝗔𝗦 🝢 **تـم تـحـديـث مـيـوزك**\n**•─────────────────•**\n**•⎆┊تم تحديث ميوزك اراس بنجاح ✅**\n**•⎆┊يمكنك الآن استخدام الميوزك**")
    except Exception as e:
        await zzz4.edit(f"**✧︙ فشل تحديث ميوزك اراس:\n`{str(e)}`**")
