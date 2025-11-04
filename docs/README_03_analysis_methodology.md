# Metodologia de Análise – Cidades Médias (métricas e procedimentos)

**Escopo.** Este documento descreve as métricas e o fluxo analítico aplicados às cidades médias brasileiras (100–500 mil hab.). A implementação foi feita em **Python**, tomando como referência o arcabouço de **Hoffmann et al. (2019)** para medidas de desigualdade, pobreza, concentração, segregação e correlação.

---

## 1) Dados de entrada (pré-requisitos)

Os insumos deste estágio são produtos dos scripts anteriores:

- **Setores 2022 com variáveis integradas**  
  `Setores_Indicadores_Censo_22.shp`  
  (demografia; percentuais de raça; saneamento; alfabetização).

- **Renda per capita harmonizada (2010→2022)**  
  Campo `RpC_2010` inserido em `Setores_Indicadores_Censo_22.shp` via **interseção espacial** (2010×2022) com **ponderação por área** (Brazil Albers, ellps GRS80).

- **Seleção espacial das cidades médias**  
  Filtro urbano `CD_SIT ∈ {1,2}` (alta/baixa densidade), **dissolve** por `NM_MUN`+`NM_UF`, **conurbações** por contiguidade **Queen** e regras de população (100–500 mil).  
  Seleção final dos **setores** por **`CD_SETOR`** (join por chave).  
  **Resultado:** `Cidades_Medias_Variaveis_atualizado_v2.shp` (usado nas análises abaixo).

> **Nota:** colunas legadas removidas do dataset publicável **não** são consideradas nesta metodologia.

---

## 2) Escalas analíticas

- **Nacional**: conjunto dos setores das **92 cidades médias**.  
- **Regional**: agregação por **macrorregião** (`NM_REGIAO`).  
- **Interurbana**: leitura cartográfica (ênfase em **Q1** e **Q5**); **sem** métricas estatísticas adicionais.

---

## 3) Métricas

As métricas seguem Hoffmann et al. (2019) e são implementadas com `pandas`, `numpy` e `geopandas`.

### 3.1 Quintis de renda (por cidade)
Particiona a distribuição de `RpC_2010` em **5** partes de igual tamanho **em cada município** (`NM_MUN`), rotulando cada setor com `Quintil ∈ {1,2,3,4,5}`.

- Implementação: `pd.qcut(RpC_2010, 5, labels=[1,2,3,4,5])` por cidade.  
- Fórmula (ordem estatística):  
  \[
  Q_k = x_{\,k\cdot(n+1)/5}, \quad k \in \{1,\dots,5\}
  \]
  em que \(n\) é o número de setores da cidade.

> **Observação:** em casos de empates, usar `duplicates="drop"` e registrar a ocorrência.

### 3.2 Proporção por raça no quintil
Para cada **quintil** \(q\), calcula-se a **proporção interna** das raças.

\[
\text{Proporção}_{\text{raça},q} =
\frac{\text{Total da raça no quintil } q}{\text{Total de pessoas no quintil } q}\times 100
\]

Na prática, também se utiliza a normalização **por setor** para correlações:
\[
\%\text{raça}_i = 100 \cdot \frac{\text{raça}_i}{v0001_i}
\]

### 3.3 Linha de equidade e discrepância
Define-se a **linha de equidade**: a participação **ideal** de cada raça em cada quintil é a sua participação **global** na escala analisada (nacional ou regional) **dividida por 5**.

- **Esperado por quintil** (absoluto):  
  \[
  \text{Esperado}_{\text{raça}} = \frac{\text{Total da raça (na escala)}}{5}
  \]
- **Discrepância** (absoluto):  
  \[
  \Delta_{\text{raça},q} = \text{Observado}_{\text{raça},q} - \text{Esperado}_{\text{raça}}
  \]
Sinal positivo indica **sobrerrepresentação**; negativo, **sub-representação**.

### 3.4 Correlação de Pearson
Associação linear entre **renda** e **composição racial** (em %) e entre **renda** e **infraestrutura** (em %).

\[
r_{xy} = \frac{\sum_i (x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i (x_i-\bar{x})^2\;\sum_i (y_i-\bar{y})^2}}
\]

Exemplos: \(x = \text{RpC\_2010}\); \(y \in \{\%\text{Brancos},\%\text{Pretos},\ldots\}\) ou \(y \in \{P\_Agua, P\_Esgo, P\_Lixo\}\).

---

## 4) Procedimentos computacionais (o que os scripts fazem)

> **Arquivo base:** `Cidades_Medias_Variaveis_atualizado_v2.shp`  
> **Colunas-chave:** `RpC_2010`, `Brancos`, `Pretos`, `Amarelos`, `Pardos`, `Indigena`, `v0001`, `P_Agua`, `P_Esgo`, `P_Lixo`, `NM_REGIAO`, `NM_MUN`.

1. **Conversões e limpeza**  
   - Converter `RpC_2010` para numérico; tratar `NaN` conforme necessário.  
   - Normalizar raças **por setor**: \(\%\text{raça}_i = 100 \cdot \frac{\text{raça}_i}{v0001_i}\) (quando `v0001>0`).

2. **Quintis por cidade**  
   - Calcular `Quintil` por `NM_MUN` com `qcut` sobre `RpC_2010`.

3. **Agregações por quintil (escala regional)**  
   Para cada **região** e **quintil**:
   - Somar **populações por raça** (absoluto) e obter **percentuais** dentro do quintil;  
   - Estimar **população com acesso** à infraestrutura:  
     \[
     \text{pop\_acesso} = \sum \bigl( v0001 \times \tfrac{P\_{\text{infra}}}{100} \bigr)
     \]
     e **sem acesso**: \(\text{pop\_total} - \text{pop\_acesso}\).

4. **Discrepância (linha de equidade)**  
   - Para cada **região**:  
     \(\text{Esperado}_{\text{raça}} = \text{Total regional da raça} / 5\).  
     Para cada quintil, calcular \(\Delta = \text{Observado} - \text{Esperado}\) por raça.

5. **Correlação (nacional e por região)**  
   - Calcular `corr(RpC_2010, %raça)` por raça; opcionalmente, ajustar **reta de tendência**.

---

## 5) Produtos e scripts (estrutura padronizada)

> Pastas de **saída** numeradas (01–05). Scripts de **análise** numerados **04–08** (os scripts **01–03** preparam os insumos).

- **01 — Correlação nacional (todas as raças)**  
  - **Saída:** `outputs/01_correlation_national/All_Races_Correlation.png`  
  - **Script:** `scripts/04_plot_correlation_national.py` *(função: `plot_correlations`)*  
  - **Descrição:** dispersão + linha de tendência entre `RpC_2010` e `% de raça` (Brancos, Pretos, Amarelos, Pardos, Indígena) para o conjunto das 92 cidades.

- **02 — Correlação por região**  
  - **Saídas:** `outputs/02_correlation_region/{REGIAO}_racial_correlation.png`  
  - **Script:** `scripts/05_plot_correlation_by_region.py` *(função: `plot_correlations_by_region`)*  
  - **Descrição:** mesma lógica da correlação nacional, estratificada por `NM_REGIAO`.

- **03 — Acesso à infraestrutura × quintil (por região)**  
  - **Saídas:** `outputs/03_access_infra_quintile/{REGIAO}_acesso_raca_quintil.png`  
  - **Script:** `scripts/06_plot_access_infrastructure_quintile.py`  
  - **Descrição:** para cada região e quintil (Q1–Q5), mostra:  
    (i) % por raça; (ii) população por raça (absoluto); (iii) população **com/sem** acesso (`P_Agua`, `P_Esgo`, `P_Lixo`) via \(v0001 \times P_{\text{infra}}/100\).

- **04 — Discrepância (observado − esperado) por raça e quintil (por região)**  
  - **Saídas:** `outputs/04_discrepancy_region/{REGIAO}_regional_population_discrepancy.png`  
  - **Script:** `scripts/07_plot_discrepancy_by_region.py` *(função: `plot_regional_discrepancy_data`)*  
  - **Descrição:** aplica **linha de equidade** (participação regional da raça / 5) e plota \(\text{observado} - \text{esperado}\) por quintil.

- **05 — Participação (%) por raça em cada quintil (por região)**  
  - **Saídas:** `outputs/05_participation_region/{REGIAO}_participacao_raca.png`  
  - **Script:** `scripts/08_plot_participation_by_region.py` *(função: `analyze_and_plot_discrepancies_by_region`)*  
  - **Descrição:** barras com a **participação relativa** de cada raça em Q1–Q5 (porcentagens somando 100% ao longo dos quintis para cada raça na região).

**Observações de organização**
- Manter nomes **ASCII** (sem acentos) para compatibilidade com GitHub/Zenodo.  
- Se houver pastas locais (`G:\...\5 Graficos Censo 2022\...`), espelhar a estrutura acima dentro de `outputs/` no repositório.

---

## 6) Notas técnicas e limitações

- **Renda (`RpC_2010`)**: harmonizada para 2022 via overlay 2010×2022 (Brazil Albers, ellps GRS80) com **ponderação por área**; valores aproximados e sujeitos a incertezas dos limites setoriais e imputações do IBGE.  
- **Denominadores**: `P_Agua`, `P_Esgo`, `P_Lixo` usam **`V0007`** (DPO) como denominador; raças usam **`V0001`**.  
- **Quintis por cidade**: refletem a **ordem interna** de cada município; comparações intermunicipais devem considerar cortes **locais**.  
- **Curva de Lorenz**: avaliada, mas **não** utilizada para recorte racial por baixa sensibilidade à (sub/sobre)representação nos quintis; adotou-se **linha de equidade** + **discrepância**.  
- **Interurbano**: análise **descritiva** (mapas Q1/Q5); não se aplicam as métricas acima nessa escala.  
- **Tratamento de zeros/NaN**: divisões por zero são evitadas (percentuais = 0 quando denominador = 0); documentar casos de baixa cobertura.  
- **Seleção via `CD_SETOR`**: etapas espaciais finais usam a **chave** para robustez diante de eventuais ajustes de projeção/topologia.

---

## 7) Referências essenciais

- **Hoffmann, R. et al. (2019).** *Distribuição de renda: medidas de desigualdade, pobreza, concentração, segregação e polarização.*  
- **IBGE (2010; 2022/2023).** Censos Demográficos – agregados por setor censitário (cor/raça; características dos domicílios).