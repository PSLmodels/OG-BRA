#!/usr/bin/env bash
# Fetch the raw data for OG-BRA multi-industry calibration (preliminary).
# Raw files are gitignored; this script re-downloads them from source.
# See README.md for the full manifest and provenance.
#
# Usage:  bash fetch_data.sh
# Note:   IBGE/EPE reject bare curl (HTTP 403) — a browser User-Agent is required.

set -uo pipefail
cd "$(dirname "$0")"

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

get() {  # get <url> <output-path>
  local url="$1" out="$2"
  mkdir -p "$(dirname "$out")"
  echo ">> $out"
  curl -sSL --fail --max-time 300 -A "$UA" -o "$out" "$url" \
    -w "   HTTP %{http_code} | %{size_download} bytes\n" \
    || echo "   FAILED: $url"
}

echo "== 1. IPEA/UFRJ annual MIP (Alves-Passoni & Freitas 2023, PPE v.53 n.1) =="
IPEA_ZIP="concordances/PPE_v53_n1_Artigo4_apendice.zip"
get "https://repositorio.ipea.gov.br/bitstream/11058/13345/2/PPE_v53_n1_Artigo4_apendice_eletronico.zip" \
    "$IPEA_ZIP"
if [ -f "$IPEA_ZIP" ]; then
  echo "   extracting MIP xlsx (skipping mac/lock junk)..."
  unzip -oq "$IPEA_ZIP" -d io_ipea_ufrj/ \
    -x "__MACOSX/*" "*/.DS_Store" "*/.~lock*" "*/Icon*" "*.Rhistory" || true
  find io_ipea_ufrj -name ".DS_Store" -delete 2>/dev/null || true
fi

echo "== 2. EPE Balanço Energético Nacional 2025 (base year 2024) =="
EPE_BASE="https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-885/topico-766"
get "$EPE_BASE/Anexo%20IX%20-%20Balan%C3%A7os%20Consolidados%20(em%20tep)%201970%20a%202024.xlsx" \
    "energy_epe/BEN2025_AnexoIX_Balancos_Consolidados_tep_1970-2024.xlsx"
get "$EPE_BASE/Matriz%20ab2024.xlsx" \
    "energy_epe/BEN2025_Matriz_ab2024.xlsx"
# Full open matrix (53 MB) — uncomment if needed:
# get "$EPE_BASE/Anexo%20X%20-%20Matriz%20aberta%20e%20Comercial%201970%20a%202024.xlsx" \
#     "energy_epe/BEN2025_AnexoX_Matriz_aberta_Comercial_1970-2024.xlsx"

echo "== 3. IBGE official benchmark MIP 2015, Nível 67 (validation anchor) =="
get "https://ftp.ibge.gov.br/Contas_Nacionais/Matriz_de_Insumo_Produto/2015/Matriz_de_Insumo_Produto_2015_Nivel_67.xls" \
    "io_ibge/Matriz_de_Insumo_Produto_2015_Nivel_67.xls"

echo "== 4. Receita Federal — arrecadação by CNAE section & tax (2016+) =="
# ISO-8859-1 encoded, ';'-separated, Brazilian decimals. IRPJ + CSLL columns
# give the effective cit_rate numerator; denominator = EOB from the MIP.
get "https://www.gov.br/receitafederal/dados/arrecadacao-cnae.csv" \
    "tax_rfb/arrecadacao-cnae.csv"

echo ""
echo "== Not automated (portal/verification needed — see README.md) =="
echo "   - SNIS water sector (optional, low priority):  snis.gov.br"
echo ""
echo "Done. Raw files are gitignored; commit only README.md + this script."
