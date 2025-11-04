# Metodologia de mapeamento – Q1 × Q5 nas cidades médias brasileiras

**Autor:** Pedro Igor Galvão Gomes
**Instituição:** Universidade Federal do Tocantins (UFT)
**Ano:** 2025
**Licença:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## 🧭 Descrição geral

Este documento apresenta a metodologia utilizada para o **mapeamento espacial dos quintis extremos de renda (Q1 e Q5)** nas **92 cidades médias brasileiras** definidas na base `mid_sized_cities_indicators_2022.gpkg`.
O objetivo deste procedimento é permitir a **visualização comparativa das desigualdades intraurbanas**, destacando a localização dos 20% mais pobres e dos 20% mais ricos em cada município.

A rotina foi desenvolvida em **Python**, com base em operações de geoprocessamento, conectividade espacial e agrupamento cartográfico, utilizando as bibliotecas **GeoPandas**, **NetworkX**, **Matplotlib** e **NumPy**.

---

## 🗺️ Base de partida

O mapeamento parte do arquivo vetorial `Cidades_Medias_Variaveis.shp`, gerado a partir das etapas anteriores da pesquisa. Este arquivo contém os **setores censitários urbanos** das cidades médias brasileiras, com informações integradas de **renda**, **população**, **raça/cor** e **infraestrutura básica**.

Além disso, são utilizadas duas camadas auxiliares para o contexto geográfico:

| Camada                            | Descrição                              | Fonte         |
| --------------------------------- | -------------------------------------- | ------------- |
| `ne_10m_ocean.shp`                | Delimitação dos oceanos                | Natural Earth |
| `geoft_bho_massa_dagua_v2019.shp` | Hidrografia e massas d’água interiores | IBGE / ANA    |

---

## 🧮 Etapa 1 – Cálculo dos quintis de renda por município

A primeira etapa consiste em dividir a distribuição da variável `RpC_2010` (renda média domiciliar per capita harmonizada) em **cinco partes iguais** dentro de cada município (`NM_MUN`):

[
Quintil = pd.qcut(RpC_{2010}, 5, labels=[1, 2, 3, 4, 5])
]

Cada setor censitário recebe um rótulo de quintil, onde:

* **Q1** representa os 20% de menor renda;
* **Q5** representa os 20% de maior renda.

Essas classes são locais (por município), assegurando comparabilidade **interna** entre setores urbanos da mesma cidade.

---

## ✂️ Etapa 2 – Extração dos extratos extremos (Q1 e Q5)

Após o cálculo dos quintis, são gerados dois arquivos derivados:

| Arquivo                | Conteúdo                             | Descrição                                                   |
| ---------------------- | ------------------------------------ | ----------------------------------------------------------- |
| `quintil_inferior.shp` | Setores do **primeiro quintil (Q1)** | Representam as áreas de menor renda relativa em cada cidade |
| `quintil_superior.shp` | Setores do **quinto quintil (Q5)**   | Representam as áreas de maior renda relativa em cada cidade |

Esses shapefiles funcionam como **máscaras de sobreposição** para destacar os extremos da distribuição de renda nos mapas regionais.

---

## 🧩 Etapa 3 – Delimitação da mancha urbana principal

Para cada município, define-se automaticamente o **perímetro urbano contínuo** (massa urbana principal), a partir de um grafo de conectividade espacial:

1. Conversão das geometrias para **projeção métrica (EPSG:3857)**;
2. Aplicação de um **buffer de 1 km** sobre cada setor;
3. Construção de um grafo (*Graph*) com nós representando os setores e arestas conectando buffers que se interceptam;
4. Identificação dos **componentes conectados** e cálculo da área total de cada um;
5. Seleção do **maior componente urbano** (ou união dos dois maiores se distarem ≤1 km);
6. Conversão de volta para **EPSG:4326** e obtenção do **bounding box** final para enquadramento do mapa.

Este processo assegura que o enquadramento de cada figura se limite à área efetivamente urbanizada, evitando vazios ou extensões rurais.

---

## 🧭 Etapa 4 – Geração dos painéis cartográficos por macrorregião

Os mapas são produzidos separadamente para cada **macrorregião brasileira** (`NM_REGIAO`), agrupando os municípios em blocos de seis (2×3 subplots) para composição visual homogênea.

Para cada município:

* a base setorial é representada em **cinza claro**;
* o **quintil inferior (Q1)** é destacado em **vermelho (#EF7C80)**;
* o **quintil superior (Q5)** é destacado em **verde petróleo (#156E7A)**;
* oceanos e massas d’água aparecem em tons de **azul (#4e76b7 / #4cc4d9)**.

Cada painel regional recebe título e identificação alfabética dos municípios, exportando arquivos em **PNG (300 dpi)**.

---

## 📦 Estrutura de saídas

```
outputs/
  03_mapping/
    quintil_inferior.shp
    quintil_superior.shp
    Norte/
      Norte_municipios_01_agrupados.png
      Norte_municipios_02_agrupados.png
    Nordeste/
    Sudeste/
    Sul/
    Centro-Oeste/
```

---

## ⚙️ Scripts utilizados

| Nº | Script                                     | Função principal                                                                          |
| -- | ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| 09 | `09_select_quintiles_q1_q5.py`             | Calcula os quintis de renda e gera os shapefiles `quintil_inferior` e `quintil_superior`. |
| 10 | `10_plot_income_maps_grouped_by_region.py` | Gera os painéis de mapas regionais com sobreposição Q1/Q5 e enquadramento automático.     |

> Os caminhos de entrada e saída podem ser ajustados manualmente no início de cada script.

---

## ▶️ Execução

1. **Gerar os shapefiles Q1 e Q5:**

```bash
python pipelines/03_mapping/09_select_quintiles_q1_q5.py
```

2. **Produzir os mapas regionais:**

```bash
python pipelines/03_mapping/10_plot_income_maps_grouped_by_region.py
```

---

## 📎 Observações técnicas

* **CRS:** cálculos de distância realizados em **EPSG:3857**; saídas exportadas em **EPSG:4326**.
* **Performance:** cidades com alta fragmentação urbana podem demandar tempo de processamento; o parâmetro `buffer_km` (0.5–2 km) pode ser ajustado.
* **Geometrias inválidas:** o uso de `buffer(0)` corrige inconsistências topológicas simples.
* **Reprodutibilidade:** recomenda-se registrar as versões das camadas auxiliares (IBGE/ANA, Natural Earth) no README principal do repositório.
* **Escala visual:** os mapas são descritivos e não representam proporções demográficas absolutas.

---

**Citação sugerida:**

> GOMES, Pedro Igor Galvão. *Metodologia de mapeamento (Q1 × Q5) nas cidades médias brasileiras.* Palmas: Universidade Federal do Tocantins, 2025.
> Disponível em: [https://github.com/pedroigorggomes/mid_sized_cities_env_inequality/docs/README_04_mapping.md](https://github.com/pedroigorggomes/mid_sized_cities_env_inequality/docs/README_04_mapping.md)
