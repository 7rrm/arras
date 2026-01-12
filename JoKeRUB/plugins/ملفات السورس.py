from JoKeRUB import l313l
import pkg_resources
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils, parse_pre, yaml_format
from ..Config import Config
import json
import requests
import os
from telethon import events 
plugin_category = "tools"

#Reda

@l313l.ar_cmd(pattern="المكاتب")
async def reda(event):
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
    for i in installed_packages])
    list = "**قائمة المكاتب المثبته**\n"
    for i in installed_packages_list:
        list += f"{i}\n"
    list += "**سورس الجوكر**"
    await edit_or_reply(event, list)

@l313l.ar_cmd(
    pattern="الملفات$",
    command=("الملفات", plugin_category),
    info={
        "header": "To list all plugins in JoKeRUB.",
        "usage": "{tr}plugins",
    },
)
async def _(event):
    "To list all plugins in JoKeRUB"
    cmd = "ls JoKeRUB/plugins"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = f"**[الجوكر](tg://need_update_for_some_feature/) الـمـلفـات:**\n{o}"
    await edit_or_reply(event, OUTPUT)


@l313l.ar_cmd(
    pattern="فاراتي$",
    command=("فاراتي", plugin_category),
    info={
        "header": "To list all environment values in JoKeRUB.",
        "description": "to show all heroku vars/Config values in your JoKeRUB",
        "usage": "{tr}env",
    },
)
async def _(event):
    "To show all config values in JoKeRUB"
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (
        f"**[الجوكر](tg://need_update_for_some_feature/) قـائمـة الـفـارات:**\n\n\n{o}\n\n**انتبه هنالك معلومات حساسة لا تُعطِها لشخص غير موثوق**"
    )
    await edit_or_reply(event, "**تم ارسال المعلومات في الرسائل المحفوضة \nانتبه من الاشخاص الي يطلبون منك كتابة هذا الامر يريد ان يخترقك!**")
    await l313l.send_message("me", OUTPUT)

@l313l.ar_cmd(
    pattern="متى$",
    command=("متى", plugin_category),
    info={
        "header": "To get date and time of message when it posted.",
        "usage": "{tr}when <reply>",
    },
)
async def _(event):
    "To get date and time of message when it posted."
    reply = await event.get_reply_message()
    if reply:
        try:
            result = reply.fwd_from.date
        except Exception:
            result = reply.date
    else:
        result = event.date
    await edit_or_reply(
        event, f"**᯽︙ نـشـرت هـذه الـرسالة فـي  :** `{yaml_format(result)}`"
    )
@l313l.ar_cmd(pattern="رابط مباشر")
async def upload_reda(event):
    r = await event.get_reply_message()
    if r is None:
        return await edit_delete(event, "**᯽︙قم بالرد على ملف لرفعهُ**")
    if r.media is None:
        return await edit_delete(event, "**᯽︙قم بالرد على ملف لرفعهُ**")
    file = await event.client.download_media(r, Config.TEMP_DIR)
    await edit_or_reply(event, "**᯽︙ يُجري عملية الرفع . .**")
    payload = {}
    image = {"file": open(file, "rb")}
    response = requests.request("POST", "https://api.anonfiles.com/upload", files=image, data = payload)
    res = response.json()
    if res["status"] == False:
        er = res["error"]["message"]
        return await edit_delete(event, f"حدث خطأ عند رفع الملف\n{er}") 
    url = res["data"]["file"]["url"]["short"]
    size = res["data"]["file"]["metadata"]["size"]["readable"]
    await edit_or_reply(event, f"**تم رفع الملف ✓**\n**᯽︙ الرابط:** {url}\n**᯽︙الحجم:** {size}")
    os.remove(file)


@l313l.ar_cmd(
    pattern="الاوامرر$",
    command=("الاوامرر", plugin_category),
    info={
        "header": "لعرض جميع أوامر السورس",
        "usage": "{tr}الاوامر",
    },
)
async def show_all_commands(event):
    "لعرض جميع أوامر السورس"
    import os
    import re
    
    commands_list = []
    plugins_dir = "JoKeRUB/plugins"
    
    # البحث عن جميع الأوامر
    pattern = r'\.ar_cmd\(pattern=["\']([^"\']+)["\']'
    
    for root, dirs, files in os.walk(plugins_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.findall(pattern, content)
                        for cmd in matches:
                            # البحث عن وصف الأمر
                            desc_pattern = r'info=\{.*?"header":\s*["\']([^"\']+)["\']'
                            desc_match = re.search(desc_pattern, content, re.DOTALL)
                            description = desc_match.group(1) if desc_match else "لا يوجد وصف"
                            
                            commands_list.append({
                                'command': cmd,
                                'plugin': file,
                                'description': description
                            })
                except:
                    continue
    
    # ترتيب الأوامر
    commands_list.sort(key=lambda x: x['command'])
    
    # إنشاء الرسالة
    message = "**📋 قائمة جميع أوامر الجوكر:**\n\n"
    
    current_plugin = ""
    for cmd_info in commands_list:
        if cmd_info['plugin'] != current_plugin:
            current_plugin = cmd_info['plugin']
            message += f"\n**┏━━ {current_plugin} ━━**\n"
        
        message += f"**┣ ⦗** `{cmd_info['command']}` **⦘**\n"
        message += f"**┗** {cmd_info['description']}\n"
    
    message += f"\n**📊 الإحصائيات:**\n"
    message += f"**• عدد الملفات:** {len(set(c['plugin'] for c in commands_list))}\n"
    message += f"**• عدد الأوامر:** {len(commands_list)}\n"
    message += f"**• البادئة:** `{Config.COMMAND_HAND_LER}`"
    
    # تقسيم الرسالة إذا كانت طويلة
    if len(message) > 4096:
        parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
        for part in parts:
            await event.edit(part)
            await asyncio.sleep(1)
    else:
        await edit_or_reply(event, message)
