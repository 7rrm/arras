mport os
import requests
import json
import random
import user_agent
import time
import asyncio
from requests import get, post
from re import findall
from random import choice, randint
from time import sleep
from os import chdir

try:
    from sqlite3 import connect
except ModuleNotFoundError:
    os.system("pip3 install sqlite3")
    from sqlite3 import connect

from telethon.sync import events, Button
from . import l313l
from ..Config import Config
from ..utils import Zed_Vip
from ..sql_helper.globals import gvarstatus
from ..core.session import tgbot

#################################
"""
هذه الدالة تقوم بارسال طلب لزيادة لايكات منشور على انستاغرام
باستخدام  LikesJet API.

Args:
    username: اسم مستخدم انستاغرام  بدون @.
    link: رابط منشور انستاغرام.
"""

async def likes_instagram_post(username, link):
    url = "https://api.likesjet.com/freeboost/7"
    useragent = user_agent.generate_user_agent()
    email = str(random.randint(100000, 999999)) + "@gmail.com"
    
    payload = json.dumps({
      "link": link,
      "instagram_username": "@" + username,
      "email": email
    })

    headers = {
      'User-Agent': useragent,
      'Accept': "application/json, text/plain, */*",
      'Content-Type': "application/json",
      'sec-ch-ua': "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\""
    }

    response = requests.post(url, data=payload, headers=headers)

    if "Success! You will receive likes within next few minutes." in response.text:
        url = "https://api.likesjet.com/list/7"
    
        payload = json.dumps({
        "email": email,
        "page": 1,
        "status": "All"
        })
    
        headers = {
        'User-Agent': useragent,
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\""
        }
    
        response = requests.post(url, data=payload, headers=headers)
        if "successfully" in response.text:
            return "**- تم رشـق 50 لايك انستـا .. بنجـاح ✅**"
        else:
            return "**- اووبـسس حدث خطـأ ❌**"
    else:
        return "**- انتظـر 24 سـاعـة .. ثم حـاول مجـدداً ⏳**"
#################################
"""
  هذه الدالة تقوم بإرسال طلب لزيادة مشاهدات فيديو تيك توك 
  باستخدام LikesJet API.

  Args:
  username: اسم مستخدم تيك توك بدون @.
  link: رابط فيديو تيك توك.
"""
  
async def view_tiktok_video(username, link):
    url = "https://api.likesjet.com/freeboost/3"
    useragent = user_agent.generate_user_agent()
    email = str(random.randint(100000, 999999)) + "@gmail.com"

    payload = json.dumps({
      "link": link,
      "tiktok_username": "@" + username,
      "email": email
    })

    headers = {
      'User-Agent': useragent,
      'Accept': "application/json, text/plain, */*",
      'Content-Type': "application/json",
      'sec-ch-ua': "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\""
    }

    response = requests.post(url, data=payload, headers=headers)
    #print(response.text)  #  لعرض  رد  API  

    if "Success! You will receive views on your tiktok video within next few minutes." in response.text:
        return "**- تم رشـق 1000 مشاهـدة تيك توك .. بنجـاح ✅**\n**- سـوف تصلك المشاهـدات خـلال دقائـق 🪁**"
    else:
        return "**- انتظـر 24 سـاعـة .. ثم حـاول مجـدداً ⏳**"
#################################

class delete:
    def __init__(self,connection = None):
        self.conn = connection
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS data(id,phone,random_hash,hash,cookie)")
        cursor.close()

    def send_code(self,id,phone):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute
            if len(exe("SELECT * FROM data WHERE id = '{}'".format(id)).fetchall()): self.remove(id)
            for x in range(2):
                try:
                    res = post("https://my.telegram.org/auth/send_password", data=f"phone={phone}")
                    
                    
                    if 'random_hash' in res.text:
                        res = res.json()
                        exe("INSERT INTO data(id,phone,random_hash) VALUES ('{}','{}','{}')".format(id,phone,res['random_hash']))
                        return 0 #ok
                    elif "too many tries" in res.text:
                        return 1 #limit
                    else:
                        return 2 #unknown
                except Exception as e:
                    if x < 4 : sleep(randint(1,3))
        finally:
            self.conn.commit()
            cursor.close()
        return 3 #server
    
    def check_code(self,id,code):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute
            phone,random_hash = next(exe("SELECT phone,random_hash FROM data WHERE id = '{}'".format(id)))
            for x in range(2):
                try:
                    res = post("https://my.telegram.org/auth/login", data=f"phone={phone}&random_hash={random_hash}&password={code}")
                    if res.text == "true":
                        cookies = res.cookies.get_dict()
                        req = get("https://my.telegram.org/delete", cookies=cookies)
                        if "Delete Your Account" in req.text:
                            _hash = findall("hash: '(\\w+)'",req.text)[0]
                            
                            exe("UPDATE data SET hash = '{}',cookie = '{}' WHERE id = '{}'".format(_hash,cookies['stel_token'],id))
                            return 0 #ok
                        else:
                            return 2 #unknown
                    elif "too many tries" in res.text:
                        return 1 #limit
                    elif "Invalid confirmation code!" in res.text:
                        return 4 #invalid code
                    else: print(res.text)
                except Exception as e:
                    if x < 4 : sleep(randint(1,3));print(type(e),e)
        except Exception as e:
             print(type(e),e)
        finally:
            self.conn.commit()
            cursor.close()
        return 3 #server

    def delete(self,id):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute

            _hash,cookies = next(exe("SELECT hash,cookie FROM data WHERE id = '{}'".format(id)))
            for x in range(2):
                try:
                    res = post("https://my.telegram.org/delete/do_delete", cookies={'stel_token':cookies}, data=f"hash={_hash}&message=goodby").text
                    if res == "true":
                        return 0 #ok
                    else:
                        return 5
                except Exception as e:
                    pass
        finally:
            self.conn.commit()
            cursor.close()
        return 3 #server
    def remove(self,id):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute
            exe("DELETE FROM data WHERE id = '{}'".format(id))
        finally:
            self.conn.commit()
            cursor.close()


conn = connect("dataa.db")
delete = delete(connection = conn)
dd = []
kk = []
nn = []
link_insta = None
user_insta = None
link_tiktok = None
user_tiktok = None
steps = {}
@l313l.tgbot.on(events.NewMessage(func = lambda  e: e.is_private))
async def robot(event):
    global steps, user_insta, link_insta, user_tiktok, link_tiktok
    text = event.raw_text
    id = event.sender_id
    zid = 5427469031
    if gvarstatus("ZThon_Vip") is None:
        zid = 5427469031
    else:
        zid = int(gvarstatus("ZThon_Vip"))
    try:
        if "• إلغاء •" in text or text == "• إلغاء •":
            if int(id) in kk:
                kk.remove(int(id))
                del steps[id]
            return await l313l.tgbot.send_message(event.chat_id, "**• تم الغاء حذف الحساب ✅**")
        if "/exit" in text:
            if int(id) in nn:
                nn.remove(int(id))
                del steps[id]
            return await l313l.tgbot.send_message(event.chat_id, "**• تم الغـاء عمليـة الرشـق .. بنجـاح ☑️**")
        if "حذف حسابي" in text or text == "احذف حسابي":
            kk.append(int(id))
            steps[id] = 1
            await l313l.tgbot.send_message(event.chat_id, "**• مرحبًا بك عزيزي\n• في بوت حذف حسابات تيليجرام\n• يمكنك إرسال رقمك عبر الزر أدناه**", buttons = [[Button.request_phone("• اضغـط لـ الحـذف •", resize = True)]])
            delete.remove(id)
            return
        if ("/insta" in text) and id == Config.OWNER_ID and id == zid:
            nn.append(int(id))
            steps[id] = 3
            await l313l.tgbot.send_message(event.chat_id, "**• مرحبًا بك عزيزي 🫂\n• في قسم رشق لايكات انستكرام ♥️\n• قم بإرسال يوزر حسابك الانستا الان 🌀\n\n• لـ الالغـاء والخـروج ارسـل /exit** 🔚")
            delete.remove(id)
            return
        if ("/tiktok" in text) and id == Config.OWNER_ID and id == zid:
            nn.append(int(id))
            steps[id] = 5
            await l313l.tgbot.send_message(event.chat_id, "**• مرحبًا بك عزيزي 🫂\n• في قسم رشق مشاهدات تيك توك 👁‍🗨\n• قم بإرسال يوزر حسابك تيك توك الان 🌀\n\n• لـ الالغـاء والخـروج ارسـل /exit** 🔚")
            delete.remove(id)
            return
        step = steps[id]
        if step  == 1:
            if event.contact:
                phone = "+"+event.contact.to_dict()['phone_number']
                res = delete.send_code(id,phone)
                if not res:
                    steps[id] = 2
                    return await l313l.tgbot.send_message(event.chat_id, "**• تم إرسال الرمز إليك ✅\n• يرجى ارسـال الكـود 🗒**", buttons = [[Button.text("• إلغاء •", resize = True)]])
                elif res == 1:
                    return await l313l.tgbot.send_message(event.chat_id, "**• اخذت فلود تكرار\n• لا يمكنك حذف الحساب الان\n• حاول مرة أخرى بعد بضع ساعات**")
                elif res == 2:
                     return await l313l.tgbot.send_message(event.chat_id, "**• اووبس حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**")
                else:
                    return await l313l.tgbot.send_message(event.chat_id, "**• اووبس حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**")
            else:
                return await l313l.tgbot.send_message(event.chat_id, "**• يرجى استخدام الأزرار فقط**")
        if step == 2:
            if event.forward:
                code = event.raw_text.split("بك:\n")[1].split("\n")[0]
                res = delete.check_code(id,code)
                if not res:
                    del steps[id]
                    msg = await l313l.tgbot.send_message(event.chat_id, "**• الى اللقاء .. في امان الله 🔚**")
                    #sleep(1);input('wait ')
                    delete.delete(id)
                    delete.remove(id)
                elif res == 1:
                    return await l313l.tgbot.send_message(event.chat_id, "**• اخذت فلود تكرار\n• لا يمكنك حذف الحساب الان\n• حاول مرة أخرى بعد بضع ساعات**")
                elif res == 2:
                     return await l313l.tgbot.send_message(event.chat_id, "**• اووبس حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**")
                elif res == 3:
                     return await l313l.tgbot.send_message(event.chat_id, "**• كود غير صالح أو منتهي ؟!**")
                else:
                    return await l313l.tgbot.send_message(event.chat_id, "**• اووبس حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**")
            else:
                code = event.raw_text
                res = delete.check_code(id,code)
                if not res:
                    del steps[id]
                    msg = await l313l.tgbot.send_message(event.chat_id, "**• الى اللقاء .. في امان الله 🔚**")
                    #sleep(1);input('wait ')
                    delete.delete(id)
                    delete.remove(id)
                elif res == 1:
                    return await l313l.tgbot.send_message(event.chat_id, "**• اخذت فلود تكرار\n• لا يمكنك حذف الحساب الان\n• حاول مرة أخرى بعد بضع ساعات**")
                elif res == 2:
                     return await l313l.tgbot.send_message(event.chat_id, "**• اووبس حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**")
                elif res == 3:
                     return await l313l.tgbot.send_message(event.chat_id, "**• كود غير صالح أو منتهي ؟!**")
                else:
                    return await l313l.tgbot.send_message(event.chat_id, "**• اووبس حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**")
        if step == 3:
            if event.raw_text:
                user_insta = event.raw_text
                steps[id] = 4
                return await l313l.tgbot.send_message(event.chat_id, "**• حسنـاً .. عزيزي 🙇🏻\n• ارسـل رابـط المنشور الان 🖇\n• وسوف اقوم برشق 50 لايك في ثواني 💘\n\n• لـ الالغـاء والخـروج ارسـل /exit** 🔚")
        if step == 4:
            if text.startswith("http"):
                link_insta = event.raw_text
                res = await likes_instagram_post(user_insta, link_insta)
                del steps[id]
                return await l313l.tgbot.send_message(event.chat_id, res)
        if step == 5:
            if event.raw_text:
                user_tiktok = event.raw_text
                steps[id] = 6
                return await l313l.tgbot.send_message(event.chat_id, "**• حسنـاً .. عزيزي 🙇🏻\n• ارسـل رابـط الفيديـو الان 🖇\n• وسوف اقوم برشق 1000 مشاهدة في دقائق 👀\n\n• لـ الالغـاء والخـروج ارسـل /exit** 🔚")
        if step == 6:
            if text.startswith("http"):
                link_tiktok = event.raw_text
                res = await view_tiktok_video(user_tiktok, link_tiktok)
                del steps[id]
                return await l313l.tgbot.send_message(event.chat_id, res)
    except Exception as e:
        print(type(e),e)
