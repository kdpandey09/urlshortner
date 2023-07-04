

# doc = {
#     "special_key":"9ai",
#     "url":"9ai.in"
# }
# collection.count_documents()
# print(collection.find_one({"special_key":"9ai"}))

class urls():
    def __init__(self,mongo_db_collection_object) -> None:
        self.db = mongo_db_collection_object
        
    def insert_url(self,special_key,url):
        if self.db.count_documents({"special_key":special_key})>0:
            return False
        else:
            doc = {
                "special_key":special_key,
                "url":url,
                "clicks":0
            }
            self.db.insert_one(doc)
            return True
    
    def fetch_url(self,special_key):
        try:
            data = self.db.find_one({"special_key":special_key})
            self.db.update_one({"special_key":special_key},{"$inc":{"clicks":1}})
            return data["url"]
        except:
            return "https://9ai.in"
    def count(self,special_key):
        try:
            data = self.db.find_one({"special_key":special_key})
            return data["clicks"]
        except:
            return 0
    
# obj = urls(collection)
# print(obj.fetch_url("kdp"))