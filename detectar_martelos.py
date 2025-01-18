# https://pypi.org/project/yfinance/
# https://github.com/ranaroussi/yfinance/wiki/Ticker

# !python -m pip install yfinance
import yfinance as yf

# !python -m pip install mplfinance
# import mplfinance as mpf

import numpy as np



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


    from sklearn.linear_model import LinearRegression
    import matplotlib.pyplot as plt
    from matplotlib import ticker
    import matplotlib.dates as mdates


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

    if print_variaveis == True:
        print("Média: " + "{:.4f}".format(media))
        print("Desvio padrão: " + "{:.4f}".format(desvio_padrao))
        print("Desvio padrão (%): " + "{:.4f}".format(margem))
        print("Inclinação da reta (alfa, coeficiente angular): " + "{:.4f}".format(alfa))
        print("Valor de fechamento (R$): " + "{:.2f}".format(valor_fechamento))


    if plot_grafico == True:
        plt.figure(figsize = tamanho_figsize)

        ax = plt.gca()

        if var_pular_final_de_semana_feriados == True:
            ax.xaxis.set_major_locator(ticker.LinearLocator(len(bd_acao_coluna)))
            # ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
            # ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt = "%d/%m/%y"))

            plt.xticks(rotation = rotacao)

            plt.scatter(x = bd_acao_coluna[bd_acao.index.name].dt.strftime("%d/%m/%y").astype(str), y = coluna, data = bd_acao_coluna, edgecolors='black', facecolors='none')

            plt.plot(bd_acao_coluna[bd_acao.index.name].dt.strftime("%d/%m/%y").astype(str), bd_acao_coluna["Regressão"]-desvio_padrao, color = "blue", linestyle='dashed')
            plt.plot(bd_acao_coluna[bd_acao.index.name].dt.strftime("%d/%m/%y").astype(str), bd_acao_coluna["Regressão"], color='green')
            plt.plot(bd_acao_coluna[bd_acao.index.name].dt.strftime("%d/%m/%y").astype(str), bd_acao_coluna["Regressão"]+desvio_padrao, color = "blue", linestyle='dashed')

            # ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt = "%d/%m/%y"))
            # ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

        else:
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

            plt.xticks(bd_acao_coluna[bd_acao.index.name], rotation = rotacao)

            plt.scatter(x = bd_acao_coluna[bd_acao.index.name], y = coluna, data = bd_acao_coluna, edgecolors='black', facecolors='none')

            plt.plot(bd_acao_coluna[bd_acao.index.name], bd_acao_coluna["Regressão"]-desvio_padrao, color = "blue", linestyle='dashed')
            plt.plot(bd_acao_coluna[bd_acao.index.name], bd_acao_coluna["Regressão"], color='green')
            plt.plot(bd_acao_coluna[bd_acao.index.name], bd_acao_coluna["Regressão"]+desvio_padrao, color = "blue", linestyle='dashed')


        plt.title(titulo)
        plt.show()

    return [bd_acao_coluna, media, desvio_padrao, modelo_linear, valor_fechamento]



def candle_plot( # Usa o navegador para criar o gráfico interativo
    dados,
    volume = True,
    mav = np.nan,
    colors = ["orange", "yellow", "blue"],
    titulo = "",
    ):
  
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    if volume == True:
        fig = make_subplots(
            rows = 2,
            cols = 1,
            shared_xaxes = True,
            vertical_spacing = 0.1,
            subplot_titles = ("Candlesticks", "Volume transacionado"),
            row_width = [0.2, 0.7]
        )
    else:
        fig = make_subplots(
            rows = 1,
            cols = 1,
            shared_xaxes = True,
            vertical_spacing = 0.1,
            subplot_titles = ("Candlesticks"),
            row_width = [0.2, 0.7]
        )

    fig.add_trace(go.Candlestick(x=dados.index,
                        open = dados['Open'],
                        high = dados['High'],
                        low = dados['Low'],
                        close = dados['Close']),
                    row = 1, col = 1)

    if mav is not np.nan:
        for i in range(len(mav)):
        # print(i)
            dados["Close "+ str(mav[i]) +" dias"] = dados["Close"].rolling(window=mav[i]).mean()
            fig.add_trace(go.Scatter(x=dados.index,
                            y = dados["Close "+ str(mav[i]) +" dias"],
                            mode = "lines",
                            name = "Média móvel fechamento " + str(mav[i]) + " dias",
                            marker=dict(color=colors[i])),
                        row = 1, col = 1)

    if volume == True:
        fig.add_trace(go.Bar(x=dados.head(60).index,
                            y = dados['Volume'],
                            name = "Volume"),
                    row = 2, col = 1)


    fig.update_layout(
        yaxis_title = "Preço",
        xaxis_rangeslider_visible=False,
        title=titulo,
        )

    fig.show()



def plota_candlestick_acha_martelos(
    acao,
    periodo = "21d",
    intervalo = "1d",
    taxa_máxima_para_ser_martelo = 0.2,
    display_candlestick = True,

  ):
    
    bd_acao = yf.Ticker(acao).history(
        period = periodo,
        interval = intervalo
    )
    bd_acao["Amplitude Open-Close"] = abs(bd_acao["Open"] - bd_acao["Close"])
    bd_acao["Amplitude High-Low"] = abs(bd_acao["High"] - bd_acao["Low"])

    # taxa_máxima_para_ser_martelo = 0.2
    bd_acao["Martelo?"] = (bd_acao["Amplitude Open-Close"] < taxa_máxima_para_ser_martelo * bd_acao["Amplitude High-Low"])

    lista_datas_martelo = bd_acao[bd_acao["Martelo?"] == True].sort_index(ascending = False).index.to_pydatetime()
    string_datas_martelo = ""
    for data in lista_datas_martelo:
        string_datas_martelo = data.strftime("%d/%m/%y") + ", " + string_datas_martelo


    if display_candlestick == True:
        candle_plot(
            bd_acao,
            volume = True,
            # mav = np.nan,
            # colors = ["orange", "yellow", "blue"],
            titulo = acao,
        )

    return [bd_acao, string_datas_martelo]



# [bd_acao, string_datas_martelo] = plota_candlestick_acha_martelos(
#     acao =  "PETR3" + ".SA",
#     periodo = "60d",
#     intervalo = "1d",
#     taxa_máxima_para_ser_martelo = 0.2,
#     display_candlestick = True,
# )
# print(string_datas_martelo)
# # print(bd_acao)



def detectar_martelos_todos_os_tickers():
    import pandas as pd
    from datetime import datetime, timedelta


    bd_lista_acoes_analise = pd.read_excel("Bases/Lista de ações Tratada.xlsx", index_col = "Ticker")

    coluna_analise = "HLC"

    qtd_dias_maximo = int(np.round(55/7*5))
    qtd_dias_minimo = int(np.round(21/7*5))
    for acao in bd_lista_acoes_analise.index:#[[0]]:
        # print(acao)

        bd_acao = yf.Ticker(acao + ".SA").history(
            start = datetime.today() - timedelta(days=qtd_dias_maximo),
            end = datetime.today(),
            interval = "1d"
        )
        bd_acao.index = bd_acao.index.tz_localize(None)
        bd_acao[coluna_analise] = (bd_acao["High"] + bd_acao["Low"] + bd_acao["Close"])/3

        bd_acao_minimo = bd_acao.iloc[-(qtd_dias_minimo):].copy()

        [_, _, _, modelo_linear, _] = criar_regressao_bd_acao(
            bd_acao_minimo,
            coluna = coluna_analise,
            print_variaveis = False,
            plot_grafico = False,
            # titulo = acao + " (fechamento dos últimos " + str(qtd_dias_minimo) + " dias)",
            # tamanho_figsize = (15, 6),
            # rotacao = 60,
        )

        bd_lista_acoes_analise.loc[acao, "Alfa (" + str(qtd_dias_minimo) +" dias)"] = modelo_linear.coef_[0][0]
        bd_lista_acoes_analise.loc[acao, "Preço Close há " + str(qtd_dias_minimo) +" dias"] = bd_acao_minimo.iloc[0]["Close"]
        # bd_lista_acoes_analise["Taxa média de Remuneração (R$)"] = bd_lista_acoes_analise["Preço fechamento (R$)"]*bd_lista_acoes_analise["Alfa"]
        # bd_lista_acoes_analise["Taxa média de Remuneração (pp/R$, " + str(qtd_dias_minimo) +" dias)"] = \
        # bd_lista_acoes_analise["Alfa (" + str(qtd_dias_minimo) +" dias)"]/bd_lista_acoes_analise["Preço fechamento (R$, " + str(qtd_dias_minimo) +" dias)"]
        bd_lista_acoes_analise.loc[acao, "Preço HLC em "+ datetime.now().strftime("%d/%m/%Y")] = \
        (bd_acao_minimo.iloc[len(bd_acao_minimo)-1].loc["High"]+bd_acao_minimo.iloc[len(bd_acao_minimo)-1].loc["Low"]+bd_acao_minimo.iloc[len(bd_acao_minimo)-1].loc["Close"])/3
        bd_lista_acoes_analise.loc[acao, "Preço HLC há "+ str(qtd_dias_minimo) +" dias"] = \
        (bd_acao_minimo.iloc[0].loc["High"]+bd_acao_minimo.iloc[0].loc["Low"]+bd_acao_minimo.iloc[0].loc["Close"])/3


        [_, _, _, modelo_linear, _] = criar_regressao_bd_acao(
            bd_acao,
            coluna = coluna_analise,
            print_variaveis = False,
            plot_grafico = False,
            # titulo = acao + " (fechamento dos últimos " + str(qtd_dias_maximo) + " dias)",
            # tamanho_figsize = (15, 6),
            # rotacao = 60,
        )

        bd_lista_acoes_analise.loc[acao, "Alfa (" + str(qtd_dias_maximo) +" dias)"] = modelo_linear.coef_[0][0]
        bd_lista_acoes_analise.loc[acao, "Preço Close há " + str(qtd_dias_maximo) +" dias"] = bd_acao.iloc[0]["Close"]
        # bd_lista_acoes_analise["Taxa média de Remuneração (R$)"] = bd_lista_acoes_analise["Preço fechamento (R$)"]*bd_lista_acoes_analise["Alfa"]
        # bd_lista_acoes_analise["Taxa média de Remuneração (pp/R$, " + str(qtd_dias_maximo) +" dias)"] = \
        # bd_lista_acoes_analise["Alfa (" + str(qtd_dias_maximo) +" dias)"]/bd_lista_acoes_analise["Preço fechamento (R$, " + str(qtd_dias_maximo) +" dias)"]
        bd_lista_acoes_analise.loc[acao, "Preço HLC há "+ str(qtd_dias_maximo) +" dias"] = \
        (bd_acao.iloc[0].loc["High"]+bd_acao.iloc[0].loc["Low"]+bd_acao.iloc[0].loc["Close"])/3
        # bd_lista_acoes_analise


        [_, string_datas_martelo] = plota_candlestick_acha_martelos(
            acao =  acao + ".SA",
            periodo = str(qtd_dias_maximo)+"d",
            intervalo = "1d",
            taxa_máxima_para_ser_martelo = 0.2,
            display_candlestick = False,
        )
        # display(string_datas_martelo)
        bd_lista_acoes_analise.loc[acao, "Datas dos martelos"] = string_datas_martelo[:-2]


    bd_lista_acoes_analise.to_excel('Bases/Lista de ações Análise ' + datetime.today().strftime("%Y-%m-%d") + '.xlsx')

    return bd_lista_acoes_analise

detectar_martelos_todos_os_tickers()