"""
Script: 09_select_quintiles_q1_q5.py
Autor: Pedro Igor Galvão Gomes
Instituição: Universidade Federal do Tocantins (UFT)
Ano: 2025
Licença: CC BY 4.0

Descrição:
-----------
Este script calcula os quintis de renda per capita (RpC_2010) por município nas 92 cidades médias brasileiras
e gera dois shapefiles correspondentes aos extratos extremos da distribuição:
- Q1 → 20% mais pobres (quintil inferior)
- Q5 → 20% mais ricos (quintil superior)

Entrada:
---------
- Shapefile base com variáveis integradas: `Cidades_Medias_Variaveis.shp`
  (gerado no pipeline 02_preprocessing ou 03_selection)

Saídas:
--------
- `quintil_inferior.shp`
- `quintil_superior.shp`

Esses arquivos são utilizados no script seguinte (`10_plot_income_maps_grouped_by_region.py`)
para gerar os mapas regionais comparando Q1 e Q5.
"""

# =============================================================================
# 📦 Importação de bibliotecas
# =============================================================================
import geopandas as gpd
import pandas as pd
import os

# =============================================================================
# ⚙️ Função principal
# =============================================================================
def select_quintiles(input_shp, output_inferior, output_superior):
    """
    Calcula os quintis de renda (RpC_2010) por município e exporta shapefiles
    com os setores correspondentes ao 1º e 5º quintis (Q1 e Q5).
    """

    # -------------------------------------------------------------------------
    # Etapa 1: Leitura da base
    # -------------------------------------------------------------------------
    print("🔹 Lendo o shapefile de entrada...")
    gdf = gpd.read_file(input_shp)
    print(f"Total de feições lidas: {len(gdf)}")

    # -------------------------------------------------------------------------
    # Etapa 2: Conversão e verificação da variável de renda
    # -------------------------------------------------------------------------
    print("🔹 Convertendo variável RpC_2010 para tipo numérico...")
    gdf['RpC_2010'] = pd.to_numeric(gdf['RpC_2010'], errors='coerce')

    # -------------------------------------------------------------------------
    # Etapa 3: Cálculo dos quintis por município
    # -------------------------------------------------------------------------
    print("🔹 Calculando quintis de renda por município...")
    gdf['Quintil'] = gdf.groupby('NM_MUN')['RpC_2010'].transform(
        lambda x: pd.qcut(x, 5, labels=[1, 2, 3, 4, 5]) 
        if x.notna().sum() >= 5 else pd.Series([None] * len(x))
    )

    # Converte para inteiro (tratando valores nulos)
    gdf['Quintil'] = pd.to_numeric(gdf['Quintil'], errors='coerce').astype('Int64')

    # -------------------------------------------------------------------------
    # Etapa 4: Filtragem dos extratos Q1 e Q5
    # -------------------------------------------------------------------------
    print("🔹 Filtrando os setores dos quintis extremos...")
    gdf_inferior = gdf[gdf['Quintil'] == 1]
    gdf_superior = gdf[gdf['Quintil'] == 5]

    print(f"Feições no quintil inferior (Q1): {len(gdf_inferior)}")
    print(f"Feições no quintil superior (Q5): {len(gdf_superior)}")

    # -------------------------------------------------------------------------
    # Etapa 5: Exportação dos resultados
    # -------------------------------------------------------------------------
    os.makedirs(os.path.dirname(output_inferior), exist_ok=True)
    os.makedirs(os.path.dirname(output_superior), exist_ok=True)

    print("💾 Salvando shapefiles resultantes...")
    gdf_inferior.to_file(output_inferior)
    gdf_superior.to_file(output_superior)

    print("✅ Shapefiles salvos com sucesso:")
    print(f"   → Quintil inferior (Q1): {output_inferior}")
    print(f"   → Quintil superior (Q5): {output_superior}")


# =============================================================================
# ▶️ Execução direta do script
# =============================================================================
if __name__ == "__main__":
    # Caminho de entrada (produto do Script 03)
    input_shp = r"C:\\path\\to\\data\\Cidades_Medias_Variaveis.shp"

    # Caminhos de saída (ajustar conforme organização local)
    output_inferior = r"C:\\path\\to\\outputs\\03_mapping\\quintil_inferior.shp"
    output_superior = r"C:\\path\\to\\outputs\\03_mapping\\quintil_superior.shp"

    # Executar processo
    select_quintiles(input_shp, output_inferior, output_superior)