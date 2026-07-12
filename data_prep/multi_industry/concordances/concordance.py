"""
DRAFT concordance: IBGE SCN Nível 67 activities -> OG-BRA 10 sectors.

Source classification: IPEA/UFRJ annual MIP (Nível 67 activities / Nível 126
products), verified against MIP_2018_67_PCR.xlsx. Products map to activities by
their 4-digit code prefix (e.g. product 01911 -> activity 0191), so this single
activity->sector map induces the product->sector map as well.

STATUS: draft for review. Judgment calls are flagged inline (see NOTES). Nothing
here is wired into the ogbra package yet.
"""

# The agreed M=10 target sectors (slug -> human label).
SECTORS = {
    "agriculture": "Agriculture, forestry & fishing",
    "mining": "Mining & extractives",
    "manufacturing": "Manufacturing",
    "electricity_gas": "Electricity & gas",          # CLEWS energy node
    "water_waste": "Water, sewage & waste",           # CLEWS water node
    "construction": "Construction",
    "trade_transport": "Trade, transport & accommodation",
    "info_fin_business": "Info, financial & business services",
    "real_estate": "Real estate & dwellings",
    "public_social_other": "Public, social & other services",
}

# 67 IBGE Nível-67 activity codes -> sector slug.
ACTIVITY_TO_SECTOR = {
    # 1. Agriculture, forestry & fishing
    "0191": "agriculture",   # Agricultura
    "0192": "agriculture",   # Pecuária
    "0280": "agriculture",   # Produção florestal; pesca e aquicultura
    # 2. Mining & extractives
    "0580": "mining",        # Carvão e minerais não metálicos
    "0680": "mining",        # Petróleo e gás (extração)
    "0791": "mining",        # Minério de ferro
    "0792": "mining",        # Minerais metálicos não ferrosos
    # 3. Manufacturing
    "1091": "manufacturing", # Abate e produtos de carne/laticínio/pesca
    "1092": "manufacturing", # Açúcar
    "1093": "manufacturing", # Outros produtos alimentares
    "1100": "manufacturing", # Bebidas
    "1200": "manufacturing", # Fumo
    "1300": "manufacturing", # Têxteis
    "1400": "manufacturing", # Vestuário
    "1500": "manufacturing", # Calçados e couro
    "1600": "manufacturing", # Madeira
    "1700": "manufacturing", # Celulose e papel
    "1800": "manufacturing", # Impressão e reprodução
    "1991": "manufacturing", # Refino de petróleo e coquerias  [FLAG: energy]
    "1992": "manufacturing", # Biocombustíveis                 [FLAG: energy]
    "2091": "manufacturing", # Químicos orgânicos/inorgânicos
    "2092": "manufacturing", # Defensivos, tintas, químicos diversos
    "2093": "manufacturing", # Limpeza, cosméticos, higiene
    "2100": "manufacturing", # Farmoquímicos e farmacêuticos
    "2200": "manufacturing", # Borracha e plástico
    "2300": "manufacturing", # Minerais não metálicos (produtos)
    "2491": "manufacturing", # Siderurgia
    "2492": "manufacturing", # Metalurgia não ferrosos
    "2500": "manufacturing", # Produtos de metal
    "2600": "manufacturing", # Informática, eletrônicos e ópticos
    "2700": "manufacturing", # Máquinas e equipamentos elétricos
    "2800": "manufacturing", # Máquinas e equipamentos mecânicos
    "2991": "manufacturing", # Automóveis, caminhões e ônibus
    "2992": "manufacturing", # Peças e acessórios
    "3000": "manufacturing", # Outros equipamentos de transporte
    "3180": "manufacturing", # Móveis e indústrias diversas
    "3300": "manufacturing", # Manutenção/reparação/instalação
    # 4. Electricity & gas (CLEWS energy)
    "3500": "electricity_gas",   # Energia elétrica, gás natural e outras utilidades
    # 5. Water, sewage & waste (CLEWS water)
    "3680": "water_waste",       # Água, esgoto e gestão de resíduos
    # 6. Construction
    "4180": "construction",      # Construção
    # 7. Trade, transport & accommodation
    "4580": "trade_transport",   # Comércio atacado e varejo
    "4900": "trade_transport",   # Transporte terrestre
    "5000": "trade_transport",   # Transporte aquaviário
    "5100": "trade_transport",   # Transporte aéreo
    "5280": "trade_transport",   # Armazenamento e correio
    "5500": "trade_transport",   # Alojamento           [FLAG: accommodation]
    "5600": "trade_transport",   # Alimentação (serviço)[FLAG: food service]
    # 8. Info, financial & business services
    "5800": "info_fin_business", # Edição/publishing    [FLAG: ISIC J]
    "5980": "info_fin_business", # TV, rádio, cinema
    "6100": "info_fin_business", # Telecomunicações
    "6280": "info_fin_business", # Desenvolvimento de sistemas / TI
    "6480": "info_fin_business", # Intermediação financeira e seguros
    "6980": "info_fin_business", # Jurídicas, contábeis, consultoria
    "7180": "info_fin_business", # Arquitetura, engenharia, P&D
    "7380": "info_fin_business", # Outras profissionais/científicas/técnicas
    "7700": "info_fin_business", # Aluguéis não imobiliários e gestão de PI
    "7880": "info_fin_business", # Administrativas e serviços complementares
    "8000": "info_fin_business", # Vigilância, segurança e investigação
    # 9. Real estate & dwellings
    "6800": "real_estate",       # Atividades imobiliárias (incl. aluguel imputado)
    # 10. Public, social & other services
    "8400": "public_social_other",  # Administração pública, defesa, seguridade
    "8591": "public_social_other",  # Educação pública
    "8592": "public_social_other",  # Educação privada
    "8691": "public_social_other",  # Saúde pública
    "8692": "public_social_other",  # Saúde privada
    "9080": "public_social_other",  # Atividades artísticas e criativas
    "9480": "public_social_other",  # Organizações associativas / serviços pessoais
    "9700": "public_social_other",  # Serviços domésticos
}

# NOTES — judgment calls to confirm before this is finalized:
# 1. Petroleum refining (1991) + biofuels (1992) are placed in Manufacturing per
#    standard ISIC. For a tighter CLEWS *energy-supply* representation one could
#    instead pool an "energy" grouping = extraction 0680 + refining 1991 +
#    biofuels 1992 + electricity 3500. Kept in Manufacturing for the baseline.
# 2. Accommodation (5500) + food service (5600) go with Trade & transport to match
#    the agreed sector-7 label; alternatively they could join "other services" (10).
# 3. Publishing (5800) is Info services (ISIC J), distinct from Printing (1800),
#    which stays in Manufacturing.
# 4. Education/health, public and private, are all pooled in sector 10. If the model
#    wants a market vs non-market split, 8592/8692 could move elsewhere.
#
# PENDING DECISION — consumption dimension I:
#   alpha_c and io_matrix (Π^I) need the I consumption categories chosen. Natural
#   default is I = M = 10 (consumption good i ≡ output of sector i), with household
#   consumption of the 126 products aggregated to sectors and Π^I built from the
#   market-share matrix D. Confirm I before building the consumer side.

assert len(ACTIVITY_TO_SECTOR) == 67, len(ACTIVITY_TO_SECTOR)
assert set(ACTIVITY_TO_SECTOR.values()) <= set(SECTORS), "unknown sector slug"
