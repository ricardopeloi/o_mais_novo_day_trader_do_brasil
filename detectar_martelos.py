# https://pypi.org/project/yfinance/
# https://github.com/ranaroussi/yfinance/wiki/Ticker

# !python -m pip install yfinance
import yfinance as yf

# !python -m pip install mplfinance
# import mplfinance as mpf

import numpy as np

import os
from pathlib import Path  # Python 3.6+ only
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
var_caminho = os.environ.get('var_caminho_fonte')


def criar_regressao_bd_acao(
    bd_acao,
    coluna = "Close",
    print_variaveis = False,
    plot_grafico = False,
    tamanho_figsize = (10,5),
    rotacao = 45,
    titulo = "Pontos no fechamento da ação",
    var_pular_final_de_semana_feriados = False,
):

    # !python -m pip install scikit-learn
    from sklearn.linear_model import LinearRegression

    bd_acao_coluna = bd_acao.reset_index()[[bd_acao.index.name, coluna]]

    X = bd_acao_coluna.reset_index()["index"].array.reshape(-1, 1)
    y = bd_acao_coluna.loc[:, coluna].array.reshape(-1, 1)

    modelo_linear = LinearRegression()
    modelo_linear.fit(X, y)

    bd_acao_coluna.loc[:, "Regressão"] = modelo_linear.predict(X)
    # bd_acao_fim

    desvio_padrao = bd_acao_coluna[coluna].std()
    media = bd_acao_coluna[coluna].mean()
    alfa = modelo_linear.coef_[0][0]
    valor_fechamento = bd_acao_coluna.sort_index(ascending = False).iloc[0][coluna]

    # margem = 0.005
    margem = desvio_padrao/media

    var_print = \
        "Preço médio (R$): " + "{:.4f}".format(media) + '\n' + \
        "Desvio padrão (R$): " + "{:.4f}".format(desvio_padrao) + '\n' + \
        "Desvio padrão (%): " + "{:.4f}".format(margem) + '\n' + \
        "Inclinação da reta (alfa, coeficiente angular): " + "{:.4f}".format(alfa) + '\n' + \
        "Preço de fechamento (R$): " + "{:.2f}".format(valor_fechamento) + '\n' + '\n'
    
    if print_variaveis == True:        
        print(var_print)


    if plot_grafico == True:
        from realizar_analises import plotar_grafico_regressao
        plotar_grafico_regressao(
            bd_acao_coluna,
            coluna_analise = "HLC",
            coluna_data = bd_acao.index.name,
            tamanho_figsize = tamanho_figsize,
            rotacao = rotacao,
            titulo = titulo,
            var_pular_final_de_semana_feriados = var_pular_final_de_semana_feriados
        )

    return [bd_acao_coluna, media, desvio_padrao, modelo_linear, valor_fechamento, var_print]



def plota_candlestick_acha_martelos(
    bd_acao,
    # periodo = "21d",
    # intervalo = "1d",
    taxa_máxima_para_ser_martelo = 0.2,
  ):
    
    # bd_acao = yf.Ticker(acao).history(
        # period = periodo,
        # interval = intervalo
    # )
    bd_acao["Amplitude Open-Close"] = abs(bd_acao["Open"] - bd_acao["Close"])
    bd_acao["Amplitude High-Low"] = abs(bd_acao["High"] - bd_acao["Low"])

    # taxa_máxima_para_ser_martelo = 0.2
    bd_acao["Martelo?"] = (bd_acao["Amplitude Open-Close"] < taxa_máxima_para_ser_martelo * bd_acao["Amplitude High-Low"])
    # display(bd_acao)

    # bd_acao.loc[:, "Tipo Martelo"] = ""
    bd_acao.loc[(bd_acao["Martelo?"] == True) * (bd_acao["Open"] > bd_acao["Close"]), "Tipo Martelo"] = "Descida"
    bd_acao.loc[(bd_acao["Martelo?"] == True) * (bd_acao["Open"] <= bd_acao["Close"]), "Tipo Martelo"] = "Subida"
    # display(bd_acao)

    lista_datas_martelo = bd_acao[bd_acao["Martelo?"] == True].sort_index(ascending = False).index.to_list()
    string_datas_martelo = ""

    lista_tipos_martelo = bd_acao[bd_acao["Martelo?"] == True].sort_index(ascending = False)["Tipo Martelo"].to_list()
    string_tipos_martelo = ""

    for data in lista_datas_martelo:
        string_datas_martelo = data.strftime("%Y-%m-%d") + ", " + string_datas_martelo

    for tipo in lista_tipos_martelo:
        string_tipos_martelo = tipo + ", " + string_tipos_martelo


    return [bd_acao, string_datas_martelo, string_tipos_martelo]
    # return [bd_acao, lista_datas_martelo, lista_tipos_martelo]
    # return [bd_acao, string_datas_martelo, lista_tipos_martelo]



# [bd_acao, string_datas_martelo] = plota_candlestick_acha_martelos(
#     acao =  "PETR3" + ".SA",
#     periodo = "60d",
#     intervalo = "1d",
#     taxa_máxima_para_ser_martelo = 0.2,
#     display_candlestick = True,
# )
# print(string_datas_martelo)
# # print(bd_acao)


def processar_regressao_e_lista_de_indicadores(
    bd_acao,
    coluna_analise,
    qtd_dias,
):

    [_, _, _, modelo_linear, _, _] = criar_regressao_bd_acao(
        bd_acao,
        coluna = coluna_analise,
        print_variaveis = False,
        plot_grafico = False,
        # titulo = acao + " (fechamento dos últimos " + str(qtd_dias) + " dias)",
        # tamanho_figsize = (15, 6),
        # rotacao = 60,
    )

    lista_regressao_e_indicadores = []
    lista_regressao_e_indicadores_cabecalho = []
    
    lista_regressao_e_indicadores.append(modelo_linear.coef_[0][0]) # 
    lista_regressao_e_indicadores_cabecalho.append("Alfa HLC; últimos "  + str(qtd_dias) + " dias")
        
    # bd_lista_acoes_analise["Taxa média de Remuneração (R$)"] = bd_lista_acoes_analise["Preço fechamento (R$)"]*bd_lista_acoes_analise["Alfa"]
    # bd_lista_acoes_analise["Taxa média de Remuneração (pp/R$, " + str(qtd_dias) +" dias)"] = \
    # bd_lista_acoes_analise["Alfa (" + str(qtd_dias) +" dias)"]/bd_lista_acoes_analise["Preço fechamento (R$, " + str(qtd_dias) +" dias)"]

    return lista_regressao_e_indicadores_cabecalho, lista_regressao_e_indicadores



def gerar_arquivo_historico():

    import pandas as pd
    from datetime import datetime, timedelta


    bd_arquivo_original = pd.read_excel(var_caminho + r"\Bases\Lista de ações Tratada.xlsx").set_index("Ticker")
    bd_arquivo_original = bd_arquivo_original[bd_arquivo_original["Data da leitura (último dia útil)"] == max(bd_arquivo_original["Data da leitura (último dia útil)"])]


    coluna_analise = "HLC"
    acoes = bd_arquivo_original.index#[[0]]
    # acoes = ["VIVT3", "CLSA3"]

    print("=== LENDO DADOS DE HISTÓRICO ===")
    # var_qtd_acoes = 5
    var_qtd_acoes = len(acoes)

    for contador_acoes, acao in enumerate(acoes[:var_qtd_acoes]):
        print(str(contador_acoes + 1) + " de " + str(var_qtd_acoes) + "; " + acao)
        # print(acao)
        if contador_acoes == 0:
            bd_acoes = pd.DataFrame()

        try:
            bd_acao = yf.Ticker(acao + ".SA").history(
                # start = datetime.today() - timedelta(days=qtd_dias_maximo),
                # assim ele lê apenas os dados entre a maior data da importação e o dia atual
                start = max(bd_arquivo_original["Data da leitura (último dia útil)"]).date(), 
                end = datetime.today(),
                interval = "1d"
            )

            if len(bd_acao) != 0:
                bd_acao[coluna_analise] = (bd_acao["High"] + bd_acao["Low"] + bd_acao["Close"])/3
                bd_acao["Ticker"] = acao
                bd_acoes = pd.concat([bd_acoes, bd_acao])
                # bd_acao = bd_acao.drop("Ação", axis = 1)
                # print(bd_acao)

                if contador_acoes == 0:
                    lista_datas = bd_acao.index.strftime("%Y-%m-%d").to_list()
                    # display(lista_datas)
                
                lista_acao = []

                for counter, data in enumerate(lista_datas):
                    # display(data)
                    
                    lista_acao = lista_acao + bd_acao.iloc[counter].to_list()

        except Exception as e:
            contador_acoes = contador_acoes - 1
            # print("erro")
            print(e.args)

    print("=== FIM DA LEITURA DOS DADOS DE HISTÓRICO ===")


    bd_acoes = bd_acoes.reset_index()
    bd_acoes["Date"] = bd_acoes["Date"].dt.tz_localize(None)

    bd_acoes_import = pd.read_excel(var_caminho + r"\Bases\Base de Dados Histórico.xlsx",
                                    index_col = 0).reset_index()
    bd_acoes_empilhada = pd.concat([bd_acoes_import, bd_acoes]).drop_duplicates(subset = ["Date", "Ticker"])
    bd_acoes_empilhada.set_index("Date").to_excel(var_caminho + r"\Bases\Base de Dados Histórico.xlsx")


    return bd_acoes



def detectar_martelos_todos_os_tickers(qtd_dias_maximo = 55, qtd_dias_minimo = 13):
    # qtd_dias_maximo = int(np.round(55/7*5))
    # qtd_dias_minimo = int(np.round(21/7*5))
    
    import pandas as pd
    from datetime import datetime, timedelta

    # print(os.environ.get('var_caminho_fonte') + r"\Bases\Lista de ações Tratada.xlsx")
    bd_arquivo_original = pd.read_excel(var_caminho + r"\Bases\Lista de ações Tratada.xlsx").set_index("Ticker")
    #f
    bd_arquivo_original = bd_arquivo_original[bd_arquivo_original["Data da leitura (último dia útil)"] == max(bd_arquivo_original["Data da leitura (último dia útil)"])]

    bd_acoes_import_historico = pd.read_excel(var_caminho + r"\Bases\Base de Dados Histórico.xlsx")
    #f  

    acoes = bd_acoes_import_historico["Ticker"].unique()
    # acoes = ["CPLE6", "COCE5", "ALUP4"]
    # acoes = ["COCE5", "ALUP4" ,"HAPV3" ,"AZUL4" ,"COGN3" ,"PETR4" ,"B3SA3" ,"USIM5"]

    coluna_analise = "HLC"

    print("=== MONTANDO BASE DE ANÁLISE ===")
    # var_qtd_acoes = 5
    var_qtd_acoes = len(acoes)

    for contador_acoes, acao in enumerate(acoes[:var_qtd_acoes]):
        print(str(contador_acoes + 1) + " de " + str(var_qtd_acoes) + "; " + acao)
        # print(acao)
        
        bd_acao = bd_acoes_import_historico[
            (bd_acoes_import_historico["Ticker"] == acao) *
            (bd_acoes_import_historico["Date"] >= (max(bd_acoes_import_historico["Date"]) - timedelta(days=qtd_dias_maximo)))
        ].set_index("Date")
        bd_acao = bd_acao.select_dtypes(exclude=['object']).interpolate()
        bd_acao["Ticker"] = acao
        
        try:
            if len(bd_acao) != 0:

                if contador_acoes == 0:
                    lista_datas = bd_acao.index.strftime("%Y-%m-%d").to_list()
                    # display(lista_datas)

                    lista_cabecalho = []
                    lista_acoes = []

                lista_acao = []
                # lista_cabecalho = []

                for counter, data in enumerate(lista_datas):
                    # display(data)
                    
                    if contador_acoes == 0:
                        lista_cabecalho = lista_cabecalho + [data + '; ' + s for s in bd_acao.columns]
                    # lista_cabecalho = lista_cabecalho + [data + '; ' + s for s in bd_acao.columns]
                    lista_acao = lista_acao + bd_acao.iloc[counter].to_list()


                lista_regressao_e_indicadores_cabecalho_minimo, lista_regressao_e_indicadores_minimo = processar_regressao_e_lista_de_indicadores(
                    bd_acao.iloc[-(qtd_dias_minimo):].copy(),
                    coluna_analise,
                    qtd_dias_minimo
                )
                # display(lista_regressao_e_indicadores_minimo)

                lista_regressao_e_indicadores_cabecalho_maximo, lista_regressao_e_indicadores_maximo = processar_regressao_e_lista_de_indicadores(
                    bd_acao.iloc[-(qtd_dias_maximo):].copy(),
                    coluna_analise,
                    qtd_dias_maximo
                )
                # display(lista_regressao_e_indicadores_maximo)

                [_, string_datas_martelo, string_tipos_martelo] = plota_candlestick_acha_martelos(
                    bd_acao,
                    # periodo = str(qtd_dias_maximo)+"d",
                    # intervalo = "1d",
                    taxa_máxima_para_ser_martelo = 0.2,
                    # display_candlestick = False,
                )
                # display(string_datas_martelo)


                if contador_acoes == 0:
                    lista_cabecalho = bd_arquivo_original.reset_index().columns.to_list() \
                        + lista_cabecalho \
                        + lista_regressao_e_indicadores_cabecalho_minimo \
                        + lista_regressao_e_indicadores_cabecalho_maximo \
                        + ["Martelos", "Tipos de Martelos"]
                    # display(len(lista_cabecalho))
                    # display(lista_cabecalho)

                lista_acao = [acao] + bd_arquivo_original.loc[acao].to_list() \
                    + lista_acao \
                    + lista_regressao_e_indicadores_minimo \
                    + lista_regressao_e_indicadores_maximo \
                    + [string_datas_martelo, string_tipos_martelo]
                # display(len(lista_acao))

                lista_acoes.append(lista_acao)
                # display(lista_acoes)

        except Exception as e:
            contador_acoes = contador_acoes - 1
            print(e.args)

    print("=== FIM DA GERAÇÃO BASE DE ANÁLISE ===")

    bd_acao_historico = pd.DataFrame(columns = lista_cabecalho, data = lista_acoes)
    # display(bd_acao_historico)

    bd_acao_historico = bd_acao_historico.drop([item for item in bd_acao_historico.columns.to_list() if "; Ticker" in item], axis = 1)

    bd_acao_historico.set_index("Ticker").to_excel('Bases/Lista de ações Análise ' + datetime.today().strftime("%Y-%m-%d") + '.xlsx')
    # bd_acao_historico.set_index("Ticker").to_excel(var_caminho + r"\Bases\Lista de ações Análise " + datetime.today().strftime("%Y-%m-%d") + '.xlsx')
    


    return bd_acao_historico



# gerar_arquivo_historico()
# detectar_martelos_todos_os_tickers()

# import pandas as pd
# bd_historico_completo = pd.read_excel(r"Bases\Base de Dados Histórico.xlsx")
# lista_acoes = ["AMBP3", "SBSP3", "ORVR3", "JBSS3", "TUPY3"]
# for acao in lista_acoes:
#     # print(bd_historico_completo[bd_historico_completo["Ticker"] == acao].head())
#     from realizar_analises import candle_plot
#     candle_plot( # Usa o navegador para criar o gráfico interativo
#         bd_historico_completo[bd_historico_completo["Ticker"] == acao].sort_values("Date").set_index("Date"),
#         volume = True,
#         mav = np.nan,
#         colors = ["orange", "yellow", "blue"],
#         titulo = acao,
#     )