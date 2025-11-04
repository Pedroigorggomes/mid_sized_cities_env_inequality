# scripts/04_plot_correlation_national.py

import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# >>>>>> PREENCHA AQUI <<<<<<
# Shapefile de entrada: produto do script 03 (Cidades_Medias_Variaveis.shp)
INPUT_SHP = r"inputs/Cidades_Medias_Variaveis.shp"

# Pasta de saída para o PNG gerado
OUTPUT_DIR = r"outputs/01_correlation_national"

def plot_correlations(df, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Atualizar as colunas de raça para os novos nomes
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
    
    # Converter os valores das raças para porcentagem (por registro)
    total_population = df[races].sum(axis=1)
    df[races] = df[races].div(total_population, axis=0) * 100

    # Configurar o layout: 2 linhas x 3 colunas (último subplot oculto, pois são 5 raças)
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 10))
    axes = axes.ravel()

    for i, race in enumerate(races):
        axes[i].scatter(df['RpC_2010'], df[race], color=color_map[race], alpha=0.5)
        axes[i].set_title(f'Correlação: RpC_2010 x % {race_names[race]}', fontsize=14, pad=10)
        axes[i].set_xlabel('Renda Média Domiciliar Per Capita (RpC_2010)', fontsize=12)
        axes[i].set_ylabel(f'% {race_names[race]}', fontsize=12)
        axes[i].tick_params(axis='both', which='major', labelsize=10)
        
        # Calcular a correlação de Pearson e exibi-la
        correlation = df['RpC_2010'].corr(df[race])
        axes[i].text(0.95, 0.95, f'Pearson: {correlation:.2f}', transform=axes[i].transAxes,
                     horizontalalignment='right', verticalalignment='top', fontsize=12,
                     color='#3F8D73', fontweight='bold')
        
        # Adicionar a linha de tendência (regressão linear)
        data_fit = df[['RpC_2010', race]].dropna()
        if len(data_fit) > 1:
            x = data_fit['RpC_2010']
            y = data_fit[race]
            coeffs = np.polyfit(x, y, 1)
            poly = np.poly1d(coeffs)
            x_vals = np.linspace(x.min(), x.max(), 100)
            y_vals = poly(x_vals)
            axes[i].plot(x_vals, y_vals, color='red', linewidth=2.5)
        
        # Garantir que o eixo Y comece em 0 e não ultrapasse 100
        y_min, y_max = axes[i].get_ylim()
        axes[i].set_ylim(bottom=0, top=min(y_max, 100))
    
    # Ocultar o último subplot
    axes[-1].set_visible(False)
    
    plt.suptitle('Correlação entre Renda e Percentual Racial - Brasil', fontsize=16, y=0.98)
    filename = "All_Races_Correlation.png"
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    output_file = os.path.join(save_path, filename)
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Gráfico salvo: {output_file}")

if __name__ == "__main__":
    # Caminhos
    file_path = INPUT_SHP
    save_path = OUTPUT_DIR
    os.makedirs(save_path, exist_ok=True)

    # Ler dados
    data = gpd.read_file(file_path)
    print("Total de registros lidos:", len(data))

    # RpC_2010 como numérico
    data['RpC_2010'] = pd.to_numeric(data['RpC_2010'], errors='coerce')

    # Plot
    plot_correlations(data, save_path)