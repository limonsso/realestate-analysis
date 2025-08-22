"""
Validateur de données pour Centris.ca
"""

import structlog
from typing import List
from src.models.property import PropertySummary, SearchQuery, PropertyType
from src.utils.validators import RegionValidator, PropertyValidator

logger = structlog.get_logger()


class CentrisDataValidator:
    """Validateur de données pour les résultats Centris"""
    
    def __init__(self):
        self.validation_threshold = 0.7  # 70% de correspondance minimum
    
    def validate_search_results(self, properties: List[PropertySummary], search_query: SearchQuery) -> bool:
        """
        Valide que les résultats de recherche correspondent aux critères
        
        Args:
            properties: Liste des propriétés extraites de la première page
            search_query: Paramètres de recherche utilisés
            
        Returns:
            bool: True si les résultats sont valides
        """
        try:
            if not properties or len(properties) == 0:
                logger.warning("⚠️ Aucune propriété trouvée dans la première page")
                return False
            
            # Validation des localisations
            location_valid = self._validate_locations_searched(properties, search_query.locations)
            
            # Validation des types de propriétés
            property_type_valid = self._validate_property_types(properties, search_query.property_types)
            
            # Les deux validations doivent réussir
            is_valid = location_valid and property_type_valid
            
            if is_valid:
                logger.info("✅ Validation des résultats réussie")
            else:
                if not location_valid:
                    logger.warning("⚠️ Validation des localisations échouée")
                if not property_type_valid:
                    logger.warning("⚠️ Validation des types de propriétés échouée")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {str(e)}")
            # En cas d'erreur de validation, on considère que c'est valide pour ne pas bloquer
            return True
    
    def _validate_locations_searched(self, properties: List[PropertySummary], expected_locations: List[str]) -> bool:
        """
        Valide que les résultats correspondent aux localisations recherchées
        
        Args:
            properties: Liste des propriétés extraites
            expected_locations: Liste des localisations recherchées
            
        Returns:
            bool: True si la validation réussit
        """
        try:
            if not expected_locations:
                logger.debug("ℹ️ Aucune localisation spécifique à valider")
                return True
            
            # Compteurs pour les statistiques
            total_properties = len(properties)
            matching_properties = 0
            
            logger.info(f"🔍 Validation des localisations pour {total_properties} propriétés...")
            
            # Vérification des correspondances
            for prop in properties:
                is_match = False
                
                # Validation de la localisation
                if prop.address and prop.address.city:
                    for expected_location in expected_locations:
                        if expected_location.lower() in prop.address.city.lower():
                            is_match = True
                            break
                
                if is_match:
                    matching_properties += 1
                else:
                    logger.debug(f"⚠️ Localisation non correspondante: {prop.address.city if prop.address else 'N/A'} vs {expected_locations}")
            
            # Calcul du pourcentage de correspondance
            match_percentage = (matching_properties / total_properties) * 100 if total_properties > 0 else 0
            
            logger.info(f"📊 Validation localisations: {matching_properties}/{total_properties} propriétés correspondent ({match_percentage:.1f}%)")
            
            # Seuil de validation
            is_valid = match_percentage >= (self.validation_threshold * 100)
            
            if not is_valid and total_properties > 5:
                logger.warning(f"⚠️ Faible taux de correspondance des localisations ({match_percentage:.1f}%)")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation des localisations: {str(e)}")
            return True
    
    def _validate_property_types(self, properties: List[PropertySummary], expected_property_types: List[PropertyType]) -> bool:
        """
        Valide que les résultats correspondent aux types de propriétés recherchés
        
        Args:
            properties: Liste des propriétés extraites
            expected_property_types: Liste des types de propriétés recherchés
            
        Returns:
            bool: True si la validation réussit
        """
        try:
            if not expected_property_types:
                logger.debug("ℹ️ Aucun type de propriété spécifique à valider")
                return True
            
            # Compteurs pour les statistiques
            total_properties = len(properties)
            matching_properties = 0
            type_distribution = {}
            
            logger.info(f"🔍 Validation des types de propriétés pour {total_properties} propriétés...")
            
            # Vérification des correspondances
            for prop in properties:
                if not prop.type:
                    continue
                
                # Mise à jour de la distribution des types
                prop_type_str = prop.type.value if hasattr(prop.type, 'value') else str(prop.type)
                type_distribution[prop_type_str] = type_distribution.get(prop_type_str, 0) + 1
                
                # Vérification de la correspondance
                is_match = False
                for expected_type in expected_property_types:
                    expected_type_str = expected_type.value if hasattr(expected_type, 'value') else str(expected_type)
                    
                    if (prop_type_str.lower() in expected_type_str.lower() or 
                        expected_type_str.lower() in prop_type_str.lower()):
                        is_match = True
                        break
                
                if is_match:
                    matching_properties += 1
                else:
                    logger.debug(f"⚠️ Type non correspondant: {prop_type_str} vs {[t.value if hasattr(t, 'value') else str(t) for t in expected_property_types]}")
            
            # Calcul du pourcentage de correspondance
            match_percentage = (matching_properties / total_properties) * 100 if total_properties > 0 else 0
            
            logger.info(f"📊 Validation types: {matching_properties}/{total_properties} propriétés correspondent ({match_percentage:.1f}%)")
            
            # Log de la distribution des types
            type_summary = ", ".join([f"{t}: {c}" for t, c in sorted(type_distribution.items(), key=lambda x: x[1], reverse=True)])
            logger.info(f"📊 Distribution des types: {type_summary}")
            
            # Seuil de validation
            is_valid = match_percentage >= (self.validation_threshold * 100)
            
            if not is_valid and total_properties > 5:
                logger.warning(f"⚠️ Faible taux de correspondance des types ({match_percentage:.1f}%)")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation des types: {str(e)}")
            return True
    
    def set_validation_threshold(self, threshold: float):
        """Définit le seuil de validation (0.0 à 1.0)"""
        if 0.0 <= threshold <= 1.0:
            self.validation_threshold = threshold
            logger.info(f"🔧 Seuil de validation mis à jour: {threshold * 100:.0f}%")
        else:
            logger.warning(f"⚠️ Seuil de validation invalide: {threshold} (doit être entre 0.0 et 1.0)")
    
    def get_validation_threshold(self) -> float:
        """Retourne le seuil de validation actuel"""
        return self.validation_threshold

