import os
import requests
import re
import random
import sqlite3
from random import randint
from time import sleep
from telethon.sync import events, Button
from . import l313l
from ..Config import Config

#################################

class DeleteAccount:
    def __init__(self, connection=None):
        self.conn = connection
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS data(id,phone,random_hash,hash,cookie)")
        cursor.close()

    def send_code(self, id, phone):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute
            if len(exe("SELECT * FROM data WHERE id = '{}'".format(id)).fetchall()):
                self.remove(id)
            for x in range(2):
                try:
                    res = requests.post("https://my.telegram.org/auth/send_password", data=f"phone={phone}")
                    
                    if 'random_hash' in res.text:
                        res = res.json()
                        exe("INSERT INTO data(id,phone,random_hash) VALUES ('{}','{}','{}')".format(id, phone, res['random_hash']))
                        return 0  # ok
                    elif "too many tries" in res.text:
                        return 1  # limit
                    else:
                        return 2  # unknown
                except Exception as e:
                    if x < 4:
                        sleep(random.randint(1, 3))
        finally:
            self.conn.commit()
            cursor.close()
        return 3  # server
    
    def check_code(self, id, code):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute
            phone, random_hash = next(exe("SELECT phone,random_hash FROM data WHERE id = '{}'".format(id)))
            for x in range(2):
                try:
                    res = requests.post("https://my.telegram.org/auth/login", data=f"phone={phone}&random_hash={random_hash}&password={code}")
                    if res.text == "true":
                        cookies = res.cookies.get_dict()
                        req = requests.get("https://my.telegram.org/delete", cookies=cookies)
                        if "Delete Your Account" in req.text:
                            _hash = re.findall("hash: '(\\w+)'", req.text)[0]
                            
                            exe("UPDATE data SET hash = '{}',cookie = '{}' WHERE id = '{}'".format(_hash, cookies['stel_token'], id))
                            return 0  # ok
                        else:
                            return 2  # unknown
                    elif "too many tries" in res.text:
                        return 1  # limit
                    elif "Invalid confirmation code!" in res.text:
                        return 4  # invalid code
                except Exception as e:
                    if x < 4:
                        sleep(random.randint(1, 3))
        except Exception as e:
            print(f"Error in check_code: {type(e).__name__}: {e}")
        finally:
            self.conn.commit()
            cursor.close()
        return 3  # server

    def delete_account(self, id):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute

            _hash, cookies = next(exe("SELECT hash,cookie FROM data WHERE id = '{}'".format(id)))
            for x in range(2):
                try:
                    res = requests.post("https://my.telegram.org/delete/do_delete", 
                                      cookies={'stel_token': cookies}, 
                                      data=f"hash={_hash}&message=goodby").text
                    if res == "true":
                        return 0  # ok
                    else:
                        return 5
                except Exception as e:
                    pass
        finally:
            self.conn.commit()
            cursor.close()
        return 3  # server
    
    def remove(self, id):
        try:
            cursor = self.conn.cursor()
            exe = cursor.execute
            exe("DELETE FROM data WHERE id = '{}'".format(id))
        finally:
            self.conn.commit()
            cursor.close()

# إنشاء اتصال قاعدة البيانات
conn = sqlite3.connect("dataa.db")
delete_manager = DeleteAccount(connection=conn)

# قائمة لتتبع المستخدمين النشطين
active_users = []
steps = {}

def clear_user_session(user_id):
    """مسح جلسة المستخدم من جميع القوائم"""
    if user_id in active_users:
        active_users.remove(user_id)
    if user_id in steps:
        del steps[user_id]

@l313l.tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def account_deletion_handler(event):
    global steps, active_users
    text = event.raw_text
    user_id = event.sender_id
    
    try:
        # إذا كان المستخدم يرسل /start أو أي شيء آخر وهو في وضع الحذف
        if user_id in active_users and (text == "/start" or text == "رجوع" or text == "الغاء"):
            clear_user_session(user_id)
            return await l313l.tgbot.send_message(
                event.chat_id,
                "**• تم الخروج من وضع حذف الحساب\n• يمكنك الآن استخدام البوت بشكل طبيعي**",
                buttons=Button.clear()
            )
        
        # إخفاء الكيبورد
        if text == "• اخفاء الكيبورد •":
            return await l313l.tgbot.send_message(
                event.chat_id,
                "**• تم إخفاء الكيبورد ✅\n• لإعادة إظهاره أرسل 'حذف حسابي'**",
                buttons=Button.clear()
            )
        
        # إلغاء العملية
        if "• إلغاء •" in text or text == "• إلغاء •":
            clear_user_session(user_id)
            return await l313l.tgbot.send_message(
                event.chat_id,
                "**• تم إلغاء عملية حذف الحساب ✅**",
                buttons=Button.clear()
            )
        
        # بدء عملية حذف الحساب
        if "حذف حسابي" in text or text == "احذف حسابي":
            clear_user_session(user_id)
            active_users.append(user_id)
            steps[user_id] = 1
            await l313l.tgbot.send_message(
                event.chat_id,
                "**• مرحبًا بك عزيزي\n• في بوت حذف حسابات تيليجرام\n• يمكنك إرسال رقمك عبر الزر أدناه**",
                buttons=[
                    [Button.request_phone("• اضغط لحذف الحساب •", resize=True)],
                    [Button.text("• اخفاء الكيبورد •", resize=True)]
                ]
            )
            delete_manager.remove(user_id)
            return
        
        # متابعة خطوات حذف الحساب فقط إذا كان المستخدم في القائمة
        if user_id not in active_users:
            return  # دع الرسالة تمر للوظائف الأخرى في البوت
            
        if user_id not in steps:
            clear_user_session(user_id)
            return
            
        step = steps[user_id]
        
        # الخطوة 1: الحصول على رقم الهاتف
        if step == 1:
            if event.contact:
                phone = "+" + event.contact.to_dict()['phone_number']
                res = delete_manager.send_code(user_id, phone)
                
                if res == 0:
                    steps[user_id] = 2
                    return await l313l.tgbot.send_message(
                        event.chat_id,
                        "**• تم إرسال الرمز إليك ✅\n• يرجى إرسال الكود 🗒**",
                        buttons=[[Button.text("• إلغاء •", resize=True)]]
                    )
                elif res == 1:
                    clear_user_session(user_id)
                    return await l313l.tgbot.send_message(
                        event.chat_id,
                        "**• تم تجاوز الحد المسموح للمحاولات\n• لا يمكنك حذف الحساب الآن\n• حاول مرة أخرى بعد بضع ساعات**",
                        buttons=Button.clear()
                    )
                else:
                    clear_user_session(user_id)
                    return await l313l.tgbot.send_message(
                        event.chat_id,
                        "**• حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**",
                        buttons=Button.clear()
                    )
            else:
                clear_user_session(user_id)
                return await l313l.tgbot.send_message(
                    event.chat_id,
                    "**• تم إلغاء العملية\n• لإعادة المحاولة أرسل 'حذف حسابي'**",
                    buttons=Button.clear()
                )
        
        # الخطوة 2: التحقق من الكود
        if step == 2:
            # استخراج الكود إذا كان مرسلاً كتوجيه
            if event.forward:
                code = event.raw_text.split("بك:\n")[1].split("\n")[0]
            else:
                code = event.raw_text
            
            res = delete_manager.check_code(user_id, code)
            
            if res == 0:
                clear_user_session(user_id)
                await l313l.tgbot.send_message(
                    event.chat_id,
                    "**• إلى اللقاء .. في أمان الله 🔚**",
                    buttons=Button.clear()
                )
                
                delete_manager.delete_account(user_id)
                delete_manager.remove(user_id)
                
            elif res == 1:
                clear_user_session(user_id)
                return await l313l.tgbot.send_message(
                    event.chat_id,
                    "**• تم تجاوز الحد المسموح للمحاولات\n• لا يمكنك حذف الحساب الآن\n• حاول مرة أخرى بعد بضع ساعات**",
                    buttons=Button.clear()
                )
            elif res == 4:
                clear_user_session(user_id)
                return await l313l.tgbot.send_message(
                    event.chat_id,
                    "**• الكود غير صالح أو منتهي الصلاحية!\n• لإعادة المحاولة أرسل 'حذف حسابي'**",
                    buttons=Button.clear()
                )
            else:
                clear_user_session(user_id)
                return await l313l.tgbot.send_message(
                    event.chat_id,
                    "**• حدث خطأ غير معروف\n• يرجى المحاولة مرة أخرى بعد بضع دقائق**",
                    buttons=Button.clear()
                )
    
    except Exception as e:
        print(f"حدث خطأ في المعالج: {type(e).__name__}: {e}")
        clear_user_session(user_id)
        await l313l.tgbot.send_message(
            event.chat_id,
            "**• حدث خطأ غير متوقع\n• تم الخروج من وضع الحذف\n• يمكنك إعادة المحاولة لاحقاً**",
            buttons=Button.clear()
                )
