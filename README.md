# mid_sized_cities_env_inequality
“Base de dados e scripts da dissertação ‘Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras’ (GOMES, 2025).”
# Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras

**Autor:** Pedro Igor Galvão Gomes  
**Orientadora:** Profa. Dra. Lucimara Albieri de Oliveira  
**Programa:** Pós-Graduação em Ciências do Ambiente (PPGCiamb) – Universidade Federal do Tocantins  
**Ano:** 2025  
**Licença:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)  
**DOI:** _[aguardando integração Zenodo]_  

---

## Descrição geral

Este repositório reúne os **dados, scripts e materiais de apoio** da dissertação *“Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras”*, apresentada ao Programa de Pós-Graduação em Ciências do Ambiente da Universidade Federal do Tocantins (UFT).  

O estudo analisa como **raça/cor** e **renda** estruturam **padrões desiguais de acesso à infraestrutura urbana básica** (abastecimento de água, esgotamento sanitário e coleta de lixo) em **92 cidades médias brasileiras**, evidenciando dinâmicas de **injustiça ambiental** e a permanência de desigualdades raciais e fundiárias na produção do espaço urbano:contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}.

---

## Objetivos

**Objetivo geral:**  
Analisar como a articulação entre raça/cor e renda estrutura padrões desiguais de acesso à infraestrutura urbana básica em cidades médias brasileiras:contentReference[oaicite:2]{index=2}.  

**Objetivos específicos:**  
- Investigar a influência das heranças históricas de colonização, escravidão e patrimonialismo na formação socioespacial das cidades médias;  
- Identificar padrões de estratificação racial e econômica no espaço urbano;  
- Mapear a cobertura de serviços básicos de saneamento e confrontá-la com a composição racial e econômica dos setores censitários;  
- Evidenciar gradientes de acesso e formas de injustiça ambiental associadas:contentReference[oaicite:3]{index=3}.

---

## Metodologia

A pesquisa adota uma **abordagem exploratória e quali-quantitativa**, fundamentada no **materialismo histórico-dialético** e na **interpretação crítica do espaço urbano**:contentReference[oaicite:4]{index=4}.  
As etapas metodológicas incluem:

1. **Seleção do recorte de análise** – 92 cidades médias (100–500 mil habitantes) distribuídas nas cinco macrorregiões brasileiras;  
2. **Integração de dados censitários (IBGE 2010 e 2022)** sobre raça, renda e saneamento;  
3. **Geoprocessamento** via *Python (GeoPandas, Pandas)* e *QGIS* para gerar indicadores normalizados por setor censitário;  
4. **Cálculo de métricas** (quintis, discrepância, correlação de Pearson) baseadas em Hoffmann et al. (2019):contentReference[oaicite:5]{index=5};  
5. **Visualização espacial e análise regional comparativa**.

---

## Principais resultados

- Identificou-se **um padrão robusto de estratificação racial da renda** nas cidades médias: a população branca é super-representada nos quintis de maior renda (Q4-Q5), enquanto pretos e pardos concentram-se nos quintis inferiores:contentReference[oaicite:6]{index=6}.  
- Essa inflexão entre Q3 e Q4 representa **uma “fronteira simbólica racial” da renda urbana**, marcando a separação entre grupos racializados e o acesso aos benefícios da urbanização:contentReference[oaicite:7]{index=7}.  
- Persistem **desigualdades regionais**: as regiões Norte e Nordeste apresentam os maiores déficits de saneamento, com predominância de população preta e parda em áreas de baixa renda.  
- A pesquisa demonstra que as **cidades médias** reproduzem, em menor escala, as desigualdades estruturais das metrópoles, configurando-se como **espaços-chave na engrenagem das injustiças socioambientais brasileiras**:contentReference[oaicite:8]{index=8}.

---

## Estrutura do repositório
mid_sized_cities_env_inequality/
│
├── data/
│ ├── mid_sized_cities_indicators_2022.gpkg
│ ├── mid_sized_cities_indicators_2022.csv
│ └── mid_sized_cities_indicators_2022_metadata.md
│
├── scripts/
│ ├── preprocess_census.ipynb
│ ├── merge_tables.py
│ ├── calc_indicators.py
│ └── mapping_outputs.ipynb
│
├── docs/
│ ├── methodology_summary.pdf
│ ├── figures/
│ └── README_data.md
│
├── LICENSE
├── requirements.txt
└── README.md

---
## ⚙️ Instalação

Para reproduzir as análises:

pip install -r requirements.txt

## Dependências

geopandas==0.14.4
pandas==2.2.3
numpy==1.26.4
matplotlib==3.9.2
shapely==2.0.4
networkx==3.3

## Citação sugerida
ABNT
GOMES, Pedro Igor Galvão. Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras: Base de Dados e Scripts. Palmas: Universidade Federal do Tocantins, 2025. DOI: https://doi.org/10.xxxx/zenodo.xxxxxxx

APA
Gomes, P. I. G. (2025). Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras [dataset]. Universidade Federal do Tocantins. Zenodo. https://doi.org/10.xxxx/zenodo.xxxxxxx

“Entender as raízes desse processo e cartografar as desigualdades evidencia que nenhum discurso sobre ‘progresso’ se sustenta enquanto persistirem as contradições raciais e fundiárias que engendraram a formação social brasileira.”
Pedro I. G. Gomes (2025)