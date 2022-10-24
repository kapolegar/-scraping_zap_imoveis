# **Scraping Zap Imoveis**


O objetivo geral desse projeto foi avaliar o preço médio de aluguel + condomínio dos apartamentos na cidade de Porto Alegre por zona e bairro para guiar futuras escolhas de local de moradia focando a escolha dentro das possibilidades de um orçamento pessoal. Para isso, foi realizado um web scraping do site Zap Imóveis, ETL, análise de dados, dashboard e deploy da dashboard para acesso geral.

Previamente ao scraping, foi realizada uma busca direto no site Zap Imóveis conforme abaixo:

**Filtros realizados direto no link:**

  - **Tipo de transação:** Aluguel
  
  - **Número de quartos:** 2 a 3
  
  - **Cidade:** Porto Alegre / Rio Grande do Sul
  
  **O conjunto de dados para este projeto é originário do link:**

https://www.zapimoveis.com.br/aluguel/apartamentos/rs+porto-alegre/?onde=,Rio%20Grande%20do%20Sul,Porto%20Alegre,,,,,city,BR%3ERio%20Grande%20do%20Sul%3ENULL%3EPorto%20Alegre,-30.036818,-51.208989,&transacao=Aluguel&tipo=Im%C3%B3vel%20usado&tipoUnidade=Residencial,Apartamento&quartos=2,3&pagina=1

## **Arquivos do Projeto:**

### **- rastreador(scraping)** 

Refere-se ao scraping no site Zap Imóveis. 
O processo desenvolvido também reconhece o número de páginas de anúncios e endereços e bairros não identificados e com erros de digitação, assim como faz a distribuição entre as Zonas da Cidade através de uma lista de bairros por zona pré-definida. Em seguida, é realizado o tratamento para identificação e remoção de itens únicos, alugueis zerados e outliers na coluna "Aluguel". Ainda no arquivo **rastreador(scraping)**, há uma breve análise e visualização dos dados através de gráficos com seaborn. Ao final, é gerado o arquivo **dataset.csv** que será utilizado posteriormente na Dashboard. 

### - **dataset.csv**

Base de dados no formato .csv gerada após tratamento referente ao scraping do site Zap Imóveis.
Este arquivo contém xxx registros (linhas) de imóveis e xxx colunas.

### - **dashboard** 

Refere-se à dashboard para análise dos valores médios de aluguel e condomínio.
Para confecção, foi utilizada uma combinação das bibliotecas **dash** para a estrutura em html e conexão dos filtros com os dados e **plotly.express** para as visualizações através de gráficos.
Os três primeiros gráficos gerados na Dashboard são estáticos e se referem ao conjunto completo de dados, segundo os critérios em cada títulos. A seguir, é apresentada uma lista de filtros dinâmicos entre si que modificam o resultado do gráfico principal intitulado "Valor Médio de Aluguel e Condomínio". 
Obs.: Ao selecionar um ou mais bairros na lista Bairro(s), o gráfico é modificado para informar o valor médio por Rua dentro do(s) bairro(s) selecionado(s).
Ao fim, a dashboard apresenta uma tabela dinâmica contendo todos os apartamentos encontrados a partir dos filtros selecionados. Os dados destes são os mesmos compilados no gráfico mencionado anteriormente.

## **Deploy da Dashboard**

Para que fosse possível o acesso fora da máquina local, foi realizado o Deploy da dashboard desenvolvida através da ferramenta Heroku.
A mesma pode ser acessada em seu computador através do link: https://rastreador-apartamento.herokuapp.com/
