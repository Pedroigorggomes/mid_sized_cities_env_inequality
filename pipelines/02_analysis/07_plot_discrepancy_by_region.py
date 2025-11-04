# scripts/07_plot_discrepancy_by_region.py

import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# >>>>>> PREENCHA AQUI <<<<<<
# Shapefile de entrada: produto do script 03 (Cidades_Medias_Variaveis.shp)
INPUT_SHP = r"inputs/Cidades_Medias_Variaveis.shp"

# Pasta de saída (um PNG por região)
OUTPUT_DIR = r"outputs/04_discrepancy_region"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<

def plot_regional_discrepancy_data(df, region, save_path):
    """
    Plota, para cada quintil de renda, a discrepância entre a população observada
    (soma, em valores absolutos, da raça no quintil) e a população esperada
    (total regional da raça / 5).
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
        'Pretos': '#0a2329',
        'Amarelos': '#BBB134',
        'Pardos': '#605821',
        'Indigena': '#3F8D73'
    }
    
    quintiles = range(1, 6)
    x_labels = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    x = np.arange(len(x_labels))
    width = 0.15  # Largura das barras

    # Para cada raça, calcular a discrepância (observado - esperado) por quintil.
    # O esperado é o total da raça na região dividido por 5.
    for i, race in enumerate(races):
        discrepancies = []
        for quintil in quintiles:
            regional_data_q = df[(df['Region'] == region) & (df['Quintil'] == quintil)]
            observed_population = regional_data_q[race].sum()
            expected_population = df[df['Region'] == region][race].sum() / 5
            discrepancy = observed_population - expected_population
            discrepancies.append(discrepancy)
        
        # Barras por raça
        ax.bar(x - width*2 + i*width, discrepancies, width, label=race_names[race], color=color_map[race])
    
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Quintil de Renda', fontsize=12)
    ax.set_ylabel('Diferença Populacional (Observado - Esperado)', fontsize=12)
    ax.set_title(f'Discrepâncias Populacionais por Raça em cada Quintil de Renda - Região {region}', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    filename = f"{region}_regional_population_discrepancy.png"
    output_file = os.path.join(save_path, filename)
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Gráfico salvo: {output_file}")

def main():
    # Carregar dados
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
            plot_regional_discrepancy_data(regional_data, region, OUTPUT_DIR)

if __name__ == "__main__":
    main()
