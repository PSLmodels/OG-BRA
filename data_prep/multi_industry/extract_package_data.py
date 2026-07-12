"""Extract the compact CSVs that ship in the ogbra package from the IPEA MIP.

Reads MIP_2018_67_PCR.xlsx (Alves-Passoni & Freitas 2023 electronic appendix;
re-download with fetch_data.sh) and writes four small CSVs to ogbra/data/:

  * mip_2018_activity.csv     - per-activity value added, factor payments,
                                occupations, and gross output (67 rows)
  * mip_2018_consumption.csv  - per-product household consumption at consumer
                                prices (Usos) and of domestic production at
                                basic prices (Usos Nacional) (126 rows)
  * mip_2018_market_share.csv - the D matrix (activity share of each
                                product's domestic supply), 67 x 126
  * mip_2018_leontief.csv     - the domestic Leontief inverse (I - An)^-1,
                                67 x 67

These are the only pieces of the MIP the calibration needs (see
CODE_ASSESSMENT.md). Run from this directory:

    ../../.venv/bin/python extract_package_data.py [YEAR]
"""

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.realpath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
YEAR = sys.argv[1] if len(sys.argv) > 1 else "2018"
MIP = os.path.join(
    HERE,
    "io_ipea_ufrj",
    "PPE_apendice_eletronico",
    "MIP_67_PCR_PPE",
    f"MIP_{YEAR}_67_PCR.xlsx",
)
OUT = os.path.join(REPO, "ogbra", "data")

usos = pd.read_excel(MIP, sheet_name="Usos", header=None)
unac = pd.read_excel(MIP, sheet_name="Usos Nacional", header=None)
imp = pd.read_excel(MIP, sheet_name="Impostos", header=None)
dmat = pd.read_excel(MIP, sheet_name="D", header=None)
leo = pd.read_excel(MIP, sheet_name="Z", header=None)

# --- activities: codes at Usos row 3 (cols 2..68), labels row 4 ---
acts = [str(usos.iat[3, j]).split(".")[0].zfill(4) for j in range(2, 69)]
act_labels = [str(usos.iat[4, j]).strip() for j in range(2, 69)]
assert len(acts) == 67

# --- VA block rows (verified layout, identical across years) ---
row_names = {
    141: "value_added",
    142: "compensation",
    149: "mixed_income",
    150: "operating_surplus",
    153: "gross_output",
    154: "occupations",
}
for r, _ in row_names.items():
    assert pd.notna(usos.iat[r, 0]), f"row {r} label missing"
assert "Valor adicionado bruto" in str(usos.iat[141, 0])
assert "Remunera" in str(usos.iat[142, 0])
assert "misto bruto" in str(usos.iat[149, 0])
assert "(EOB)" in str(usos.iat[150, 0])
assert "Valor da produ" in str(usos.iat[153, 0])
assert "ocupa" in str(usos.iat[154, 0]).lower()

act_df = pd.DataFrame({"activity_code": acts, "activity_label": act_labels})
for r, name in row_names.items():
    act_df[name] = [float(usos.iat[r, j]) for j in range(2, 69)]
act_df.to_csv(os.path.join(OUT, f"mip_{YEAR}_activity.csv"), index=False)

# --- products: household consumption, total (col 73) and domestic ---
assert "famílias" in str(usos.iat[3, 73]) and "famílias" in str(
    unac.iat[3, 73]
)
assert "famílias" in str(imp.iat[3, 73])
prods, plabels, hh_tot, hh_dom, hh_tax = [], [], [], [], []
for i in range(5, 131):
    code = usos.iat[i, 0]
    if pd.isna(code):
        continue
    prods.append(str(code).split(".")[0].zfill(5))
    plabels.append(str(usos.iat[i, 1]).strip())
    v = usos.iat[i, 73]
    hh_tot.append(float(v) if pd.notna(v) else 0.0)
    v = unac.iat[i, 73]
    hh_dom.append(float(v) if pd.notna(v) else 0.0)
    v = imp.iat[i, 73]
    hh_tax.append(float(v) if pd.notna(v) else 0.0)
assert len(prods) == 126
pd.DataFrame(
    {
        "product_code": prods,
        "product_label": plabels,
        "hh_consumption_consumer_prices": hh_tot,
        "hh_consumption_domestic_basic": hh_dom,
        "hh_taxes_on_products": hh_tax,
    }
).to_csv(os.path.join(OUT, f"mip_{YEAR}_consumption.csv"), index=False)

# --- D matrix (rows: activities from row 5; cols: products from col 2) ---
d_prods = [str(dmat.iat[3, j]).split(".")[0].zfill(5) for j in range(2, 128)]
assert d_prods == prods
D = np.array(
    [
        [
            float(dmat.iat[5 + r, 2 + j])
            if pd.notna(dmat.iat[5 + r, 2 + j])
            else 0.0
            for j in range(126)
        ]
        for r in range(67)
    ]
)
d_acts = [str(dmat.iat[5 + r, 0]).split(".")[0].zfill(4) for r in range(67)]
assert d_acts == acts
pd.DataFrame(D, index=acts, columns=prods).to_csv(
    os.path.join(OUT, f"mip_{YEAR}_market_share.csv"),
    index_label="activity_code",
)

# --- Leontief inverse (activities x activities) ---
l_acts = [str(leo.iat[3, j]).split(".")[0].zfill(4) for j in range(2, 69)]
assert l_acts == acts
L = np.array(
    [
        [
            float(leo.iat[5 + r, 2 + j])
            if pd.notna(leo.iat[5 + r, 2 + j])
            else 0.0
            for j in range(67)
        ]
        for r in range(67)
    ]
)
pd.DataFrame(L, index=acts, columns=acts).to_csv(
    os.path.join(OUT, f"mip_{YEAR}_leontief.csv"), index_label="activity_code"
)

for f in sorted(os.listdir(OUT)):
    if f.startswith(f"mip_{YEAR}"):
        path = os.path.join(OUT, f)
        print(f"{f}: {os.path.getsize(path) // 1024} KB")
