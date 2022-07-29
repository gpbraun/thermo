"""
Cálculo de temperatura adiabática de chama
"""

import streamlit as st
import cantera as ct
import pandas as pd
import json

st.title('LQM ICT')

st.header('Composição')

with open('data/compositions.json', 'r') as json_file:
        compositions = json.load(json_file)

options = [comp for comp in compositions]
options.append('Outro')

composition = st.radio('Pólvora', options)

if composition == 'Outro':
    st.file_uploader('Arquivo CSV')
    st.experimental_rerun()
else:
    composition_dict = compositions[composition]['composition']

st.header('Parâmetros')

st.radio('Modo', ['Volume constante'])

V = float(st.number_input('Volume V/cm3', value = 100)) * 1e-6
m = float(st.number_input('Massa m/g', value = 2.5)) * 1e-3

bd = ct.Solution('data/thermodat.yaml')
bd.TDY = 300, m/V, composition_dict

U0 = bd.int_energy_mass

st.header('Resultados')

bd.equilibrate('UV', max_steps=1e5)

q = ct.Quantity(bd, mass=m)

P = bd.P/1e6

U = bd.int_energy_mass

dU = (U - U0) * 1000 / 4.2

st.text(f'Temperatura: {bd.T:.2f} K')
st.text(f'Pressão: {P:.2f} MPa')
# st.text(f'Calor de combustão: {dU} cal/g')

st.header('Produtos de Combustão')

fractions = bd.mass_fraction_dict(1e-4)
mole_fractions = bd.mole_fraction_dict(1e-4)

for substance, mass_fraction in fractions.items():
    try:
        fractions[substance] = [mass_fraction, mole_fractions[substance]]
    except KeyError:
        pass

df = pd.DataFrame.from_dict(fractions, orient='index', columns=['Fração mássica', 'Fração molar'])

st.bar_chart(df)

    

