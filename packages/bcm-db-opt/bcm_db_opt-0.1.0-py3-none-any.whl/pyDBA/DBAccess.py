from pymongo import MongoClient, client_options

class DBAccess(object):
    db = None
    def __init__(self, dbName, host='localhost', port=27127, username=None, password=None) -> None:
        client = MongoClient(host=host, port=port, username=username, password=password)
        print(client)
        DBAccess.db = client[dbName]
        super().__init__()