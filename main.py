import os
from pathlib import Path  # Python 3.6+ only
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def check_and_install_packages(packages):
    import importlib
    import subprocess
    import sys

    # FONTE: https://stackoverflow.com/questions/76386461/how-to-use-python-to-check-for-and-install-librarys

    for package in packages:
        try:
            importlib.import_module(package)
            # print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")


def main():

    ## ATUALIZA DADOS NA PASTA
    from receber_lista_atualizada_tickers import tratar_lista_B3, ler_lista_B3
    
    ### Lê tudo do zero, via lista no site da B3
    var_caminho = os.environ.get('var_caminho_fonte') + r"\Bases"
    # var_caminho = r"\Bases"
    print(var_caminho)

    # # bd_lista_acoes = ler_lista_B3()
    # tratar_lista_B3(ler_lista_B3())
    tratar_lista_B3(ler_lista_B3(var_caminho, var_print_tickers = False), var_caminho)
    
    # ### Lê a lista já lida anteriormente, presente na pasta do projeto
    # import pandas as pd
    # bd_lista_acoes = pd.read_excel('Bases/Lista de ações.xlsx', index_col = "Ticker")
    
    # # tratar_lista_B3(bd_lista_acoes)


    from detectar_martelos import detectar_martelos_todos_os_tickers
    detectar_martelos_todos_os_tickers(
        # qtd_dias_maximo = 55,
        # qtd_dias_minimo = 13
    )


    ## IMPRIME AS TOP AÇÕES DO ÚLTIMO ARQUIVO ATUALIZADO
    from realizar_analises import gerar_top_recomendacoes
    gerar_top_recomendacoes(
        var_qtd_top_acoes = 5
    )

    input("Aperte Enter para sair... ")


if __name__ == "__main__":
    # pip install -r requirements.txt 
    main()