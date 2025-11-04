# mid_sized_cities_env_inequality
“Base de dados e scripts da dissertação ‘Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras’ (GOMES, 2025).”
# 🌎 Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras

**Autor:** Pedro Igor Galvão Gomes  
**Instituição:** Universidade Federal do Tocantins (UFT)  
**Ano:** 2025  
**Licença:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  

---

## 🧭 Descrição geral

Este repositório reúne a **base de dados e os scripts analíticos** desenvolvidos para a dissertação *“Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras”* (GOMES, 2025).  

O objetivo é disponibilizar, de forma aberta e reprodutível, as **etapas de tratamento, análise e mapeamento** utilizadas para mensurar desigualdades socioambientais no contexto das cidades médias (100–500 mil habitantes).  

A base de dados foi consolidada em um **único arquivo GeoPackage (`.gpkg`)**, a fim de reduzir o tamanho e simplificar a distribuição — substituindo os múltiplos shapefiles utilizados no processamento original.

---

## 📁 Estrutura do repositório

```
mid_sized_cities_env_inequality/
│
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
└── pipelines/
    ├── 01_build_base/
    │   ├── 01_build_indicators_from_excels.py
    │   ├── 02_harmonize_renda_2010_to_2022.py
    │   └── 03_select_mid_sized_cities_idsafe.py
    │
    ├── 02_analysis/
    │   ├── 04_plot_correlation_national.py
    │   ├── 05_plot_correlation_by_region.py
    │   ├── 06_plot_access_infrastructure_quintile.py
    │   ├── 07_plot_discrepancy_by_region.py
    │   └── 08_plot_participation_by_region.py
    │
    └── 03_mapping/
        ├── 09_select_quintiles_q1_q5.py
        └── 10_plot_income_maps_grouped_by_region.py
```

---

## 🧩 Organização lógica dos conteúdos

### **1️⃣ Pasta `/data/`**
Contém os **arquivos de dados prontos para uso** e o **dicionário de variáveis**.  
O arquivo principal é o **`mid_sized_cities_inequality_data_2022.gpkg`**, que reúne:
- setores censitários urbanos das **92 cidades médias** (Censo 2022);
- variáveis socioeconômicas e raciais harmonizadas com o Censo 2010;
- indicadores de infraestrutura (água, esgoto e coleta de lixo).

> 💡 O formato `.gpkg` (GeoPackage) substitui dezenas de shapefiles, preservando a geometria e metadados em um único arquivo leve.  
> Caso o usuário deseje gerar shapefiles, basta exportar via QGIS, GeoPandas ou ogr2ogr.

---

### **2️⃣ Pasta `/docs/`**
Reúne a documentação metodológica em quatro etapas:

| Arquivo | Conteúdo |
|----------|-----------|
| `README_01_variables.md` | Construção dos indicadores censitários (variáveis e fórmulas). |
| `README_02_cities.md` | Definição das 92 cidades médias (manchas urbanas, contiguidade e critérios populacionais). |
| `README_03_analysis_methodology.md` | Descrição das métricas de desigualdade e dos scripts de análise. |
| `README_04_Mapping.md` | Procedimentos de geração dos mapas e identificação dos quintis (Q1 e Q5). |

Cada documento corresponde a uma **etapa da pipeline** descrita na dissertação e pode ser lido independentemente.

---

### **3️⃣ Pasta `/pipelines/`**
Contém os **scripts Python** que implementam o fluxo completo de tratamento, análise e visualização.

Os scripts estão divididos em **três módulos funcionais**:

| Módulo | Descrição | Observação |
|--------|------------|-------------|
| **01_build_base** | Geração dos indicadores, harmonização da renda (2010→2022) e seleção das cidades médias. | O produto final dessa etapa já está disponível no `.gpkg`; não é necessário executá-la novamente. |
| **02_analysis** | Aplicação das métricas e geração dos gráficos de correlação, discrepância e participação por raça e quintil. | Scripts independentes — podem ser executados a partir do arquivo `.gpkg`. |
| **03_mapping** | Seleção dos quintis extremos (Q1 e Q5) e plotagem dos mapas regionais de renda e desigualdade. | Requer arquivos adicionais do IBGE (massas d’água e oceanos), indicados no README_04. |

> ⚠️ **Importante:** os caminhos originais (`G:\Meu Drive\Dissertacao\...`) devem ser substituídos por caminhos locais do usuário.  
> Nenhum script é automaticamente vinculado aos dados do repositório — todos requerem **ajuste manual dos diretórios de entrada e saída**.

---

## 🚀 Fluxo sugerido de reprodução

1. **Baixar ou clonar** o repositório:
   ```bash
   git clone https://github.com/pedroigorggomes/mid_sized_cities_env_inequality.git
   ```
2. **Abrir no VS Code ou JupyterLab**.
3. **Usar como base principal** o arquivo:
   ```
   data/mid_sized_cities_inequality_data_2022.gpkg
   ```
4. Executar:
   - Scripts do diretório `02_analysis` → gera gráficos (.png);
   - Scripts do diretório `03_mapping` → gera mapas (.png).

> Os scripts do diretório `01_build_base` servem apenas como **registro metodológico** do processamento original, descrito nas dissertações e READMEs correspondentes.

---

## ⚙️ Dependências

Instale o ambiente mínimo de execução:
```bash
pip install -r requirements.txt
```

Principais bibliotecas:
- `geopandas`, `pandas`, `matplotlib`, `numpy`
- `shapely`, `networkx`
- `seaborn` (opcional para gráficos)

---

## 🧭 Limitações e observações técnicas

- Os shapefiles originais do **IBGE** (malhas setoriais, oceanos e massas d’água) **não estão incluídos** no repositório por questões de tamanho e licença.  
  - Devem ser obtidos diretamente do site do IBGE (2022) e inseridos nos diretórios indicados nos scripts de mapeamento.  
- O arquivo `.gpkg` contém todos os atributos e geometrias necessárias para replicar as análises.  
- As métricas podem variar ligeiramente em função de arredondamentos e projeções locais.  
- Recomenda-se manter o CRS **SIRGAS 2000 / UTM 22S (EPSG:31982)** em todas as operações espaciais.  

---

## 🧾 Citação sugerida

> GOMES, Pedro Igor Galvão. *Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras.* Dissertação (Mestrado em Ciências do Ambiente) — Universidade Federal do Tocantins, 2025.  
> Repositório de dados e scripts: [https://github.com/pedroigorggomes/mid_sized_cities_env_inequality](https://github.com/pedroigorggomes/mid_sized_cities_env_inequality)


“Entender as raízes desse processo e cartografar as desigualdades evidencia que nenhum discurso sobre ‘progresso’ se sustenta enquanto persistirem as contradições raciais e fundiárias que engendraram a formação social brasileira.”
Pedro I. G. Gomes (2025)
