# To-Do
## 1. Coleta de dados



## 2. Modelagem dos indicadores/variáveis
- [] Testar se é realmente interessante utilizar colunas como dividendos e tamanho de mercado no modelo
- [] Criar indicadores relacionados aos martelos, como a quantidade, se é subida/descida, há quantos dias foi o último



## 3. Análises
- []  Análise boa e simples:
    - Alfa mostra tendência
    - Desvio padrão é o canal
    - Se o valor está abaixo da média da tendência, compra
    - Se o valor está acima da tendência, vende (ou não compra)
- [] Priorizar ações top 10 usando alfa 55 dias e refinando top 5 com alfa 34 dias.
    - 12/05/2025: em construção no arquivo de análise _Rascunhão_
- [] Um bom momento é quando o preço está voltando para a média móvel, pois é sinal que voltará a subir
    - Exemplo é CEMIG (CMIG4)
- [] Fazer um modelo regressor para tentar prever o valor
- [] Melhorar variáveis usadas, pois acredito que algumas variáveis ainda estão muito recentes e influenciam no output do modelo
- [] Melhorar balanceamento e também a escala dos números das colunas



# Concluído até...
## Concluído até 01/05/2025
- [X] Deixar sistema mais discreto (env)
- [X] Adicionar forma de instalar pacotes sem precisar fazê-lo manualmente cada vez ([exemplo](https://stackoverflow.com/questions/46419607/how-to-automatically-install-required-packages-from-a-python-script-as-necessary))
    - A solução era usar um arquivo de requirements
- ~~[] Adicionar coluna de %13d e %55d, que é o Preço/Alfa~~
    - Retirei isso da To-Do List pq vi que é melhor ter a base de dados completa e ir desdobrando daí as análises com as funções que eu criei



## Concluído até 27/04/2025
- [X] Criar sistema de atualização dos dados com base na data da última atualização, e assim dá pra parar de ficar criando arquivos novos



## Concluído até 19/04/2025
- [X] Na Análise Exploratória, remover as colunas que sejam do tipo string
- [X] Fazer um modelo classificador para prever subida ou descida da ação
    - Criado o modelo de classificação com estimadores _Decision Tree Classifier_, _Dummy_ e _Random Forest Classifier_, chegando a um baseline de 76% de acerto sobre o resultado de crescimento ou não das ações com dados de no máximo 13 dias atrás



## Concluído até 30/03/2025
- [X] Automatizar execução diária



## Concluído até 16/03/2025
- [X] Fazer a base empilhada simples original
- [X] Adicionar os indicadores que já estão presentes (além de Market Cap)



## Concluído até 15/03/2025
- [X] Ajustar alfas para 13 e 55 dias
- [X] Revisar se meu cálculo de martelo está ok ou não
    - ok e adicionei o tipo de martelo
- [X] Bug: está tentando ler ações da DASA11 e não acha. Essa ação deixou de existir? Por que não consegue ler? E ainda lê duas vezes...
    - havia uma leitura duplicada mesmo
- [X] Execução demora muito, acho que não precisa atualizar a lista de ações toda vez, vou tirar isso para ver se dá para demorar menos
    - 15/03: O que demora mais é que as ações precisam ser lidas uma a uma, mas eu já reduzi algumas leituras duplicadas da mesma ação
- [X] Ordenar por essa coluna de maiores alfas (variações positivas no valor HLC da ação)



## Concluído antes de 18/01/2025
- [X] Adicionar uma visão só com o fechamento
- [X] Comparar a inclinação da curva (alfa) de várias ações. Os que tem maiores alfas crescem mais
- [X] Entender como o valor se comporta nos finais de semana e feriados (saltos) -> _coloquei uma opção na função de plot para ignorar finais de semana e feriados_
- [X] Entender pq visualmente parece que a faixa de desvio padrão fica variando ao longo do período -> _não era só visual, a faixa estava mudando pq eu multiplicada a regressão pelo % de desvio/média. Mas é só eu somar o desvio padrão à regressão que ele fica estável ao longo da curca de regressão. Já ajustado na função que plota_
- [] ~~Quando troca a taxa de remuneração para (alfa/último preço), fica muito estranho, pois ações de baixo preço ficarão com uma taxa altíssima. É isso mesmo?~~
- [X] Replicar o que já existe no Jupyter Notebook (antes de 18/01/2025) para um conjunto de arquivos em Python que possa ser executado diariamente
    - [X] Ler dados da B3 usando BeautifulSoup
    - [X] Montar uma base completa com os dados de mercado de cada Ticker
    - [X] Replicar análise de Martelo e cálculo das inclinações das curvas (Alfa)