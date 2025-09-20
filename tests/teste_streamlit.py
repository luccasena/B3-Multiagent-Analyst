import streamlit as st

# Inicialização
if 'nome' not in st.session_state:
    st.session_state.nome = ''
if 'idade' not in st.session_state:
    st.session_state.idade = 0

# Função de callback para submeter o formulário
def submeter_formulario():
    st.session_state.submetido = True

# Campos de entrada
st.text_input("Nome", key='nome')
st.number_input("Idade", key='idade', min_value=0)

# Botão para submeter o formulário
st.button("Submeter", on_click=submeter_formulario)

# Exibir os dados submetidos
if st.session_state.get('submetido', False):
    st.write(f"Nome: {st.session_state.nome}")
    st.write(f"Idade: {st.session_state.idade}")