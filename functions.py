import random
import requests
from pymongo import MongoClient


def bankuser(data):

    # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    # client = pymongo.MongoClient("mongodb+srv://ajinkya:ajinkya@cluster0.gp5dx.mongodb.net/test")
    client = MongoClient("mongodb+srv://test:test@cluster0.gp5dx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",connect=False)
    db = client["bankdata"]
    collection = db["userinfo"]
    data["accNo"]= " ".join([str(random.randint(0,999)).zfill(3) for _ in range(2)])
    data ["balance"] = 0
    __pipeline__ = [
                        {
                            '$project':{
                                '_id': 0,
                                'accNo': 1
                            }
                        }
                     ]
    acc_list = list(collection.aggregate(__pipeline__))
    acc_list = [i['accNo'] for i in acc_list]
    if data['accNo'] in acc_list:
        data['accNo'] = ' '.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        collection.insert_one(data)
    else:
        collection.insert_one(data)
    return f"You have registered successfully and your account number is {data['accNo']} "

def bank_balance(accNo):
    # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    # client = pymongo.MongoClient("mongodb+srv://ajinkya:ajinkya@cluster0.gp5dx.mongodb.net/test")
    client = MongoClient("mongodb+srv://test:test@cluster0.gp5dx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",connect=False)

    db = client["bankdata"]
    collection = db["userinfo"]
    __pieline__ = [
                    {
                        '$match':{
                            'accNo':accNo['accNo']
                        }

                    }
                  ]

    acc_data = list(collection.aggregate(__pieline__))
    
    if len(acc_data)!=1:
        return "Please check your account number"
    else:
        return f" Your balance is {acc_data[0]['balance']}"


def withdrawl(data):
    # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    # client = pymongo.MongoClient("mongodb+srv://ajinkya:ajinkya@cluster0.gp5dx.mongodb.net/test")
    client = MongoClient("mongodb+srv://test:test@cluster0.gp5dx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",connect=False)
    db = client["bankdata"]
    collection = db["userinfo"]
    __pieline__ = [
                    {
                         '$match': {
                         'accNo': data['accNo']
                        }
                     }
                  ]

    acc_data = list(collection.aggregate(__pieline__))
    
    if len(acc_data)!=1:
        return "Please check your account number"
    elif int(data['withdraw_bal']) > int(acc_data[0]['balance']):
        return "Your balance is insufficient"
    else:
        balance = acc_data[0]['balance']
        update = int(balance) - int(data['withdraw_bal'])
        collection.update_one({'accNo':data['accNo']},{'$set':{'balance': update}})
        return f" Your withrawal is successful and remaining balance is {update}"

def deposit(data):
    # client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    # client = pymongo.MongoClient("mongodb+srv://ajinkya:ajinkya@cluster0.gp5dx.mongodb.net/test")
    client = MongoClient("mongodb+srv://test:test@cluster0.gp5dx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",connect=False)
    db = client["bankdata"]
    collection = db["userinfo"]
    __pieline__ = [
                    {
                         '$match': {
                         'accNo': data['accNo']
                        }
                     }
                  ]

    acc_data = list(collection.aggregate(__pieline__))
    if len(acc_data)!=1:
        return "Please check your account number"
    else:
        balance = acc_data[0]['balance']
        update = int(balance) + int(data['deposit_amt'])
        collection.update_one({'accNo':data['accNo']},{'$set':{'balance':update}})
        return f"Your deposit is successful and current balance is {update}"