import os, uuid
from azure.cosmos import CosmosClient, exceptions
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

cosmos_uri = os.environ['COSMOS_DB_URI']
cosmos_key = os.environ['COSMOS_DB_KEY']
cosmos_database = os.environ['COSMOS_DB_DATABASE']
cosmos_container = os.environ['COSMOS_DB_CONTAINER']

cosmos_client = CosmosClient(cosmos_uri, credential=cosmos_key)
database_client = cosmos_client.get_database_client(cosmos_database)
container_client = database_client.get_container_client(cosmos_container)

@app.route('/')
def index():
    item_iterator = container_client.read_all_items()
    storeList = [item for item in item_iterator]
    return render_template('index.html', stores = storeList)

@app.route('/create', methods=['POST'])
def create():

    def generate_uuid(partition_key):
        while True:
            random_uuid = str(uuid.uuid4())
            try:
                item = container_client.read_item(item=random_uuid, partition_key=partition_key)
            except exceptions.CosmosResourceNotFoundError:
                return random_uuid

    if request.method == 'POST':
        name = request.form['name']
        cnpj = request.form['cnpj']

        container_client.create_item({'name': name, 'cnpj': cnpj, 'id': generate_uuid(cnpj)})
        
        flash('Empresa cadastrada com sucesso!')
        return redirect(url_for('index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cnpj = request.form['cnpj']
        
        item = container_client.read_item(item=id_data, partition_key=cnpj)
        item['name'] = name
        item['cnpj'] = cnpj
        container_client.replace_item(item=id_data, body=item)
        flash('Empresa atualizada com sucesso!')
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>/<string:cnpj>', methods=['POST', 'GET'])
def delete(id_data, cnpj):
    container_client.delete_item(item=id_data, partition_key=cnpj)
    flash('Empresa removida com sucesso!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)