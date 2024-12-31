import pandas as pd
from bson import ObjectId
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongodb_to_dataframe(db, collection, query={}, host='localhost', port=27017, username=None, password=None,
                              no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(
        read_mongodb(db, collection, query=query, host=host, port=port, username=username, password=password))

    # Delete the _id
    if no_id:
        del df['_id']

    return df


def read_mongodb(db, collection, query={}, host='localhost', port=27017, username=None, password=None):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    result = list(cursor)
    # Expand the cursor and construct the DataFrame
    return result


def rewrite_data(db, collection, data, host='localhost', port=27017, username=None, password=None):
    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    collection = db[collection]
    properties_ids = [x['_id'] for x in data] + [f"{x['_id']}" for x in data]
    # Suppression des documents correspondant à un critère
    # Exemple : Suppression de tous les documents où 'status' est 'obsolete'
    result = collection.delete_many({'_id': {'$in': properties_ids}})
    print(f"{result.deleted_count} documents supprimés.")
    # Insertion de nouveaux documents
    insert_result = collection.insert_many(data)
    print(f"Documents insérés avec les identifiants : {insert_result.inserted_ids}")


# Fonction pour convertir l'id en entier
def convertir_id_en_entier(db, collection,host='localhost', port=27017, username=None, password=None):
    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    collection = db[collection]
    count = 0
    i = 0
    for document in collection.find():
        id_value = document.get('_id')
        count += 1
        # Vérifie si l'id est une chaîne de caractères et non un ObjectId
        if isinstance(id_value, str):
            try:
                # Tente de convertir en entier
                id_int = int(id_value)

                # Met à jour le document avec l'id converti en entier
                collection.update_one(
                    {'_id': document['_id']},
                    {'$set': {'_id': id_int}}
                )
                #print(f"Document {document['_id']} mis à jour avec l'id {id_int}")
                i += 1  # Augmente i de 1
            except ValueError:
                print(f"Impossible de convertir l'id {id_value} en entier pour le document {document['_id']}")

    print(f'{i}/{count}')

