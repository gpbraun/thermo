"""
Cálculo de temperatura adiabática de chama
"""

import streamlit as st
import cantera as ct
import pandas as pd

st.title('LQM ICT')

st.header('Composição')

composition = st.radio('Pólvora', ['IMBEL BD 528'])

composition_dict = {'NC': 56.50, 'NG': 39.8, 'DBP': 1.40, 'EC': 2.30, 'C': 0.05}

st.header('Parâmetros')

st.radio('Modo', ['Volume constante'])

V = float(st.number_input('Volume V/cm3', value = 100)) * 1e-6
m = float(st.number_input('Massa m/g', value = 2.5)) * 1e-3

bd = ct.Solution('data/thermodat.yaml')
bd.TDY = 300, m/V, composition_dict

st.header('Resultados')

bd.equilibrate('UV', max_steps=1e5)

q = ct.Quantity(bd, mass=m)

P = bd.P/1e6

st.text(f'Temperatura: {bd.T:.2f} K')
st.text(f'Pressão: {P:.2f} MPa')

st.header('Produtos de Combustão')

fractions = bd.mass_fraction_dict(1e-4)
mole_fractions = bd.mole_fraction_dict(1e-4)

for substance, mass_fraction in fractions.items():
    fractions[substance] = [mass_fraction, mole_fractions[substance]]

df = pd.DataFrame.from_dict(fractions, orient='index', columns=['Fração mássica', 'Fração molar'])

st.bar_chart(df)
