# https://pypi.org/project/yfinance/
# https://github.com/ranaroussi/yfinance/wiki/Ticker

# !python -m pip install yfinance
import yfinance as yf

# !python -m pip install mplfinance
# import mplfinance as mpf

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



def gerar_top_recomendacoes(
        var_qtd_top_acoes = 5,
        qtd_dias = 55
    ):
    from os import listdir
    from datetime import datetime, timedelta
    import pandas as pd

    from detectar_martelos import criar_regressao_bd_acao
    
    # var_qtd_top_acoes = 5

    lista_arquivos = listdir("Bases")
    # lista_arquivos = listdir(os.environ.get('var_caminho_fonte').split("\\")[-1])
    lista_arquivos_analises = []
    for arquivo in lista_arquivos:
        if arquivo.find(" Análise") > 0:
            lista_arquivos_analises.append(datetime.strptime(arquivo.split(" Análise ")[1].split(".xls")[0], "%Y-%m-%d"))

    # var_arquivo_mais_recente = os.environ.get('var_caminho_fonte') + r"\Bases\Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx"
    # var_arquivo_mais_recente = r"\Bases\Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx"
    # print(var_arquivo_mais_recente)

    
    # bd_lista_acoes_analise = pd.read_excel(var_arquivo_mais_recente, index_col = "Ticker")
    bd_lista_acoes_analise = pd.read_excel(r"C:\Users\ricardopeloi\OneDrive - falconi365\Data Science\O_Mais_Novo_Day_Trader_do_Brasil\o_mais_novo_day_trader_do_brasil\Bases\Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx", index_col = "Ticker")
    
    # print(bd_lista_acoes_analise.sort_values("Alfa HLC; últimos 55 dias", ascending = False).head(5))
    # print()

    # bd_historico_completo = pd.read_excel("Bases\Base de Dados Histórico.xlsx")
    bd_historico_completo = pd.read_excel(r"C:\Users\ricardopeloi\OneDrive - falconi365\Data Science\O_Mais_Novo_Day_Trader_do_Brasil\o_mais_novo_day_trader_do_brasil\Bases\Base de Dados Histórico.xlsx")


    
    var_print_arquivo = ""
    
    for acao in bd_lista_acoes_analise.sort_values("Alfa HLC; últimos " + str(qtd_dias) + " dias", ascending = False).head(var_qtd_top_acoes).index:
        # print(acao)

        # bd_acao = yf.Ticker(acao + ".SA").history(
        #     start = datetime.today() - timedelta(days=qtd_dias),
        #     end = datetime.today(),
        #     interval = "1d"
        # )
        bd_historico_completo_acao = bd_historico_completo[bd_historico_completo["Ticker"] == acao].set_index("Date")
        # bd_historico_completo_acao.index = bd_historico_completo_acao.index.tz_localize(None)

        # print(acao)
        var_print_arquivo = var_print_arquivo + acao + '\n'

        [_, _, _, _, _, var_print] = criar_regressao_bd_acao(
            bd_historico_completo_acao.sort_index().iloc[:int(qtd_dias/7*5), :],
            coluna = "Close",
            print_variaveis = False,
            # plot_grafico = True,
            titulo = acao + " (fechamento dos últimos " + str(qtd_dias) + " dias)",
            tamanho_figsize = (15, 6),
            # rotacao = 60,
        )
        
        # print(var_print)
        var_print_arquivo = var_print_arquivo + var_print

    print(var_print_arquivo)

    arquivo_output = open("Recomendações/Top " + str(var_qtd_top_acoes) + " ações.txt", "w")
    arquivo_output.write(var_print_arquivo)
    arquivo_output.close() 



def main():

    ## ATUALIZA DADOS NA PASTA
    from receber_lista_atualizada_tickers import tratar_lista_B3, ler_lista_B3
    
    ### Lê tudo do zero, via lista no site da B3
    # var_caminho = os.environ.get('var_caminho_fonte')
    # var_caminho = r"\Bases"

    # # bd_lista_acoes = ler_lista_B3()
    tratar_lista_B3(ler_lista_B3())
    # tratar_lista_B3(ler_lista_B3(var_caminho), var_caminho)
    
    # ### Lê a lista já lida anteriormente, presente na pasta do projeto
    # # bd_lista_acoes = pd.read_excel('Bases/Lista de ações.xlsx', index_col = "Ticker")
    
    # # tratar_lista_B3(bd_lista_acoes)


    from detectar_martelos import detectar_martelos_todos_os_tickers
    detectar_martelos_todos_os_tickers(
        # qtd_dias_maximo = 55,
        # qtd_dias_minimo = 13
    )


    ## IMPRIME AS TOP AÇÕES DO ÚLTIMO ARQUIVO ATUALIZADO
    gerar_top_recomendacoes(
        var_qtd_top_acoes = 5
    )

    input("Aperte Enter para sair... ")


if __name__ == "__main__":
    main()