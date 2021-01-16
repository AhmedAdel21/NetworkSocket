import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/") #connect to MongoDB

mydb = myclient["networkDB"] # create a database
mydb.drop_collection("users")
print(myclient.list_database_names()) # all database in the system

userData = mydb["ChatBot"] # create a collection 

print(mydb.list_collection_names()) # print all the collection in my DB
for i in mydb.list_collection_names():
    if i == "dolaBot":
        print("dasdsad")
d = open("replies.txt")
p = d.read()
data = []
fisrt = p.split("\n")
for i in fisrt:
    data.append(i.split(":"))

# print(data)
sendingData = []
for i in data:
    sendingData.append({i[0]:' '.join(map(str, i[1:]))})

# print(sendingData)
userData.insert_many(sendingData)
# for x in userData.find():
#   print(x)
dola = "hello"
for x in userData.find({},{ "_id": 0, dola: 1,}):
    if x:
        print(x[dola])
  

userData.drop()
# print(x.inserted_ids) 

# rep =p.split(" ")
# for i in rep:

#####

# myUser = { "name": "admin", "password": "123456" }
# for i in mongoData:
#     print(mongoData[i])
# print(mongoData)
# x = userData.insert_one(mongoData)

# print(x.inserted_id) 

#####

# mylist = [
#   { "name": "Amy", "password": "45354"},
#   { "name": "Hannah", "password": "057257"},

# ]
# x = userData.insert_many(mongoData[0])

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

