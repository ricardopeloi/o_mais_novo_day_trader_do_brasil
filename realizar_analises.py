import os
from os import listdir
from datetime import datetime, timedelta
import pandas as pd
from IPython.display import display

from pathlib import Path  # Python 3.6+ only
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
var_caminho = os.environ.get('var_caminho_fonte')


def get_lista_arquivos_analise():
    lista_arquivos = listdir("Bases")
    # print(lista_arquivos)
    
    lista_arquivos_analises = []
    for arquivo in lista_arquivos:
        if arquivo.find(" Análise") > 0:
            lista_arquivos_analises.append(datetime.strptime(arquivo.split(" Análise ")[1].split(".xls")[0], "%Y-%m-%d"))
    
    return lista_arquivos_analises
# print(get_lista_arquivos_analise())



def gerar_base_top_analises(
    var_qtd_top_acoes = 5,
    qtd_dias = 55
):
    lista_arquivos_analises = get_lista_arquivos_analise()
    # print(lista_arquivos_analises)

    bd_analises_top_acoes = pd.DataFrame()

    # for data_arquivo in lista_arquivos_analises[:2]:
    for data_arquivo in lista_arquivos_analises:
        print("Lendo arquivo de " + data_arquivo.strftime("%Y-%m-%d"))
        var_arquivo = var_caminho + r"\Bases\Lista de ações Análise " + data_arquivo.strftime("%Y-%m-%d") + ".xlsx"
        bd_lista_acoes_analise = pd.read_excel(var_arquivo, index_col = "Ticker")
        
        # display(bd_lista_acoes_analise.reset_index().reset_index())
        # display(bd_lista_acoes_analise)
        # display(bd_lista_acoes_analise.columns)

        try:
            try:
                bd_lista_analise = bd_lista_acoes_analise.sort_values("Alfa (" + str(round(qtd_dias/7*5)) + " dias)", ascending = False).head(var_qtd_top_acoes).reset_index().reset_index()
                bd_lista_analise["Data análise"] = data_arquivo
                bd_lista_analise = bd_lista_analise.drop(['Market Cap'], axis = 1)
                bd_lista_analise.columns = ['index', 'Ticker', 'Nome da Empresa',
                    'Volume no último dia útil',
                    'Alfa (15 dias)', 'Preço Close há 15 dias', 'Preço HLC',
                    'Preço HLC há 15 dias', 'Alfa (39 dias)', 'Preço Close há 39 dias',
                    'Preço HLC há 39 dias', 'Datas dos martelos', 'Data análise']

            except:
                try:
                    bd_lista_analise = bd_lista_acoes_analise.sort_values("Alfa (" + str(qtd_dias) + " períodos)", ascending = False).head(var_qtd_top_acoes).reset_index().reset_index()
                    bd_lista_analise = bd_lista_analise.drop(['Market Cap', 'Alfa/Preço HLC (55 períodos)', 'Alfa/Preço HLC (13 períodos)'], axis = 1)
                    bd_lista_analise.columns = ['index', 'Ticker', 
                        'Nome da Empresa', 'Volume no último dia útil', 'Data análise', 
                        'Preço HLC', 
                        'Alfa (39 dias)', 'Preço Close há 39 dias', 'Preço HLC há 39 dias',
                        'Alfa (15 dias)', 'Preço Close há 15 dias', 'Preço HLC há 15 dias',
                        'Datas dos martelos']
                    bd_lista_analise['Data análise'] = pd.to_datetime(bd_lista_analise['Data análise'], format = "%d/%m/%Y")
                except:
                    bd_lista_analise = bd_lista_acoes_analise.sort_values("Alfa HLC; últimos " + str(qtd_dias) + " dias", ascending = False).head(var_qtd_top_acoes).reset_index().reset_index()
                    # bd_lista_analise = bd_lista_analise.drop(['Market Cap'], axis = 1)

                    try:
                        bd_lista_analise = bd_lista_analise[[
                            'index', 'Ticker', 
                            'Nome da Empresa', 'Volume no último dia útil (lido em ' + data_arquivo.strftime("%d/%m/%Y") + ')',
                            data_arquivo.strftime("%Y-%m-%d") + '; HLC',
                            'Alfa HLC; últimos 55 dias', (data_arquivo-timedelta(days=50)).strftime("%Y-%m-%d") + '; Close', (data_arquivo-timedelta(days=50)).strftime("%Y-%m-%d") + '; HLC',
                            'Alfa HLC; últimos 13 dias', (data_arquivo-timedelta(days=13)).strftime("%Y-%m-%d") + '; Close', (data_arquivo-timedelta(days=13)).strftime("%Y-%m-%d") + '; HLC',
                            'Martelos'
                        ]]
                    except:
                        try:
                            bd_lista_analise = bd_lista_analise[[
                                'index', 'Ticker', 
                                'Nome da Empresa', 'Volume no último dia útil (lido em ' + data_arquivo.strftime("%d/%m/%Y") + ')',
                                (data_arquivo-timedelta(days=1)).strftime("%Y-%m-%d") + '; HLC',
                                'Alfa HLC; últimos 55 dias', (data_arquivo-timedelta(days=50)).strftime("%Y-%m-%d") + '; Close', (data_arquivo-timedelta(days=50)).strftime("%Y-%m-%d") + '; HLC',
                                'Alfa HLC; últimos 13 dias', (data_arquivo-timedelta(days=15)).strftime("%Y-%m-%d") + '; Close', (data_arquivo-timedelta(days=15)).strftime("%Y-%m-%d") + '; HLC',
                                'Martelos'
                            ]]
                        except:
                            bd_lista_analise = bd_lista_analise[[
                                'index', 'Ticker', 
                                'Nome da Empresa', 'Volume no último dia útil (lido em ' + data_arquivo.strftime("%d/%m/%Y") + ')',
                                (data_arquivo-timedelta(days=2)).strftime("%Y-%m-%d") + '; HLC',
                                'Alfa HLC; últimos 55 dias', (data_arquivo-timedelta(days=50)).strftime("%Y-%m-%d") + '; Close', (data_arquivo-timedelta(days=50)).strftime("%Y-%m-%d") + '; HLC',
                                'Alfa HLC; últimos 13 dias', (data_arquivo-timedelta(days=15)).strftime("%Y-%m-%d") + '; Close', (data_arquivo-timedelta(days=15)).strftime("%Y-%m-%d") + '; HLC',
                                'Martelos'
                            ]]
                    bd_lista_analise["Data análise"] = data_arquivo
                    bd_lista_analise.columns = ['index', 'Ticker', 'Nome da Empresa',
                        'Volume no último dia útil', 
                        'Preço HLC', 
                        'Alfa (39 dias)', 'Preço Close há 39 dias', 'Preço HLC há 39 dias',
                        'Alfa (15 dias)', 'Preço Close há 15 dias', 'Preço HLC há 15 dias',
                        'Datas dos martelos', 'Data análise']
            # print("ok")
            bd_analises_top_acoes = pd.concat([bd_analises_top_acoes, bd_lista_analise])
            print(len(bd_analises_top_acoes))
        
        except:
            pass

    # for acao in bd_lista_acoes_analise.sort_values("Alfa (39 dias)", ascending = False).head(var_qtd_top_acoes).index:
        # display(bd_lista_acoes_analise.loc[acao])
    
        
        
    bd_analises_top_acoes = bd_analises_top_acoes.drop("index", axis = 1).reset_index()
    
    # print(var_caminho + r'\Recomendações\Top ' + var_qtd_top_acoes + '' todas as análises.xlsx')
    bd_analises_top_acoes.to_excel(var_caminho + r'\Recomendações\Top ' + str(var_qtd_top_acoes) + ' todas as análises.xlsx', index = False)
    
    return bd_analises_top_acoes

# display(gerar_base_top_analises().columns)
# display(gerar_base_top_analises())

# var_arquivo = var_caminho + r"\Bases\Lista de ações Análise 2024-06-15.xlsx"
# var_arquivo = var_caminho + r"\Bases\Lista de ações Análise 2025-03-15.xlsx"
# var_arquivo = var_caminho + r"\Bases\Lista de ações Análise 2025-03-16.xlsx"
# bd_lista_acoes_analise = pd.read_excel(var_arquivo, index_col = "Ticker")
# print(bd_lista_acoes_analise.columns)



def gerar_top_recomendacoes(
        var_qtd_top_acoes = 5,
        qtd_dias = 55
    ):

    from detectar_martelos import criar_regressao_bd_acao
    
    # var_qtd_top_acoes = 5

    lista_arquivos_analises = get_lista_arquivos_analise()
    
    var_arquivo_mais_recente = var_caminho + r"\Bases\Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx"
    # var_arquivo_mais_recente = r"\Bases\Lista de ações Análise " + max(lista_arquivos_analises).strftime("%Y-%m-%d") + ".xlsx"
    # print(var_arquivo_mais_recente)

    
    bd_lista_acoes_analise = pd.read_excel(var_arquivo_mais_recente, index_col = "Ticker")
    #f
    
    # print(bd_lista_acoes_analise.sort_values("Alfa HLC; últimos 55 dias", ascending = False).head(5))
    # print()

    bd_historico_completo = pd.read_excel(r"Bases\Base de Dados Histórico.xlsx")
    #f


    
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

# gerar_top_recomendacoes(
#         # var_qtd_top_acoes = 5,
#         # qtd_dias = 55
#     )