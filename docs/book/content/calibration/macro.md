(Chap_MacroCalib)=
# Calibration of Macroeconomic Parameters

## Economic Assumptions

As the default rate of labor augmenting technological change, $g_y$, we use a value of 2.1%.  This is the average annual growth rate in GDP per capita in Brazil from 1947 to 2024, as reported in the World Bank World Development Indicators (`NY.GDP.PCAP.KD`).

## Open Economy Parameters

### Foreign holding of government debt in the initial period

The path of foreign holding of domestic debt is endogenous, but the initial period stock of debt held by foreign investors is exogenous.  We set this parameter, `initial_foreign_debt_ratio` to 0.146, as determined from data on gross public sector debt from the World Bank's Quarterly Public Sector Debt (QPSD) database.

### Foreign purchases of newly issued debt

We set $\zeta_D = 0.146$.  This was not directly observed in the data, so the value was set to the current share of foreign holdings of government debt.

### Foreign holdings of excess capital

We set $\zeta_K = 0.9$. Note, this parameter is harder to pin down from the data as foreign purchases on "excess" capital demand is not typically directly measured or reported.  A value of 0.9 implies a high degree of openness to international capital flows.

## Government Debt, Spending and Transfers

### Government Debt

The path of government debt is endogenous.  But the initial value is exogenous.  To avoid converting between model units and dollars, we calibrate the initial debt to GDP ratio, rather than the dollar value of the debt.  This is the model parameter $\alpha_D$.  We compute this from the World Bank's Quarterly Public Sector Debt (QPSD) database (`DP.DOD.DECT.CR.GG.Z1`).  The most recent available value gives an initial debt-to-GDP ratio of 0.741.

### Aggregate transfers

Aggregate (non-Social Security) transfers to households are set as a share of GDP with the parameter $\alpha_T$. We exclude Social Security from transfers since it is modeled specifically. With this definition, the share of transfers to GDP is found to be 3.8% using data from the [IMF Government Finance Statistics (GFS)](https://www.imf.org/en/Data) database.  The value is computed as total social benefits (GFS indicator `G27_T`) minus social security contributions (`G271_T`), expressed as a share of GDP.

### Government expenditures

Government spending on goods and services are also set as a share of GDP with the parameter $\alpha_G$. We define government spending as:
    <center>Government Spending = Total Outlays - Transfers - Net Interest on Debt - Social Security</center>
With this definition, the share of government expenditure to GDP is 11.8%, computed from the [IMF Government Finance Statistics (GFS)](https://www.imf.org/en/Data) database as total expenditure (`G2_T`) minus interest (`G24_T`) minus social benefits (`G27_T`), expressed as a share of GDP.
