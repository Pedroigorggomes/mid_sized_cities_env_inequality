# 🌎 Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras

DOI: 10.5281/zenodo.17518966

“Base de dados e scripts da dissertação ‘Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras’ (GOMES, 2025).”

**Autor:** Pedro Igor Galvão Gomes  
**Instituição:** Universidade Federal do Tocantins (UFT)  
**Ano:** 2025  
**Licença:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  

---

## 🧭 Descrição geral

Este repositório apresenta os **scripts, dados e metodologias** utilizados na dissertação *“Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras”* (GOMES, 2025).

A estrutura organiza-se em três grandes blocos:

1. **Construção da base de dados** (pipeline 01);
2. **Análise estatística e visualização de desigualdades** (pipeline 02);
3. **Mapeamento interurbano e representação cartográfica** (pipeline 03).

O repositório disponibiliza a base final consolidada (`mid_sized_cities_inequality_data_2022.gpkg`), documentação metodológica e scripts em **Python**, permitindo a reprodução completa das etapas de análise.

---

## 🗂️ Estrutura do repositório

```bash
mid_sized_cities_env_inequality/
├── data/
│   ├── data_dictionary.txt
│   ├── data_dictionary_EN.txt
│   ├── mid_sized_cities_inequality_data_2022.csv
│   └── mid_sized_cities_inequality_data_2022.gpkg
│
├── docs/
│   ├── README_01_variables.md
│   ├── README_02_cities.md
│   ├── README_03_analysis_methodology.md
│   └── README_04_Mapping.md
│
├── pipelines/
│   ├── 01_build_base/
│   │   ├── 01_build_indicators_from_excels.py
│   │   ├── 02_harmonize_renda_2010_to_2022.py
│   │   └── 03_select_mid_sized_cities_idsafe.py
│   │
│   ├── 02_analysis/
│   │   ├── 04_plot_correlation_national.py
│   │   ├── 05_plot_correlation_by_region.py
│   │   ├── 06_plot_access_infrastructure_quintile.py
│   │   ├── 07_plot_discrepancy_by_region.py
│   │   └── 08_plot_participation_by_region.py
│   │
│   └── 03_mapping/
│       ├── 09_select_quintiles_q1_q5.py
│       └── 10_plot_income_maps_grouped_by_region.py
│
├── requirements.txt
├── LICENSE.txt
└── README.md
```

---

## ⚙️ Orientações de uso

Os scripts foram desenvolvidos em **Python 3.14**, utilizando as bibliotecas `GeoPandas`, `Pandas`, `Matplotlib`, `NumPy`, `NetworkX` e `Shapely`.

1. **Ajuste dos caminhos** – todos os scripts utilizam caminhos locais (`G:/...`). Antes de executar, substitua pelos diretórios do seu sistema operacional.
2. **Formato do arquivo** – o arquivo principal está em formato `.gpkg`. Caso prefira, converta para `.shp` (shapefile) para uso direto em SIGs ou scripts.
3. **Dependências** – instale via `pip install -r requirements.txt`.
4. **Execução sequencial** – siga a ordem dos pipelines (`01_build_base → 02_analysis → 03_mapping`).

> 💡 **Dica:** os shapefiles auxiliares (massas d’água, oceanos, malhas do IBGE) **não estão incluídos**, mas suas fontes e códigos são indicados nos README internos de cada etapa.

---

## 🧱 Organização dos scripts e funções principais

### 🧩 1. Construção da base (`01_build_base/`)

Esta etapa gera a base integrada de indicadores socioeconômicos, raciais e de infraestrutura por setor censitário.

1. `01_build_indicators_from_excels.py` – consolida variáveis do Censo (raça, domícilios, infraestrutura).
2. `02_harmonize_renda_2010_to_2022.py` – ajusta a renda per capita de 2010 para a malha de 2022 por interseção espacial ponderada.
3. `03_select_mid_sized_cities_idsafe.py` – seleciona os setores das **92 cidades médias** (100–500 mil hab.).

🗺️ O produto final é o arquivo `mid_sized_cities_inequality_data_2022.gpkg`, que serve como entrada para todas as demais análises.

---

### 📊 2. Análise de desigualdades (`02_analysis/`)

Os scripts desta etapa produzem gráficos e indicadores de desigualdade racial, renda e acesso à infraestrutura.

#### 2.1 Correlação entre renda e composição racial

O script `04_plot_correlation_national.py` gera os gráficos de dispersão entre `RpC_2010` e as proporções raciais (%), aplicando o coeficiente de **Pearson (r)** para o conjunto das 92 cidades.

<img width="967" height="602" alt="image" src="https://github.com/user-attachments/assets/1eff1b00-aa3c-4912-8a75-815192faf989" />

> **Fonte:** Autor (2025).
> **Interpretação:** observa-se correlação positiva entre renda e população branca (r = 0,46) e correlações negativas entre renda e populações preta (r = -0,32) e parda (r = -0,44).

---

#### 2.2 Estratificação por quintis de renda

O script `06_plot_access_infrastructure_quintile.py` estratifica os setores por **quintis de renda** (Q1 = 20% mais pobres; Q5 = 20% mais ricos) e calcula indicadores por grupo racial e infraestrutura.

<img width="664" height="554" alt="image" src="https://github.com/user-attachments/assets/525bc892-6608-470a-a20d-8940289e6033" />

> **Fonte:** Autor (2025).
> A estratificação permite comparar perfis sociais e raciais entre faixas de renda, revelando padrões de segregação intraurbana.

<img width="653" height="779" alt="image" src="https://github.com/user-attachments/assets/efde2566-9435-49ea-b1f5-48221edb66fd" />

> **Fonte:** Autor (2025).


---

#### 2.3 Distribuição racial e acesso à infraestrutura

O mesmo script gera gráficos agregados por região, mostrando a variação da composição racial e do acesso à infraestrutura.

<img width="636" height="683" alt="image" src="https://github.com/user-attachments/assets/201e2c51-adc2-4199-a58f-a759ad71fc17" />


<img width="562" height="600" alt="image" src="https://github.com/user-attachments/assets/69a33ba5-8944-4b4d-84de-de1492730233" />

> **Fonte:** Autor (2025).
> A figura ilustra a leitura da **linha de equidade** — representação teórica de igualdade na distribuição racial por renda.
> **Resultado:** observa-se que os quintis superiores concentram as populações brancas e o maior acesso a serviços urbanos.

---

#### 2.4 Discrepância populacional e linha de equidade

O script `07_plot_discrepancy_by_region.py` calcula a diferença entre a população **observada** e a **esperada** por quintil, segundo a linha de equidade.

<img width="651" height="566" alt="image" src="https://github.com/user-attachments/assets/88e76c79-8f85-45ee-8d56-423c5d9ea92e" />


<img width="725" height="440" alt="image" src="https://github.com/user-attachments/assets/e4e0ddc3-3eae-4d30-bdad-8cfd570e76f1" />

> **Fonte:** Autor (2025).
> **Interpretação:** nas regiões Norte e Nordeste, observa-se sub-representação de brancos nos quintis superiores e sobrerrepresentação de pretos e pardos nos inferiores.

---

### 🗺️ 3. Mapeamento interurbano (`03_mapping/`)

Os scripts desta etapa representam espacialmente os extremos da renda (Q1 e Q5), destacando o contraste territorial entre pobreza e riqueza urbana.

* `09_select_quintiles_q1_q5.py` – seleciona os 20% mais pobres e mais ricos por cidade.
* `10_plot_income_maps_grouped_by_region.py` – plota os mapas comparativos por região.

<img width="893" height="589" alt="image" src="https://github.com/user-attachments/assets/9531fb91-fc7f-4703-90bc-2f43d76b25b0" />

> **Fonte:** Autor (2025).
> Os mapas revelam padrões de **segregação morfológica** e **contrastes socioespaciais** que reforçam hierarquias raciais e fundiárias no espaço urbano.

---

## ⚠️ Limitações e adaptações recomendadas

* Os caminhos (`path`) devem ser **editados manualmente** conforme o ambiente de execução.
* O formato `.gpkg` reduz o tamanho do repositório, mas pode exigir conversão para `.shp` para uso direto.
* Nem todos os shapefiles auxiliares (IBGE, massas d’água, oceanos) estão incluídos.
* As figuras geradas podem variar conforme o sistema, versão de biblioteca e configuração de fontes.

---

## 📚 Citação sugerida

Se este repositório for utilizado total ou parcialmente em análises, publicações ou atividades acadêmicas, cite da seguinte forma:

🔹 Formato ABNT:

GOMES, Pedro Igor Galvão. mid_sized_cities_env_inequality: Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras.
Palmas: Universidade Federal do Tocantins, 2025. Dataset e scripts. DOI: 10.5281/zenodo.17518966

🔹 Formato APA:

Gomes, P. I. G. (2025). mid_sized_cities_env_inequality: Race, Income, and Environmental (In)Justice in Brazilian Mid-Sized Cities [Data set & scripts].
Universidade Federal do Tocantins. Zenodo. https://doi.org/10.5281/zenodo.17518966

## 🧩 Consideração final

> *Entender as raízes desse processo e cartografar as desigualdades, conforme aqui proposto, evidencia que nenhum discurso sobre “progresso” ou “crescimento” se sustenta de forma legítima enquanto persistirem as contradições raciais e fundiárias que engendraram a formação social brasileira.*

> **Pedro I. G. Gomes (2025)**


