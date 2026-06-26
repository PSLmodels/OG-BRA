(Chap_Tax)=
# Taxes in OG-BRA

The government is not an optimizing agent in `OG-BRA`. The government levies taxes on household income, corporate income, and value added. With these resources, the government provides transfers to households, spends resources on public goods, and makes rule-based adjustments to stabilize the economy in the long-run. The government can run budget deficits or surpluses in a given year and must, therefore, be able to accumulate debt or savings.  The spending and debt parameters are discussed in Chapter {ref}`Chap_MacroCalib`.  Taxes are discussed in this chapter.


## Personal income taxes
The government sector influences households through two terms in the household budget constraint {eq}`EqHHBC`---government transfers $TR_{t}$ and through the total tax liability function $T_{s,t}$, which can be decomposed into the effective tax rate times total income {eq}`EqTaxCalcLiabETR2`. In this chapter, we detail the household tax component of government activity $T_{s,t}$ in `OG-BRA`.

```{math}
:label: EqHHBC
  c_{j,s,t} + b_{j,s+1,t+1} &= (1 + r_{hh,t})b_{j,s,t} + w_t e_{j,s} n_{j,s,t} + \\
  &\quad\quad\zeta_{j,s}\frac{BQ_t}{\lambda_j\omega_{s,t}} + \eta_{j,s,t}\frac{TR_{t}}{\lambda_j\omega_{s,t}} + ubi_{j,s,t} - T_{s,t}  \\
  &\quad\forall j,t\quad\text{and}\quad s\geq E+1 \quad\text{where}\quad b_{j,E+1,t}=0\quad\forall j,t
```

The total tax function, $T_{s,t}$, is a function of personal income taxes, taxes on bequests, and wealth taxes.  In the default calibration, wealth and bequest taxes are set to zero in `OG-BRA`. Personal income taxes are modeled as linear taxes and set to average effective and marginal tax rates.  The [OG-Core documentation](https://pslmodels.github.io/OG-Core/content/theory/government.html#taxes) details more detailed ways to match the progressivity of the tax system.  But given limited data for Brazil, we start with simple linear tax rates of 12% for effective tax rates on personal income (`etr_params`), an 18% marginal tax rate on labor income (`mtrx_params`), and an 18% marginal tax rate on capital income (`mtry_params`).

Brazil's individual income tax (IRPF) has five statutory brackets ranging from 0% to 27.5%, with an exemption threshold of approximately R\$2,824 per month (pre-2026 rules). Beginning in January 2026, Law No. 15,270/2025 raises the full exemption threshold to R\$5,000 per month and introduces a new minimum income tax (IRPFM) for taxpayers with annual income exceeding R\$600,000. Given the broad exemption and large informal sector, the effective average income tax rate across all earners is substantially below the top statutory rate. We use 12% as a stylized economy-wide effective rate and 18% as the marginal rate on both labor and capital income. These parameters should be updated with microdata-based estimates from PNAD or Receita Federal administrative data when available. Source: [PwC Brazil Individual Tax Summary](https://taxsummaries.pwc.com/brazil/individual/taxes-on-personal-income); [Trench Rossi Watanabe — Law 15,270/2025](https://www.trenchrossi.com/en/legal-alerts/brazil-enacts-law-15270-2025-which-taxes-dividends-and-amend-personal-income-tax-rules/).

## Payroll taxes

Brazil's payroll tax system is administered through the National Social Security Institute (INSS) and the Government Severance Fund (FGTS). Employers are required to contribute 20% of gross wages to INSS and an additional 8% to FGTS, for a combined employer payroll tax burden of **28%** (`tau_payroll = 0.28`). Employees also pay progressive INSS contributions ranging from 7.5% to 14% of their wages, capped at approximately R\$952 per month in 2025. Source: [Vialto Partners — Brazil Social Security 2025](https://vialtopartners.com/regional-alerts/brazil-social-security-updated-social-security-tax-table-for-2025); [Boundless — Payroll Taxes in Brazil](https://boundlesshq.com/guides/brazil/taxes/).

## Corporate income taxes

`OG-BRA` uses a combined statutory corporate income tax rate of **34%** (`cit_rate = 0.34`), comprising the Corporate Income Tax (IRPJ) at 25% (a 15% base rate plus a 10% surtax on annual taxable profits exceeding R\$240,000) and the Social Contribution on Net Profit (CSLL) at 9%. This combined rate has been stable and applies to most non-financial businesses. Financial institutions face higher CSLL rates (15–20%), yielding combined rates of 40–45%. Source: [PwC Brazil Corporate Tax Summary](https://taxsummaries.pwc.com/brazil/corporate/taxes-on-corporate-income).

## Value-added taxes

Brazil does not currently have a unified VAT. Its indirect tax system is composed of multiple overlapping federal, state, and municipal levies. The two main federal consumption taxes are PIS (Programa de Integração Social, 1.65%) and COFINS (Contribuição para o Financiamento da Seguridade Social, 7.6%), which together total approximately 9.25% on revenues. State ICMS rates range from 17–20%, and municipal ISS applies at 2–5% on services.

`OG-BRA` sets `tau_c = 0.09`, calibrated to the combined PIS + COFINS federal consumption tax rate of approximately 9%, which represents the federal VAT-equivalent component applicable to most goods and services.

Brazil is currently undertaking a major indirect tax reform (Constitutional Amendment 132/2023) that will replace PIS, COFINS, ICMS, IPI, and ISS with a dual VAT system consisting of a federal CBS (Contribuição sobre Bens e Serviços, targeting ~8.8%) and a state/municipal IBS (Imposto sobre Bens e Serviços, targeting ~17.7%) for a combined rate of approximately 26.5%. The transition runs from 2026 through 2033, with CBS becoming fully operational in 2027. The `tau_c` parameter should be revisited as the reform proceeds. Source: [PwC Brazil Corporate Other Taxes](https://taxsummaries.pwc.com/brazil/corporate/other-taxes); [TaxUp — Brazil Tax Reform Guide 2026–2033](https://taxup.com.br/en/solutions/tax-reform/).
