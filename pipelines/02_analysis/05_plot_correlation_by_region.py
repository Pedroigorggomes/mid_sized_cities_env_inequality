# scripts/05_plot_correlation_by_region.py

import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# >>>>>> PREENCHA AQUI <<<<<<
# Shapefile de entrada: produto do script 03 (Cidades_Medias_Variaveis.shp)
INPUT_SHP = r"inputs/Cidades_Medias_Variaveis.shp"

# Pasta de saída (um PNG por região)
OUTPUT_DIR = r"outputs/02_correlation_region"

def plot_correlations_by_region(df, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Colunas de raça com os novos nomes
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
    
    # Usar a coluna NM_REGIAO para definir a região
    df['Region'] = df['NM_REGIAO']
    
    # Converter as colunas de raça para porcentagem (por registro)
    total_population = df[races].sum(axis=1)
    df[races] = df[races].div(total_population, axis=0) * 100

    # Gerar gráficos para cada região
    for region in df['Region'].unique():
        if region:
            region_data = df[df['NM_REGIAO'] == region]
            
            # Configurar subplots: layout 2x3 (usando 5 subplots; último oculto)
            fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 10))
            axes = axes.ravel()
            
            for i, race in enumerate(races):
                axes[i].scatter(region_data['RpC_2010'], region_data[race], color=color_map[race], alpha=0.5)
                axes[i].set_title(f'Correlação: RpC_2010 x % {race_names[race]}', fontsize=14, pad=10)
                axes[i].set_xlabel('Renda Média Domiciliar Per Capita (RpC_2010)', fontsize=12)
                axes[i].set_ylabel(f'% {race_names[race]}', fontsize=12)
                axes[i].tick_params(axis='both', which='major', labelsize=10)
                
                correlation = region_data['RpC_2010'].corr(region_data[race])
                axes[i].text(0.95, 0.95, f'Pearson: {correlation:.2f}', transform=axes[i].transAxes,
                             horizontalalignment='right', verticalalignment='top', fontsize=12,
                             color='#3F8D73', fontweight='bold')
                
                # Linha de tendência: regressão linear
                data_fit = region_data[['RpC_2010', race]].dropna()
                if len(data_fit) > 1:
                    x = data_fit['RpC_2010']
                    y = data_fit[race]
                    coeffs = np.polyfit(x, y, 1)
                    poly = np.poly1d(coeffs)
                    x_vals = np.linspace(x.min(), x.max(), 100)
                    y_vals = poly(x_vals)
                    axes[i].plot(x_vals, y_vals, color='red', linewidth=2.5)
            
            # Ocultar o último subplot, se houver
            if len(races) < len(axes):
                axes[-1].set_visible(False)
            
            plt.suptitle(f'Correlação entre RpC_2010 e Percentual Racial - Região {region}', fontsize=16, y=0.98)
            # Salvar o gráfico diretamente na pasta de save_path com o nome incluindo a região
            filename = os.path.join(save_path, f"{region}_racial_correlation.png")
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.savefig(filename, bbox_inches='tight')
            plt.close()
            print(f"Gráfico salvo: {filename}")

if __name__ == "__main__":
    # Caminhos
    file_path = INPUT_SHP
    save_path = OUTPUT_DIR
    os.makedirs(save_path, exist_ok=True)

    # Ler dados
    data = gpd.read_file(file_path)
    print("Total de registros lidos:", len(data))

    # Converter a coluna de renda para numérico
    data['RpC_2010'] = pd.to_numeric(data['RpC_2010'], errors='coerce')

    # Plotar
    plot_correlations_by_region(data, save_path)
