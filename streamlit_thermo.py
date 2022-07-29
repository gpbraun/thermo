"""
Aplicativo para o cálculo da temperatura adiabática de chama
"""

import streamlit as st
import json

import constant_volume
import constant_pressure

st.set_page_config(page_title='LQM', page_icon=':bomb:')

col1, col2 = st.columns((10,1)) 

col1.title('LQM - Simulação de Explosão')
col1.caption('Centro Tecnológico do Exército, Laboratório de Química Militar')
col1.markdown("**Contato:** braun.pineschi@eb.mil.br")

# col2.image('images/logo-ctex.png', width = 100)

st.header('Composição')

with open('data/compositions.json', 'r') as json_file:
    COMPOSITIONS = json.load(json_file)

other_key = 'Outro'

composition_id = st.radio('Pólvora', list(COMPOSITIONS) + [other_key])

if composition_id == other_key:
    st.file_uploader('Arquivo CSV')
else:
    composition = COMPOSITIONS[composition_id]['composition']

st.header('Parâmetros')

MODES = {
    'Volume constante': constant_volume.main,
    'Pressão constante': constant_pressure.main
}

mode = st.radio('Modo', list(MODES))

parameters_container = st.container()

st.header('Resultados')

results_container = st.container()

try:
    MODES[mode](parameters_container, results_container, composition)
except NameError:
    st.error('Erro na definição da composição!')
