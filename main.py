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
    # tratar_lista_B3(ler_lista_B3())
    # bd_lista_acoes = ler_lista_B3()
    # bd_lista_acoes = pd.read_excel('Bases/Lista de ações.xlsx', index_col = "Ticker")
    # tratar_lista_B3(bd_lista_acoes)

    from detectar_martelos import criar_regressao_bd_acao, detectar_martelos_todos_os_tickers
    detectar_martelos_todos_os_tickers(
        # qtd_dias_maximo = 55,
        # qtd_dias_minimo = 13
    )


    ## IMPRIME AS 5 MELHORES AÇÕES DOS ÚLTIMOS DIAS
    lista_arquivos = listdir("Bases")
    lista_arquivos_analises = []
    for arquivo in lista_arquivos:
        if arquivo.find(" Análise") > 0:
            lista_arquivos_analises.append(datetime.strptime(arquivo.split(" Análise ")[1].split(".xls")[0], "%Y-%m-%d"))

    var_arquivo_mais_recente = "Bases/Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx"
    # print(var_arquivo_mais_recente)

    
    bd_lista_acoes_analise = pd.read_excel(var_arquivo_mais_recente, index_col = "Ticker")
    print(bd_lista_acoes_analise.sort_values("Alfa HLC; últimos 55 dias", ascending = False).head(5))
    print()

    bd_historico_completo = pd.read_excel("Bases\Base de Dados Histórico.xlsx")


    qtd_dias = 15
    for acao in bd_lista_acoes_analise.sort_values("Alfa HLC; últimos 55 dias", ascending = False).head(5).index:
        # print(acao)

        # bd_acao = yf.Ticker(acao + ".SA").history(
        #     start = datetime.today() - timedelta(days=qtd_dias),
        #     end = datetime.today(),
        #     interval = "1d"
        # )
        bd_historico_completo_acao = bd_historico_completo[bd_historico_completo["Ticker"] == acao].set_index("Date")
        # bd_historico_completo_acao.index = bd_historico_completo_acao.index.tz_localize(None)

        print(acao)
        [_, _, _, _, _] = criar_regressao_bd_acao(
            bd_historico_completo_acao,
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