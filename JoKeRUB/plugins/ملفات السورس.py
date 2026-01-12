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
    pattern="جميع_الاوامر$",
    command=("جميع_الاوامر", plugin_category),
    info={
        "header": "لعرض جميع أوامر السورس بدقة",
        "usage": "{tr}جميع_الاوامر",
    },
)
async def show_all_commands_exact(event):
    "لعرض جميع أوامر السورس بدقة"
    import os
    import re
    import ast
    from pathlib import Path
    
    plugins_dir = Path("JoKeRUB/plugins")
    all_commands = {}
    
    def extract_commands_from_file(file_path):
        """استخراج الأوامر من ملف بايثون"""
        commands = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # النمط 1: @l313l.ar_cmd(pattern="...")
            pattern1 = r'@l313l\.ar_cmd\s*\(\s*pattern\s*=\s*["\']([^"\']+)["\']'
            matches1 = re.findall(pattern1, content, re.DOTALL)
            commands.extend([('قياسي', cmd.strip()) for cmd in matches1])
            
            # النمط 2: @l313l.on(admin_cmd(pattern="..."))
            pattern2 = r'@l313l\.on\s*\(\s*admin_cmd\s*\(\s*pattern\s*=\s*["\']([^"\']+)["\']'
            matches2 = re.findall(pattern2, content, re.DOTALL)
            commands.extend([('أدمن', cmd.strip()) for cmd in matches2])
            
            # النمط 3: @l313l.on(events.NewMessage(pattern="..."))
            pattern3 = r'@l313l\.on\s*\(\s*events\.NewMessage\s*\(\s*pattern\s*=\s*["\']([^"\']+)["\']'
            matches3 = re.findall(pattern3, content, re.DOTALL)
            commands.extend([('حدث', cmd.strip()) for cmd in matches3])
            
            # النمط 4: command=("...", في @l313l.ar_cmd
            pattern4 = r'command\s*=\s*\(\s*["\']([^"\']+)["\']'
            matches4 = re.findall(pattern4, content)
            commands.extend([('أمر مباشر', cmd.strip()) for cmd in matches4])
            
            # النمط 5: .ar_cmd( بدون pattern
            pattern5 = r'\.ar_cmd\s*\(\s*["\']([^"\']+)["\']'
            matches5 = re.findall(pattern5, content)
            commands.extend([('ar_cmd قصير', cmd.strip()) for cmd in matches5])
            
        except Exception as e:
            return []
        
        return commands
    
    # جمع الأوامر من جميع الملفات
    for file_path in plugins_dir.rglob("*.py"):
        if file_path.is_file():
            file_name = file_path.name
            commands_list = extract_commands_from_file(file_path)
            if commands_list:
                all_commands[file_name] = commands_list
    
    # إنشاء الرسالة
    message = "**📋 جميع أوامر سورس الجوكر:**\n\n"
    total_commands_count = 0
    
    for file_name, commands in sorted(all_commands.items()):
        if commands:
            message += f"**━━━━━━━ {file_name.replace('.py', '')} ━━━━━━━**\n"
            
            for cmd_type, cmd_text in commands:
                total_commands_count += 1
                # تنظيف النص
                clean_cmd = cmd_text
                # إزالة الرموز الزائدة
                clean_cmd = clean_cmd.replace('(?:', '').replace(')?', '').replace('\\s', ' ')
                clean_cmd = clean_cmd.replace('|$', '').replace('$', '')
                
                message += f"• **{cmd_type}:** `{clean_cmd}`\n"
            
            message += "\n"
    
    message += f"**📊 الإحصائيات:**\n"
    message += f"• **عدد الملفات:** {len(all_commands)}\n"
    message += f"• **عدد الأوامر:** {total_commands_count}\n"
    message += f"• **البادئة:** `{Config.COMMAND_HAND_LER}`"
    
    # إذا كانت الرسالة طويلة، حفظها في ملف
    if len(message) > 4000:
        filename = "جميع_اوامر_الجوكر.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(message)
        
        await event.edit("**📁 تم حفظ جميع الأوامر في ملف نصي**")
        await event.client.send_file(
            event.chat_id,
            filename,
            caption="**📋 جميع أوامر سورس الجوكر**"
        )
        os.remove(filename)
    else:
        await edit_or_reply(event, message)


