from pymongo import MongoClient

# 시간가져오기 코드
import datetime
#
# now_time = datetime.datetime.now()
# now_time = str(now_time)
# print(now_time[:16])


ut = datetime.datetime.utcnow()
print(ut)