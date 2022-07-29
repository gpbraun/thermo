import cantera as ct
import pandas as pd


def input(container):
    """Recebe os dados para o cálculo de ignição em volume constante."""
    V = float(container.number_input('Volume V/cm³', value=100)) * 1e-6
    m = float(container.number_input('Massa m/g', value=2.5)) * 1e-3

    return V, m


def constant_volume_burn(composition: dict, V: float, m: float) -> ct.Quantity:
    """Retorna o estado final da queima a volume constante."""
    sol = ct.Solution('data/thermodat.yaml')
    sol.TDY = 300, m/V, composition
    sol.equilibrate('UV', max_steps=1e5)

    return ct.Quantity(sol, mass=m)


def results(container, composition, V, m):
    """Apresenta os resultados da queima em volume constante."""
    out = constant_volume_burn(composition, V, m)

    col1, col2 = container.columns(2)

    col1.metric(label='Temperatura', value=f'{out.T:.2f} K')
    col2.metric(label='Pressão final', value=f'{out.P/1e6:.2f} MPa')

    container.subheader('Produtos de Explosão')

    fractions = out.mass_fraction_dict(1e-4)

    df = pd.DataFrame.from_dict(
        fractions, orient='index', columns=['Fração mássica'])

    container.bar_chart(df)


def main(parameters_container, results_container, composition):
    V, m = input(parameters_container)
    results(results_container, composition, V, m)
