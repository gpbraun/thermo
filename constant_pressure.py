import streamlit as st
import cantera as ct
import pandas as pd


def input():
    """Recebe os dados para o cálculo de ignição em volume constante.
    """
    V = float(st.number_input('Pressão P/MPa', value=100)) * 1e6
    m = float(st.number_input('Massa m/g', value=2.5)) * 1e-3
    return V, m


def constant_pressure_burn(composition: dict, P: float, m: float) -> ct.Quantity:
    """Retorna o estado final da queima a volume constante
    """
    sol = ct.Solution('data/thermodat.yaml')
    sol.TPY = 300, P, composition
    sol.equilibrate('HP', max_steps=1e5)

    return ct.Quantity(sol, mass=m)


def results(composition, V, m):
    """Apresenta os resultados da queima em volume constante.
    """
    out = constant_pressure_burn(composition, V, m)

    st.header('Resultados')

    st.text(f'Temperatura: {out.T:.2f} K')
    st.text(f'Volume final: {out.volume*1e6:.2f} cm3')

    st.header('Produtos de Combustão')

    fractions = out.mass_fraction_dict(1e-4)

    df = pd.DataFrame.from_dict(
        fractions, orient='index', columns=['Fração mássica'])

    st.bar_chart(df)


def main(composition):
    P, m = input()
    results(composition, P, m)

