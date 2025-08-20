import pandas as pd
from bson import ObjectId
from pymongo import MongoClient
import logging
from typing import List, Dict, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _connect_mongo(host: str, port: int, username: Optional[str], password: Optional[str], db: str) -> MongoClient:
    """
    Establish a connection to MongoDB

    Args:
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication
        db: Database name

    Returns:
        MongoClient: MongoDB client connection
    """
    try:
        # Create connection string
        if username and password:
            connection_string = f"mongodb://{username}:{password}@{host}:{port}/{db}"
        else:
            connection_string = f"mongodb://{host}:{port}/{db}"

        # Connect to MongoDB
        client = MongoClient(connection_string)

        # Test connection
        client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB at {host}:{port}")

        return client[db]
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


def read_mongodb_to_dataframe(
        db: str,
        collection: str,
        query: Dict = {},
        limit: int = 100,
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None,
        no_id: bool = True
) -> pd.DataFrame:
    """
    Read from MongoDB and return data as a pandas DataFrame

    Args:
        db: Database name
        collection: Collection name
        query: MongoDB query to filter documents
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication
        no_id: Whether to exclude the _id field from the result

    Returns:
        pd.DataFrame: Data from MongoDB as a DataFrame
    """
    try:
        # Get data from MongoDB
        data = read_mongodb(
            db=db,
            collection=collection,
            query=query,
            limit=limit,
            host=host,
            port=port,
            username=username,
            password=password
        )

        # Convert to DataFrame
        if not data:
            logger.warning(f"No data found in {db}.{collection} with query {query}")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # Delete the _id column if requested
        if no_id and '_id' in df.columns:
            del df['_id']

        logger.info(f"Successfully read {len(df)} records from {db}.{collection}")
        return df
    except Exception as e:
        logger.error(f"Error reading data from MongoDB: {str(e)}")
        raise


def read_mongodb(
        db: str,
        collection: str,
        query: Dict = {},
        limit: int = 100,
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Read from MongoDB and return raw data

    Args:
        db: Database name
        collection: Collection name
        query: MongoDB query to filter documents
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication

    Returns:
        List[Dict]: List of documents from MongoDB
    """
    try:
        # Connect to MongoDB
        mongo_db = _connect_mongo(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db
        )

        # Exécution de la requête
        cursor = collection.find(query).limit(limit) if limit else collection.find(query)
        result = list(cursor)

        logger.info(f"Successfully read {len(result)} documents from {db}.{collection}")
        return result
    except Exception as e:
        logger.error(f"Error reading from MongoDB: {str(e)}")
        raise


def rewrite_data(
        db: str,
        collection: str,
        data: List[Dict[str, Any]],
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> None:
    """
    Delete existing documents and insert new data into MongoDB collection

    Args:
        db: Database name
        collection: Collection name
        data: List of documents to insert
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication
    """
    if not data:
        logger.warning("No data provided for rewriting. Operation aborted.")
        return

    try:
        # Connect to MongoDB
        mongo_db = _connect_mongo(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db
        )
        collection_obj = mongo_db[collection]

        # Extract IDs from data, handling both string and ObjectId formats
        properties_ids = []
        for doc in data:
            if '_id' in doc:
                # Add the ID as is
                properties_ids.append(doc['_id'])

                # If it's not already a string, add string version too
                if not isinstance(doc['_id'], str):
                    properties_ids.append(str(doc['_id']))

        # Delete existing documents with matching IDs
        if properties_ids:
            result = collection_obj.delete_many({'_id': {'$in': properties_ids}})
            logger.info(f"{result.deleted_count} documents deleted from {db}.{collection}")

        # Insert new documents
        if data:
            insert_result = collection_obj.insert_many(data)
            logger.info(f"{len(insert_result.inserted_ids)} documents inserted into {db}.{collection}")
    except Exception as e:
        logger.error(f"Error rewriting data in MongoDB: {str(e)}")
        raise


def convert_id_to_integer(
        db: str,
        collection: str,
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> None:
    """
    Convert string IDs to integers in MongoDB collection

    Args:
        db: Database name
        collection: Collection name
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication
    """
    try:
        # Connect to MongoDB
        mongo_db = _connect_mongo(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db
        )
        collection_obj = mongo_db[collection]

        # Process documents
        total_count = collection_obj.count_documents({})
        converted_count = 0

        for document in collection_obj.find({}):
            id_value = document.get('_id')

            # Check if ID is a string and not an ObjectId
            if isinstance(id_value, str):
                try:
                    # Try to convert to integer
                    id_int = int(id_value)

                    # Update document with integer ID
                    collection_obj.delete_one({'_id': id_value})
                    document['_id'] = id_int
                    collection_obj.insert_one(document)

                    converted_count += 1
                except ValueError:
                    logger.warning(f"Could not convert ID '{id_value}' to integer")

        logger.info(f"Converted {converted_count} out of {total_count} document IDs to integers")
    except Exception as e:
        logger.error(f"Error converting IDs to integers: {str(e)}")
        raise


def update_documents(
        db: str,
        collection: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> int:
    """
    Update documents in MongoDB collection

    Args:
        db: Database name
        collection: Collection name
        query: Query to select documents to update
        update: Update operations to apply
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication

    Returns:
        int: Number of documents updated
    """
    try:
        # Connect to MongoDB
        mongo_db = _connect_mongo(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db
        )
        collection_obj = mongo_db[collection]

        # Update documents
        result = collection_obj.update_many(query, update)
        logger.info(f"Updated {result.modified_count} documents in {db}.{collection}")

        return result.modified_count
    except Exception as e:
        logger.error(f"Error updating documents in MongoDB: {str(e)}")
        raise


def get_distinct_values(
        db: str,
        collection: str,
        field: str,
        query: Dict[str, Any] = {},
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None
) -> List[Any]:
    """
    Get distinct values for a field in MongoDB collection

    Args:
        db: Database name
        collection: Collection name
        field: Field to get distinct values for
        query: Query to filter documents
        host: MongoDB host address
        port: MongoDB port
        username: MongoDB username for authentication
        password: MongoDB password for authentication

    Returns:
        List: List of distinct values
    """
    try:
        # Connect to MongoDB
        mongo_db = _connect_mongo(
            host=host,
            port=port,
            username=username,
            password=password,
            db=db
        )
        collection_obj = mongo_db[collection]

        # Get distinct values
        distinct_values = collection_obj.distinct(field, query)
        logger.info(f"Found {len(distinct_values)} distinct values for {field} in {db}.{collection}")

        return distinct_values
    except Exception as e:
        logger.error(f"Error getting distinct values from MongoDB: {str(e)}")
        raise
