#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gera 'Setores_Indicadores_Censo_22.shp' a partir de:
- Shapefile de setores censitários 2022 (BR inteiro)
- Excel agregados do IBGE (varridos em subpastas), usando apenas:
    * caracteristicas_domicilio2 (água, esgoto, lixo)
    * cor_ou_raca (percentuais por raça/cor)
Fluxo:
  1) Lê o SHP de setores 2022 e garante CD_SETOR como string
  2) Varre input-excel-dir (recursivo), lê XLSX/XLS, trata CD_setor e 'X'
  3) Calcula:
       - P_Agua  = V00111 / V0007 * 100
       - P_Esgo  = (V00309 + V00310) / V0007 * 100  (fallback: só V00309 se V00310 ausente)
       - P_Lixo  = V00397 / V0007 * 100
       - P_Branca  = V01317 / V0001 * 100
         P_Preta   = V01318 / V0001 * 100
         P_Amarela = V01319 / V0001 * 100
         P_Parda   = V01320 / V0001 * 100
         P_Indigena= V01321 / V0001 * 100
  4) Faz merge por CD_SETOR e salva:
       - (opcional) intermediários: *_indice_calculado.shp
       - final: Setores_Indicadores_Censo_22.shp
"""

import argparse
from pathlib import Path
import os
import re
import numpy as np
import pandas as pd
import geopandas as gpd

VALID_EXT = (".xlsx", ".xls")


def find_col(df_or_gdf, candidates, required=True):
    """Procura coluna (case-insensitive) em DataFrame/GeoDataFrame."""
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
    Converte valores de CD_setor (inclusive notação científica) para string de dígitos.
    Ex.: '1,10002E+14' -> '110002000000000'
    """
    s = str(val).strip().replace(",", "")
    # já é inteiro longo?
    if re.fullmatch(r"\d+", s):
        return s
    try:
        f = float(s)
        return f"{f:.0f}"
    except Exception:
        return s  # devolve como veio se não der pra converter


def read_and_clean_excels(input_excel_dir):
    """
    Lê todos XLSX/XLS recursivamente.
    - Garante CD_setor como texto normalizado
    - Substitui 'X' por NaN e converte numéricos
    Retorna um dicionário {basename_lower: DataFrame}
    """
    out = {}
    for root, _, files in os.walk(input_excel_dir):
        for file in files:
            if not file.lower().endswith(VALID_EXT):
                continue
            path = os.path.join(root, file)
            try:
                df = pd.read_excel(path)
            except Exception as e:
                print(f"[!] Erro lendo {path}: {e}")
                continue

            # CD_setor como string normalizada
            if "CD_setor" in df.columns:
                df["CD_setor"] = df["CD_setor"].apply(format_cd_setor).astype(str)

            # troca 'X' por NA e tenta numerificar as demais colunas
            for col in df.columns:
                if col == "CD_setor":
                    continue
                df[col] = df[col].replace("X", pd.NA)
                df[col] = pd.to_numeric(df[col], errors="coerce")

            base = os.path.splitext(file)[0].lower()
            out[base] = df
            print(f"✔ Excel lido: {path}  (linhas={len(df)})")
    return out


def compute_domicile_indicators(df):
    """
    A partir de um DF de 'caracteristicas_domicilio2', cria P_Agua, P_Esgo, P_Lixo.
    Usa denominador V0007.
    Fallback: se V00310 não existir, usa só V00309 para esgoto.
    """
    v0007 = find_col(df, ["V0007", "v0007"])
    v00111 = find_col(df, ["V00111", "v00111"])
    v00309 = find_col(df, ["V00309", "v00309"])
    v00310 = find_col(df, ["V00310", "v00310"], required=False)
    v00397 = find_col(df, ["V00397", "v00397"])

    den = df[v0007].fillna(0)
    df["P_Agua"] = np.where(den > 0, (df[v00111].fillna(0) / den) * 100, 0)

    if v00310 and v00310 in df.columns:
        esg = df[v00309].fillna(0) + df[v00310].fillna(0)
    else:
        esg = df[v00309].fillna(0)
    df["P_Esgo"] = np.where(den > 0, (esg / den) * 100, 0)

    df["P_Lixo"] = np.where(den > 0, (df[v00397].fillna(0) / den) * 100, 0)
    return df[["CD_setor", "P_Agua", "P_Esgo", "P_Lixo"]].copy()


def compute_race_indicators(df):
    """
    A partir de um DF de 'cor_ou_raca', cria percentuais P_Branca, P_Preta, etc., usando V0001.
    """
    v0001 = find_col(df, ["V0001", "v0001"])
    cols_map = {
        "V01317": "P_Branca",
        "V01318": "P_Preta",
        "V01319": "P_Amarela",
        "V01320": "P_Parda",
        "V01321": "P_Indigena",
    }
    den = df[v0001].fillna(0)

    out = {"CD_setor": df["CD_setor"].astype(str)}
    for num_col, out_col in cols_map.items():
        src = find_col(df, [num_col, num_col.lower()], required=False)
        if src and src in df.columns:
            out[out_col] = np.where(den > 0, (df[src].fillna(0) / den) * 100, 0.0)
        else:
            out[out_col] = 0.0
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser(
        description="Gera Setores_Indicadores_Censo_22.shp a partir de Excel agregados (domicílio e raça/cor)."
    )
    ap.add_argument("--input-excel-dir", required=True, help="Pasta-raiz dos Excel agregados (varre subpastas).")
    ap.add_argument("--sectors-shp", required=True, help="Shapefile de setores 2022 (Brasil inteiro).")
    ap.add_argument("--out-dir", required=True, help="Pasta de saída dos arquivos gerados.")
    ap.add_argument("--emit-intermediate", action="store_true",
                    help="Se definido, salva shapefiles intermediários *_indice_calculado.shp.")
    args = ap.parse_args()

    input_excel_dir = Path(args.input_excel_dir)
    sectors_shp = Path(args.sectors_shp)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    # Arquivos de saída
    FINAL_SHP = out_dir / "Setores_Indicadores_Censo_22.shp"
    DOM_INTER = out_dir / "Agregados_por_setores_caracteristicas_domicilio2_BR_indice_calculado.shp"
    RACA_INTER = out_dir / "Agregados_por_setores_cor_ou_raca_BR_indice_calculado.shp"

    # 1) Carrega shapefile base
    print(f"🔄 Lendo shapefile base: {sectors_shp}")
    gdf = gpd.read_file(sectors_shp)
    # padroniza ID
    cd_setor_g = find_col(gdf, ["CD_SETOR", "CDSETOR", "CD_SETOR_2022"])
    gdf[cd_setor_g] = gdf[cd_setor_g].apply(format_cd_setor).astype(str)
    print(f"✅ Setores: {len(gdf)} linhas")

    # 2) Lê excéis
    print(f"\n📁 Lendo Excel agregados em: {input_excel_dir} (varredura recursiva)")
    excels = read_and_clean_excels(str(input_excel_dir))

    # 3) Localiza os dois conjuntos de interesse (por padrão, usa 'contains' no nome)
    #    - caracteristicas_domicilio2
    #    - cor_ou_raca
    def pick_df(excels_dict, key_substr):
        for k, df in excels_dict.items():
            if key_substr in k:
                return df
        return None

    df_dom = pick_df(excels, "caracteristicas_domicilio2")
    df_rac = pick_df(excels, "cor_ou_raca")

    if df_dom is None:
        raise SystemExit("Não encontrei arquivo de 'caracteristicas_domicilio2' nas subpastas.")
    if df_rac is None:
        raise SystemExit("Não encontrei arquivo de 'cor_ou_raca' nas subpastas.")

    # 4) Calcula indicadores
    print("\n🧮 Calculando indicadores de domicílio (P_Agua, P_Esgo, P_Lixo)…")
    dom_idx = compute_domicile_indicators(df_dom)

    print("🧮 Calculando indicadores de raça/cor (% por raça)…")
    rac_idx = compute_race_indicators(df_rac)

    # 5) Merges por CD_SETOR
    print("\n🔗 Integrando ao shapefile por CD_SETOR…")
    gdf = gdf.merge(dom_idx, left_on=cd_setor_g, right_on="CD_setor", how="left")
    gdf.drop(columns=["CD_setor"], inplace=True)

    gdf = gdf.merge(rac_idx, left_on=cd_setor_g, right_on="CD_setor", how="left")
    gdf.drop(columns=["CD_setor"], inplace=True)

    # 6) (opcional) intermediários
    if args.emit_intermediate:
        # Precisamos de geometria para salvar como SHP
        # DOM
        dom_geo = gdf[[cd_setor_g, "geometry", "P_Agua", "P_Esgo", "P_Lixo"]].copy()
        dom_geo = gpd.GeoDataFrame(dom_geo, geometry="geometry", crs=gdf.crs)
        dom_geo.to_file(DOM_INTER)
        print(f"💾 Intermediário (domicílio): {DOM_INTER}")

        # RAÇA
        rac_cols = [cd_setor_g, "geometry", "P_Branca", "P_Preta", "P_Amarela", "P_Parda", "P_Indigena"]
        rac_geo = gdf[rac_cols].copy()
        rac_geo = gpd.GeoDataFrame(rac_geo, geometry="geometry", crs=gdf.crs)
        rac_geo.to_file(RACA_INTER)
        print(f"💾 Intermediário (raça): {RACA_INTER}")

    # 7) Salva final
    gdf.to_file(FINAL_SHP)
    print(f"\n🎯 Arquivo final salvo: {FINAL_SHP}")
    print("✅ Concluído.")


if __name__ == "__main__":
    main()
