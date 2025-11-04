"""
Script: 10_plot_income_maps_grouped_by_region.py
Autor: Pedro Igor Galvão Gomes
Instituição: Universidade Federal do Tocantins (UFT)
Ano: 2025
Licença: CC BY 4.0

Descrição:
-----------
Gera mapas comparativos dos quintis extremos de renda (Q1 e Q5) nas 92 cidades médias brasileiras,
destacando espacialmente as áreas de menor e maior renda per capita em cada município.

O script utiliza as saídas do script anterior (09_select_quintiles_q1_q5.py),
produzindo painéis de 6 municípios por figura, agrupados por macrorregião.

Entradas:
---------
- `Cidades_Medias_Variaveis.shp` → shapefile base com variáveis integradas.
- `quintil_inferior.shp` → setores do 1º quintil (Q1).
- `quintil_superior.shp` → setores do 5º quintil (Q5).
- `ne_10m_ocean.shp` → camada auxiliar (oceanos).
- `geoft_bho_massa_dagua_v2019.shp` → camada auxiliar (massas d’água).

Saídas:
--------
- Painéis regionais (PNG, 300 dpi), agrupando até 6 municípios por figura:
  `outputs/03_mapping/{REGIAO}/{REGIAO}_municipios_01_agrupados.png`
"""

# =============================================================================
# 📦 Importação de bibliotecas
# =============================================================================
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
from shapely.ops import unary_union

# =============================================================================
# 🧩 Função 1 – Determinar a principal massa urbana do município
# =============================================================================
def determine_main_urban_area(municipality_data, buffer_km=1):
    """
    Determina os limites da massa urbana conectada de um município.

    Procedimento:
    -------------
    1. Reprojeta para CRS métrico (EPSG:3857);
    2. Aplica buffer de 'buffer_km' em km;
    3. Cria grafo de conectividade entre setores (arestas = intersecção dos buffers);
    4. Calcula a área de cada componente urbano;
    5. Seleciona o maior (ou une o 2º se distante ≤ buffer_km);
    6. Retorna o bounding box da área unificada em EPSG:4326.
    """
    if municipality_data.empty:
        return None

    # Reprojeção para CRS métrico
    metric_data = municipality_data.to_crs(epsg=3857).reset_index(drop=True)
    buffered = metric_data.geometry.buffer(buffer_km * 1000)

    # Construção do grafo de conectividade
    G = nx.Graph()
    for idx, geom in buffered.items():
        G.add_node(idx)
    for idx, geom in buffered.items():
        possible = list(buffered.sindex.intersection(geom.bounds))
        for j in possible:
            if idx != j and geom.intersects(buffered.loc[j]):
                G.add_edge(idx, j)

    components = list(nx.connected_components(G))
    if not components:
        return None

    # União e área dos componentes
    comp_area, comp_geom = {}, {}
    for comp in components:
        union_geom = unary_union(metric_data.loc[list(comp)].geometry)
        comp_geom[frozenset(comp)] = union_geom
        comp_area[frozenset(comp)] = union_geom.area

    # Selecionar o maior componente
    sorted_comps = sorted(comp_area.items(), key=lambda x: x[1], reverse=True)
    comp1 = sorted_comps[0][0]
    union1 = comp_geom[comp1]

    # Verificar se há segundo componente a ≤ 1 km
    if len(sorted_comps) > 1:
        comp2 = sorted_comps[1][0]
        union2 = comp_geom[comp2]
        distance = union1.distance(union2)
        final_union = unary_union([union1, union2]) if distance <= buffer_km * 1000 else union1
    else:
        final_union = union1

    # Retornar bounding box reprojetado
    final_union_gs = gpd.GeoSeries([final_union], crs=metric_data.crs).to_crs(epsg=4326).iloc[0]
    return final_union_gs.bounds


# =============================================================================
# 🗺️ Função 2 – Geração dos mapas regionais (Q1 × Q5)
# =============================================================================
def plot_income_maps_grouped_by_region_unified(base_shp, upper_quintil_shp, lower_quintil_shp, ocean_shp, water_bodies_shp, save_path):
    """
    Cria mapas comparativos entre o quintil inferior (Q1) e superior (Q5)
    de renda per capita, agrupados por macrorregião e até 6 municípios por painel.
    """
    os.makedirs(save_path, exist_ok=True)

    # Paleta de cores
    quintil_superior_color = '#156E7A'  # verde petróleo (Q5)
    quintil_inferior_color = '#EF7C80'  # vermelho (Q1)
    ocean_color = '#4e76b7'
    water_body_color = '#4cc4d9'

    # Carregar camadas
    base_data = gpd.read_file(base_shp)
    upper_quintil = gpd.read_file(upper_quintil_shp)
    lower_quintil = gpd.read_file(lower_quintil_shp)
    ocean_data = gpd.read_file(ocean_shp)
    water_bodies = gpd.read_file(water_bodies_shp)

    # Reprojeção para WGS84
    for layer in [base_data, upper_quintil, lower_quintil, ocean_data, water_bodies]:
        layer.to_crs(epsg=4326, inplace=True)

    base_data['Region'] = base_data['NM_REGIAO']
    upper_quintil['Region'] = upper_quintil['NM_REGIAO']
    lower_quintil['Region'] = lower_quintil['NM_REGIAO']

    base_data['RpC_2010'] = pd.to_numeric(base_data['RpC_2010'], errors='coerce')

    # Processar por região
    regions = base_data['Region'].dropna().unique()
    for region in regions:
        region_path = os.path.join(save_path, region)
        os.makedirs(region_path, exist_ok=True)

        region_data = base_data[base_data['Region'] == region]
        upper_region = upper_quintil[upper_quintil['Region'] == region]
        lower_region = lower_quintil[lower_quintil['Region'] == region]

        municipalities = sorted(region_data['NM_MUN'].unique())
        municipality_ids = {m: f"{i+1:02d}" for i, m in enumerate(municipalities)}

        # Agrupar 6 municípios por figura
        for i in range(0, len(municipalities), 6):
            grouped = municipalities[i:i + 6]
            fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))
            fig.suptitle(f"Região {region} - Municípios Agrupados", fontsize=26, fontweight='bold')
            axes = axes.ravel()

            for j, municipality in enumerate(grouped):
                municipality_data = region_data[region_data['NM_MUN'] == municipality]
                upper_data = upper_region[upper_region['NM_MUN'] == municipality]
                lower_data = lower_region[lower_region['NM_MUN'] == municipality]
                uf = municipality_data['NM_UF'].iloc[0] if 'NM_UF' in municipality_data.columns else ''

                urban_bounds = determine_main_urban_area(municipality_data, buffer_km=1)
                if urban_bounds:
                    xlim = [urban_bounds[0], urban_bounds[2]]
                    ylim = [urban_bounds[1], urban_bounds[3]]
                    municipality_id = municipality_ids[municipality]

                    # Plotagem
                    ocean_data.plot(color=ocean_color, ax=axes[j])
                    water_bodies.plot(color=water_body_color, ax=axes[j])
                    municipality_data.plot(color='#D6E6F2', linewidth=0.1, edgecolor='gray', ax=axes[j])
                    lower_data.plot(color=quintil_inferior_color, linewidth=0.1, edgecolor='gray', ax=axes[j])
                    upper_data.plot(color=quintil_superior_color, linewidth=0.1, edgecolor='gray', ax=axes[j])

                    axes[j].set_title(f"({municipality_id}) {municipality} - {uf}", fontsize=15, fontweight='bold')
                    axes[j].set_xlim(xlim)
                    axes[j].set_ylim(ylim)
                    axes[j].axis("off")

            # Ocultar subplots vazios
            for k in range(len(grouped), len(axes)):
                axes[k].set_visible(False)

            filename = os.path.join(region_path, f"{region}_municipios_{(i // 6) + 1}_agrupados.png")
            plt.tight_layout()
            plt.subplots_adjust(top=0.92)
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"🗺️ Mapa salvo: {filename}")


# =============================================================================
# ▶️ Execução direta
# =============================================================================
if __name__ == "__main__":
    # Caminhos de entrada (ajustar conforme diretório local)
    base_shp = r"C:\\path\\to\\data\\Cidades_Medias_Variaveis.shp"
    upper_quintil_shp = r"C:\\path\\to\\outputs\\03_mapping\\quintil_superior.shp"
    lower_quintil_shp = r"C:\\path\\to\\outputs\\03_mapping\\quintil_inferior.shp"
    ocean_shp = r"C:\\path\\to\\data\\auxiliary\\ne_10m_ocean.shp"
    water_bodies_shp = r"C:\\path\\to\\data\\auxiliary\\geoft_bho_massa_dagua_v2019.shp"

    # Diretório de saída
    save_path = r"C:\\path\\to\\outputs\\03_mapping\\maps"

    # Executar função
    plot_income_maps_grouped_by_region_unified(
        base_shp, upper_quintil_shp, lower_quintil_shp,
        ocean_shp, water_bodies_shp, save_path
    )