"""DRAFT extractor: IPEA MIP -> 10-sector VA shares, gamma, alpha_c, Pi^I.

Verified end-to-end on MIP_2018_67_PCR.xlsx (2026-07-09): 126/126 products map,
VA and alpha_c shares each sum to 100%, Pi^I rows sum to 1 for consumed goods.
This is the seed of the future ogbra/input_output.py rewrite — see
CODE_ASSESSMENT.md for known caveats (mixed-income gamma treatment, zero
consumption rows for mining/construction, near-diagonal Pi^I at I=M).

Run:  python extract_10sectors_draft.py [YEAR]   (default 2018; needs pandas+openpyxl)
"""

import os
import sys
import pandas as pd
import numpy as np

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(HERE, "concordances"))
from concordance import ACTIVITY_TO_SECTOR, SECTORS  # noqa: E402

YEAR = sys.argv[1] if len(sys.argv) > 1 else "2018"
F = os.path.join(
    HERE, "io_ipea_ufrj", "PPE_apendice_eletronico", "MIP_67_PCR_PPE",
    f"MIP_{YEAR}_67_PCR.xlsx",
)
slugs = list(SECTORS)

usos = pd.read_excel(F, sheet_name="Usos", header=None)

# ---- activity columns (row 3 codes, cols 2..68) ----
act_col = {}  # code -> col index
for j in range(2, 69):
    c = usos.iat[3, j]
    if pd.notna(c):
        act_col[str(c).split(".")[0].zfill(4)] = j
assert len(act_col) == 67, len(act_col)
assert set(act_col) == set(ACTIVITY_TO_SECTOR), "activity code mismatch"

# ---- VA block: separate mini-table, rows 138-154, same column order ----
va_codes = [
    str(usos.iat[139, j]).split(".")[0].zfill(4) for j in range(2, 69)
]
assert va_codes == [
    str(usos.iat[3, j]).split(".")[0].zfill(4) for j in range(2, 69)
], "VA block column order differs from use-table order"

lab_row, cap_row, vab_row = 142, 148, 141
assert "Remunera" in str(usos.iat[lab_row, 0])
assert "Excedente" in str(usos.iat[cap_row, 0])
assert "Valor adicionado bruto" in str(usos.iat[vab_row, 0])

sec_lab = dict.fromkeys(slugs, 0.0)
sec_cap = dict.fromkeys(slugs, 0.0)
sec_vab = dict.fromkeys(slugs, 0.0)
for code, j in act_col.items():
    s = ACTIVITY_TO_SECTOR[code]
    sec_lab[s] += float(usos.iat[lab_row, j])
    sec_cap[s] += float(usos.iat[cap_row, j])
    sec_vab[s] += float(usos.iat[vab_row, j])

tot_vab = sum(sec_vab.values())
print(f"=== Production side: 10-sector VA shares & gamma (IPEA MIP {YEAR}) ===")
print(f"{'sector':22s}{'VA%':>7}{'gamma':>7}   (gamma = EOB+misto / (Rem+EOB+misto))")
for s in slugs:
    fac = sec_lab[s] + sec_cap[s]
    g = sec_cap[s] / fac if fac else float("nan")
    print(f"{s:22s}{sec_vab[s]/tot_vab*100:6.1f}%{g:7.2f}")
print(f"{'SUM':22s}{sum(sec_vab.values())/tot_vab*100:6.1f}%")

# ---- consumer side: alpha_c from "Consumo das famílias" (col 73) ----
assert "famílias" in str(usos.iat[3, 73]), str(usos.iat[3, 73])
prod_sector = {}   # 5-digit product code -> sector slug (via 4-digit prefix)
hh = dict.fromkeys(slugs, 0.0)
unmapped = []
for i in range(5, 131):
    code = usos.iat[i, 0]
    if pd.isna(code):
        continue
    pcode = str(code).split(".")[0].zfill(5)
    pref = pcode[:4]
    if pref not in ACTIVITY_TO_SECTOR:
        unmapped.append(pcode)
        continue
    s = ACTIVITY_TO_SECTOR[pref]
    prod_sector[pcode] = s
    v = usos.iat[i, 73]
    hh[s] += float(v) if pd.notna(v) else 0.0

print(f"\nproducts mapped: {len(prod_sector)}/126; unmapped: {unmapped}")
assert not unmapped, f"unmapped products: {unmapped}"
tot_hh = sum(hh.values())
print("\n=== Consumer side: alpha_c (household consumption shares, I=10) ===")
for s in slugs:
    print(f"{s:22s}{hh[s]/tot_hh*100:6.1f}%")
print(f"{'SUM':22s}{sum(hh.values())/tot_hh*100:6.1f}%")

# ---- Pi^I (io_matrix): consumption bridge from market-share matrix D ----
d = pd.read_excel(F, sheet_name="D", header=None)
# D: rows = activities (codes col 0, from row 5), cols = products (codes row 3)
d_act = [str(d.iat[i, 0]).split(".")[0].zfill(4) for i in range(5, 72)]
d_prod_cols = {}
for j in range(2, d.shape[1]):
    c = d.iat[3, j]
    if pd.notna(c):
        d_prod_cols[str(c).split(".")[0].zfill(5)] = j
assert len(d_act) == 67 and len(d_prod_cols) == 126

# Pi[i,m] = sum_{p in i} ( hhcons_p * sum_{a in m} D[a,p] ) / hhcons_i
# Note: D covers national production only; imported consumption is ignored.
hh_by_prod = {}
for i in range(5, 131):
    code = usos.iat[i, 0]
    if pd.isna(code):
        continue
    pcode = str(code).split(".")[0].zfill(5)
    v = usos.iat[i, 73]
    hh_by_prod[pcode] = float(v) if pd.notna(v) else 0.0

Pi = np.zeros((10, 10))
for pcode, j in d_prod_cols.items():
    w = hh_by_prod.get(pcode, 0.0)
    if w <= 0:
        continue
    i_idx = slugs.index(prod_sector[pcode])
    for r, acode in enumerate(d_act):
        val = d.iat[5 + r, j]
        if pd.notna(val) and val != 0:
            m_idx = slugs.index(ACTIVITY_TO_SECTOR[acode])
            Pi[i_idx, m_idx] += w * float(val)
row_tot = Pi.sum(axis=1, keepdims=True)
Pi = np.divide(Pi, row_tot, out=np.zeros_like(Pi), where=row_tot > 0)

print("\n=== Pi^I (io_matrix) 10x10: row sums and diagonal ===")
for k, s in enumerate(slugs):
    print(f"{s:22s} rowsum={Pi[k].sum():6.3f}  diag={Pi[k, k]:6.3f}")
