import uuid
import services.database as db
from azure.cosmos import exceptions

def generate_uuid(cnpj):
    """
    Gera um UUID único para o estabelecimento caso o UUID gerado não exista no banco de dados.

    :param cnpj: string (CNPJ do estabelecimento)

    :return string (UUID único)
    """
    while True:
        random_uuid = str(uuid.uuid4())
        try:
            item = db.container.read_item(item=random_uuid, partition_key=cnpj)
        except exceptions.CosmosResourceNotFoundError:
            return random_uuid