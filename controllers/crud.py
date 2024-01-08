import services.database as db
from azure.cosmos import exceptions
import models.Store as store

def create(store):
    """
    Cria um novo estabelecimento no banco de dados.

    :param store: Store (objeto da classe Store)

    :return string (mensagem de sucesso ou erro)
    """
    output = ""
    item_to_create = {'id': store.uuid, 'cnpj': store.cnpj, 'nome': store.nome, 'tipo': store.tipo}
    try:
        db.container.create_item(body=item_to_create)
        output = "Cadastrado"
    except exceptions.CosmosHttpResponseError as e:
        output = e.message
    return output

def read_by_uuid(uuid, cnpj, executor="user"):
    """
    Lê um estabelecimento cadastrado no banco de dados.

    :param uuid: string (UUID do estabelecimento)
    :param cnpj: string (CNPJ do estabelecimento)
    :param executor: string (executor da função - só deve ser informado se for executado pelo sistema)

    :return Store (objeto da classe Store)
    """
    try:
        item = db.container.read_item(item=uuid, partition_key=cnpj)
        if executor == "system":
            return item
        else:
            return store.Store(item['id'], item['nome'], item['cnpj'], item['tipo'])
    except exceptions.CosmosResourceNotFoundError:
        return "404"
    except exceptions.CosmosHttpResponseError as e:
        return e.message

def read():
    """
    Lê todos os estabelecimentos cadastrados no banco de dados.

    :return list (lista de objetos da classe Store)
    """
    item_iterator = db.container.read_all_items()
    storeList = []
    for item in item_iterator:
        storeList.append(store.Store(item['id'], item['nome'], item['cnpj'], item['tipo']))
    return storeList

def update(store):
    """
    Atualiza um estabelecimento no banco de dados.

    :param store: Store (objeto da classe Store)

    :return string (mensagem de sucesso ou erro)
    """
    try:
        item = read_by_uuid(store.uuid, store.cnpj, "system")
        item['nome'] = store.nome
        item['tipo'] = store.tipo
        item['cnpj'] = store.cnpj
    except Exception as e:
        return e.message
    
    try:
        db.container.replace_item(item=store.uuid, body=item)
        return "200"
    except exceptions.CosmosResourceNotFoundError:
        return "404"
    except exceptions.CosmosHttpResponseError as e:
        return e.message

def delete(uuid, cnpj):
    """
    Deleta um estabelecimento do banco de dados.

    :param uuid: string (UUID do estabelecimento)
    :param cnpj: string (CNPJ do estabelecimento)

    :return string (mensagem de sucesso ou erro)
    """
    try:
        db.container.delete_item(item=uuid, partition_key=cnpj)
        return "200"
    except exceptions.CosmosResourceNotFoundError:
        return "404"
    except exceptions.CosmosHttpResponseError as e:
        return e.message