from fastapi import FastAPI, Request, HTTPException, Header
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage,MessageEvent,TextSendMessage
from linebot.exceptions import LineBotApiError
import base64
import hashlib
import hmac
import os
import uvicorn
from datetime import datetime
from core import PostgreSQL
from core import OverviewConversation, GeneratePrompt

db = PostgreSQL(
    host="database", 
    database="conversation",  
    user="user", 
    password="1234" 
)

summary_service = OverviewConversation()
prompt_service = GeneratePrompt()
# Initialize FastAPI instance
app = FastAPI()
channel_access_token = "W/JB2tJO36XxKIPJpj6swjOTqTjx0LoMoYHdJemPUFgf1QEB16Tj35INHlSpUdUQf9clfKpwd37PjD2NXHmisQntSD0buvmEzzkxo+CjIv1CmfgBB0RLj47f0QZrS/0xQlPle9lW7D85TOx5TWMDPAdB04t89/1O/w1cDnyilFU="
channel_secret = "cdc056fc6cb19278942292c6158655b9"
# Initialize LineBot API and Webhook Handler with environment variables
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.post("/")
async def callback(request: Request, x_line_signature: str = Header(None)):
    # Get request body as a text
    body = await request.body()
    body = body.decode("utf-8")

    # Log the request body (optional)
    print("Request body:", body)
    # Verify the signature
    hash = hmac.new(channel_secret.encode('utf-8'),
    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    if signature != x_line_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")
    # Handle the webhook
    try:
        
        handler.handle(body, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"

# Handle Line MessageEvent for TextMessage
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取用戶發送的文本消息
    user_message = event.message.text

    # 獲取發送消息的用戶 ID
    user_id = event.source.user_id

    try:
        # 使用 Line API 查詢用戶的個人資料
        profile = line_bot_api.get_profile(user_id)
        user_name = profile.display_name  # 用戶的顯示名稱
        # status_message = profile.status_message  # 用戶的狀態消息（可以是空的）
        timestamp = event.timestamp

        # 將時間戳轉換為日期時間格式（將毫秒轉換為秒）
        event_time = datetime.fromtimestamp(timestamp / 1000)

        # 回覆用戶，包含顯示名稱
        reply_message = TextSendMessage(text=f"你好，{user_name}！你在{event_time}說了：{user_message}")
        

    except LineBotApiError as e:
        # 處理 API 調用錯誤
        print(f"Error getting profile: {e.status_code} - {e.error.message}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法獲取你的個人資料"))
    if "懶趴包" in user_message:
        results = db.get("conversation_his", '"id","user","time","content"')
        ids =[]
        if len(results)>3:
            for info in results:
                conversation = f"{info['user']}在{info['time']}說了:{info['content']}"
                prompt_service.set_user_conversation(conversation = conversation)
                ids.append(int(info['id']))
            db.delete("conversation_his", ids)
            summary = summary_service.run(prompt=prompt_service.get())
            reply_message = TextSendMessage(summary)
        else:
            reply_message = TextSendMessage("沒有很長的聊天紀錄問，懶趴包是要統整三小?")
        line_bot_api.reply_message(event.reply_token, reply_message)
    else:
        db.add("conversation_his", '"user","time","content"', (user_name,event_time, user_message))
        line_bot_api.reply_message(event.reply_token, reply_message)


# Run the app with Uvicorn
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8001))
    uvicorn.run("app:app", host='0.0.0.0', port=port, reload=True)
