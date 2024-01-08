import streamlit as st
import models.Store as store
import controllers.crud as crud
import services.uuid as svc_uuid

def create():
    parametros_alteracao = st.experimental_get_query_params()
    st.experimental_set_query_params()
    uuid = None
    cnpj = None
    clienteRecuperado = None
    if parametros_alteracao.get("id") != None and parametros_alteracao.get("cnpj") != None:
        uuid = parametros_alteracao.get("id")[0]
        cnpj = parametros_alteracao.get("cnpj")[0]
        st.title('Alteração de Estabelecimentos')
        clienteRecuperado = crud.read_by_uuid(uuid, cnpj)
        st.experimental_set_query_params(id=[uuid], cnpj=[cnpj])
    else:
        st.title('Cadastro de Estabelecimentos')
    with st.form (key='include_store'):
        if clienteRecuperado == None:
            input_name = st.text_input(label='Insira o nome do seu estabelecimento')
            input_cnpj = st.text_input(label='Insira o CNPJ do seu estabelecimento')
            input_store_type = st.selectbox(label='Selecione o tipo do seu estabalecimento', options=['Digital', 'Físico'])
        elif clienteRecuperado == '404':
            st.error('Estabelecimento não encontrado!')
        elif type(clienteRecuperado) is store.Store:
            input_name = st.text_input(label='Insira o nome do seu estabelecimento', value=clienteRecuperado.nome)
            input_cnpj = st.text_input(label='Insira o CNPJ do seu estabelecimento', value=clienteRecuperado.cnpj)
            input_store_type = st.selectbox(label='Selecione o tipo do seu estabalecimento', options=['Digital', 'Físico'], index=0 if clienteRecuperado.tipo == 'Digital' else 1)
        else:
            st.error('Erro ao recuperar estabelecimento!\nErro: ' + clienteRecuperado)
        input_button_submit = st.form_submit_button(label='Enviar')
    if input_button_submit:
        if clienteRecuperado == None:
            resposta = crud.create(store.Store(svc_uuid.generate_uuid(input_cnpj), input_name, input_cnpj, input_store_type))
            if resposta == 'Cadastrado':
                st.success('Estabelecimento cadastrado com sucesso!')
            else:
                st.error('Erro ao cadastrar estabelecimento!\nErro: ' + resposta)
        elif type(clienteRecuperado) is store.Store:
            st.experimental_set_query_params()
            resposta = crud.update(store.Store(uuid, input_name, input_cnpj, input_store_type))
            if resposta == '200':
                st.success('Estabelecimento alterado com sucesso!')
            elif resposta == '404':
                st.error('Estabelecimento não encontrado!')
            else:
                st.error('Erro ao alterar estabelecimento!\nErro: ' + resposta)