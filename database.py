import datetime
from pymongo import MongoClient
connectionString="mongodb+srv://admin:admin@cluster0.snt3m.mongodb.net/<dbname>?retryWrites=true&w=majority"
# localConnection=""
client = MongoClient(connectionString)
db=client.scraped
authors = db.authors

def queryDatabase(search_param):
    result = authors.find_one({ 'full_name' : search_param }, {'_id':False} )
    if(result is not None):
        return result
    else: 
        return None

def insertData(name, data):

    if(queryDatabase(name) is not None):
        authors.replace_one({ 'full_name' : name }, {
        'full_name' : name,
        'date' : datetime.datetime.now(),
        'microsoft_academic' : data['microsoft_academic'],
        'google' : data['google']
        }) 
    else:
        authors.insert_one({
        'full_name' : name,
        'date' : datetime.datetime.now(),
        'microsoft_academic' : data['microsoft_academic'],
        'google' : data['google']
        })

    insertedData = queryDatabase(name)

    return insertedData

def insertTest(name):
    authors.insert_one({
        'full_name' : name,
        'date' : datetime.datetime.now(),
        'research_gate' : 'No data',
        'google' : 'No data'
    })

    inserted = queryDatabase(name)

    return inserted


def replaceTest(name, newname):
    authors.replace_one({ 'full_name' : name }, {
        'full_name' : newname,
        'date' : datetime.datetime.now(),
        'research_gate' : 'No data',
        'google' : 'No data'
    }) 

    replaced = queryDatabase(newname)

    return replaced

