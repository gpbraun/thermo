import cantera as ct
import pandas as pd


def input(container):
    """Recebe os dados para o cálculo de ignição em volume constante."""
    V = float(container.number_input('Pressão P/MPa', value=30)) * 1e6
    m = float(container.number_input('Massa m/g', value=2.5)) * 1e-3
    return V, m


def constant_pressure_burn(composition: dict, P: float, m: float) -> ct.Quantity:
    """Retorna o estado final da queima a volume constante"""
    sol = ct.Solution('data/thermodat.yaml')
    sol.TPY = 300, P, composition
    sol.equilibrate('HP', max_steps=1e5)

    return ct.Quantity(sol, mass=m)


def results(container, composition, V, m):
    """Apresenta os resultados da queima em volume constante."""
    out = constant_pressure_burn(composition, V, m)

    col1, col2 = container.columns(2)

    col1.metric(label='Temperatura', value=f'{out.T:.2f} K')
    col2.metric(label='Volume final', value=f'{out.volume*1e6:.2f} cm³')

    container.subheader('Produtos de Explosão')

    fractions = out.mass_fraction_dict(1e-3)

    df = pd.DataFrame.from_dict(
        fractions, orient='index', columns=['Fração mássica'])

    container.bar_chart(df)


def main(parameters_container, results_container, composition):
    P, m = input(parameters_container)
    results(results_container, composition, P, m)
