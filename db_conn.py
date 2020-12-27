from pymongo import MongoClient

conn=MongoClient('127.0.0.1',27017)
db = conn.new_engineering
new_set = db.blog_new_engineering_table
