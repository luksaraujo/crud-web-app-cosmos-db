import os
from azure.cosmos import CosmosClient

uri = os.environ['COSMOS_URI']
key = os.environ['COSMOS_KEY']
client = CosmosClient(uri, credential=key)

db_name = os.environ['COSMOS_DB_NAME']
database = client.get_database_client(db_name)

container_name = os.environ['COSMOS_CONTAINER_NAME']
container = database.get_container_client(container_name)