(Chap_FirmCalib)=
# Calibration of Firms Parameters

## Aggregate Production Function and Capital Accumulation

The [OG-Core firm theory documentation](https://pslmodels.github.io/OG-Core/content/theory/firms.html) outlines the constant returns to scale, constant elasticity of substitution production function of the representative firm.  This function has two parameters; the elasticity of substitution and capital's share of output.

### Elasticity of substitution

`OG-BRA`'s default parameterization has an elasticity of substitution of $\varepsilon=1.0$, which implies a Cobb-Douglas production function.

### Capital's share of output

Here, we use a default value of $\gamma =0.407$, which is derived from the ILO's SDG indicator 10.4.1 (labour share of GDP, series `SDG_1041_NOC_RT_A`) for Brazil.  Capital's share is computed as one minus the labour share.
