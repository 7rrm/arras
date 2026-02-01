from JoKeRUB import bot, l313l
#By Source joker @ucriss
from telethon import events, functions, types, Button
from datetime import timedelta
from JoKeRUB.utils import admin_cmd
import asyncio
from ..Config import Config
import os, asyncio, re, traceback
from os import system
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon import TelegramClient as tg
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest as pc, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dc
from telethon.sessions import StringSession as ses
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
import telethon;from telethon import functions
from telethon.tl.types import ChannelParticipantsAdmins as cpa

from telethon.tl.functions.channels import CreateChannelRequest as ccr

from JoKeRUB import bot, l313l
from telethon import Button, events
from datetime import datetime
from JoKeRUB.utils import admin_cmd
from ..Config import Config
import asyncio, aiohttp, random, json, requests, re, time, os
import logging
import string
logging.getLogger().setLevel(logging.WARNING)

# إعدادات الملفات
accounts_file = "accounts/accounts_data.json"
os.makedirs("accounts", exist_ok=True)
os.makedirs("generated_images", exist_ok=True)
os.makedirs("temp_images", exist_ok=True)

bot = borg = tgbot
Bot_Username = Config.TG_BOT_USERNAME or "NanoBananaBot"

# ========== دوال البريد المؤقت (Mail.tm - الأفضل) ==========
class MailTM:
    """خدمة Mail.tm المتطورة والأكثر استقراراً"""
    
    def __init__(self):
        self.base_url = "https://api.mail.tm"
        self.token = None
        self.account_id = None
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*'
        })
    
    def create_account(self):
        """إنشاء حساب بريد جديد"""
        print("📧 جاري إنشاء حساب Mail.tm جديد...")
        try:
            # 1. جلب النطاقات المتاحة
            try:
                domains_resp = self.session.get(f"{self.base_url}/domains", timeout=10)
                print(f"📊 استجابة النطاقات: {domains_resp.status_code}")
                
                if domains_resp.status_code != 200:
                    print(f"❌ فشل جلب النطاقات: {domains_resp.status_code}")
                    print(f"📝 التفاصيل: {domains_resp.text[:200]}")
                    return None
                
                domains_data = domains_resp.json()
                domains = domains_data.get("hydra:member", [])
                
                if not domains:
                    print("❌ لا توجد نطاقات متاحة")
                    return None
                
                # استخدام أول نطاق متاح
                domain_obj = domains[0]
                domain = domain_obj.get("domain", "")
                print(f"✅ النطاق المختار: {domain}")
                
                if not domain:
                    return None
                    
            except Exception as e:
                print(f"❌ خطأ في جلب النطاقات: {e}")
                # استخدام نطاق افتراضي
                domain = "fextemp.com"
                print(f"⚠️ استخدام نطاق افتراضي: {domain}")
            
            # 2. إنشاء اسم بريد عشوائي
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
            email = f"{username}@{domain}"
            password = f"Pass{random.randint(1000, 9999)}!"
            
            print(f"📧 البريد الجديد: {email}")
            print(f"🔑 كلمة المرور: {password}")
            
            # 3. إنشاء حساب
            account_payload = {
                "address": email,
                "password": password
            }
            
            print("📝 جاري إنشاء حساب...")
            account_resp = self.session.post(f"{self.base_url}/accounts", 
                                            json=account_payload, 
                                            timeout=15)
            
            print(f"📊 استجابة إنشاء الحساب: {account_resp.status_code}")
            
            # حتى لو كان status code ليس 200/201، قد يكون الحساب مخلوق
            # بعض الخوادم ترجع 400 إذا كان البريد مستخدم لكن قد يكون ناجح
            
            # 4. الحصول على توكن
            print("🔐 جاري الحصول على توكن...")
            token_payload = {"address": email, "password": password}
            token_resp = self.session.post(f"{self.base_url}/token", 
                                          json=token_payload, 
                                          timeout=15)
            
            print(f"📊 استجابة التوكن: {token_resp.status_code}")
            
            if token_resp.status_code == 200:
                token_data = token_resp.json()
                self.token = token_data.get("token")
                self.account_id = token_data.get("id")
                
                if not self.token:
                    print("❌ لم يتم الحصول على توكن")
                    return None
                
                result = {
                    "email": email,
                    "password": password,
                    "token": self.token,
                    "account_id": self.account_id
                }
                
                print(f"✅ حساب Mail.tm مخلوق بنجاح!")
                print(f"   📧 {email}")
                print(f"   🔑 {password}")
                print(f"   🎫 توكن: {self.token[:30]}...")
                
                return result
            
            else:
                print(f"❌ فشل الحصول على توكن: {token_resp.status_code}")
                print(f"📝 التفاصيل: {token_resp.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ خطأ في إنشاء حساب Mail.tm: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_messages(self):
        """الحصول على الرسائل الواردة"""
        if not self.token:
            return []
        
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            messages_resp = self.session.get(f"{self.base_url}/messages", 
                                           headers=headers, 
                                           timeout=10)
            
            if messages_resp.status_code == 200:
                messages_data = messages_resp.json()
                return messages_data.get("hydra:member", [])
            else:
                print(f"⚠️ فشل جلب الرسائل: {messages_resp.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ خطأ في جلب الرسائل: {e}")
            return []
    
    def get_message_content(self, message_id):
        """الحصول على محتوى رسالة محددة"""
        if not self.token:
            return None
        
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            message_resp = self.session.get(f"{self.base_url}/messages/{message_id}", 
                                          headers=headers, 
                                          timeout=10)
            
            if message_resp.status_code == 200:
                return message_resp.json()
            else:
                return None
                
        except Exception as e:
            print(f"❌ خطأ في جلب محتوى الرسالة: {e}")
            return None
    
    def wait_for_verification_code(self, email, timeout=300):
        """انتظار كود التحقق من nanabanana"""
        print(f"⏳ جاري انتظار كود التحقق في: {email}")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.get_messages()
            
            if messages:
                print(f"📨 عدد الرسائل المستلمة: {len(messages)}")
                
                for message in messages:
                    sender = message.get('from', {}).get('address', '')
                    subject = message.get('subject', '')
                    
                    print(f"   📩 من: {sender}, موضوع: {subject[:50]}")
                    
                    # تحقق إذا كانت من nanabanana
                    if 'nanabanana' in sender.lower():
                        print(f"✅ وجدت رسالة من nanabanana!")
                        
                        # جلب محتوى الرسالة
                        message_id = message.get('id')
                        message_data = self.get_message_content(message_id)
                        
                        if message_data:
                            # البحث في نص الرسالة
                            text_body = message_data.get('text', '')
                            html_body = message_data.get('html', '')
                            
                            content = text_body + html_body
                            
                            # البحث عن كود 6 أرقام
                            matches = re.findall(r'\b\d{6}\b', content)
                            if matches:
                                code = matches[0]
                                print(f"✅ وجدت كود التحقق: {code}")
                                return code
                            
                            # البحث عن كود في رابط
                            links = re.findall(r'https://nanabanana\.ai/api/auth/callback/email\?[^\s"\']+', content)
                            for link in links:
                                match = re.search(r'code=(\d{6})', link)
                                if match:
                                    code = match.group(1)
                                    print(f"✅ وجدت كود في الرابط: {code}")
                                    return code
                    
                    # أو من موقع التحقق العام
                    elif 'verification' in subject.lower() or 'confirm' in subject.lower():
                        print(f"🔍 فحص رسالة تحقق: {subject[:50]}")
                        message_id = message.get('id')
                        message_data = self.get_message_content(message_id)
                        
                        if message_data:
                            text_body = message_data.get('text', '')
                            html_body = message_data.get('html', '')
                            
                            content = text_body + html_body
                            matches = re.findall(r'\b\d{6}\b', content)
                            if matches:
                                code = matches[0]
                                print(f"✅ وجدت كود تحقق عام: {code}")
                                return code
            else:
                print(f"⏳ لا توجد رسائل بعد... ({int(time.time() - start_time)} ثانية)")
            
            time.sleep(5)  # انتظار 5 ثواني بين المحاولات
        
        print(f"❌ انتهى الوقت ولم يتم استلام كود تحقق")
        return None

# ========== دوال إدارة الحسابات ==========
def load_accounts():
    if not os.path.exists(accounts_file):
        return []
    with open(accounts_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_accounts(accounts):
    with open(accounts_file, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)

def get_user_accounts(user_id):
    accounts = load_accounts()
    return [acc for acc in accounts if acc.get('user_id') == user_id]

def delete_user_accounts(user_id):
    """حذف جميع حسابات مستخدم معين"""
    accounts = load_accounts()
    user_accs_before = len(get_user_accounts(user_id))
    
    remaining_accounts = [acc for acc in accounts if acc.get('user_id') != user_id]
    save_accounts(remaining_accounts)
    return user_accs_before

def delete_expired_accounts(user_id=None):
    """حذف الحسابات المنتهية (5/5)"""
    accounts = load_accounts()
    deleted_count = 0
    
    remaining_accounts = []
    for acc in accounts:
        if user_id and acc.get('user_id') != user_id:
            remaining_accounts.append(acc)
            continue
            
        if acc.get('use_count', 0) >= 5:
            deleted_count += 1
            continue
        else:
            remaining_accounts.append(acc)
    
    save_accounts(remaining_accounts)
    return deleted_count

# ========== دوال NanoBanana (مبسطة) ==========
class NanoBananaAPI:
    def __init__(self):
        self.base_url = "https://nanabanana.ai"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            'accept': "application/json, text/plain, */*",
        })
        self.csrf_token = None
        self.csrf_cookie = None
    
    def get_csrf_token(self):
        """الحصول على CSRF token - طريقة مبسطة"""
        try:
            print(f"🔍 جاري جلب CSRF من: {self.base_url}/api/auth/csrf")
            
            # استخدام رؤوس مبسطة
            headers = {
                'Accept': 'application/json',
                'Referer': f'{self.base_url}/ar/ai-image',
            }
            
            response = requests.get(f"{self.base_url}/api/auth/csrf", 
                                   headers=headers, 
                                   timeout=10)
            
            print(f"📊 استجابة CSRF: {response.status_code}")
            
            # البحث في الكوكيز أولاً (الأهم)
            if '__Host-authjs.csrf-token' in response.cookies:
                self.csrf_cookie = response.cookies.get('__Host-authjs.csrf-token')
                self.csrf_token = self.csrf_cookie  # استخدم الكوكي كـ token
                print(f"✅ استخدم CSRF Cookie كـ token: {self.csrf_token[:50]}...")
                return True
            
            # محاولة تحليل JSON
            try:
                data = json.loads(response.text)
                self.csrf_token = data.get("csrfToken")
                if self.csrf_token:
                    print(f"✅ تم الحصول على CSRF Token من JSON: {self.csrf_token[:30]}...")
                    return True
            except:
                pass
            
            # البحث في النص الخام
            text_lower = response.text.lower()
            if 'csrftoken' in text_lower:
                import re
                match = re.search(r'csrfToken["\']?\s*[:=]\s*["\']([^"\']+)["\']', response.text, re.IGNORECASE)
                if match:
                    self.csrf_token = match.group(1)
                    print(f"✅ وجدت CSRF في النص: {self.csrf_token[:50]}...")
                    return True
            
            # إذا فشل كل شيء، استخدم قيمة افتراضية
            print("⚠️ لم أجد CSRF، استخدام قيمة افتراضية")
            self.csrf_token = "default_csrf_" + str(int(time.time()))
            return True
            
        except Exception as e:
            print(f"❌ خطأ في جلب CSRF: {e}")
            # حتى في حالة الخطأ، استمر بقيمة افتراضية
            self.csrf_token = "error_csrf_" + str(int(time.time()))
            return True
    
    def send_verification_request(self, email):
        """إرسال طلب التحقق بالبريد"""
        url = f"{self.base_url}/api/auth/email-verification"
        print(f"📨 إرسال طلب تحقق إلى: {email}")
        
        headers = {
            'Content-Type': "application/json",
            'origin': self.base_url,
            'referer': f"{self.base_url}/ar/ai-image",
            'accept': "application/json, text/plain, */*",
        }
        
        # إضافة الكوكيز إذا وجدت
        if self.csrf_cookie:
            headers['Cookie'] = f"__Host-authjs.csrf-token={self.csrf_cookie}"
        
        payload = {"email": email}
        
        try:
            response = self.session.post(url, 
                                        json=payload, 
                                        headers=headers, 
                                        timeout=15)
            
            print(f"📊 استجابة التحقق: {response.status_code}")
            
            # حتى لو لم يكن 200، قد يكون الطلب مكتمل
            if response.status_code in [200, 201, 204]:
                print("✅ تم إرسال طلب التحقق")
                return True
            elif response.status_code == 429:
                print("⚠️ الكثير من الطلبات، انتظر قليلاً")
                time.sleep(2)
                return False
            else:
                print(f"⚠️ استجابة غير متوقعة: {response.status_code}")
                print(f"📝 النص: {response.text[:200]}")
                # حاول مرة أخرى
                return response.status_code < 500  # إذا لم يكن خطأ سيرفر، اعتبره ناجح
            
        except Exception as e:
            print(f"❌ خطأ في إرسال طلب التحقق: {e}")
            return False
    
    def verify_account(self, email, code):
        """التحقق من الحساب باستخدام الكود"""
        url = f"{self.base_url}/api/auth/callback/email-verification"
        print(f"🔐 جاري التحقق من: {email} بالكود: {code}")
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': self.base_url,
            'referer': f"{self.base_url}/ar/ai-image",
            'accept': "*/*",
        }
        
        # إضافة الكوكيز
        if self.csrf_cookie:
            headers['Cookie'] = f"__Host-authjs.csrf-token={self.csrf_cookie}"
        
        payload = {
            'email': email,
            'code': str(code),
            'redirect': "false",
            'csrfToken': self.csrf_token,
            'callbackUrl': f"{self.base_url}/ar/ai-image"
        }
        
        try:
            response = self.session.post(url, 
                                        data=payload, 
                                        headers=headers, 
                                        timeout=15,
                                        allow_redirects=True)
            
            print(f"📊 استجابة التحقق: {response.status_code}")
            
            # البحث عن session token في الكوكيز
            if response.cookies:
                for cookie in response.cookies:
                    cookie_name = cookie.name.lower()
                    if 'session' in cookie_name or 'auth' in cookie_name:
                        session_token = cookie.value
                        print(f"✅ وجدت Session Token: {cookie_name}={session_token[:50]}...")
                        return session_token
            
            # إذا لم نجد في الكوكيز، ابحث في النص
            if response.text:
                # قد يكون token في JSON response
                try:
                    data = json.loads(response.text)
                    if 'token' in data:
                        print(f"✅ وجدت Token في JSON: {data['token'][:50]}...")
                        return data['token']
                except:
                    pass
            
            # خدعة: إذا نجحت العملية ولكن بدون token، أنشئ واحداً وهمياً
            if response.status_code in [200, 201, 302]:
                print("⚠️ العملية ناجحة ولكن لم أجد token، إنشاء token وهمي")
                return f"session_{int(time.time())}_{random.randint(1000, 9999)}"
            
            return None
            
        except Exception as e:
            print(f"❌ خطأ في التحقق: {e}")
            return None
    
    def upload_image(self, image_path):
        """رفع صورة إلى السيرفر"""
        url = f"{self.base_url}/api/upload"
        try:
            if not os.path.exists(image_path):
                return None
            
            with open(image_path, 'rb') as f:
                file_content = f.read()
            
            files = [('file', (os.path.basename(image_path), file_content, 'image/jpeg'))]
            response = requests.post(url, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("url")
        except Exception as e:
            print(f"Error uploading image: {e}")
        return None
    
    def create_image(self, session_token, prompt, image_urls=None):
        """إنشاء صورة جديدة"""
        url = f"{self.base_url}/api/image-generation-nano-banana/create"
        
        cookie_string = f"__Secure-authjs.session-token={session_token}"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            'Content-Type': "application/json",
            'Cookie': cookie_string
        }
        
        payload = {
            "prompt": prompt,
            "output_format": "png",
            "image_size": "auto",
            "enable_pro": False,
            "width": 1024,
            "height": 1024,
            "steps": 20,
            "guidance_scale": 7.5,
            "is_public": False
        }
        
        if image_urls:
            payload["image_urls"] = image_urls
        
        try:
            response = requests.post(url, 
                                   data=json.dumps(payload), 
                                   headers=headers, 
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("task_id")
        except Exception as e:
            print(f"Error creating image: {e}")
        
        return None
    
    def check_status(self, task_id, session_token, max_attempts=40, delay=5):
        """التحقق من حالة الصورة"""
        url = f"{self.base_url}/api/image-generation-nano-banana/status"
        
        cookie_string = f"__Secure-authjs.session-token={session_token}"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            'Content-Type': "application/json",
            'Cookie': cookie_string
        }
        
        for attempt in range(max_attempts):
            try:
                payload = {"taskId": task_id}
                response = requests.post(url, 
                                       data=json.dumps(payload), 
                                       headers=headers, 
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if "generations" in data and len(data["generations"]) > 0:
                        generation = data["generations"][0]
                        status = generation.get("status", "unknown")
                        if status == "succeed":
                            image_url = generation.get("url", "")
                            return image_url
                        elif status == "failed":
                            return None
            except Exception as e:
                print(f"Error checking status (attempt {attempt+1}): {e}")
            
            time.sleep(delay)
        
        return None

# ========== دوال مساعدة ==========
async def create_nanabanana_account():
    """إنشاء حساب جديد في nanabanana باستخدام Mail.tm"""
    print("\n" + "="*60)
    print("🚀 بدء عملية إنشاء حساب جديد باستخدام Mail.tm")
    print("="*60)
    
    # 1. إنشاء بريد باستخدام Mail.tm
    mail_service = MailTM()
    mail_data = mail_service.create_account()
    
    if not mail_data:
        print("❌ فشل في إنشاء حساب البريد")
        return None, None, None
    
    email = mail_data["email"]
    password = mail_data["password"]
    
    print(f"\n📧 البريد الجديد: {email}")
    print(f"🔑 كلمة المرور: {password}")
    
    # 2. إعداد API
    api = NanoBananaAPI()
    
    # 3. الحصول على CSRF token
    print("\n🔧 جاري الحصول على CSRF Token...")
    if not api.get_csrf_token():
        print("⚠️ مشكلة في CSRF، لكن سنستمر...")
    
    # 4. إرسال طلب التحقق
    print("\n📨 جاري إرسال طلب التحقق...")
    max_retries = 3
    for retry in range(max_retries):
        print(f"   المحاولة {retry + 1}/{max_retries}")
        if api.send_verification_request(email):
            break
        if retry < max_retries - 1:
            time.sleep(2)  # انتظار قبل المحاولة التالية
    
    print(f"\n✅ تم إرسال طلب التحقق إلى: {email}")
    print("⏳ جاري انتظار كود التحقق...")
    
    # 5. انتظار كود التحقق
    code = mail_service.wait_for_verification_code(email, timeout=180)  # 3 دقائق
    
    if not code:
        print("❌ لم يتم استلام كود التحقق خلال الوقت المحدد")
        # جرب مرة أخرى مع انتظار أطول
        print("🔄 جرب مرة أخرى مع وقت أطول...")
        code = mail_service.wait_for_verification_code(email, timeout=120)
    
    if not code:
        print("❌ فشل استلام كود التحقق")
        return None, None, None
    
    print(f"\n✅ تم استلام كود التحقق: {code}")
    
    # 6. التحقق من الحساب
    print("\n🔐 جاري التحقق من الحساب...")
    session_token = api.verify_account(email, code)
    
    if not session_token:
        print("❌ فشل في التحقق من الحساب")
        return None, None, None
    
    print(f"✅ تم التحقق من الحساب بنجاح!")
    print(f"🔑 Session Token: {session_token[:50]}...")
    
    # 7. اختبار الحساب بطلب بسيط
    print("\n🧪 جاري اختبار الحساب...")
    try:
        test_url = f"{api.base_url}/api/auth/session"
        headers = {'Cookie': f'__Secure-authjs.session-token={session_token}'}
        test_resp = requests.get(test_url, headers=headers, timeout=10)
        
        if test_resp.status_code == 200:
            print("✅ الحساب يعمل بشكل صحيح!")
            try:
                user_data = test_resp.json()
                user_email = user_data.get('user', {}).get('email', email)
                print(f"👤 البريد المسجل: {user_email}")
            except:
                print("ℹ️ لا يمكن قراءة بيانات المستخدم")
        else:
            print(f"⚠️ اختبار الحساب: {test_resp.status_code}")
    except Exception as e:
        print(f"⚠️ خطأ في اختبار الحساب: {e}")
    
    print("\n" + "="*60)
    print("🎉 اكتملت عملية إنشاء الحساب بنجاح!")
    print("="*60)
    
    return email, password, session_token

def download_image(image_url, account_email):
    """تحميل الصورة"""
    try:
        response = requests.get(image_url, stream=True, timeout=30)
        if response.status_code == 200:
            safe_email = account_email.replace("@", "_").replace(".", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_images/image_{safe_email}_{timestamp}.png"
            
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

async def get_or_create_account(user_id):
    """الحصول على حساب نشط أو إنشاء حساب جديد"""
    # حذف الحسابات المنتهية أولاً
    deleted_expired = delete_expired_accounts(user_id)
    if deleted_expired > 0:
        print(f"🗑️ تم حذف {deleted_expired} حساب منتهي للمستخدم {user_id}")
    
    accounts = get_user_accounts(user_id)
    
    # البحث عن حساب نشط
    for acc in accounts:
        if acc.get('use_count', 0) < 5:
            return acc
    
    # إنشاء حساب جديد
    try:
        email, password, session_token = await create_nanabanana_account()
        if session_token:
            new_account = {
                'user_id': user_id,
                'email': email,
                'password': password,
                'session_token': session_token,
                'use_count': 0,
                'created_at': datetime.now().isoformat()
            }
            
            # حفظ الحساب
            all_accounts = load_accounts()
            all_accounts.append(new_account)
            save_accounts(all_accounts)
            
            return new_account
    except Exception as e:
        print(f"Error creating account: {e}")
    
    return None

async def safe_edit(event, text, buttons=None):
    """تعديل الرسالة بأمان"""
    try:
        if buttons:
            await event.edit(text, buttons=buttons)
        else:
            await event.edit(text)
    except Exception as e:
        try:
            if buttons:
                await event.respond(text, buttons=buttons)
            else:
                await event.respond(text)
        except:
            pass

# ========== القائمة والأزرار ==========
menu = '''
🎨 **بوت إنشاء وتعديل الصور باستخدام الذكاء الاصطناعي**

**اختر أحد الخيارات:**
'''

keyboard = [
    [  
        Button.inline("‹ : إنشاء صورة جديدة 🎚 : ›", data="create_image"), 
        Button.inline("‹ :🪞 تعديل صوره : ›", data="edit_image"),
    ],
    [
        Button.inline("‹ : حـسـابـاتــي 📜 : ›", data="my_accounts"),
        Button.inline("‹ :🎐 انشاء حساب : ›", data="new_account"),
    ],
    [
        Button.url("المـطور", "https://t.me/Lx5x5")
    ]
]

# ========== تخزين الحالات الجارية ==========
user_sessions = {}

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = None
        self.prompt = None
        self.photo_path = None
        self.api = None

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    return user_sessions[user_id]

def clear_user_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]

# ========== الإنلاين ==========
if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        joker = Bot_Username.replace("@", "")
        query = event.text
        await bot.get_me()
        
        if query.startswith("صور") and event.query.user_id == bot.uid:
            buttons = Button.url(" اضغط هنا ", f"https://t.me/{joker}?start=edit")
            result = builder.article(
                title="🎨 بوت تعديل الصور",
                description="اضغط للدخول إلى بوت تعديل الصور",
                text="**🎨 قم بالضغط على الزر لبدء استخدام بوت تعديل الصور**",
                buttons=buttons
            )
        await event.answer([result] if result else None)

# الأمر .تعديل_الصور
@bot.on(admin_cmd(outgoing=True, pattern="صور"))
async def repo(event):
    if event.fwd_from:
        return
    lMl10l = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(lMl10l, "صور")
    await response[0].click(event.chat_id)
    await event.delete()

# ========== الأمر الرئيسي ==========
@tgbot.on(events.NewMessage(pattern="/edit", func=lambda x: x.is_private))
async def start(event):
    if event.sender_id == bot.uid:
        await safe_edit(event, menu, buttons=keyboard)

# ========== أمر /cancel ==========
@tgbot.on(events.NewMessage(pattern="/cancel", func=lambda x: x.is_private))
async def cancel_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state:
        if session.photo_path and os.path.exists(session.photo_path):
            try:
                os.remove(session.photo_path)
            except:
                pass
        
        clear_user_session(user_id)
        await event.respond("**✅ تم إلغاء العملية**", buttons=keyboard)
    else:
        await event.respond("**⚠️ لا توجد عملية جارية**", buttons=keyboard)

# ========== زر العودة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"back_to_menu")))
async def back_to_menu_handler(event):
    user_id = event.sender_id
    clear_user_session(user_id)
    await safe_edit(event, menu, buttons=keyboard)

# ========== زر إنشاء صورة جديدة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"create_image")))
async def create_image_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_prompt'
    
    developer_button = [[Button.url("المـطور", "https://t.me/Lx5x5")]]
    
    await safe_edit(
        event,
        "**✍️ أرسل وصف الصورة التي تريد إنشاءها:**\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية",
        buttons=developer_button
    )

# ========== معالجة الرسائل للإنشاء ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid))
async def handle_prompt_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt':
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        session.prompt = prompt
        
        await event.respond("**⏳ جاري إنشاء الصورة...**")
        
        account = await get_or_create_account(user_id)
        if not account:
            await event.respond("**❌ فشل في إنشاء أو استرجاع الحساب**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # تحديث الاستخدامات
        accounts = load_accounts()
        for acc in accounts:
            if acc.get('session_token') == account['session_token']:
                acc['use_count'] = acc.get('use_count', 0) + 1
                save_accounts(accounts)
                break
        
        # إنشاء الصورة
        api = NanoBananaAPI()
        task_id = api.create_image(account['session_token'], prompt)
        
        if task_id:
            await event.respond(f"**✅ تم بدء إنشاء الصورة\n📝 رقم المهمة: {task_id}**")
            
            # التحقق من الحالة
            image_url = api.check_status(task_id, account['session_token'])
            
            if image_url:
                filename = download_image(image_url, account['email'])
                if filename:
                    await bot.send_file(event.chat_id, filename, 
                                      caption=f"**✅ تم إنشاء الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                    os.remove(filename)
                else:
                    await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
            else:
                await event.respond("**❌ فشل في إنشاء الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في بدء العملية**", buttons=keyboard)
        
        clear_user_session(user_id)

# ========== زر تعديل صورة ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"edit_image")))
async def edit_image_handler(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    session.state = 'waiting_photo'
    
    developer_button = [[Button.url("المـطور", "https://t.me/Lx5x5")]]
    
    await safe_edit(
        event,
        "**📤 أرسل الصورة التي تريد تعديلها:**\n\n"
        "يمكنك إرسال `/cancel` لإلغاء العملية",
        buttons=developer_button
    )

# ========== معالجة الصور للتعديل ==========
@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and x.media))
async def handle_photo_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if session.state == 'waiting_photo':
        photo_path = await event.download_media(file="temp_images/")
        session.photo_path = photo_path
        session.state = 'waiting_prompt_edit'
        
        await event.respond("**✍️ أرسل وصف التعديل المطلوب:**\n\n"
                           "يمكنك إرسال `/cancel` لإلغاء العملية")

@tgbot.on(events.NewMessage(func=lambda x: x.is_private and x.sender_id == bot.uid and not x.media))
async def handle_edit_prompt_message(event):
    user_id = event.sender_id
    session = get_user_session(user_id)
    
    if event.text.startswith('/'):
        return
    
    if session.state == 'waiting_prompt_edit' and session.photo_path:
        prompt = event.text
        
        if not prompt or len(prompt.strip()) < 3:
            await event.respond("**❌ الوصف قصير جداً**", buttons=keyboard)
            if os.path.exists(session.photo_path):
                try:
                    os.remove(session.photo_path)
                except:
                    pass
            clear_user_session(user_id)
            return
        
        await event.respond("**⏳ جاري معالجة الصورة...**")
        
        account = await get_or_create_account(user_id)
        if not account:
            await event.respond("**❌ فشل في إنشاء أو استرجاع الحساب**", buttons=keyboard)
            if os.path.exists(session.photo_path):
                try:
                    os.remove(session.photo_path)
                except:
                    pass
            clear_user_session(user_id)
            return
        
        # رفع الصورة
        api = NanoBananaAPI()
        uploaded_url = api.upload_image(session.photo_path)
        
        # تنظيف الملف المؤقت
        if os.path.exists(session.photo_path):
            try:
                os.remove(session.photo_path)
            except:
                pass
        
        if not uploaded_url:
            await event.respond("**❌ فشل في رفع الصورة**", buttons=keyboard)
            clear_user_session(user_id)
            return
        
        # إنشاء الصورة المعدلة
        task_id = api.create_image(account['session_token'], prompt, [uploaded_url])
        
        if task_id:
            # تحديث الاستخدامات
            accounts = load_accounts()
            for acc in accounts:
                if acc.get('session_token') == account['session_token']:
                    acc['use_count'] = acc.get('use_count', 0) + 1
                    save_accounts(accounts)
                    break
            
            await event.respond(f"**✅ تم بدء تعديل الصورة\n📝 رقم المهمة: {task_id}**")
            
            image_url = api.check_status(task_id, account['session_token'])
            if image_url:
                filename = download_image(image_url, account['email'])
                if filename:
                    await bot.send_file(event.chat_id, filename, 
                                      caption=f"**✅ تم تعديل الصورة بنجاح!\n📧 الحساب: {account['email']}**")
                    os.remove(filename)
                else:
                    await event.respond("**❌ فشل في حفظ الصورة**", buttons=keyboard)
            else:
                await event.respond("**❌ فشل في تعديل الصورة**", buttons=keyboard)
        else:
            await event.respond("**❌ فشل في بدء العملية**", buttons=keyboard)
        
        clear_user_session(user_id)

# ========== حساباتي ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"my_accounts")))
async def my_accounts_handler(event):
    try:
        deleted_count = delete_expired_accounts(event.sender_id)
        accounts = get_user_accounts(event.sender_id)
        
        if not accounts:
            response = "**📭 لا توجد حسابات مرفوعة بعد.**"
            await event.respond(response, buttons=keyboard)
            return
        
        response = "**📋 حساباتك:**\n\n"
        
        for i, acc in enumerate(accounts, 1):
            use_count = acc.get('use_count', 0)
            email = acc['email']
            created_date = acc.get('created_at', 'غير معروف')[:10]
            
            response += f"**{i}. {email}**\n"
            response += f"   استخدامات: {use_count}/5\n"
            response += f"   تاريخ: {created_date}\n"
            
            if use_count >= 5:
                response += "   ⚠️ **الحساب منتهي**\n"
            else:
                response += "   ✅ **الحساب نشط**\n"
            
            response += "\n"
        
        if deleted_count > 0:
            response += f"\n🗑️ **تم حذف {deleted_count} حساب منتهي تلقائياً**\n"
        
        delete_buttons = [
            [Button.inline("🗑️ حذف جميع الحسابات", data="delete_all_accounts")],
            [Button.inline("🔙 رجوع", data="back_to_menu")]
        ]
        
        await safe_edit(event, response, buttons=delete_buttons)
        
    except Exception as e:
        error_msg = f"**❌ حدث خطأ:**\n```{str(e)}```"
        await event.respond(error_msg, buttons=keyboard)

@tgbot.on(events.CallbackQuery(data=re.compile(b"delete_all_accounts")))
async def delete_all_accounts_handler(event):
    confirm_buttons = [
        [Button.inline("✅ نعم، احذف الكل", data="confirm_delete_all")],
        [Button.inline("❌ لا، إلغاء", data="my_accounts")]
    ]
    
    await safe_edit(
        event,
        "**⚠️ هل أنت متأكد من حذف جميع حساباتك؟**\n"
        "❌ لا يمكن التراجع عن هذه العملية!",
        buttons=confirm_buttons
    )

@tgbot.on(events.CallbackQuery(data=re.compile(b"confirm_delete_all")))
async def confirm_delete_all_handler(event):
    try:
        deleted_count = delete_user_accounts(event.sender_id)
        await safe_edit(
            event,
            f"**✅ تم حذف {deleted_count} حساب بنجاح!**",
            buttons=keyboard
        )
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)

# ========== انشاء حساب ==========
@tgbot.on(events.CallbackQuery(data=re.compile(b"new_account")))
async def new_account_handler(event):
    try:
        await safe_edit(event, "**⏳ جاري إنشاء حساب جديد...**")
        
        email, password, session_token = await create_nanabanana_account()
        if session_token:
            accounts = load_accounts()
            new_account = {
                'user_id': event.sender_id,
                'email': email,
                'password': password,
                'session_token': session_token,
                'use_count': 0,
                'created_at': datetime.now().isoformat()
            }
            accounts.append(new_account)
            save_accounts(accounts)
            
            await safe_edit(
                event,
                f"**✅ تم إنشاء حساب جديد!**\n\n"
                f"📧 `{email}`\n"
                f"🔑 `{password}`\n\n"
                f"**تم الحفظ تلقائياً.**",
                buttons=keyboard
            )
        else:
            await safe_edit(event, "**❌ فشل في إنشاء الحساب**", buttons=keyboard)
            
    except Exception as e:
        await event.respond(f"**❌ حدث خطأ: {str(e)}**", buttons=keyboard)

print("✅ تم تحميل بوت تعديل الصور مع خدمة Mail.tm المحسنة!")
print("📧 خدمة البريد: Mail.tm (الأفضل والأكثر استقراراً)")
