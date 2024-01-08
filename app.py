import streamlit as st
import controllers.crud as crud
import pages.cliente.create as create_page

st.sidebar.title('Menu')
screen = st.sidebar.selectbox('Selecione uma tela para visualizar', ['Create', 'Read'])
if screen == "Read":
    params = st.experimental_get_query_params()
    if params == {}:
        st.experimental_set_query_params()
        columns = st.columns((3, 2, 3, 1, 2, 2))
        campos = ['UUID', 'Nome', 'CNPJ', 'Tipo', 'Excluir', 'Alterar']
        for col, campo_nome in zip(columns, campos):
            col.write(campo_nome)
        for item in crud.read():
            col1, col2, col3, col4, col5, col6 = st.columns((3, 2, 3, 1, 2, 2))
            col1.write(item.uuid)
            col2.write(item.nome)
            col3.write(item.cnpj)
            col4.write(item.tipo)
            button_space_excluir = col5.empty()
            on_click_excluir = button_space_excluir.button('Excluir', 'btnExcluir' + str(item.uuid))
            button_space_alterar = col6.empty()
            on_click_alterar = button_space_alterar.button('Alterar', 'btnAlterar' + str(item.uuid))
            if on_click_excluir:
                resposta = crud.delete(item.uuid, item.cnpj)
                if resposta == '200':
                    st.success('Estabelecimento excluído com sucesso!')
                elif resposta == '404':
                    st.error('Estabelecimento não encontrado!')
                else:
                    st.error('Erro ao excluir estabelecimento!\nErro: ' + resposta)
                button_space_excluir.button('Excluído', 'btnExcluir' + str(item.uuid))
            if on_click_alterar:
                st.experimental_set_query_params(id=[item.uuid], cnpj=[item.cnpj])
                st.experimental_rerun()
    else:
        on_click_voltar = st.button('Voltar')
        if on_click_voltar:
            st.experimental_set_query_params()
            st.experimental_rerun()
        create_page.create()
elif screen == "Create":
    st.experimental_set_query_params()
    create_page.create()
else:
    pass
