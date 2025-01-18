def ler_lista_B3():
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime
    import pandas as pd

    url = "https://www.dadosdemercado.com.br/bolsa/acoes"
    response = requests.get(url)

    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # soup
    soup_tabela_acoes = soup.find('div', class_='table-container').find_all("tr")
    lista_acoes = []
    # data_de_hoje = "Volume em " + datetime.now().strftime("%d/%m/%Y")
    data_de_hoje = "Volume no último dia útil (lido em " + datetime.now().strftime("%d/%m/%Y") + ")"

    for soup_acao in soup_tabela_acoes:
    # print("")

        try:
            lista_acoes.append({
                "Nome da Empresa": soup_acao.find_all("td")[1].text.strip(),
                "Ticker": soup_acao.find("a").text.strip(),
                data_de_hoje: soup_acao.find_all("td")[2].text.strip()
            })
        except:
            pass

    bd_lista_acoes = pd.DataFrame(lista_acoes)
    # bd_lista_acoes[data_de_hoje] = bd_lista_acoes[data_de_hoje].str.replace(".", "", regex = True).astype(int)
    bd_lista_acoes[data_de_hoje] = bd_lista_acoes[data_de_hoje].str.replace(".", "").astype(int)
    bd_lista_acoes.to_excel('Bases/Lista de ações.xlsx')

    bd_lista_acoes = bd_lista_acoes.set_index("Ticker")
    return bd_lista_acoes



def tratar_lista_B3(bd_lista_acoes):
    var_corte_market_cap = 50000000
    var_corte_volume = 20000
    var_coluna_volume = [col for col in bd_lista_acoes.columns if "Volume" in col]


    # https://pypi.org/project/yfinance/
    # https://github.com/ranaroussi/yfinance/wiki/Ticker

    # !python -m pip install yfinance
    import yfinance as yf

    # !python -m pip install mplfinance
    # import mplfinance as mpf

    
    for ticker_acao in bd_lista_acoes.index:
        acao = yf.Ticker(ticker_acao + ".SA")
        try:
            bd_lista_acoes.loc[ticker_acao, "Market Cap"] = acao.info["marketCap"]
        except:
            pass


    bd_lista_acoes_tratada = bd_lista_acoes[
        (bd_lista_acoes["Market Cap"] >= var_corte_market_cap)
        * (bd_lista_acoes[var_coluna_volume].iloc[:, 0] >= var_corte_volume)
        # * (~bd_lista_acoes["Quote Type"].isna()) \
        ]


    bd_lista_acoes_tratada.to_excel('Bases/Lista de ações Tratada.xlsx')

    return bd_lista_acoes_tratada



tratar_lista_B3(ler_lista_B3())