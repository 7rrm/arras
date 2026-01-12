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
        "header": "لعرض جميع أوامر السورس بشكل دقيق",
        "usage": "{tr}الاوامر_المحسنة",
    },
)
async def show_all_commands_enhanced(event):
    "لعرض جميع أوامر السورس بشكل دقيق"
    import os
    import re
    from collections import defaultdict
    
    commands_dict = defaultdict(list)
    plugins_dir = "JoKeRUB/plugins"
    
    # أنماط متعددة للبحث عن الأوامر
    patterns = [
        # النمط القياسي
        r'\.ar_cmd\(pattern=["\']([^"\']+)["\']',
        # الأوامر بـ @l313l.on
        r'@l313l\.on\(admin_cmd\(pattern=["\']([^"\']+)["\']',
        # الأوامر بـ @l313l.on مباشرة
        r'@l313l\.on\(events\.NewMessage\(pattern=["\']([^"\']+)["\']',
        # الأوامر مع command=
        r'command=["\']([^"\']+)["\']',
    ]
    
    for root, dirs, files in os.walk(plugins_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # البحث بجميع الأنماط
                        for pattern in patterns:
                            matches = re.findall(pattern, content)
                            if matches:
                                for cmd in matches:
                                    # تنظيف الأمر
                                    clean_cmd = cmd.strip()
                                    if clean_cmd and clean_cmd not in ["tools", "utils", "الاوامر"]:
                                        # البحث عن وصف الأمر
                                        desc_pattern = r'info=\{[\s\S]*?"header":\s*["\']([^"\']+)["\'][\s\S]*?\}'
                                        desc_match = re.search(desc_pattern, content)
                                        description = desc_match.group(1).strip() if desc_match else "بدون وصف"
                                        
                                        commands_dict[file].append({
                                            'command': clean_cmd,
                                            'description': description,
                                            'pattern': pattern_type(pattern)
                                        })
                except Exception as e:
                    continue
    
    # دالة لتحديد نوع النمط
    def pattern_type(pattern):
        if "ar_cmd" in pattern:
            return "قياسي"
        elif "admin_cmd" in pattern:
            return "أدمن"
        elif "events.NewMessage" in pattern:
            return "حدث"
        elif "command=" in pattern:
            return "أمر مباشر"
        else:
            return "مجهول"
    
    # عرض النتائج
    message = "**📋 قائمة جميع أوامر الجوكر (محسنة):**\n\n"
    total_commands = 0
    
    # التركيز على ملف gggi أولاً
    if 'gggi.py' in commands_dict:
        message += "**━━━━━━━ gggi.py (مفصل) ━━━━━━━**\n"
        for cmd_info in commands_dict['gggi.py']:
            total_commands += 1
            message += f"• **الأمر:** `{cmd_info['command']}`\n"
            message += f"  **النوع:** {cmd_info['pattern']}\n"
            message += f"  **الوصف:** {cmd_info['description']}\n\n"
    
    # باقي الملفات
    for plugin_name, commands in sorted(commands_dict.items()):
        if plugin_name != 'gggi.py':
            message += f"**━━━━━━━ {plugin_name.replace('.py', '')} ━━━━━━━**\n"
            for cmd_info in commands:
                total_commands += 1
                message += f"• **الأمر:** `{cmd_info['command']}`\n"
                message += f"  **النوع:** {cmd_info['pattern']}\n"
                message += f"  **الوصف:** {cmd_info['description']}\n\n"
    
    message += f"**📊 الإحصائيات:**\n"
    message += f"• **عدد الملفات:** {len(commands_dict)}\n"
    message += f"• **عدد الأوامر:** {total_commands}\n"
    message += f"• **البادئة:** `{Config.COMMAND_HAND_LER}`"
    
    await edit_or_reply(event, message)
