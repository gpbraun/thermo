"""
Cálculo de temperatura adiabática de chama
"""

import cantera as ct

COMPOSITIONS = {
    "BD IMBEL 409": {
        "composition": {
            "NC": 56.90,
            "NG": 40.09,
            "EC": 3.01,
            "C": 0.05
        }
    },
    "BD IMBEL 257": {
        "composition": {
            "NC": 54.72,
            "NG": 43.86,
            "EC": 1.42,
            "C": 0.05
        }
    },
    "BD IMBEL 258": {
        "composition": {
            "NC": 56.50,
            "NG": 39.80,
            "EC": 1.40,
            "DBP": 2.30, 
            "C": 0.05
        }
    }
}

def main():
    V = 100e-6 # m3
    m = 3e-3 # g

    composition_dict = {'NC': 56.50, 'NG': 39.8, 'DBP': 1.40, 'EC': 2.30, 'C': 0.05}

    bd = ct.Solution('data/BD.yaml')
    bd.TDY = 300, m/V, composition_dict

    mix = ct.Mixture([
        (bd, 1),
        (ct.Solution('data/gas.yaml'), 0)
    ])

    mix.equilibrate('UV')

    print(mix.T)
    print(mix.P/1e6)

if __name__ == '__main__':
    
    main()
