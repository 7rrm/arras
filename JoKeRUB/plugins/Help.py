import re
from telethon import Button, events
from telethon.events import CallbackQuery
from ..core import check_owner
from ..Config import Config
from . import l313l

HELP = "**🧑🏻‍💻┊مـࢪحبـاً عـزيـزي**\n**🛂┊في قائمـة المسـاعـده والشـروحـات\n🛃┊من هنـا يمكنـك ايجـاد شـرح لكـل اوامـر السـورس**\n\n[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗮𝗥𝗥𝗮𝗦 ♥️](https://t.me/lx5x5)\n\n"

# إيموجيات ملونة للأزرار
EMOJI_PRIMARY = "5258215850745275216"      # ✨
EMOJI_SUCCESS = "5411580731929411768"      # ✅
EMOJI_DANGER = "5350477112677515642"       # 🔥
EMOJI_SECONDARY = "5408997493784467607"    # 💎
EMOJI_WARNING = "5188619457651567219"      # ⚠️

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    @check_owner
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        
        if query.startswith("مساعدة"):
            buttons = [
                [
                    {
                        "text": "اوامر الادارة 👮",
                        "callback_data": "admin_commands",
                        "style": "primary",
                        "icon_custom_emoji_id": EMOJI_PRIMARY
                    }
                ],
                [
                    {
                        "text": "اوامر التنظيف 🧹",
                        "callback_data": "clean_cmd",
                        "style": "success",
                        "icon_custom_emoji_id": EMOJI_SUCCESS
                    },
                    {
                        "text": "اوامر المسح 🗑️",
                        "callback_data": "delete_cmd",
                        "style": "danger",
                        "icon_custom_emoji_id": EMOJI_DANGER
                    }
                ],
                [
                    {
                        "text": "اوامر الوقت والتاريخ 📅",
                        "callback_data": "time_date_cmd",
                        "style": "secondary",
                        "icon_custom_emoji_id": EMOJI_SECONDARY
                    }
                ],
                [
                    {
                        "text": "اوامر الوقتي 🔄",
                        "callback_data": "timely_cmd",
                        "style": "primary",
                        "icon_custom_emoji_id": EMOJI_PRIMARY
                    },
                    {
                        "text": "اوامر الصلاة 🕌",
                        "callback_data": "prayer_cmd",
                        "style": "success",
                        "icon_custom_emoji_id": EMOJI_SUCCESS
                    }
                ],
                [
                    {
                        "text": "اوامر المساعدة 🆘",
                        "callback_data": "help_commands",
                        "style": "warning",
                        "icon_custom_emoji_id": EMOJI_WARNING
                    }
                ],
                [
                    {
                        "text": "اوامر الروابط 🔗",
                        "callback_data": "link_commands",
                        "style": "secondary",
                        "icon_custom_emoji_id": EMOJI_SECONDARY
                    },
                    {
                        "text": "اوامر الكشف 🔍",
                        "callback_data": "detect_commands",
                        "style": "primary",
                        "icon_custom_emoji_id": EMOJI_PRIMARY
                    }
                ],
                [
                    {
                        "text": "اوامر التسلية والميمز 😂",
                        "callback_data": "fun_meme_commands",
                        "style": "success",
                        "icon_custom_emoji_id": EMOJI_SUCCESS
                    }
                ],
                [
                    {
                        "text": "اوامر الاذاعة 📢",
                        "callback_data": "broadcast_commands",
                        "style": "danger",
                        "icon_custom_emoji_id": EMOJI_DANGER
                    },
                    {
                        "text": "اوامر التحويل 🔄",
                        "callback_data": "convert_commands",
                        "style": "secondary",
                        "icon_custom_emoji_id": EMOJI_SECONDARY
                    }
                ],
                [
                    {
                        "text": "اوامر الجهات 👥",
                        "callback_data": "contacts_commands",
                        "style": "primary",
                        "icon_custom_emoji_id": EMOJI_PRIMARY
                    }
                ],
                [
                    {
                        "text": "اوامر الحساب 👤",
                        "callback_data": "account_commands",
                        "style": "success",
                        "icon_custom_emoji_id": EMOJI_SUCCESS
                    },
                    {
                        "text": "اوامر الفارات ⚙️",
                        "callback_data": "var_commands",
                        "style": "warning",
                        "icon_custom_emoji_id": EMOJI_WARNING
                    }
                ],
                [
                    {
                        "text": "اوامر التجميع 💰",
                        "callback_data": "collect_commands",
                        "style": "danger",
                        "icon_custom_emoji_id": EMOJI_DANGER
                    }
                ],
                [
                    {
                        "text": "اوامر وعد 🏦",
                        "callback_data": "w3d_commands",
                        "style": "secondary",
                        "icon_custom_emoji_id": EMOJI_SECONDARY
                    },
                    {
                        "text": "اوامر الاذكار 📿",
                        "callback_data": "azkar_commands",
                        "style": "success",
                        "icon_custom_emoji_id": EMOJI_SUCCESS
                    }
                ],
            ]
            result = builder.article(
                title="قائمة المساعدة - آراس",
                text=HELP,
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
