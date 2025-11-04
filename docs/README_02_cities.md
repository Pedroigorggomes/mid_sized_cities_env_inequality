# Metodologia de definição das 92 cidades médias brasileiras

**Autor:** Pedro Igor Galvão Gomes  
**Instituição:** Universidade Federal do Tocantins (UFT)  
**Ano:** 2025  
**Licença:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  

---

## 🧭 Descrição geral

Este documento descreve o processo de **definição das 92 cidades médias brasileiras** incluídas na base `mid_sized_cities_indicators_2022.gpkg`, utilizada na dissertação *“Raça, Renda e (In)Justiça Ambiental nas Cidades Médias Brasileiras”* (GOMES, 2025).  

O recorte das cidades médias foi obtido a partir da **construção de manchas urbanas nacionais** derivadas dos **setores censitários urbanos do Censo Demográfico 2022**, com base na população residente e na contiguidade espacial das áreas urbanizadas.

---

## 🗺️ Base de partida

A base inicial foi o shapefile `Setores_raca_renda.shp`, que reúne as variáveis censitárias (população, raça/cor, infraestrutura e renda) para todos os setores do Brasil.  
A partir dessa camada, foram selecionados apenas os setores **urbanos de alta e baixa densidade**, conforme o código da variável `CD_SITU` do IBGE:

| Código `CD_SITU` | Descrição |
|------------------|------------|
| 1 | Área urbana de alta densidade |
| 2 | Área urbana de baixa densidade |

Esses dois tipos de setores formam, juntos, o **tecido urbano contínuo** de cada município.

---

## 🧱 Etapa 1 – Construção das manchas urbanas municipais

1. **Filtragem dos setores urbanos:**  
   foram mantidos apenas os setores com `CD_SITU` igual a 1 ou 2.  
2. **Dissolução espacial:**  
   os polígonos foram dissolvidos por `NM_MUN` e `NM_UF` (nome do município e do estado), de modo a evitar a fusão indevida de cidades homônimas em diferentes estados.  
3. **Cálculo da população urbana municipal:**  
   a variável `v0001` (população residente) foi somada, gerando o total de habitantes em áreas urbanas de cada município.  

✅ **Resultado:** uma camada vetorial com as **manchas urbanas municipais** do Brasil, cada uma representando o perímetro contínuo da ocupação urbana de um município, com sua população total e composição racial agregada.

---

## 🔗 Etapa 2 – Identificação de conurbações e agrupamento espacial

A partir da camada de manchas urbanas, foi criado um **grafo de contiguidade espacial** (critério *Queen*), no qual cada polígono representa uma mancha e cada aresta representa o compartilhamento de fronteira entre manchas.  

- As manchas **isoladas** mantiveram-se individualizadas.  
- As manchas **conectadas** (ou seja, que compartilham fronteiras) foram agrupadas em **componentes urbanos**.  
- Para cada componente, foi calculada a **população total somando as populações das manchas contíguas**.  

Esse processo identificou **aglomerados urbanos contínuos** (grupos de municípios espacialmente integrados) em todo o território nacional.

---

## 📊 Etapa 3 – Aplicação dos critérios populacionais

Para cada mancha urbana ou grupo de manchas conectadas, aplicou-se o critério de faixa populacional:

- **Mantidas:** manchas isoladas ou agrupamentos com **população total entre 100.000 e 500.000 habitantes**;  
- **Excluídas:**  
  - manchas ou grupos com população **inferior a 100 mil habitantes**;  
  - manchas ou grupos cuja soma populacional **ultrapassava 500 mil habitantes**.

O limiar inferior de 100 mil habitantes reflete o ponto de transição entre pequenas e médias cidades; o superior (500 mil) separa as médias das metrópoles regionais e aglomerações consolidadas.

---

## ⚖️ Etapa 4 – Tratamento de casos de conurbação

Durante a agregação espacial, alguns municípios com manchas urbanas contíguas formaram agrupamentos que ultrapassavam o limite superior de 500 mil habitantes.  
Nesses casos, o algoritmo excluiu **todas as manchas envolvidas na conurbação**, uma vez que elas não poderiam ser tratadas individualmente como cidades médias.  

Da mesma forma, quando duas manchas estavam conectadas mas **uma delas possuía população inferior a 100 mil habitantes**, essa mancha menor foi **eliminada**.  
O objetivo foi preservar apenas manchas urbanas cuja dinâmica socioespacial correspondesse efetivamente a núcleos urbanos médios e autônomos, sem dependência metropolitana, conforme a figura abaixo.

Aplicação dos critérios de seleção para cidades médias
<img width="941" height="908" alt="image" src="https://github.com/user-attachments/assets/f17ea725-3d6c-47ec-8182-d49262a96694" />
Fonte: Autor (2025).

---

## 📦 Resultado final

| Descrição | Valor |
|------------|--------|
| Total de cidades médias identificadas | **92** |
| Faixa populacional adotada | 100.000 – 500.000 habitantes |
| Ano de referência | Censo 2022 |
| Tipo de unidade espacial | Mancha urbana contínua (áreas de alta e baixa densidade) |
| Sistema de referência | SIRGAS 2000 / UTM 22S (EPSG:31982) |

---

## 🗺️ Síntese metodológica

| Etapa | Operação principal | Arquivo gerado |
|--------|--------------------|----------------|
| 1 | Filtragem de setores `CD_SITU = 1` e `2` | `Areas_Urbanas_Com_Variaveis.shp` |
| 2 | Dissolução por município e estado | `Manchas_Urbanas_Populacao_Total_Raca.shp` |
| 3 | Cálculo de contiguidade e população por mancha | `Cidades_Medias_100_500_mil_SEM_Conurbacoes.shp` |
| 4 | Exclusão de manchas <100 mil ou >500 mil habitantes | — |
| 5 | Revisão manual e consolidação final | `Cidades_Medias_Variaveis_atualizado_v2.shp` |

---

## 📎 Observações finais

- O procedimento privilegia a **integridade morfológica da urbanização** e não apenas os limites administrativos municipais.  
- A eliminação das conurbações garante que o conjunto represente **cidades médias isoladas**, com centralidade própria.  
- O produto final constitui o **recorte espacial das cidades médias brasileiras**, base para todas as análises de desigualdade socioambiental da dissertação.

---

**Citação sugerida:**
> GOMES, Pedro Igor Galvão. *Metodologia de definição das 92 cidades médias brasileiras.* Palmas: Universidade Federal do Tocantins, 2025.  
> Disponível em: [https://github.com/pedroigorggomes/mid_sized_cities_env_inequality/docs/README_cities.md](https://github.com/pedroigorggomes/mid_sized_cities_env_inequality/docs/README_cities.md)

