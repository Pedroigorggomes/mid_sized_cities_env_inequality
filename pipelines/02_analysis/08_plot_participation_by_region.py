# scripts/08_plot_participation_by_region.py

import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# >>>>>> PREENCHA AQUI <<<<<<
# Shapefile de entrada: produto do script 03 (Cidades_Medias_Variaveis.shp)
INPUT_SHP = r"inputs/Cidades_Medias_Variaveis.shp"

# Pasta de saída (um PNG por região)
OUTPUT_DIR = r"outputs/05_participation_region"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<

def analyze_and_plot_discrepancies_by_region(df, region, save_path):
    """
    Plota um gráfico de barras com a PARTICIPAÇÃO (%) de cada raça em cada quintil (Q1–Q5)
    dentro da REGIÃO informada. Para cada raça, soma-se a população por quintil e divide-se
    pelo total regional daquela raça, multiplicando por 100.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Colunas de raça
    races = ['Brancos', 'Pretos', 'Amarelos', 'Pardos', 'Indigena']
    race_names = {
        'Brancos': 'Brancos',
        'Pretos': 'Pretos',
        'Amarelos': 'Amarelos',
        'Pardos': 'Pardos',
        'Indigena': 'Indígenas'
    }
    color_map = {
        'Brancos': '#187E94',
        'Pretos': '#605821',
        'Amarelos': '#BBB134',
        'Pardos': '#0a2329',
        'Indigena': '#3F8D73'
    }
    
    # Assume-se que os quintis já foram calculados (coluna 'Quintil')
    quintiles = range(1, 6)
    x_labels = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    x = np.arange(len(x_labels))
    width = 0.15  # Largura das barras

    # Seleciona os dados da região e totais regionais por raça
    regional_data = df[df['Region'] == region]
    total_population_by_race = regional_data[races].sum()

    for i, race in enumerate(races):
        race_total = total_population_by_race[race]
        percentages = []
        for quintil in quintiles:
            quintil_population = regional_data[regional_data['Quintil'] == quintil][race].sum()
            if race_total > 0:
                percentage = (quintil_population / race_total) * 100
            else:
                percentage = 0
            percentages.append(percentage)
        ax.bar(x - width*2 + i*width, percentages, width, label=race_names[race], color=color_map[race])
    
    ax.set_xlabel('Quintil de Renda', fontsize=12)
    ax.set_ylabel('Participação por Raça (%)', fontsize=12)
    ax.set_title(f'Participação das Raças por Quintil de Renda - Região {region}', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    filename = f"{region}_participacao_raca.png"
    output_file = os.path.join(save_path, filename)
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Gráfico salvo: {output_file}")

def main():
    # Carregar dados do shapefile (produto do script 03)
    data = gpd.read_file(INPUT_SHP)
    print("Total de registros lidos:", len(data))

    # Converter a coluna de renda para numérico (RpC_2010)
    data['RpC_2010'] = pd.to_numeric(data['RpC_2010'], errors='coerce')

    # Calcular os quintis de RpC_2010 por município (NM_MUN)
    data['Quintil'] = data.groupby('NM_MUN')['RpC_2010'].transform(
        lambda x: pd.qcut(x, 5, labels=[1, 2, 3, 4, 5])
    )

    # Definir a região a partir da coluna NM_REGIAO
    data['Region'] = data['NM_REGIAO']

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Gerar e salvar os gráficos para cada região
    for region in data['Region'].unique():
        if region:
            regional_data = data[data['Region'] == region]
            analyze_and_plot_discrepancies_by_region(regional_data, region, OUTPUT_DIR)

if __name__ == "__main__":
    main()
