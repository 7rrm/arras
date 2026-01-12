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
    pattern="الاوامر$",
    command=("الاوامر", plugin_category),
    info={
        "header": "لعرض جميع أوامر السورس بشكل منظم",
        "usage": "{tr}الاوامر",
    },
)
async def show_all_commands(event):
    "لعرض جميع أوامر السورس بشكل منظم"
    import os
    import re
    from collections import defaultdict
    
    commands_dict = defaultdict(list)
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
                        # استخراج جميع الأوامر من الملف
                        matches = re.findall(pattern, content)
                        if matches:
                            for cmd in matches:
                                # البحث عن وصف الأمر
                                desc_pattern = r'info=\{[\s\S]*?"header":\s*["\']([^"\']+)["\'][\s\S]*?\}'
                                desc_match = re.search(desc_pattern, content)
                                description = desc_match.group(1).strip() if desc_match else "بدون وصف"
                                
                                # البحث عن الاستخدام
                                usage_pattern = r'"usage":\s*["\']([^"\']+)["\']'
                                usage_match = re.search(usage_pattern, content)
                                usage = usage_match.group(1) if usage_match else cmd
                                
                                commands_dict[file].append({
                                    'command': cmd,
                                    'description': description,
                                    'usage': usage
                                })
                except Exception as e:
                    continue
    
    # إنشاء الرسالة المنظمة
    message = "**📋 قائمة جميع أوامر الجوكر:**\n\n"
    total_commands = 0
    total_plugins = len(commands_dict)
    
    # ترتيب الملفات أبجدياً
    sorted_plugins = sorted(commands_dict.items(), key=lambda x: x[0])
    
    for plugin_name, commands in sorted_plugins:
        message += f"**━━━━━━ {plugin_name.replace('.py', '')} ━━━━━━**\n"
        
        for cmd_info in commands:
            total_commands += 1
            # تنظيف صيغة الأمر
            clean_cmd = cmd_info['command'].replace('(', '').replace(')', '').replace('|', ' | ')
            message += f"• **الأمر:** `{clean_cmd}`\n"
            message += f"  **الوصف:** {cmd_info['description']}\n"
            message += f"  **الاستخدام:** `{cmd_info['usage']}`\n\n"
    
    message += f"**📊 الإحصائيات:**\n"
    message += f"• **عدد الملفات:** {total_plugins}\n"
    message += f"• **عدد الأوامر:** {total_commands}\n"
    message += f"• **البادئة:** `{Config.COMMAND_HAND_LER}`\n"
    message += f"• **المساعد:** @{Config.TG_BOT_USERNAME if hasattr(Config, 'TG_BOT_USERNAME') else 'بدون'}"
    
    # تقسيم الرسالة إذا كانت طويلة
    if len(message) > 4000:
        # حفظ في ملف بدلاً من تقسيمه
        with open("جميع_الاوامر.txt", "w", encoding="utf-8") as f:
            f.write(message)
        
        await event.edit("**📁 تم حفظ جميع الأوامر في ملف نصي**")
        await event.client.send_file(
            event.chat_id,
            "جميع_الاوامر.txt",
            caption="**📋 قائمة جميع أوامر الجوكر**"
        )
        os.remove("جميع_الاوامر.txt")
    else:
        await edit_or_reply(event, message)
