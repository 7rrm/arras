import html
import os
import random
from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from JoKeRUB import l313l
from random import choice
from l313l.razan.resources.strings import *
from telethon import events
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch
from telethon.utils import get_display_name
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format

plugin_category = "utils"


@l313l.on(admin_cmd(pattern="رفع مرتي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.last_name.replace("\u2060", "") if user.last_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"🚻 ** ✧︙ المستخدم => • ** [{JoKeRUB}](tg://user?id={user.id}) \n ☑️ **✧︙ تم رفعها مرتك بواسطه :**{my_mention} 👰🏼‍♀️.\n**✧︙ يلا حبيبي امشي نخلف بيبي 👶🏻🤤**")

@l313l.on(admin_cmd(pattern="رفع جلب(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه جلب 🐶 بواسطة :** {my_mention} \n**✧︙ خليه خله ينبح 😂**")

@l313l.on(admin_cmd(pattern="رفع تاج(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    custom = user_info[1] if isinstance(user_info, tuple) else None
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"✧︙ المستخدم [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه تاج بواسطة :** {my_mention} 👑🔥")

@l313l.on(admin_cmd(pattern="رفع قرد(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    custom = user_info[1] if isinstance(user_info, tuple) else None
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"✧︙ المستخدم [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه قرد واعطائه موزة 🐒🍌 بواسطة :** {my_mention}")

@l313l.on(admin_cmd(pattern="رفع بكلبي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✾╎المستخـدم ** [{JoKeRUB}](tg://user?id={user.id}) \n**✾╎تـم رفعـه بــ قلبـك .. نبـضك والوريـد 🖤**",
                       )

@l313l.on(admin_cmd(pattern="رفع بقلبي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✾╎المستخـدم**  [{JoKeRUB}](tg://user?id={user.id}) \n**✾╎تـم رفعـه بڪلبك 🖤**",
                       )

@l313l.on(admin_cmd(pattern="رفع عسل(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✾╎المستخـدم ** [{JoKeRUB}](tg://user?id={user.id}) \n**✾╎تـم رفعـه عَـسل الكَـروب 🍯 .**",
                       )

@l313l.on(admin_cmd(pattern="رفع كمر(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✾╎المستخـدم ** [{JoKeRUB}](tg://user?id={user.id}) \n**✾╎تـم رفعـه كَـمـر الكَروب 🌝 .**",
                       )
    
@l313l.on(admin_cmd(pattern="رفع مطي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه مطي 🐴 بواسطة :** {my_mention} \n**✧︙ تعال حبي استلم انه **")

@l313l.on(admin_cmd(pattern="رفع زوجي(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه زوجج بواسطة :** {my_mention} \n**✧︙ يلا حبيبي امشي نخلف 🤤🔞**")

@l313l.on(admin_cmd(pattern="رفع زاحف(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفع المتهم زاحف اصلي بواسطة :** {my_mention} \n**✧︙ ها يلزاحف شوكت تبطل سوالفك حيوان 😂🐍**")

@l313l.on(admin_cmd(pattern="رفع كحبة(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفع المتهم كحبة 👙 بواسطة :** {my_mention} \n**✧︙ ها يلكحبة طوبز خلي انيجك/ج**")

@l313l.on(admin_cmd(pattern="رفع فرخ(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه فرخ الكروب بواسطة :** {my_mention} \n**✧︙ لك الفرخ استر على خمستك ياهو اليجي يزورهاً 👉🏻👌🏻**")

@l313l.ar_cmd(
    pattern="رزله(?:\s|$)([\s\S]*)",
    command=("رزله", plugin_category),
)
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"✧︙ ولك [{tag}](tg://user?id={user.id}) \n✧︙ هيو لتندك بسيادك لو بهاي 👞👈")

@l313l.on(admin_cmd(pattern="رفع حاته(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـها حاته الكروب 🤤😻 بواسطة :** {my_mention} \n**✧︙ تعاي يعافيتي اريد حضن دافي 😽**")

@l313l.on(admin_cmd(pattern="رفع هايشة(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه المتهم هايشة 🐄 بواسطة :** {my_mention} \n**✧︙ ها يلهايشة خوش بيك حليب تعال احلبك 😂**")

@l313l.on(admin_cmd(pattern="رفع صاك(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه صاك 🤤 بواسطة :** {my_mention} \n**✧︙ تعال يلحلو انطيني بوسة من رگبتك 😻🤤**")

@l313l.ar_cmd(
    pattern="مصه(?:\s|$)([\s\S]*)",
    command=("مصه", plugin_category),
)
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"** ⣠⡶⠚⠛⠲⢄⡀\n⣼⠁      ⠀⠀⠀⠳⢤⣄\n⢿⠀⢧⡀⠀⠀⠀⠀⠀⢈⡇\n⠈⠳⣼⡙⠒⠶⠶⠖⠚⠉⠳⣄\n⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄\n⠀⠀⠀⠘⣆       ⠀⠀⠀⠀⠀⠈⠓⢦⣀\n⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⢤\n⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧\n⠀⠀⠀⠀⠀⠀⠀    ⠓⠦⠀⠀⠀⠀**\n**🚹 ¦ تعال مصه عزيزي ** [{tag}](tg://user?id={user.id})")

@l313l.on(admin_cmd(pattern="كرار(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    await edit_or_reply(mention, f"**- Dev :** @Lx5x5 .")

@l313l.on(admin_cmd(pattern="رفع ايجة(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه ايچة 🤤 بواسطة :** {my_mention} \n**✧︙ ها يلأيچة تطلعين درب بـ$25 👙**")

@l313l.on(admin_cmd(pattern="رفع زبال(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعـه زبال الكروب 🧹 بواسطة :** {my_mention} \n**✧︙ تعال يلزبال اكنس الكروب لا أهينك 🗑😹**")

@l313l.on(admin_cmd(pattern="رفع كواد(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعه كواد بواسطة :** {my_mention} \n**✧︙ تعال يكواد عرضك مطشر اصير حامي عرضك ؟😎**")

@l313l.on(admin_cmd(pattern="رفع ديوث(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ المستخدم** [{JoKeRUB}](tg://user?id={user.id}) \n**✧︙ تـم رفعه ديوث الكروب بواسطة :** {my_mention} \n**✧︙ تعال يلديوث جيب اختك خلي اتمتع وياها 🔞**")

@l313l.on(admin_cmd(pattern="رفع مميز(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ الحلو** 「[{JoKeRUB}](tg://user?id={user.id})」 \n**✧︙ تـم رفعه مميز بواسطة :** {my_mention}")

@l313l.on(admin_cmd(pattern="رفع ادمن(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ الحلو** 「[{JoKeRUB}](tg://user?id={user.id})」 \n**✧︙ تـم رفعه ادمن بواسطة :** {my_mention}")

@l313l.on(admin_cmd(pattern="رفع منشئ(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ الحلو** 「[{JoKeRUB}](tg://user?id={user.id})」 \n**✧︙ تـم رفعه منشئ بواسطة :** {my_mention}")

@l313l.on(admin_cmd(pattern="رفع مالك(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور**")
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙ الحلو** 「[{JoKeRUB}](tg://user?id={user.id})」 \n**✧︙ تـم رفعه مالك الكروب بواسطة :** {my_mention}")

@l313l.on(admin_cmd(pattern="رفع مجنب(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.last_name.replace("\u2060", "") if user.last_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f" ** ✧︙  المستخدم => • ** [{JoKeRUB}](tg://user?id={user.id}) \n ☑️ **✧︙  تم رفعه مجنب بواسطه  :**{my_mention} .\n**✧︙  كوم يلمجنب اسبح مو عيب تضرب جلغ 😹** ")

@l313l.on(admin_cmd(pattern="رفع وصخ(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.last_name.replace("\u2060", "") if user.last_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"** ✧︙  المستخدم => • ** [{JoKeRUB}](tg://user?id={user.id}) \n ☑️ **✧︙  تم رفعه وصخ الكروب 🤢 بواسطه  :**{my_mention} .\n**✧︙  لك دكوم يلوصخ اسبح مو ريحتك كتلتنا 🤮 ** ")

@l313l.on(admin_cmd(pattern="زواج(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.last_name.replace("\u2060", "") if user.last_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"✧︙ ** لقد تم زواجك/ج من : **[{JoKeRUB}](tg://user?id={user.id}) 💍\n**✧︙  الف الف مبروك الان يمكنك اخذ راحتك ** ")

@l313l.on(admin_cmd(pattern="طلاك(?:\s|$)([\s\S]*)"))
async def permalink(mention):
    user_info = await get_user_from_event(mention)
    if not user_info:
        return
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    JoKeRUB = user.last_name.replace("\u2060", "") if user.last_name else user.username
    me = await mention.client.get_me()
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    await edit_or_reply(mention, f"**✧︙  انتِ طالق طالق طالق 🙎🏻‍♂️ من  :**{my_mention} .\n**✧︙  لقد تم طلاقها بلثلاث وفسخ زواجكما الان الكل حر طليق ** ")

lMl10l = [393120911, 5427469031]

@l313l.on(events.NewMessage(incoming=True))
async def Hussein(event):
    if event.reply_to and event.sender_id in lMl10l:
       reply_msg = await event.get_reply_message()
       owner_id = reply_msg.from_id.user_id
       if owner_id == l313l.uid:
           if event.message.message == "منصب؟":
               await event.reply("**يب منصب ✓**")
           elif event.message.message == "منو فخر العرب؟":
               await event.reply("**الأمام علي عليه الصلاة والسلام ❤️**")

@l313l.on(admin_cmd(pattern="رفع(?:\s|$)([\s\S]*)"))
async def custom_raise(event):
    # قائمة الأوامر المحجوزة (الأوامر القديمة)
    reserved_commands = [
        "بكلبي", "بقلبي", "عسل", "كمر", "مطي", "زوجي",
        "زاحف", "كحبة", "فرخ", "حاته", "هايشة", "صاك",
        "ايجة", "زبال", "كواد", "ديوث", "مميز", "ادمن",
        "منشئ", "مالك", "مجنب", "وصخ", "تاج", "قرد",
        "جلب", "مرتي"
    ]
    
    # الحصول على الكلمة بعد "رفع"
    full_text = event.pattern_match.group(1).strip()
    
    # إذا لم يكن هناك نص، خرج
    if not full_text:
        return
    
    # استخراج أول كلمة
    first_word = full_text.split()[0].strip()
    
    # إذا كانت الكلمة من الأوامر المحجوزة، اتركها للأوامر القديمة
    if first_word in reserved_commands:
        return  # لا تفعل شيء، دع الأمر القديم يتولى
    
    # الكلمة غير محجوزة، تابع مع الأمر الجديد
    word = first_word
    
    # باقي الكود...
    user_info = await get_user_from_event(event)
    if not user_info:
        return
    
    user = user_info[0] if isinstance(user_info, tuple) else user_info
    
    if user.id == 5427469031:
        return await edit_or_reply(event, f"**- لكك دي هذا المطور**")
    
    JoKeRUB = user.first_name.replace("\u2060", "") if user.first_name else user.username
    
    await edit_or_reply(
        event,
        f"**✧︙اَ‍لستخـدِم** [{JoKeRUB}](tg://user?id={user.id}) \n"
        f"**✧︙تَـم رفعـه {word} **."
    )

cr = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⣾⣿⠁⢸⣿⣧⠀⣿⣿⠉⠹⣿⣆⠉⠉⠉⠉⣿⣿⠟⠀⠀⠀\n"
    "⣿⣿⠀⠘⠛⠛⠀⣿⣿⠀⠀⣿⣿⠀⠀⠀⣼⣿⡟⠀⠀⠀⠀\n"
    "⣿⣿⠀⠀⠀⠀⠀⣿⣿⣤⣾⡿⠃⠀⠀⣼⣿⡟⠀⠀⠀⠀⠀\n"
    "⣿⣿⠀⠀⠀⠀⠀⣿⣿⢻⣿⣇⠀⠀⠀⣿⣿⠁⠀⠀⠀⠀⠀\n"
    "⣿⣿⠀⢸⣿⣷⠀⣿⣿⠀⣿⣿⡄⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⢻⣿⣦⣼⣿⠏⠀⣿⣿⠀⢸⣿⣧⠀⢀⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⠈⠛⠛⠛⠋⠀⠀⠛⠛⠀⠀⠛⠛⠀⠸⠛⠛⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⣴⣿⢿⣷⠒⠲⣾⣾⣿⣿⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⣴⣿⠟⠁⠀⢿⣿⠁⣿⣿⣿⠻⣿⣄⠀⠀⠀⠀⠀\n"
    "⠀⠀⣠⡾⠟⠁⠀⠀⠀⢸⣿⣸⣿⣿⣿⣆⠙⢿⣷⡀⠀⠀⠀\n"
    "⣰⡿⠋⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠉⠻⣿⡀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣆⠂⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠿⠟⠀⠀⠻⣿⣿⡇⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⢀⣾⡿⠃⠀⠀⠀⠀⠀⠘⢿⣿⡀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⣰⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀\n"
    "⠀⠀⠀⠀⢠⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣧⠀⠀⠀\n"
    "⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣆⠀⠀\n"
    "⠀⠀⠠⢾⠇⠀⠀⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡤.\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀sɪɪɪɪᴜᴜᴜᴜ⠀⠀ ⠀⠀⠀⠀⠀⠀\n"
)


@l313l.ar_cmd(pattern="كريس")
async def cr7(crr):
    await crr.edit(cr)
# ================================================================================================ #
# =========================================اوامر النسب================================================= #
# ================================================================================================ #

import html
import os
import random

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from JoKeRUB import l313l

from ..Config import Config
from l313l.razan.resources.strings import *
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event, reply_id
from . import spamwatch

plugin_category = "utils"


@l313l.ar_cmd(
    pattern="نسبة الحب(?:\s|$)([\s\S]*)",
    command=("نسبة الحب", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rza = random.choice(roz)
    await edit_or_reply(mention, f"نـسـبتكم انـت و [{muh}](tg://user?id={user.id}) هـي {rza} 😔🖤")
    
    
   
@l313l.ar_cmd(
    pattern="نسبة الانوثة(?:\s|$)([\s\S]*)",
    command=("نسبة الانوثة", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**- لكك دي هذا المطور زلمة وعلى راسك**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    sos = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الانوثة لـ [{muh}](tg://user?id={user.id}) هـي {sos}** 🥵🖤")

@l313l.ar_cmd(
    pattern="نسبة الغباء(?:\s|$)([\s\S]*)",
    command=("نسبة الغباء", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**0% ♥🙂**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الغباء لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 😂💔")

@l313l.ar_cmd(
    pattern="نسبة الكذب(?:\s|$)([\s\S]*)",
    command=("نسبة الكذب", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**0% ♥🙂**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الكذب لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 😂💔")

@l313l.ar_cmd(
    pattern="نسبة الذكاء(?:\s|$)([\s\S]*)",
    command=("نسبة الذكاء", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**100% ميحتاج تسوي نسبة الذكاء للمطور معروف**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الذكاء لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 🎈🧸")

@l313l.ar_cmd(
    pattern="نسبة الشذوذ(?:\s|$)([\s\S]*)",
    command=("نسبة الشذوذ", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**تاج راسك مطوري**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الشذوذ 🏳️‍🌈 لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 🎈🧸")

@l313l.ar_cmd(
    pattern="نسبة الدياثه(?:\s|$)([\s\S]*)",
    command=("نسبة الدياثه", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**تاج راسك مطوري**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الدياثه لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 🎈🧸")

@l313l.ar_cmd(
    pattern="نسبة الخيانه(?:\s|$)([\s\S]*)",
    command=("نسبة الخيانه", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**السيد ميخون يبقى وفي للكل**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة الخيانه 🙎🏼‍♀️ لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 🎈🧸")

@l313l.ar_cmd(
    pattern="نسبة الجمال(?:\s|$)([\s\S]*)",
    command=("نسبة الجمال", plugin_category),
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 5427469031:
        return await edit_or_reply(mention, f"**السيد حلو ميحتاج تقيمه 🤤**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    rzona = random.choice(rr7)
    await edit_or_reply(mention, f"**⏎︙ نسبة جماله 👩🏻‍🦳🧑🏻 لـ [{muh}](tg://user?id={user.id}) هـي {rzona}** 🎈🧸")
