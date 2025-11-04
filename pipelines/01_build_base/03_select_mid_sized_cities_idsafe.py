#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import geopandas as gpd
import pandas as pd
import networkx as nx
from libpysal.weights import Queen

def find_col(gdf, candidates, required=True):
    m = {c.lower(): c for c in gdf.columns}
    for cand in candidates:
        if cand.lower() in m:
            return m[cand.lower()]
    if required:
        raise ValueError(f"Coluna não encontrada. Procurei: {candidates}")
    return None

def fix_geoms(gdf):
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.apply(
        lambda geom: geom.buffer(0) if (geom is not None and not geom.is_valid) else geom
    )
    return gdf

def main():
    ap = argparse.ArgumentParser(
        description="Seleciona cidades médias (100–500k) por contiguidade (Queen) e filtra setores por CD_SETOR."
    )
    ap.add_argument("--in-2022", required=True, help="Setores 2022 (Brasil inteiro) JÁ com variáveis calculadasa partir de 02_harmonize_renda_2010_to_2022")
    ap.add_argument("--out-dir", required=True, help="Pasta de saída.")
    args = ap.parse_args()

    IN = Path(args.in_2022)
    OUT = Path(args.out_dir); OUT.mkdir(parents=True, exist_ok=True)

    areas_urbanas = OUT / "Areas_Urbanas_Com_Variaveis.shp"
    manchas_muns  = OUT / "Manchas_Urbanas_Populacao_Total_Raca.shp"
    manchas_ok    = OUT / "Cidades_Medias_100_500_mil_SEM_Conurbacoes.shp"
    comps_ok      = OUT / "Cidades_Medias_Componentes.shp"
    lista_csv     = OUT / "Cidades_Medias_Lista.csv"
    ids_csv       = OUT / "Cidades_Medias_CD_SETOR.csv"
    setores_final = OUT / "Cidades_Medias_Variaveis.shp"

    gdf = gpd.read_file(IN)
    gdf = fix_geoms(gdf)

    mun_col  = find_col(gdf, ["NM_MUN","NM_MUNICIP","NM_MUNICIPIO"])
    uf_col   = find_col(gdf, ["NM_UF","UF","SIGLA_UF"])
    pop_col0 = find_col(gdf, ["PR","V0001","v0001"])
    id_col   = find_col(gdf, ["CD_SETOR","CDSETOR","CD_SETOR_2022"])
    cd_situ  = find_col(gdf, ["CD_SITU","CD_SIT"], required=False)

    # 1) Filtra urbano
    if cd_situ:
        urban = gdf[gdf[cd_situ].astype(str).isin(["1","2",1,2])].copy()
    else:
        situ = find_col(gdf, ["SITUACAO"])
        urban = gdf[gdf[situ].astype(str).str.lower() == "urbana"].copy()
    urban = fix_geoms(urban)
    urban.to_file(areas_urbanas)

    # 2) Dissolve municipal (PR e raças se existirem)
    agg = {pop_col0: "sum"}
    for rc in ["Brancos","Pretos","Amarelos","Pardos","Indigena"]:
        if rc in urban.columns:
            agg[rc] = "sum"
    for meta in ["CD_UF","CD_MUN","NM_REGIAO"]:
        if meta in urban.columns:
            agg[meta] = "first"

    manchas = urban.dissolve(by=[mun_col, uf_col], aggfunc=agg).reset_index()
    if pop_col0 != "PR":
        manchas = manchas.rename(columns={pop_col0: "PR"})
    manchas = fix_geoms(manchas)
    manchas.to_file(manchas_muns)

    # 3) Contiguidade Queen + regras
    manchas = manchas.reset_index(drop=True)
    w = Queen.from_dataframe(manchas)
    G = w.to_networkx()
    components = list(nx.connected_components(G))

    comp_map = {}
    for comp_id, comp in enumerate(components):
        for idx in comp:
            comp_map[idx] = comp_id
    manchas["component"] = manchas.index.map(comp_map)

    comp_pop = manchas.groupby("component")["PR"].sum()
    comp_n   = manchas.groupby("component")["PR"].size()
    manchas["comp_pop"] = manchas["component"].map(comp_pop)
    manchas["comp_n"]   = manchas["component"].map(comp_n)

    keep_mask = (
        (manchas["comp_pop"] >= 100_000) &
        (manchas["comp_pop"] <= 500_000) &
        (manchas["PR"] >= 100_000)
    )
    selecionadas = manchas[keep_mask].copy()
    if len(selecionadas[selecionadas["PR"] < 100_000]) > 0:
        raise ValueError("Encontrada mancha <100k após o filtro.")

    selecionadas.to_file(manchas_ok)
    selecionadas.dissolve(by="component", aggfunc={"PR":"sum"}).to_file(comps_ok)
    selecionadas[[mun_col, uf_col, "PR", "comp_pop", "comp_n"]].sort_values([uf_col, mun_col]).to_csv(
        lista_csv, index=False, encoding="utf-8"
    )

    # 4) Seleção final por CD_SETOR (sem geom)
    pairs = set(selecionadas[[mun_col, uf_col]].apply(lambda r: (r[mun_col], r[uf_col]), axis=1))
    urban_sel = urban[urban[[mun_col, uf_col]].apply(lambda r: (r[mun_col], r[uf_col]) in pairs, axis=1)].copy()

    ids_ok = urban_sel[[id_col]].drop_duplicates().sort_values(id_col)
    ids_ok.to_csv(ids_csv, index=False, encoding="utf-8")

    setores_finais = gdf[gdf[id_col].isin(set(ids_ok[id_col]))].copy()
    # reforça urbano 1/2
    if cd_situ:
        setores_finais = setores_finais[setores_finais[cd_situ].astype(str).isin(["1","2",1,2])].copy()
    setores_finais.to_file(setores_final)

    print("✅ Concluído.")
    print(f"  - Manchas finais: {manchas_ok}")
    print(f"  - Lista municípios: {lista_csv}")
    print(f"  - IDs CD_SETOR: {ids_csv}")
    print(f"  - Setores finais: {setores_final}")

if __name__ == "__main__":
    main()
