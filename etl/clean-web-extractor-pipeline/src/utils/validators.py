"""
Utilitaires de validation pour le pipeline d'extraction immobilière
"""

from typing import List, Optional
import re


class RegionValidator:
    """Validateur pour les régions québécoises"""
    
    @staticmethod
    def get_known_quebec_regions() -> List[str]:
        """
        Retourne la liste des régions connues du Québec
        
        Returns:
            List[str]: Liste des noms de régions
        """
        return [
            "Montérégie", "Montréal (Île)", "Montréal", "Québec", "Laval", "Laurentides",
            "Lanaudière", "Estrie", "Outaouais", "Chaudière-Appalaches",
            "Capitale-Nationale", "Centre-du-Québec", "Mauricie",
            "Bas-Saint-Laurent", "Saguenay-Lac-Saint-Jean", "Abitibi-Témiscamingue",
            "Côte-Nord", "Gaspésie", "Îles-de-la-Madeleine", "Nord-du-Québec"
        ]
    
    @staticmethod
    def is_valid_region(region: Optional[str]) -> bool:
        """
        Vérifie si la région fournie est valide (non vide et fait partie des régions connues du Québec)
        
        Args:
            region: Nom de la région à vérifier
            
        Returns:
            bool: True si la région est valide, False sinon
        """
        if not region:
            return False
        
        # Vérifier si la région est non vide et fait partie des régions connues
        known_regions = RegionValidator.get_known_quebec_regions()
        
        # Normaliser la région pour la comparaison (supprimer les accents, mettre en minuscule)
        normalized_region = region.lower().strip()
        normalized_known_regions = [r.lower().strip() for r in known_regions]
        
        # Vérifier si la région est dans la liste des régions connues
        return normalized_region in normalized_known_regions or any(
            normalized_region in known_region for known_region in normalized_known_regions
        )
    
    @staticmethod
    def normalize_region(region: Optional[str]) -> Optional[str]:
        """
        Normalise le nom d'une région pour correspondre aux noms standards
        
        Args:
            region: Nom de la région à normaliser
            
        Returns:
            str: Nom de région normalisé ou None si invalide
        """
        if not region:
            return None
            
        # Mappings de normalisation
        region_mappings = {
            "montreal": "Montréal",
            "montréal": "Montréal",
            "montreal (île)": "Montréal (Île)",
            "montréal (île)": "Montréal (Île)",
            "quebec": "Québec",
            "québec": "Québec",
            "laurentides": "Laurentides",
            "lanaudiere": "Lanaudière",
            "lanaudière": "Lanaudière",
            "monteregie": "Montérégie",
            "montérégie": "Montérégie",
            "chaudiere-appalaches": "Chaudière-Appalaches",
            "chaudière-appalaches": "Chaudière-Appalaches",
            "capitale-nationale": "Capitale-Nationale",
            "centre-du-quebec": "Centre-du-Québec",
            "centre-du-québec": "Centre-du-Québec",
        }
        
        normalized = region.lower().strip()
        
        # Essayer de trouver une correspondance exacte
        if normalized in region_mappings:
            return region_mappings[normalized]
        
        # Essayer de trouver une correspondance partielle
        known_regions = RegionValidator.get_known_quebec_regions()
        for known_region in known_regions:
            if normalized in known_region.lower() or known_region.lower() in normalized:
                return known_region
        
        # Si aucune correspondance, retourner la région originale si elle est valide
        if RegionValidator.is_valid_region(region):
            return region
            
        return None


class PropertyValidator:
    """Validateur pour les données de propriétés"""
    
    @staticmethod
    def is_valid_price(price: Optional[float]) -> bool:
        """
        Vérifie si le prix est valide
        
        Args:
            price: Prix à vérifier
            
        Returns:
            bool: True si le prix est valide
        """
        if price is None:
            return False
        
        # Prix minimum et maximum raisonnables pour le Québec
        min_price = 10000  # 10k$ minimum
        max_price = 50000000  # 50M$ maximum
        
        return min_price <= price <= max_price
    
    @staticmethod
    def is_valid_property_id(property_id: Optional[str]) -> bool:
        """
        Vérifie si l'ID de propriété est valide
        
        Args:
            property_id: ID à vérifier
            
        Returns:
            bool: True si l'ID est valide
        """
        if not property_id:
            return False
        
        # ID doit être une chaîne non vide
        return isinstance(property_id, str) and len(property_id.strip()) > 0
    
    @staticmethod
    def is_valid_postal_code(postal_code: Optional[str]) -> bool:
        """
        Vérifie si le code postal canadien est valide
        
        Args:
            postal_code: Code postal à vérifier
            
        Returns:
            bool: True si le code postal est valide
        """
        if not postal_code:
            return False
        
        # Format canadien: A1A 1A1 ou A1A1A1
        pattern = r'^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d$'
        return bool(re.match(pattern, postal_code.upper().strip()))


class DataValidator:
    """Validateur général pour les données"""
    
    @staticmethod
    def is_valid_coordinates(latitude: Optional[float], longitude: Optional[float]) -> bool:
        """
        Vérifie si les coordonnées géographiques sont valides pour le Québec
        
        Args:
            latitude: Latitude à vérifier
            longitude: Longitude à vérifier
            
        Returns:
            bool: True si les coordonnées sont valides
        """
        if latitude is None or longitude is None:
            return False
        
        # Limites approximatives du Québec
        min_lat, max_lat = 44.0, 62.5
        min_lon, max_lon = -79.8, -57.1
        
        return (min_lat <= latitude <= max_lat and 
                min_lon <= longitude <= max_lon)
    
    @staticmethod
    def clean_text(text: Optional[str]) -> Optional[str]:
        """
        Nettoie et normalise un texte
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            str: Texte nettoyé ou None
        """
        if not text:
            return None
        
        # Supprimer les espaces en début/fin
        cleaned = text.strip()
        
        # Supprimer les caractères de contrôle
        cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)
        
        # Normaliser les espaces multiples
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned if cleaned else None

