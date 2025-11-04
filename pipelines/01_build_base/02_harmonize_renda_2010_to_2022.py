#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
02) Harmoniza RpC (renda per capita) de 2010 para os setores 2022 por ponderação de área.
- Entrada A: Setores 2022 com indicadores (saída do Script 01) -> Setores_Indicadores_Censo_22.shp
- Entrada B: Setores 2010 com a coluna RpC (ou nome similar)
- Saída   : Setores_raca_renda.shp  (mesma malha 2022, acrescida da coluna 'RpC_2010')

Notas:
- Ponderação de área é feita em CRS de área equivalente (Brazil Albers).
- Não usa RpC_25 (foi removido).
- Merge final é por ID (CD_SETOR), preservando geometria/CRS original do arquivo 2022.
"""

import argparse
from pathlib import Path
import re

import geopandas as gpd
import pandas as pd
import numpy as np

ALBERS_BR = "+proj=aea +lat_1=-5 +lat_2=-42 +lat_0=-25 +lon_0=-55 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"


def find_col(df_or_gdf, candidates, required=True):
    """Procura coluna (case-insensitive)."""
    cols = {c.lower(): c for c in df_or_gdf.columns}
    for cand in candidates:
        c = cols.get(cand.lower())
        if c is not None:
            return c
    if required:
        raise ValueError(f"Coluna não encontrada. Procurei: {candidates}")
    return None


def format_cd_setor(val):
    """
    Normaliza CD_SETOR para string de dígitos (remove notação científica).
    Ex.: '1,10002E+14' -> '110002000000000'
    """
    s = str(val).strip().replace(",", "")
    if re.fullmatch(r"\d+", s):
        return s
    try:
        return f"{float(s):.0f}"
    except Exception:
        return s


def fix_geoms(gdf):
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.apply(
        lambda geom: geom.buffer(0) if (geom is not None and not geom.is_valid) else geom
    )
    return gdf


def main():
    ap = argparse.ArgumentParser(
        description="Harmoniza RpC (2010) para a malha de setores 2022 por ponderação de área (Brazil Albers)."
    )
    ap.add_argument("--in-2022", required=True,
                    help="Shapefile 2022 com indicadores (saída do Script 01): Setores_Indicadores_Censo_22.shp")
    ap.add_argument("--in-2010", required=True,
                    help="Shapefile 2010 com a coluna de RpC (ex.: Pessoa_Renda_Resultado.shp)")
    ap.add_argument("--rpc-col", default="RpC",
                    help="Nome da coluna de renda per capita no arquivo de 2010 (default: RpC)")
    ap.add_argument("--out", required=True,
                    help="Caminho de saída (ex.: .../Setores_raca_renda.shp)")
    args = ap.parse_args()

    p2022 = Path(args.in_2022)
    p2010 = Path(args.in_2010)
    pout  = Path(args.out)

    # 1) Ler arquivos
    print(f"🔄 Lendo 2022: {p2022}")
    c22 = gpd.read_file(p2022)
    print(f"   Linhas 2022: {len(c22)}")

    print(f"🔄 Lendo 2010: {p2010}")
    c10 = gpd.read_file(p2010)
    print(f"   Linhas 2010: {len(c10)}")

    # 2) IDs e coluna RpC
    id22 = find_col(c22, ["CD_SETOR", "CDSETOR", "CD_SETOR_2022"])
    c22[id22] = c22[id22].apply(format_cd_setor).astype(str)
    c22["id_setor"] = c22[id22]  # chave estável

    rpc10 = find_col(c10, [args.rpc_col, args.rpc_col.lower()], required=True)

    # 3) Guardar CRS original de 2022 para a escrita final
    crs_out = c22.crs

    # 4) Reprojetar para CRS de área equivalente + corrigir geometrias
    print("📐 Reprojetando para Brazil Albers (área equivalente) e corrigindo geometrias…")
    c22_a = fix_geoms(c22.to_crs(ALBERS_BR))
    c10_a = fix_geoms(c10.to_crs(ALBERS_BR))

    # 5) Área original 2010
    c10_a["area_2010"] = c10_a.geometry.area

    # 6) Interseção 22×10 (mantém atributos de ambos)
    print("🔀 Calculando overlay (intersection) 2022×2010…")
    inter = gpd.overlay(
        c22_a[["id_setor", "geometry"]],
        c10_a[[rpc10, "area_2010", "geometry"]],
        how="intersection"
    )
    if inter.empty:
        raise SystemExit("Overlay vazio — verifique se as malhas se sobrepõem e se os CRS estão corretos.")

    # 7) Proporção de área e ponderação de RpC
    inter["area_intersec"] = inter.geometry.area
    # evita divisão por zero
    inter = inter[inter["area_2010"] > 0].copy()
    inter["prop"] = inter["area_intersec"] / inter["area_2010"]
    inter["RpC_w"] = inter["prop"] * inter[rpc10]

    # 8) Agregar por setor 2022
    print("🧮 Agregando RpC ponderada por id_setor (2022)…")
    agg = inter.groupby("id_setor", as_index=True)["RpC_w"].sum().rename("RpC_2010")

    # 9) Mesclar ao 2022 (no CRS original)
    print("🔗 Mesclando RpC_2010 de volta ao 2022 (CRS original)…")
    c22_out = c22.copy()
    c22_out = c22_out.merge(agg.to_frame(), left_on="id_setor", right_index=True, how="left")
    c22_out = c22_out.set_crs(crs_out)

    # 10) Salvar
    pout.parent.mkdir(parents=True, exist_ok=True)
    c22_out.to_file(pout)
    print(f"✅ Salvo: {pout}  | linhas={len(c22_out)}")
    print("🎯 Coluna adicionada: 'RpC_2010' (renda per capita de 2010 harmonizada para setores 2022).")


if __name__ == "__main__":
    main()
