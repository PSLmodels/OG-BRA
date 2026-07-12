"""1) Validate IPEA 2015 vs IBGE official 2015 (household consumption by product).
2) Demo: PHL-style I=5 consumption categories + Leontief VA-content Pi^I (I=5 x M=10)."""

import sys
import numpy as np
import pandas as pd

sys.path.insert(
    0, "/Users/mlafleur/Projects/OG-BRA/data_prep/multi_industry/concordances"
)
from concordance import ACTIVITY_TO_SECTOR, SECTORS  # noqa: E402

BASE = "/Users/mlafleur/Projects/OG-BRA/data_prep/multi_industry"
IPEA15 = f"{BASE}/io_ipea_ufrj/PPE_apendice_eletronico/MIP_67_PCR_PPE/MIP_2015_67_PCR.xlsx"
IPEA18 = f"{BASE}/io_ipea_ufrj/PPE_apendice_eletronico/MIP_67_PCR_PPE/MIP_2018_67_PCR.xlsx"
IBGE15 = f"{BASE}/io_ibge/Matriz_de_Insumo_Produto_2015_Nivel_67.xls"
slugs = list(SECTORS)


def header_cols(df, row):
    """Map column index -> label for a header row."""
    out = {}
    for j in range(df.shape[1]):
        v = df.iat[row, j]
        if pd.notna(v):
            out[j] = str(v)
    return out


# ---------- 1. VALIDATION: hh consumption by product, IPEA 2015 vs IBGE 2015 ----------
def hh_vector_ipea(path, sheet, hh_label="famílias"):
    u = pd.read_excel(path, sheet_name=sheet, header=None)
    hh_col = None
    for j in range(60, u.shape[1]):
        if hh_label in str(u.iat[3, j]):
            hh_col = j
            break
    assert hh_col, f"hh col not found in {sheet}"
    vec = {}
    for i in range(5, u.shape[0]):
        code = u.iat[i, 0]
        if pd.isna(code):
            continue
        c = str(code).split(".")[0]
        if not c.isdigit():
            continue
        v = u.iat[i, hh_col]
        vec[c.zfill(5)] = float(v) if pd.notna(v) else 0.0
    return vec, hh_col


def hh_vector_ibge(path, sheet="02"):
    u = pd.read_excel(path, sheet_name=sheet, header=None)
    hh_col = None
    for j in range(60, u.shape[1]):
        if "famílias" in str(u.iat[3, j]) or "famílias" in str(u.iat[2, j]):
            hh_col = j
            break
    assert hh_col, "hh col not found in IBGE sheet 02"
    vec = {}
    for i in range(5, u.shape[0]):
        code = u.iat[i, 0]
        if pd.isna(code):
            continue
        c = str(code).split(".")[0]
        if not c.isdigit():
            continue
        v = u.iat[i, hh_col]
        vec[c.zfill(5)] = float(v) if pd.notna(v) else 0.0
    return vec, hh_col


ip, ipcol = hh_vector_ipea(IPEA15, "Usos")
ib, ibcol = hh_vector_ibge(IBGE15)
common = sorted(set(ip) & set(ib))
print(f"=== VALIDATION: IPEA 2015 vs IBGE 2015, household consumption ===")
print(f"products: IPEA {len(ip)}, IBGE {len(ib)}, common {len(common)}")
a = np.array([ip[c] for c in common])
b = np.array([ib[c] for c in common])
print(f"totals: IPEA {a.sum():,.0f} | IBGE {b.sum():,.0f} | ratio {a.sum()/b.sum():.4f}")
diff = np.abs(a - b)
rel = diff / np.maximum(np.abs(b), 1.0)
print(f"max abs diff {diff.max():,.1f}; products w/ rel diff > 1%: {(rel > 0.01).sum()}")
if (rel > 0.01).sum():
    worst = np.argsort(-rel)[:5]
    for k in worst:
        print(f"  {common[k]}: IPEA {a[k]:,.0f} vs IBGE {b[k]:,.0f}")

# ---------- 2. DEMO: I=5 PHL-style categories, VA-content Pi^I ----------
# Product 4-digit prefix -> consumption category (DRAFT, by producing activity)
CAT_OF_PREFIX = {}
def assign(prefixes, cat):
    for p in prefixes:
        CAT_OF_PREFIX[p] = cat

assign(["0191", "0192", "0280", "1091", "1092", "1093", "1100"], "food_bev")
assign(["3500", "3680", "1991", "1992", "0580", "0680"], "energy_utilities")
assign(["1200", "1300", "1400", "1500", "1600", "1700", "1800",
        "2091", "2092", "2093", "2100", "2200", "2300"], "nondurables")
assign(["2491", "2492", "2500", "2600", "2700", "2800", "2991", "2992",
        "3000", "3180", "0791", "0792"], "durables")
assign(["3300", "4180", "4580", "4900", "5000", "5100", "5280", "5500",
        "5600", "5800", "5980", "6100", "6280", "6480", "6800", "6980",
        "7180", "7380", "7700", "7880", "8000", "8400", "8591", "8592",
        "8691", "8692", "9080", "9480", "9700"], "services")
cats = ["food_bev", "energy_utilities", "nondurables", "durables", "services"]
assert set(CAT_OF_PREFIX) == set(ACTIVITY_TO_SECTOR), "prefix coverage mismatch"

F = IPEA18
usos = pd.read_excel(F, sheet_name="Usos", header=None)
usos_nac = pd.read_excel(F, sheet_name="Usos Nacional", header=None)
dmat = pd.read_excel(F, sheet_name="D", header=None)
zleo = pd.read_excel(F, sheet_name="Z", header=None)

# activity order (67) from Usos row 3
acts = [str(usos.iat[3, j]).split(".")[0].zfill(4) for j in range(2, 69)]

# product order (126) from Usos col 0
prods = []
for i in range(5, 131):
    c = usos.iat[i, 0]
    if pd.notna(c):
        prods.append(str(c).split(".")[0].zfill(5))
assert len(prods) == 126

# hh consumption: total (Usos col 73, consumer prices) for alpha_c;
# domestic basic-price (Usos Nacional) for Pi^I weights
hh_tot, c73 = hh_vector_ipea(F, "Usos")
hh_nac, cnac = hh_vector_ipea(F, "Usos Nacional")
print(f"\nhh col Usos={c73}, Usos Nacional={cnac} "
      f"(labels: '{str(usos.iat[3, c73])[:30]}', '{str(usos_nac.iat[3, cnac])[:30]}')")

# D matrix 67x126 (rows: activities from row 5; cols: products from col 2)
D = np.zeros((67, 126))
dp = [str(dmat.iat[3, j]).split(".")[0].zfill(5) for j in range(2, 128)]
assert dp == prods, "D product order mismatch"
for r in range(67):
    for j in range(126):
        v = dmat.iat[5 + r, 2 + j]
        D[r, j] = float(v) if pd.notna(v) else 0.0

# Leontief inverse 67x67 (Z sheet, same layout: activities x activities)
L = np.zeros((67, 67))
zacts = [str(zleo.iat[3, j]).split(".")[0].zfill(4) for j in range(2, 69)]
assert zacts == acts, "Z activity order mismatch"
for r in range(67):
    for j in range(67):
        v = zleo.iat[5 + r, 2 + j]
        L[r, j] = float(v) if pd.notna(v) else 0.0

# v = VA / gross output by activity (Usos VA block rows 141, 153)
assert "Valor adicionado bruto" in str(usos.iat[141, 0])
assert "Valor da produção" in str(usos.iat[153, 0])
va = np.array([float(usos.iat[141, j]) for j in range(2, 69)])
go = np.array([float(usos.iat[153, j]) for j in range(2, 69)])
v = va / go

# Pi^I: for each category, f (domestic hh cons by product) -> D f -> L (D f) -> v * .
Pi = np.zeros((5, 10))
alpha = np.zeros(5)
for ci, cat in enumerate(cats):
    f = np.array([
        hh_nac.get(p, 0.0) if CAT_OF_PREFIX[p[:4]] == cat else 0.0
        for p in prods
    ])
    alpha[ci] = sum(
        hh_tot.get(p, 0.0) for p in prods if CAT_OF_PREFIX[p[:4]] == cat
    )
    va_by_act = v * (L @ (D @ f))
    for ai, acode in enumerate(acts):
        Pi[ci, slugs.index(ACTIVITY_TO_SECTOR[acode])] += va_by_act[ai]
alpha = alpha / alpha.sum()
Pi = Pi / Pi.sum(axis=1, keepdims=True)

print("\n=== DEMO (IPEA 2018): PHL-style I=5, Leontief VA-content Pi^I (5x10) ===")
print(f"\nalpha_c: " + ", ".join(f"{c}={alpha[i]:.3f}" for i, c in enumerate(cats)))
print(f"\n{'Pi^I':18s}" + "".join(f"{s[:7]:>8}" for s in slugs))
for ci, cat in enumerate(cats):
    print(f"{cat:18s}" + "".join(f"{Pi[ci, m]:8.3f}" for m in range(10)))
print("row sums:", np.round(Pi.sum(axis=1), 6))
