from core import PostgreSQL


db = PostgreSQL(
    host="database", 
    database="conversation",  
    user="user", 
    password="1234" 
)

#----Insert test----
# db.add("conversation_his", '"user","content"', ("Jay", "黑琵測試2"))

#----Get test----
results = db.get("conversation_his", '"id","user","time","content"')
for info in results:
    conversation = f"{info['user']}在{info['time']}說了:{info['content']}"
        
print(results)

#----Delete test----
# ids = [1,2,3]
# db.delete("conversation_his", ids)
