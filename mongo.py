import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/") #connect to MongoDB

mydb = myclient["networkDB"] # create a database

print(myclient.list_database_names()) # all database in the system

userData = mydb["users"] # create a collection 

print(mydb.list_collection_names()) # print all the collection in my DB

#####

# myUser = { "name": "admin", "password": "123456" }

# x = userData.insert_one(myUser)

# print(x.inserted_id) 

#####

# mylist = [
#   { "name": "Amy", "password": "45354"},
#   { "name": "Hannah", "password": "057257"},

# ]
# x = userData.insert_many(mylist)

# print(x.inserted_ids) 

#####

# x = userData.find_one()

# print(x)

#####

# for x in userData.find():
#   print(x)

#####

# for x in userData.find({},{ "_id": 0, "name": 1, "password": 1 }):
#   print(x)

#####

# myquery = { "name": "admin" }

# mydoc = userData.find(myquery)

# for x in mydoc:
#   print(x['name'])

####

# myquery = { "name": "admin" }
# newvalues = { "$set": { "password": "11111111" } }

# x= userData.update_one(myquery, newvalues)
# #print "users" after the update:
# for x in userData.find():
#   print(x)

####

# myquery = { "name": "admin" }
# newvalues = { "$set": { "password": "22222" } }

# x = userData.update_many(myquery, newvalues)

# print(x.modified_count, "documents updated.")

