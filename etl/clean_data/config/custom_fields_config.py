# ⚙️ Configuration Personnalisée - Dataset Immobilier
# Basé sur vos 67 champs spécifiques ET la stratégie de consolidation avancée
# Harmonisé avec consolidation_config.py

from .consolidation_config import ConsolidationConfig, ConsolidationGroup

class CustomFieldsConfig(ConsolidationConfig):
    """
    Configuration personnalisée pour votre dataset immobilier
    avec 67 champs spécifiques, étendue pour respecter la stratégie
    de consolidation avancée du real_estate_prompt.md
    """
    
    def __init__(self):
        super().__init__()
        # Surcharge avec vos spécificités
        self._customize_for_67_fields()
    
    def _customize_for_67_fields(self):
        """Personnalise la configuration pour vos 67 champs spécifiques"""
        
        # === AJUSTEMENT DES GROUPES POUR VOS 67 CHAMPS ===
        # Nous gardons la structure avancée mais adaptons les colonnes sources
        
        # Groupe Prix - Adapté à vos champs
        self._update_group_sources("Prix", [
            "price",              # Prix principal
            "prix_evaluation",    # Prix d'évaluation
            "price_assessment"    # Prix d'évaluation alternatif
        ])
        
        # Groupe Surface - Adapté à vos champs
        self._update_group_sources("Surface", [
            "surface",            # Surface principale
            "living_area",        # Surface habitable
            "superficie",         # Surface en français
            "lot_size"            # Taille du terrain
        ])
        
        # Groupe Chambres - Adapté à vos champs
        self._update_group_sources("Chambres", [
            "bedrooms",           # Chambres en anglais
            "nbr_chanbres",       # Nombre de chambres en français
            "nb_bedroom",         # Nombre de chambres alternatif
            "rooms"               # Pièces générales
        ])
        
        # Groupe Salles de bain - Adapté à vos champs
        self._update_group_sources("Salles de bain", [
            "bathrooms",          # Salles de bain en anglais
            "nbr_sal_deau",       # Nombre de salles d'eau
            "nbr_sal_bain",       # Nombre de salles de bain
            "nb_bathroom",        # Nombre de salles de bain alternatif
            "water_rooms"         # Salles d'eau
        ])
        
        # Groupe Salles d'eau - Adapté à vos champs
        self._update_group_sources("Salles d'eau", [
            "water_rooms",        # Salles d'eau
            "nbr_sal_deau",       # Nombre de salles d'eau
            "nb_water_room"       # Nombre de salles d'eau alternatif
        ])
        
        # Groupe Coordonnées - Adapté à vos champs
        self._update_group_sources("Latitude", ["latitude"])
        self._update_group_sources("Longitude", ["longitude"])
        self._update_group_sources("Géolocalisation", [
            "geolocation",        # Objet géolocalisation
            "geo"                 # Géolocalisation alternative
        ])
        
        # Groupe Adresses - Adapté à vos champs
        self._update_group_sources("Adresses", [
            "address",            # Adresse
            "full_address",       # Adresse complète
            "location",           # Localisation
            "city",               # Ville
            "postal_code"         # Code postal
        ])
        
        # Groupe Type propriété - Adapté à vos champs
        self._update_group_sources("Type propriété", [
            "type",               # Type principal
            "building_style",     # Style de construction
            "style"               # Style alternatif
        ])
        
        # Groupe Année construction - Adapté à vos champs
        self._update_group_sources("Année construction", [
            "year_built",         # Année de construction
            "construction_year",  # Année de construction alternatif
            "annee"               # Année en français
        ])
        
        # Groupe Taxes municipales - Adapté à vos champs
        self._update_group_sources("Taxes municipales", [
            "municipal_taxes",    # Taxes municipales
            "municipal_tax",      # Taxe municipale
            "taxes"               # Taxes générales
        ])
        
        # Groupe Taxes scolaires - Adapté à vos champs
        self._update_group_sources("Taxes scolaires", [
            "school_taxes",       # Taxes scolaires
            "school_tax"          # Taxe scolaire
        ])
        
        # Groupe Évaluation - Adapté à vos champs
        self._update_group_sources("Évaluation totale", [
            "evaluation_total",           # Évaluation totale
            "municipal_evaluation_total", # Évaluation municipale totale
        ])
        
        self._update_group_sources("Évaluation bâtiment", [
            "evaluation_batiment",         # Évaluation du bâtiment
            "municipal_evaluation_building" # Évaluation municipale du bâtiment
        ])
        
        self._update_group_sources("Évaluation terrain", [
            "evaluation_terrain",         # Évaluation du terrain
            "municipal_evaluation_land"   # Évaluation municipale du terrain
        ])
        
        # Groupe Revenus - Adapté à vos champs
        self._update_group_sources("Revenus", [
            "revenu",                     # Revenu
            "revenus_annuels_bruts",      # Revenus annuels bruts
            "plex-revenu",                # Revenu plex
            "plex_revenu",                # Revenu plex alternatif
            "potential_gross_revenue"     # Revenu brut potentiel
        ])
        
        # Groupe Dépenses - Adapté à vos champs
        self._update_group_sources("Dépenses", [
            "expense",            # Dépense
            "depenses",           # Dépenses en français
            "expense_period"      # Période de dépense
        ])
        
        # Groupe Parking - Adapté à vos champs
        self._update_group_sources("Parking total", [
            "nb_parking",         # Nombre de places de stationnement
            "parking",            # Stationnement
            "nb_garage"           # Nombre de garages
        ])
        
        # Groupe Unités - Adapté à vos champs
        self._update_group_sources("Unités", [
            "unites",             # Unités
            "residential_units",  # Unités résidentielles
            "commercial_units"    # Unités commerciales
        ])
        
        # Groupe Images - Adapté à vos champs
        self._update_group_sources("Images", [
            "image",              # Image
            "images",             # Images multiples
            "img_src"             # Source d'image
        ])
        
        # Groupe Période - Adapté à vos champs
        self._update_group_sources("Période revenus", [
            "revenu_period",      # Période de revenu
            "expense_period"      # Période de dépense
        ])
        
        # Groupe Style bâtiment - Adapté à vos champs
        self._update_group_sources("Style bâtiment", [
            "building_style",     # Style de construction
            "style"               # Style alternatif
        ])
        
        # Groupe Sous-sol - Adapté à vos champs
        self._update_group_sources("Sous-sol", [
            "basement"            # Sous-sol
        ])
        
        # Groupe Taille terrain - Adapté à vos champs
        self._update_group_sources("Taille terrain", [
            "lot_size",           # Taille du terrain
            "evaluation_terrain"  # Évaluation du terrain
        ])
        
        # === AJOUT DE GROUPES SPÉCIFIQUES À VOS DONNÉES ===
        
        # Groupe Détails unité principale
        self._add_custom_group(
            "Détails unité principale",
            "main_unit_details_final",
            ["main_unit_details"],
            "Détails de l'unité principale",
            2,
            "categorical",
            ["not_null", "format_validation"]
        )
        
        # Groupe Statut de vente
        self._add_custom_group(
            "Statut de vente",
            "vendue_final",
            ["vendue"],
            "Statut de vente de la propriété",
            2,
            "categorical",
            ["not_null", "consistency_check"]
        )
        
        # Groupe Description
        self._add_custom_group(
            "Description",
            "description_final",
            ["description"],
            "Description de la propriété",
            3,
            "categorical",
            ["not_null", "text_quality"]
        )
        
        # Groupe Métadonnées d'extraction
        self._add_custom_group(
            "Métadonnées extraction",
            "extraction_metadata_final",
            ["extraction_metadata"],
            "Métadonnées d'extraction",
            3,
            "categorical",
            ["format_validation"]
        )
        
        # Groupe Région
        self._add_custom_group(
            "Région",
            "region_final",
            ["region"],
            "Région de la propriété",
            2,
            "categorical",
            ["not_null", "geographic_consistency"]
        )
        
        # === COLONNES À CONSERVER SANS CONSOLIDATION ===
        self.PRESERVED_COLUMNS = [
            "_id",                       # Identifiant MongoDB
            "updated_at",                # Date de mise à jour
            "evaluation_year",           # Année d'évaluation
            "add_date",                  # Date d'ajout
            "created_at",                # Date de création
            "municipal_evaluation_year", # Année d'évaluation municipale
            "update_at"                  # Date de mise à jour alternative
        ]
        
        # === COLONNES À SUPPRIMER SPÉCIFIQUES ===
        self.COLUMNS_TO_REMOVE.extend([
            "link",                      # Liens non essentiels
            "company",                   # Entreprises non essentielles
            "version"                    # Versions non essentielles
        ])
        
        # === RÈGLES MÉTIER SPÉCIFIQUES À VOS DONNÉES ===
        self.BUSINESS_RULES.update({
            "quebec_coordinates": {      # Limites Québec ajustées
                "lat_min": 45.0, "lat_max": 63.0,
                "lng_min": -80.0, "lng_max": -57.0
            },
            "price_range": (10000, 10000000),      # Prix en dollars
            "surface_range": (20, 10000),          # Surface en m²
            "bedrooms_range": (0, 20),             # Nombre de chambres
            "bathrooms_range": (0, 20),            # Nombre de salles de bain
            "year_range": (1900, 2025)             # Année de construction
        })
        
        # === SEUILS DE QUALITÉ PERSONNALISÉS ===
        self.QUALITY_THRESHOLDS.update({
            "global_score": 80.0,        # Score global minimum
            "type_consistency": 85.0,    # Cohérence des types
            "value_validity": 90.0,      # Validité des valeurs
            "geographic_validation": 95.0, # Validation géographique
            "business_rules": 88.0       # Règles métier
        })
        
        # === OPTIMISATIONS SPÉCIFIQUES ===
        self.OPTIMIZATIONS.update({
            "memory_optimization": True,
            "type_optimization": True,
            "parallel_processing": True,
            "jit_compilation": False,
            "chunked_processing": True,
            "categorization": True,
            "advanced_algorithms": True
        })
    
    def _update_group_sources(self, group_name: str, new_sources: list):
        """Met à jour les colonnes sources d'un groupe existant"""
        for group in self.CONSOLIDATION_GROUPS:
            if group.name == group_name:
                group.source_columns = new_sources
                break
    
    def _add_custom_group(self, name: str, final_column: str, source_columns: list, 
                          description: str, priority: int, data_type: str, validation_rules: list):
        """Ajoute un groupe de consolidation personnalisé"""
        custom_group = ConsolidationGroup(
            name=name,
            final_column=final_column,
            source_columns=source_columns,
            description=description,
            priority=priority,
            data_type=data_type,
            validation_rules=validation_rules
        )
        self.CONSOLIDATION_GROUPS.append(custom_group)
    
    def get_67_fields_config_summary(self):
        """Retourne un résumé de la configuration pour vos 67 champs"""
        total_groups = len(self.CONSOLIDATION_GROUPS)
        total_source_columns = sum(len(group.source_columns) for group in self.CONSOLIDATION_GROUPS)
        preserved_count = len(self.PRESERVED_COLUMNS)
        
        return {
            "total_consolidation_groups": total_groups,
            "total_source_columns": total_source_columns,
            "preserved_columns": preserved_count,
            "estimated_final_columns": total_groups + preserved_count,
            "estimated_reduction": f"{((67 - (total_groups + preserved_count)) / 67 * 100):.1f}%"
        }

# Instance de configuration à utiliser
custom_config = CustomFieldsConfig()

if __name__ == "__main__":
    print("✅ Configuration personnalisée harmonisée chargée avec succès!")
    
    # Résumé de la configuration
    summary = custom_config.get_67_fields_config_summary()
    print(f"📊 Groupes de consolidation: {summary['total_consolidation_groups']}")
    print(f"📋 Colonnes sources totales: {summary['total_source_columns']}")
    print(f"🔧 Champs préservés: {summary['preserved_columns']}")
    print(f"📊 Colonnes finales estimées: {summary['estimated_final_columns']}")
    print(f"📉 Réduction estimée: {summary['estimated_reduction']}")
    
    # Afficher les groupes de consolidation
    print("\n🏗️ Groupes de consolidation personnalisés:")
    for group in custom_config.CONSOLIDATION_GROUPS:
        print(f"  {group.name} → {group.final_column}: {len(group.source_columns)} colonnes sources")
    
    print("\n🔧 Champs préservés sans consolidation:")
    for col in custom_config.PRESERVED_COLUMNS:
        print(f"  - {col}")
    
    print("\n🎯 Configuration harmonisée avec la stratégie de consolidation avancée!")
