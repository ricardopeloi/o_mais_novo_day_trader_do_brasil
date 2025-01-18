# https://pypi.org/project/yfinance/
# https://github.com/ranaroussi/yfinance/wiki/Ticker

# !python -m pip install yfinance
import yfinance as yf

# !python -m pip install mplfinance
# import mplfinance as mpf



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
    from os import listdir
    from datetime import datetime, timedelta
    import pandas as pd
    

    ## ATUALIZA DADOS NA PASTA
    from receber_lista_atualizada_tickers import tratar_lista_B3, ler_lista_B3
    tratar_lista_B3(ler_lista_B3())

    from detectar_martelos import criar_regressao_bd_acao, detectar_martelos_todos_os_tickers
    detectar_martelos_todos_os_tickers()


    ## IMPRIME AS 5 MELHORES AÇÕES DOS ÚLTIMOS DIAS
    lista_arquivos = listdir("Bases")
    lista_arquivos_analises = []
    for arquivo in lista_arquivos:
        if arquivo.find(" Análise") > 0:
            lista_arquivos_analises.append(datetime.strptime(arquivo.split(" Análise ")[1].split(".xls")[0], "%Y-%m-%d"))

    var_arquivo_mais_recente = "Bases/Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx"
    # print(var_arquivo_mais_recente)

    
    bd_lista_acoes_analise = pd.read_excel(var_arquivo_mais_recente, index_col = "Ticker")
    print(bd_lista_acoes_analise.sort_values("Alfa (15 dias)", ascending = False).head(5))
    print()


    qtd_dias = 15
    for acao in bd_lista_acoes_analise.sort_values("Alfa (15 dias)", ascending = False).head(5).index:
        # print(acao)

        bd_acao = yf.Ticker(acao + ".SA").history(
            start = datetime.today() - timedelta(days=qtd_dias),
            end = datetime.today(),
            interval = "1d"
        )
        bd_acao.index = bd_acao.index.tz_localize(None)

        print(acao)
        [bd_acao_regressao, media, margem, modelo_linear, valor_fechamento] = criar_regressao_bd_acao(
            bd_acao,
            coluna = "Close",
            print_variaveis = True,
            # plot_grafico = True,
            titulo = acao + " (fechamento dos últimos " + str(qtd_dias) + " dias)",
            tamanho_figsize = (15, 6),
            # rotacao = 60,
        )
        
        print()


if __name__ == "__main__":
    main()