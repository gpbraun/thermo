"""
Cálculo de temperatura adiabática de chama
"""

import streamlit as st
import json

import constant_volume
import constant_pressure

with open('data/compositions.json', 'r') as json_file:
    COMPOSITIONS = json.load(json_file)

st.title('LQM ICT')

st.header('Composição')

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

MODES[mode](composition)
