# Metodologia de construção dos indicadores – mid_sized_cities_indicators_2022

**Autor:** Pedro Igor Galvão Gomes  
**Instituição:** Universidade Federal do Tocantins (UFT)  
**Ano:** 2025  
**Licença:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  

---

## 🧭 Descrição geral

Este documento descreve as **variáveis e indicadores** que compõem a base de dados `mid_sized_cities_indicators_2022.gpkg`, elaborada no âmbito da dissertação *“Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras”* (GOMES, 2025).  

Os indicadores foram calculados a partir das variáveis originais dos **Censos Demográficos 2010 e 2022 (IBGE)**, integrando informações de raça/cor, renda e infraestrutura domiciliar por **setor censitário urbano**.  
Os dados foram harmonizados entre os dois períodos para possibilitar comparações consistentes e análises espaciais de desigualdade intraurbana.

---

## 📂 Fontes de dados originais

| Fonte | Descrição | Ano | Origem |
|--------|------------|------|--------|
| IBGE – Censo Demográfico | Microdados setoriais de população, domicílios e renda | 2010 e 2022 | [https://www.ibge.gov.br](https://www.ibge.gov.br) |
| Malhas setoriais | Shapefiles dos setores censitários (urbanos e rurais) | 2010 e 2022 | IBGE – Diretoria de Geociências |
| Processamento adicional | Harmonização espacial e cálculo de indicadores | 2024–2025 | Elaborado pelo autor |

---

## 🧮 Variáveis de origem (Quadro 1 – IBGE adaptado)

| ID | Tabela IBGE | Variável | Código original |
|----|--------------|-----------|----------------|
| 1 | Cor ou Raça, idade e gênero | Pessoas residentes | V0001 |
| 2 | Cor ou Raça, idade e gênero | Pessoas residentes por raça/cor (branca, preta, amarela, parda, indígena) | V01317–V01321 |
| 3 | Domicílio, moradores 2 | Domicílios com rede geral de água | V00111 |
| 4 | Domicílio, moradores 2 | Domicílios com esgoto via rede geral ou pluvial | V00309 |
| 5 | Domicílio, moradores 2 | Domicílios com coleta de lixo por serviço público | V00397 |
| 6 | Domicílio, moradores 2 | Total de domicílios particulares ocupados | V0007 |
| 7 | Domicílio Renda | Rendimento nominal mensal dos domicílios permanentes | V003 |
| 8 | Domicílio Renda | Rendimento nominal mensal dos domicílios improvisados | V004 |

---

## 📊 Indicadores derivados (Quadro 2 – Fórmulas)

| Indicador | Descrição | Sigla | Fórmula |
|------------|------------|--------|----------|
| População residente (pessoas) | Total de pessoas no setor | PR | V0001 |
| População branca (%) | Pessoas autodeclaradas brancas em relação à população total | PB | (V01317×100)/PR |
| População preta (%) | Pessoas autodeclaradas pretas | PP | (V01318×100)/PR |
| População amarela (%) | Pessoas autodeclaradas amarelas | PA | (V01319×100)/PR |
| População parda (%) | Pessoas autodeclaradas pardas | PD | (V01320×100)/PR |
| População indígena (%) | Pessoas autodeclaradas indígenas | PI | (V01321×100)/PR |
| Domicílios totais | Total de domicílios particulares ocupados | TD | V0007 |
| Acesso à rede de água (%) | Domicílios com rede geral de distribuição de água | MA | (V00111×100)/TD |
| Acesso ao esgoto (%) | Domicílios com esgoto via rede geral ou pluvial | ME | (V00309×100)/TD |
| Coleta de lixo (%) | Domicílios com coleta por serviço público | ML | (V00397×100)/TD |
| **Renda média domiciliar per capita (R$/hab)** | Rendimento total dos domicílios dividido pela população residente | **RpC** | **(V003+V004)/PR** |

> As variáveis de infraestrutura (MA, ME, ML) foram normalizadas por domicílios (`TD`), enquanto a renda (`RpC`) foi normalizada pela população residente (`PR`).

---

## 🧩 Harmonização entre os Censos 2010 e 2022

A variável de **renda média domiciliar per capita (`RpC`)** está disponível apenas para o **Censo 2010**.  
Para compatibilizá-la com a malha setorial de 2022, aplicou-se uma **ponderação espacial por área de sobreposição**, conforme descrito abaixo:

1. Reprojeção das malhas 2010 e 2022 para **Brazil Albers Equal Area (SIRGAS 2000)**;  
2. Cálculo da área de cada setor de 2010 (`area_2010`);  
3. Interseção espacial entre os setores 2010 e 2022;  
4. Cálculo da proporção de interseção (`prop = area_intersec / area_2010`);  
5. Ponderação da renda média de 2010:  RpC_weighted = prop × RpC
6. Agregação dos valores ponderados por setor de 2022 (`id_setor`);  
7. Junção dos resultados à base de 2022 e renomeação da variável final para **`RpC_2010`**, indicando sua origem temporal.  

> Este procedimento mantém a coerência espacial dos valores e possibilita comparações intertemporais sem distorções de fronteiras censitárias.

---

## ⚙️ Campos do dataset

| Campo | Descrição | Tipo | Unidade |
|--------|------------|------|---------|
| CD_SETOR | Código do setor censitário | texto | — |
| NM_MUN | Nome do município | texto | — |
| NM_UF | Unidade Federativa | texto | — |
| PR | População residente total | numérico | pessoas |
| PB, PP, PA, PD, PI | População por raça/cor (%) | numérico | % |
| TD | Total de domicílios particulares ocupados | numérico | unidades |
| MA, ME, ML | Indicadores de infraestrutura (água, esgoto, lixo) | numérico | % |
| RpC_2010 | Renda média domiciliar per capita (ajustada e harmonizada) | numérico | R$/habitante |
| geometry | Polígono do setor censitário | geométrico | — |

---

## 📎 Observações

- O CRS utilizado é **SIRGAS 2000 / UTM 22S** (`EPSG:31982`).  
- Todos os cálculos foram realizados em **Python 3.11**, utilizando **GeoPandas**, **Shapely**, **NetworkX** e **Pandas**.  
- O arquivo resultante `mid_sized_cities_indicators_2022.gpkg` contém os setores urbanos das 92 cidades médias brasileiras (definidas no recorte espacial da pesquisa).  

---

**Citação sugerida:**
> GOMES, Pedro Igor Galvão. *Metodologia de construção dos indicadores – Base de Dados mid_sized_cities_indicators_2022.* Palmas: Universidade Federal do Tocantins, 2025.  