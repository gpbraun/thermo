import streamlit as st
import cantera as ct
import pandas as pd


def input():
    """Recebe os dados para o cálculo de ignição em volume constante.
    """
    V = float(st.number_input('Volume V/cm3', value=100)) * 1e-6
    m = float(st.number_input('Massa m/g', value=2.5)) * 1e-3
    return V, m


def constant_volume_burn(composition: dict, V: float, m: float) -> ct.Quantity:
    """Retorna o estado final da queima a volume constante
    """
    sol = ct.Solution('data/thermodat.yaml')
    sol.TDY = 300, m/V, composition
    sol.equilibrate('UV', max_steps=1e5)

    return ct.Quantity(sol, mass=m)


def results(composition, V, m):
    """Apresenta os resultados da queima em volume constante.
    """
    out = constant_volume_burn(composition, V, m)

    st.header('Resultados')

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label = 'Temperatura', value = f'{out.T:.2f} K')
    
    with col2:
        st.metric(label = 'Pressão final', value = f'{out.P/1e6:.2f} MPa')

    st.subheader('Produtos de Combustão')

    fractions = out.mass_fraction_dict(1e-4)

    df = pd.DataFrame.from_dict(
        fractions, orient='index', columns=['Fração mássica'])

    st.bar_chart(df)


def main(composition):
    V, m = input()
    results(composition, V, m)
