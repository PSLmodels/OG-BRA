SHOW_RUNTIME = False  # Flag to display RuntimeWarnings when run model

REFORM_DIR = "OUTPUT_REFORM"
BASELINE_DIR = "OUTPUT_BASELINE"

# Default year for model runs
DEFAULT_START_YEAR = 2025


VAR_LABELS = {
    "Y": "GDP ($Y_t$)",
    "C": "Consumption ($C_t$)",
    "L": "Labor ($L_t$)",
    "G": "Government Expenditures ($G_t$)",
    "TR": "Lump sum transfers ($TR_t$)",
    "B": "Wealth ($B_t$)",
    "I_total": "Investment ($I_t$)",
    "K": "Capital Stock ($K_t$)",
    "K_d": "Domestically-owned Capital Stock ($K^d_t$)",
    "K_f": "Foreign-owned Capital Stock ($K^f_t$)",
    "D": "Government Debt ($D_t$)",
    "D_d": "Domestically-owned Gov Debt ($D^d_t$)",
    "D_f": "Foreign-owned Gov Debt ($D^f_t$)",
    "r": "Real interest rate ($r_t$)",
    "r_gov": "Real interest rate on gov debt ($r_{gov,t}$)",
    "r_hh": "Real interest rate on HH portfolio ($r_{hh,t}$)",
    "w": "Wage rate",
    "BQ": "Aggregate bequests ($BQ_{j,t}$)",
    "total_tax_revenue": "Total tax revenue ($REV_t$)",
    "business_tax_revenue": "Business tax revenue",
    "iit_revenue": "Individual income tax revenue",
    "payroll_tax_revenue": "Payroll tax revenue",
    "iit_payroll_tax_revenue": "IIT and payroll tax revenue",
    "n_mat": "Labor Supply ($n_{j,s,t}$)",
    "c_path": "Consumption ($c_{j,s,t}$)",
    "bmat_splus1": "Savings ($b_{j,s+1,t+1}$)",
    "bq_path": "Bequests ($bq_{j,s,t}$)",
    "bmat_s": "Savings ($b_{j,s,t}$)",
    "y_before_tax_mat": "Before tax income",
    "etr_path": "Effective Tax Rate ($ETR_{j,s,t}$)",
    "mtrx_path": "Marginal Tax Rate, Labor Income ($MTRx_{j,s,t}$)",
    "mtry_path": "Marginal Tax Rate, Capital Income ($MTRy_{j,s,t}$)",
    "tax_path": "Total Taxes",
    "nssmat": "Labor Supply ($\\bar{n}_{j,s}$)",
    "bssmat_s": "Savings ($\\bar{b}_{j,s}$)",
    "bssmat_splus1": "Savings ($\\bar{b}_{j,s+1}$)",
    "cssmat": "Consumption ($\\bar{c}_{j,s}$)",
    "yss_before_tax_mat": "Before-tax Income",
    "etr_ss": "Effective Tax Rate ($\\bar{ETR}_{j,s}$)",
    "mtrx_ss": "Marginal Tax Rate, Labor Income ($\\bar{MTRx}_{j,s}$)",
    "mtry_ss": "Marginal Tax Rate, Capital Income ($\\bar{MTRy}_{j,s}$)",
    "ETR": "Effective Tax Rates",
    "MTRx": "Marginal Tax Rates on Labor Income",
    "MTRy": "Marginal Tax Rates on Capital Income",
    "etr": "Effective Tax Rates",
    "mtrx": "Marginal Tax Rates on Labor Income",
    "mtry": "Marginal Tax Rates on Capital Income",
    "Yss": "GDP ($\\bar{Y}$)",
    "Css": "Consumption ($\\bar{C}$)",
    "Lss": "Labor ($\\bar{L}$)",
    "Gss": "Government Expenditures ($\\bar{G}$)",
    "TR_ss": "Lump sum transfers, ($\\bar{TR}$)",
    "Bss": "Wealth ($\\bar{B}$)",
    "Iss_total": "Investment ($\\bar{I}$)",
    "Kss": "Capital Stock ($\\bar{K}$)",
    "K_d_ss": "Domestically-owned Capital Stock ($\\bar{K}^d$)",
    "K_f_ss": "Foreign-owned Capital Stock ($\\bar{K}^f$)",
    "Dss": "Government Debt ($\\bar{D}$)",
    "D_d_ss": "Domestically-owned Gov Debt ($\\bar{D}^d$)",
    "D_f_ss": "Foreign-owned Gov Debt ($\\bar{D}^f$)",
    "rss": "Real interest rate ($\\bar{r}$)",
    "r_gov_ss": "Real interest rate on gov debt ($\\bar{r}_{gov}$)",
    "r_hh_ss": "Real interest rate on HH portfolio ($\\bar{r}_{hh}$)",
    "wss": "Wage rate ($\\bar{w}$)",
    "BQss": "Aggregate bequests ($\\bar{BQ}_{j}$)",
    "debt_service_ss": "Debt service cost ($\\bar{r}_{gov}\\bar{D}$)",
    "D/Y": "Debt to GDP ratio",
    "T_Pss": "Government Pensions",
}

ToGDP_LABELS = {
    "D": "Debt-to-GDP ($D_{t}/Y_t$)",
    "D_d": "Domestically-owned Debt-to-GDP ($D^d_{t}/Y_t$)",
    "D_f": "Foreign-owned Debt-to-GDP ($D^f_{t}/Y_t$)",
    "G": "Govt Spending-to-GDP ($G_{t}/Y_t$)",
    "K": "Capital-Output Ratio ($K_{t}/Y_t$)",
    "K_d": "Domestically-owned Capital-Output Ratio ($K^d_{t}/Y_t$)",
    "K_f": "Foreign-owned Capital-Output Ratio ($K^f_{t}/Y_t$)",
    "C": "Consumption-Output Ratio ($C_{t}/Y_t$)",
    "I": "Investment-Output Ratio ($I_{t}/Y_t$)",
    "total_tax_revenue": "Tax Revenue-to-GDP ($REV_{t}/Y_t$)",
}

GROUP_LABELS = {
    7: {
        0: "0-25%",
        1: "25-50%",
        2: "50-70%",
        3: "70-80%",
        4: "80-90%",
        5: "90-99%",
        6: "Top 1%",
    },
    9: {
        0: "0-25%",
        1: "25-50%",
        2: "50-70%",
        3: "70-80%",
        4: "80-90%",
        5: "90-99%",
        6: "99-99.5%",
        7: "99.5-99.9%",
        8: "Top 0.1%",
    },
    10: {
        0: "0-25%",
        1: "25-50%",
        2: "50-70%",
        3: "70-80%",
        4: "80-90%",
        5: "90-99%",
        6: "99-99.5%",
        7: "99.5-99.9%",
        8: "99.9-99.99%",
        9: "Top 0.01%",
    },
}

CBO_UNITS = {
    "Y": r"Billions of R$",
    "r": "Percent",
    "w_growth": "Percent",
    "L_growth": "Percent",
    "I_total": r"Billions of R$",
    "L": "2012=100",
    "C": r"Billions of R$",
    "agg_pension_outlays": r"Billions of R$",
    "G": r"Billions of R$",
    "iit_revenue": r"Billions of R$",
    "payroll_tax_revenue": r"Billions of R$",
    "business_tax_revenue": r"Billions of R$",
    "wL": r"Billions of R$",
    "D": r"Billions of R$",
}

PARAM_LABELS = {
    "start_year": ["Initial year", r"$\texttt{start_year}$"],
    # 'Gamma': ['Initial distribution of savings', r'\hat{\Gamma}_{0}'],
    # 'N': ['Initial population', 'N_{0}'],
    "omega": ["Population by age over time", r"${{\omega_{s,t}}}_{s=1}^{S}$"],
    # 'fert_rates': ['Fertility rates by age',
    #                r'\left{f_{s}\right}_{s=1}^{S}'],
    "imm_rates": ["Immigration rates by age", r"${{i_{s}}}_{s=1}^{S}$"],
    "rho": ["Mortality rates by age", r"${{\rho_{s}}}_{s=1}^{S}$"],
    "e": ["Deterministic ability process", r"${{e_{j,s}}}_{j,s=1}^{J,S}$"],
    "lambdas": [
        "Lifetime income group percentages",
        r"${{\lambda_{j}}}_{j=1}^{J}$",
    ],
    "J": ["Number of lifetime income groups", "$J$"],
    "S": ["Maximum periods in economically active individual life", "$S$"],
    "E": ["Number of periods of youth economically outside the model", "$E$"],
    "T": ["Number of periods to steady-state", "$T$"],
    "retirement_age": ["Retirement age", "$R$"],
    "ltilde": ["Maximum hours of labor supply", r"$\tilde{l}$"],
    "beta": ["Discount factor", r"$\beta$"],
    "sigma": ["Coefficient of constant relative risk aversion", r"$\sigma$"],
    "frisch": ["Frisch elasticity of labor supply", r"$\nu$"],
    "b_ellipse": ["Scale parameter in utility of leisure", "$b$"],
    "upsilon": ["Shape parameter in utility of leisure", r"$\upsilon$"],
    # 'k': ['Constant parameter in utility of leisure', 'k'],
    "chi_n": [
        "Disutility of labor level parameters",
        r"$\left{\chi^{n}_{s}\right}_{s=1}^{S}$",
    ],
    "chi_b": [
        "Utility of bequests level parameters",
        r"$\left{\chi^{b}_{j}\right}_{j=1}^{J}$",
    ],
    "use_zeta": [
        "Whether to distribute bequests between lifetime income groups",
        r"$\texttt{use_zeta}$",
    ],
    "zeta": ["Distribution of bequests", r"$\zeta$"],
    "Z": ["Total factor productivity", "$Z_{t}$"],
    "gamma": ["Capital share of income", r"$\gamma$"],
    "epsilon": [
        "Elasticity of substitution between capital and labor",
        r"\varepsilon",
    ],
    "delta": ["Capital depreciation rate", r"$\delta$"],
    "g_y": [
        "Growth rate of labor augmenting technological progress",
        r"$g_{y}$",
    ],
    "tax_func_type": [
        "Functional form used for income tax functions",
        r"$\texttt{tax_func_type}$",
    ],
    "analytical_mtrs": [
        "Whether use analytical MTRs or estimate MTRs",
        r"$\texttt{analytical_mtrs}$",
    ],
    "age_specific": [
        "Whether use age-specific tax functions",
        r"$\texttt{age_specific}$",
    ],
    "tau_payroll": ["Payroll tax rate", r"$\tau^{p}_{t}$"],
    # 'theta': ['Replacement rate by average income',
    #           r'\left{\theta_{j}\right}_{j=1}^{J}'],
    "tau_bq": ["Bequest (estate) tax rate", r"$\tau^{BQ}_{t}}$"],
    "tau_b": ["Entity-level business income tax rate", r"$\tau^{b}_{t}$"],
    "delta_tau": [
        "Rate of depreciation for tax purposes",
        r"$\delta^{\tau}_{t}$",
    ],
    "tau_c": ["Consumption tax rates", r"$\tau^{c}_{t,s,j}$"],
    "h_wealth": ["Coefficient on linear term in wealth tax function", "$H$"],
    "m_wealth": ["Constant in wealth tax function", "$M$"],
    "p_wealth": ["Coefficient on level term in wealth tax function", "$P$"],
    "budget_balance": [
        "Whether have a balanced budget in each period",
        r"$\texttt{budget_balance}$",
    ],
    "baseline_spending": [
        "Whether level of spending constant between "
        + "the baseline and reform runs",
        r"$\texttt{baseline_spending}$",
    ],
    "alpha_T": ["Transfers as a share of GDP", r"$\alpha^{T}_{t}$"],
    "eta": ["Distribution of transfers", r"$\eta_{j,s,t}$"],
    "alpha_G": ["Government spending as a share of GDP", r"$\alpha^{G}_{t}$"],
    "tG1": ["Model period in which budget closure rule starts", r"$t_{G1}$"],
    "tG2": ["Model period in which budget closure rule ends", r"$t_{G2}$"],
    "rho_G": ["Budget closure rule smoothing parameter", r"$\rho_{G}$"],
    "debt_ratio_ss": ["Steady-state Debt-to-GDP ratio", r"$\bar{\alpha}_{D}$"],
    "initial_debt_ratio": [
        "Initial period Debt-to-GDP ratio",
        r"$\alpha_{D,0}$",
    ],
    "r_gov_scale": [
        "Scale parameter in government interest rate wedge",
        r"$\tau_{d,t}$",
    ],
    "r_gov_shift": [
        "Shift parameter in government interest rate wedge",
        r"$\mu_{d,t}$",
    ],
    "AIME_num_years": [
        "Number of years over which compute AIME",
        r"$\texttt{AIME_num_years}$",
    ],
    "AIME_bkt_1": ["First AIME bracket threshold", r"$\texttt{AIME_bkt_1}$"],
    "AIME_bkt_2": ["Second AIME bracket threshold", r"$\texttt{AIME_bkt_2}$"],
    "PIA_rate_bkt_1": [
        "First AIME bracket PIA rate",
        r"$\texttt{PIA_rate_bkt_1}$",
    ],
    "PIA_rate_bkt_2": [
        "Second AIME bracket PIA rate",
        r"\texttt{PIA_rate_bkt_2}",
    ],
    "PIA_rate_bkt_3": [
        "Third AIME bracket PIA rate",
        r"$\texttt{PIA_rate_bkt_3}$",
    ],
    "PIA_maxpayment": ["Maximum PIA payment", r"$\texttt{PIA_maxpayment}$"],
    "PIA_minpayment": ["Minimum PIA payment", r"$\texttt{PIA_maxpayment}$"],
    "replacement_rate_adjust": [
        "Adjustment to replacement rate",
        r"$theta_{adj,t}$",
    ],
    "world_int_rate": ["World interest rate", r"$r^{*}_{t}$"],
    "initial_foreign_debt_ratio": [
        "Share of government debt held by foreigners in initial period",
        r"$D_{f,0}$",
    ],
    "zeta_D": [
        "Share of new debt issues purchased by foreigners",
        r"$\zeta_{D, t}$",
    ],
    "zeta_K": [
        "Share of excess capital demand satisfied by foreigners",
        r"$\zeta_{K, t}$",
    ],
    "nu": ["Dampening parameter for TPI", r"$\xi$"],
    "maxiter": ["Maximum number of iterations for TPI", r"$\texttt{maxiter}$"],
    "mindist_SS": ["SS solution tolerance", r"$\texttt{mindist_SS}$"],
    "mindist_TPI": ["TPI solution tolerance", r"$\texttt{mindist_TPI}$"],
}

# Ignoring the following:
# 'starting_age', 'ending_age', 'constant_demographics',
# 'constant_rates', 'zero_taxes'

"""
Create dictionaries to map micro categories to broad groups
"""

# Production side: IBGE SCN Nivel-67 activities -> the model's M = 9
# industries. Products (Nivel 126) map to activities by their four-digit
# code prefix (product 01911 -> activity 0191), so this one map also
# assigns every product to an industry. Verified against the IPEA annual
# input-output tables (Alves-Passoni & Freitas, 2023); see the industry
# calibration chapter.
# Real estate (imputed owner-occupier dwelling rent) is grouped with the
# financial and business services here, the standard FIRE aggregation
# (Finance, Insurance, Real Estate); OG-PHL likewise keeps it inside its
# services sector rather than standing alone.
# Manufacturing is kept LAST: OG-Core treats the last industry as the
# numeraire and routes all non-consumption final demand (investment,
# government purchases) through it, so it must be the investment-goods
# producer (the same convention as OG-PHL).
SECTORS = {
    "agriculture": "Agriculture, forestry & fishing",
    "mining": "Mining & extractives",
    "electricity_gas": "Electricity & gas",
    "water_waste": "Water, sewage & waste",
    "construction": "Construction",
    "trade_transport": "Trade, transport & accommodation",
    "info_fin_business": "Finance, real estate & business services",
    "public_social_other": "Public, social & other services",
    "manufacturing": "Manufacturing",
}

ACTIVITY_TO_SECTOR = {
    # Agriculture, forestry & fishing
    "0191": "agriculture",
    "0192": "agriculture",
    "0280": "agriculture",
    # Mining & extractives
    "0580": "mining",
    "0680": "mining",
    "0791": "mining",
    "0792": "mining",
    # Manufacturing
    "1091": "manufacturing",
    "1092": "manufacturing",
    "1093": "manufacturing",
    "1100": "manufacturing",
    "1200": "manufacturing",
    "1300": "manufacturing",
    "1400": "manufacturing",
    "1500": "manufacturing",
    "1600": "manufacturing",
    "1700": "manufacturing",
    "1800": "manufacturing",
    "1991": "manufacturing",
    "1992": "manufacturing",
    "2091": "manufacturing",
    "2092": "manufacturing",
    "2093": "manufacturing",
    "2100": "manufacturing",
    "2200": "manufacturing",
    "2300": "manufacturing",
    "2491": "manufacturing",
    "2492": "manufacturing",
    "2500": "manufacturing",
    "2600": "manufacturing",
    "2700": "manufacturing",
    "2800": "manufacturing",
    "2991": "manufacturing",
    "2992": "manufacturing",
    "3000": "manufacturing",
    "3180": "manufacturing",
    "3300": "manufacturing",
    # Electricity & gas (the CLEWS energy node)
    "3500": "electricity_gas",
    # Water, sewage & waste (the CLEWS water node)
    "3680": "water_waste",
    # Construction
    "4180": "construction",
    # Trade, transport & accommodation
    "4580": "trade_transport",
    "4900": "trade_transport",
    "5000": "trade_transport",
    "5100": "trade_transport",
    "5280": "trade_transport",
    "5500": "trade_transport",
    "5600": "trade_transport",
    # Finance, real estate & business services (CNAE J, K, L, M, N;
    # activity 6800 is real estate, dominated by imputed dwelling rent)
    "5800": "info_fin_business",
    "5980": "info_fin_business",
    "6100": "info_fin_business",
    "6280": "info_fin_business",
    "6480": "info_fin_business",
    "6800": "info_fin_business",
    "6980": "info_fin_business",
    "7180": "info_fin_business",
    "7380": "info_fin_business",
    "7700": "info_fin_business",
    "7880": "info_fin_business",
    "8000": "info_fin_business",
    # Public, social & other services
    "8400": "public_social_other",
    "8591": "public_social_other",
    "8592": "public_social_other",
    "8691": "public_social_other",
    "8692": "public_social_other",
    "9080": "public_social_other",
    "9480": "public_social_other",
    "9700": "public_social_other",
}

# Consumption side: the I = 7 consumption goods, defined as groups of the
# 126 MIP products by four-digit activity prefix. Electricity and water
# are their own goods for the OG-CLEWS energy and water linkages. Note
# that product 35001 bundles electricity with piped gas (bottled cooking
# gas is a refining product, already in fuels).
CONS_CATEGORIES = {
    "food_bev": "Food and beverages",
    "electricity": "Electricity",
    "water": "Water, sewage & waste services",
    "fuels": "Fuels",
    "nondurables": "Non-durables",
    "durables": "Durables",
    "services": "Services",
}

PREFIX_TO_CONS_CATEGORY = {
    # Food and beverages
    "0191": "food_bev",
    "0192": "food_bev",
    "0280": "food_bev",
    "1091": "food_bev",
    "1092": "food_bev",
    "1093": "food_bev",
    "1100": "food_bev",
    # Electricity (incl. piped gas and other network utilities)
    "3500": "electricity",
    # Water, sewage & waste
    "3680": "water",
    # Fuels (refining, biofuels, coal, oil & gas extraction)
    "1991": "fuels",
    "1992": "fuels",
    "0580": "fuels",
    "0680": "fuels",
    # Non-durables
    "1200": "nondurables",
    "1300": "nondurables",
    "1400": "nondurables",
    "1500": "nondurables",
    "1600": "nondurables",
    "1700": "nondurables",
    "1800": "nondurables",
    "2091": "nondurables",
    "2092": "nondurables",
    "2093": "nondurables",
    "2100": "nondurables",
    "2200": "nondurables",
    "2300": "nondurables",
    # Durables
    "2491": "durables",
    "2492": "durables",
    "2500": "durables",
    "2600": "durables",
    "2700": "durables",
    "2800": "durables",
    "2991": "durables",
    "2992": "durables",
    "3000": "durables",
    "3180": "durables",
    "0791": "durables",
    "0792": "durables",
    # Services
    "3300": "services",
    "4180": "services",
    "4580": "services",
    "4900": "services",
    "5000": "services",
    "5100": "services",
    "5280": "services",
    "5500": "services",
    "5600": "services",
    "5800": "services",
    "5980": "services",
    "6100": "services",
    "6280": "services",
    "6480": "services",
    "6800": "services",
    "6980": "services",
    "7180": "services",
    "7380": "services",
    "7700": "services",
    "7880": "services",
    "8000": "services",
    "8400": "services",
    "8591": "services",
    "8592": "services",
    "8691": "services",
    "8692": "services",
    "9080": "services",
    "9480": "services",
    "9700": "services",
}

# Economy-wide capital share of factor income, computed from the 2018 MIP
# with mixed income split like the rest of the economy (the Gollin
# correction): gross operating surplus / (compensation + gross operating
# surplus). The raw sector capital shares from the MIP include all mixed
# income as capital; get_gamma rescales their level to this target while
# keeping the cross-industry pattern.
TOTAL_CAPITAL_SHARE = 0.428

# Public capital's share of output by industry, carved out of the total
# capital share (following OG-PHL); see the government calibration chapter.
PUBLIC_CAPITAL_SHARE = 0.05

# National capital-output ratio anchoring the capital level in the TFP
# residual: Penn World Table 10.x for Brazil, 2018 (rnna / rgdpna, via
# FRED series RKNANPBRA666NRUG and RGDPNABRA666NRUG).
CAPITAL_OUTPUT_RATIO = 4.36
