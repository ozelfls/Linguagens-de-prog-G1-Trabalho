# Consumo de Água no Brasil

Projeto de análise e visualização de uma **base simulada** com registros mensais de 2015 a 2024. O objetivo é explorar consumo, setores, desperdício, chuva e níveis de reservatórios sem atribuir os resultados à realidade hídrica brasileira.

## Executar

Requer Python 3.10 ou superior. No Windows, execute na pasta do projeto:

```bash
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m streamlit run app.py
```

Abra `notebooks/analise_consumo_agua.ipynb` com Jupyter para reproduzir a análise. O notebook usa a mesma base e as funções de `data.py`.

## Consultas implementadas

- Evolução mensal do consumo e média móvel de 12 meses.
- Ranking de consumo por estado, região e setor.
- Mapa de calor por ano e mês para observar sazonalidade.
- Relação entre chuva média e consumo mensal com correlação de Pearson.
- KPIs de consumo, perdas, consumo per capita e reservatórios.
- Ranking do percentual médio de desperdício por estado.
- Filtros por ano, mês, região, estado, setor e nível de alerta.

## Estrutura

`app.py` apresenta o dashboard, `data.py` carrega e prepara a base e `charts.py` reúne os gráficos. `dados/` contém o CSV original. `index.html` é a página de apresentação para GitHub Pages. `database/` e `imagens/` estão reservadas para extensões futuras.

## Método e limites

A carga converte datas e números, remove registros incompletos ou inválidos e elimina duplicatas exatas. Os totais representam **somente os registros do arquivo**. A cobertura é desigual entre UFs (20 estados ou DF aparecem), por isso a soma por estado não deve ser interpretada como estimativa de consumo estadual. `consumo_per_capita` é apresentado como média da coluna fornecida; ele não é recalculado a partir de `consumo_milhoes_litros` e `populacao`, pois a granularidade desses campos não foi documentada. A correlação não estabelece causalidade.

## Publicação

Publique o repositório no GitHub. Nas configurações do GitHub Pages, escolha a raiz do repositório para servir `index.html`. No Streamlit Community Cloud, selecione `app.py` como arquivo principal. Após publicar, substitua os links de demonstração da página pelos endereços gerados.
