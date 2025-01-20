# o_mais_novo_day_trader_do_brasil

# To-Do
- [] Replicar o que já existe no Jupyter Notebook (antes de 18/01/2025) para um conjunto de arquivos em Python que possa ser executado diariamente
    - ~~[X] Ler dados da B3 usando BeautifulSoup~~
    - ~~[X] Montar uma base completa com os dados de mercado de cada Ticker~~
    - ~~[X] Replicar análise de Martelo e cálculo das inclinações das curvas (Alfa)~~
    - [] Automatizar execução diária
- [] Execução demora muito, acho que não precisa atualizar a lista de ações toda vez, vou tirar isso para ver se dá para demorar menos
- [] Bug: está tentando ler ações da DASA11 e não acha. Essa ação deixou de existir? Por que não consegue ler? E ainda lê duas vezes...
- [] Ajustar alfas para 13 e 55 dias
- [] Adicionar coluna de %13d e %55d, que é o Preço/Alfa
- [] Ordenar por essa coluna de %média
- [] Ele falou que um bom momento é quando o preço está voltando para a média móvel, pois é sinal que voltará a subir
    - Exemplo é CEMIG (CMIG4)
- [] Revisar se meu cálculo de martelo está ok ou não.

## Concluído antes de 18/01/2025
- ~~[X] Adicionar uma visão só com o fechamento~~
- ~~[X] Comparar a inclinação da curva (alfa) de várias ações. Os que tem maiores alfas crescem mais~~
- ~~[X] Entender como o valor se comporta nos finais de semana e feriados (saltos) -> _coloquei uma opção na função de plot para ignorar finais de semana e feriados_~~
- ~~[X] Entender pq visualmente parece que a faixa de desvio padrão fica variando ao longo do período -> _não era só visual, a faixa estava mudando pq eu multiplicada a regressão pelo % de desvio/média. Mas é só eu somar o desvio padrão à regressão que ele fica estável ao longo da curca de regressão. Já ajustado na função que plota_~~
- [] ~~Quando troca a taxa de remuneração para (alfa/último preço), fica muito estranho, pois ações de baixo preço ficarão com uma taxa altíssima. É isso mesmo?~~