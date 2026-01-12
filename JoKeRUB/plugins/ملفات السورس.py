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
    pattern="اوامر_الدقيقة$",
    command=("اوامر_الدقيقة", plugin_category),
    info={
        "header": "لعرض جميع أوامر السورس بدقة متناهية",
        "usage": "{tr}اوامر_الدقيقة",
    },
)
async def show_all_commands_precise(event):
    "لعرض جميع أوامر السورس بدقة متناهية"
    import os
    import re
    
    plugins_dir = "JoKeRUB/plugins"
    all_commands = {}
    
    def extract_all_patterns(content):
        """استخراج جميع الأنماط من المحتوى"""
        patterns = []
        
        # 1. أنماط @l313l.on(events.NewMessage(pattern=r'...'))
        pattern1 = r"@l313l\.on\s*\(\s*events\.NewMessage\s*\(\s*pattern\s*=\s*r?['\"]([^'\"]+)['\"]"
        matches1 = re.findall(pattern1, content, re.DOTALL)
        patterns.extend([('حدث', match.strip()) for match in matches1])
        
        # 2. أنماط @l313l.ar_cmd(pattern="...")
        pattern2 = r'@l313l\.ar_cmd\s*\(\s*pattern\s*=\s*["\']([^"\']+)["\']'
        matches2 = re.findall(pattern2, content, re.DOTALL)
        patterns.extend([('قياسي', match.strip()) for match in matches2])
        
        # 3. أنماط pattern=r'^\.(.*)$' - أي شيء بعد r'
        pattern3 = r"pattern\s*=\s*r['\"]([^'\"]+)['\"]"
        matches3 = re.findall(pattern3, content, re.DOTALL)
        patterns.extend([('نمط خام', match.strip()) for match in matches3])
        
        # 4. أنماط pattern='.أمر' بدون r
        pattern4 = r"pattern\s*=\s*['\"]([^'\"]+)['\"]"
        matches4 = re.findall(pattern4, content, re.DOTALL)
        # تصفية المطابقات من pattern3
        for match in matches4:
            if match not in [m[1] for m in patterns]:
                patterns.extend([('نمط عادي', match.strip())])
        
        # 5. البحث عن أي .on( أو .ar_cmd(
        pattern5 = r'(?:@l313l\.on|@l313l\.ar_cmd)\([^)]*pattern\s*=\s*[^)]+\)'
        matches5 = re.findall(pattern5, content, re.DOTALL)
        for match in matches5:
            # استخراج النمط من المطابقة الكاملة
            pattern_match = re.search(r"pattern\s*=\s*['\"]([^'\"]+)['\"]", match)
            if pattern_match:
                cmd = pattern_match.group(1)
                if '.on(' in match:
                    patterns.append(('حدث', cmd.strip()))
                else:
                    patterns.append(('قياسي', cmd.strip()))
        
        return patterns
    
    # مسح جميع الملفات
    for root, dirs, files in os.walk(plugins_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    patterns = extract_all_patterns(content)
                    if patterns:
                        all_commands[file] = patterns
                        
                except Exception as e:
                    continue
    
    # إنشاء الرسالة
    if all_commands:
        message = "**📋 جميع أوامر سورس الجوكر (الدقيقة):**\n\n"
        total_commands = 0
        
        for file_name, commands in sorted(all_commands.items()):
            if commands:
                message += f"**━━━━━━━ {file_name.replace('.py', '')} ━━━━━━━**\n"
                
                for cmd_type, cmd_text in commands:
                    total_commands += 1
                    # تنظيف النص - إزالة r وعلامات الاقتباس الزائدة
                    clean_cmd = cmd_text
                    clean_cmd = clean_cmd.replace('r"', '').replace("r'", '')
                    clean_cmd = clean_cmd.replace('^\.', '.')  # إزالة ^\.
                    
                    message += f"• **{cmd_type}:** `{clean_cmd}`\n"
                
                message += "\n"
        
        message += f"**📊 الإحصائيات:**\n"
        message += f"• **عدد الملفات:** {len(all_commands)}\n"
        message += f"• **عدد الأوامر:** {total_commands}\n"
        message += f"• **البادئة:** `{Config.COMMAND_HAND_LER}`"
        
        await edit_or_reply(event, message)
    else:
        await edit_or_reply(event, "**❌ لم يتم العثور على أي أوامر!**")
