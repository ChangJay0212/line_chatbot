import requests
from core import GeneratePrompt
# 定義 API URL
url = "http://model_server:11434/api/chat"  # 將此處替換為實際的 API URL
prompt_service = GeneratePrompt()
prompt_service.set_user_conversation(conversation = "9/7日，假日搭車都很久")
prompt_service.set_user_conversation(conversation = "9/7日，沒有豆皮的火鍋，都封鎖")
# 定義 JSON 資料
data = {
  "model": "taiwan:lastest",
  "messages": prompt_service.get(),
  "stream": False
}

# print(data)
# 發送 POST 請求
try:
    response = requests.post(url, json=data)

    # 檢查回應狀態
    if response.status_code == 200:
        print("請求成功，回應內容：")
        print(response.json())  # 假設回應是 JSON 格式
    else:
        print(f"請求失敗，狀態碼: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"HTTP 請求發生錯誤: {e}")
