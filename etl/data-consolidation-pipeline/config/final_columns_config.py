#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 CONFIGURATION DES COLONNES FINALES
====================================

Configuration exacte selon real_estate_prompt.md
25-30 colonnes finales maximum
"""

# === COLONNES FINALES SELON LE PROMPT ===
FINAL_COLUMNS_SPECIFICATION = {
    "identifiants": [
        "_id",
        "address_final", 
        "city",
        "region",
        "postal_code_final"
    ],
    
    "financier": [
        "price_final",
        "revenue_final", 
        "tax_municipal_final",
        "tax_school_final",
        "expenses_final",
        "roi_brut",
        "roi_net", 
        "cash_flow_mensuel"
    ],
    
    "evaluations": [
        "evaluation_total_final",
        "potentiel_plus_value"
    ],
    
    "physique": [
        "surface_final",
        "bedrooms_final",
        "bathrooms_final",
        "year_built_final"
    ],
    
    "geographique": [
        "latitude_final",
        "longitude_final"
    ],
    
    "logistique": [
        "type",
        "vendue"
    ],
    
    "performance": [
        "classe_investissement",
        "score_qualite"
    ],
    
    "metadonnees": [
        "date_created_final"
    ]
}

# === LISTE COMPLÈTE DES COLONNES FINALES ===
FINAL_COLUMNS_LIST = []
for category, columns in FINAL_COLUMNS_SPECIFICATION.items():
    FINAL_COLUMNS_LIST.extend(columns)

# === COLONNES À SUPPRIMER ABSOLUMENT ===
COLUMNS_TO_REMOVE = [
    # Colonnes métadonnées et utilitaires non nécessaires
    "link", "company", "version", "extraction_metadata",
    # Colonnes sources qui ont été consolidées (garder seulement les _final)
    "address", "full_address",  # → address_final
    "price", "prix_evaluation", "price_assessment",  # → price_final
    "revenu", "plex-revenue", "plex-revenu", "plex_revenu",  # → revenue_final
    "municipal_tax", "municipal_taxes",  # → tax_municipal_final
    "school_tax", "school_taxes",  # → tax_school_final
    "depenses", "expense",  # → expenses_final
    "surface", "living_area", "superficie",  # → surface_final
    "bedrooms", "nb_bedroom", "nbr_chanbres",  # → bedrooms_final
    "bathrooms", "nb_bathroom", "nbr_sal_bain",  # → bathrooms_final
    "water_rooms", "nbr_sal_deau", "nb_water_room",  # → water_rooms_final
    "construction_year", "year_built", "annee",  # → year_built_final
    "latitude",  # → latitude_final
    "longitude",  # → longitude_final
    "location", "geolocation", "geo",  # → geolocation_final
    "add_date", "created_at",  # → date_created_final
    "updated_at", "update_at",  # → date_updated_final
    "evaluation_total", "municipal_evaluation_total",  # → evaluation_total_final
    "evaluation_batiment", "municipal_evaluation_building",  # → evaluation_building_final
    "evaluation_terrain", "municipal_evaluation_land",  # → evaluation_land_final
    "evaluation_year", "municipal_evaluation_year",  # → evaluation_year_final
    "parking", "nb_parking", "nb_garage",  # → parking_total_final
    "unites", "residential_units", "commercial_units",  # → units_final
    "image", "img_src", "images",  # → images_final
    "building_style", "style",  # → building_style_final
]

# === CALCULS MÉTADONNÉES ===
TOTAL_FINAL_COLUMNS = len(FINAL_COLUMNS_LIST)
EXPECTED_REDUCTION_PERCENTAGE = ((78 - TOTAL_FINAL_COLUMNS) / 78) * 100

print(f"📊 Colonnes finales spécifiées: {TOTAL_FINAL_COLUMNS}")
print(f"📉 Réduction attendue: {EXPECTED_REDUCTION_PERCENTAGE:.1f}%")
print(f"🎯 Objectif atteint: {'✅' if EXPECTED_REDUCTION_PERCENTAGE >= 65 else '❌'}")
