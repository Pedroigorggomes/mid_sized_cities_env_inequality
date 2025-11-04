# scripts/06_plot_access_infrastructure_quintile.py

import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# >>>>>> PREENCHA AQUI <<<<<<
# Shapefile de entrada: produto do script 03 (Cidades_Medias_Variaveis.shp)
INPUT_SHP = r"inputs/Cidades_Medias_Variaveis.shp"

# Pasta de saída (um PNG por região)
OUTPUT_DIR = r"outputs/03_access_infra_quintile"
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Leitura do shapefile principal (contendo dados populacionais, de raça e de infraestrutura)
    data = gpd.read_file(INPUT_SHP)
    print("Total de registros lidos:", len(data))

    # Converter a coluna de renda para numérico
    data['RpC_2010'] = pd.to_numeric(data['RpC_2010'], errors='coerce')

    # Calcular os quintis de RpC_2010 por município (NM_MUN)
    data['Quintil'] = data.groupby('NM_MUN')['RpC_2010'].transform(
        lambda x: pd.qcut(x, 5, labels=[1, 2, 3, 4, 5])
    )
    print("Cálculo dos quintis concluído.")

    # Definir as raças e seus mapeamentos de cor e nomes
    races = ['Brancos', 'Pretos', 'Amarelos', 'Pardos', 'Indigena']
    color_map = {
        'Brancos': '#187E94',
        'Pretos': '#0a2329',
        'Amarelos': '#BBB134',
        'Pardos': '#605821',
        'Indigena': '#3F8D73'
    }
    race_names = {
        'Brancos': 'Brancos',
        'Pretos': 'Pretos',
        'Amarelos': 'Amarelos',
        'Pardos': 'Pardos',
        'Indigena': 'Indígenas'
    }

    # Definir colunas e rótulos para indicadores de infraestrutura
    infra_cols = ['P_Agua', 'P_Esgo', 'P_Lixo']
    infra_names = {
        'P_Agua': 'Acesso a Água',
        'P_Esgo': 'Acesso a Esgoto',
        'P_Lixo': 'Acesso a Coleta de Lixo'
    }
    infra_colors = {
        'P_Agua': '#1f77b4',
        'P_Esgo': '#ff7f0e',
        'P_Lixo': '#2ca02c'
    }

    # Obter as regiões disponíveis a partir da coluna NM_REGIAO
    regions = data['NM_REGIAO'].dropna().unique()
    print("Regiões encontradas:", regions)

    # Labels para os quintis
    quintiles = [1, 2, 3, 4, 5]
    x_labels = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']

    # Para cada região, agregamos os dados por quintil
    for region in regions:
        region_data = data[data['NM_REGIAO'] == region]
        
        # Lista para armazenar os dados agregados por quintil
        agg_list = []
        for q in quintiles:
            q_data = region_data[region_data['Quintil'] == q]
            
            # População total do quintil (usando v0001, se existir, senão soma dos registros)
            pop_res = q_data['v0001'].sum() if 'v0001' in q_data.columns else q_data[races].sum().sum()
            
            # Soma da população por raça (valores absolutos) e porcentagem dentro do quintil
            pop_dict = {f"pop_{race}": q_data[race].sum() for race in races}
            total_pop_raca = sum(pop_dict.values())
            perc_dict = {f"perc_{race}": (pop_dict[f"pop_{race}"] / total_pop_raca * 100) if total_pop_raca > 0 else 0 for race in races}
            
            # Cálculo de acesso às infraestruturas: para cada registro, considera-se v0001 * (P_infra / 100)
            infra_access_dict = {}
            for col in infra_cols:
                # População com acesso à infraestrutura
                pop_access = (q_data['v0001'] * (q_data[col] / 100)).sum() if 'v0001' in q_data.columns else 0
                pop_no_access = pop_res - pop_access
                infra_access_dict[f"pop_access_{col}"] = pop_access
                infra_access_dict[f"pop_no_access_{col}"] = pop_no_access
            
            agg_list.append({
                'Quintil': q,
                'total_pop': pop_res,
                **pop_dict,
                **perc_dict,
                **infra_access_dict
            })
        agg_df = pd.DataFrame(agg_list)
        
        # Criação da figura com 3 seções:
        # 1. Distribuição percentual da população por raça
        # 2. População total por raça
        # 3. População com e sem acesso às infraestruturas (valores absolutos)
        
        # Configurando a figura: 3 linhas (cada uma um conjunto de informações)
        fig, axes = plt.subplots(3, 1, figsize=(12, 20))
        
        ## Subplot 1: Percentual da população por raça por quintil
        ax1 = axes[0]
        for race in races:
            ax1.plot(x_labels, agg_df[f"perc_{race}"], label=race_names[race], marker='o', color=color_map[race])
            # Linha de referência: percentual global da raça na região
            global_total = region_data[races].sum().sum()
            global_perc = (region_data[race].sum() / global_total * 100) if global_total > 0 else 0
            ax1.axhline(y=global_perc, color=color_map[race], linestyle='--', linewidth=1)
        ax1.set_title(f'Distribuição Percentual da População por Quintil e Raça - Região {region}', fontsize=16)
        ax1.set_ylabel('Porcentagem (%)', fontsize=14)
        ax1.set_ylim(0, 100)
        ax1.tick_params(axis='both', labelsize=12)
        ax1.legend(fontsize=12)
        
        ## Subplot 2: População total por quintil para cada raça (valores absolutos)
        ax2 = axes[1]
        for race in races:
            ax2.plot(x_labels, agg_df[f"pop_{race}"], label=race_names[race], marker='o', color=color_map[race])
            # Linha de referência: distribuição uniforme (total da raça / 5)
            uniform_pop = region_data[race].sum() / 5
            ax2.axhline(y=uniform_pop, color=color_map[race], linestyle='--', linewidth=1)
        ax2.set_title(f'Distribuição da População Total por Quintil e Raça - Região {region}', fontsize=16)
        ax2.set_ylabel('População Total', fontsize=14)
        ax2.tick_params(axis='both', labelsize=12)
        ax2.legend(fontsize=12)
        
        ## Subplot 3: População com e sem acesso às infraestruturas por quintil
        ax3 = axes[2]
        for col in ['P_Agua', 'P_Esgo', 'P_Lixo']:
            # Linha para população com acesso
            ax3.plot(x_labels, agg_df[f"pop_access_{col}"], label=f"{infra_names[col]} (com acesso)", 
                     marker='o', color=infra_colors[col])
            # Linha para população sem acesso (linha tracejada)
            ax3.plot(x_labels, agg_df[f"pop_no_access_{col}"], label=f"{infra_names[col]} (sem acesso)", 
                     marker='o', linestyle='--', color=infra_colors[col])
        ax3.set_title(f'População com e sem Acesso às Infraestruturas por Quintil - Região {region}', fontsize=16)
        ax3.set_ylabel('População', fontsize=14)
        ax3.tick_params(axis='both', labelsize=12)
        ax3.legend(fontsize=12)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        filename = f"{region}_acesso_raca_quintil.png"
        output_file = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
        print(f"Gráfico salvo: {output_file}")

    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
