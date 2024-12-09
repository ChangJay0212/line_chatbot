from core import OverviewConversation, GeneratePrompt
import time
summary_service = OverviewConversation()
prompt_service = GeneratePrompt()
prompt_service.set_user_conversation(conversation = "9/7日，假日搭車都很久")
prompt_service.set_user_conversation(conversation = "9/7日，沒有豆皮的火鍋，都封鎖")
# print(prompt_service.get())
start = time.time()
summary = summary_service.run(prompt=prompt_service.get())
print(summary)
print(f"total: {(time.time()-start)}")