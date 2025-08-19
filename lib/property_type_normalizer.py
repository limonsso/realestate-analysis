"""
Normalisateur de types de propriétés
Utilise la collection property_types de MongoDB
Language-agnostic: peut normaliser quelque soit la langue d'entrée
"""

import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PropertyTypeNormalizer:
    """Normalise les types de propriétés selon property_types (language-agnostic)"""
    
    def __init__(self, property_types_data: List[Dict] = None, default_language: str = 'fr'):
        """
        Args:
            property_types_data: Données des types de propriétés
            default_language: Langue par défaut pour l'affichage ('fr' ou 'en')
        """
        self.default_language = default_language
        self.property_types_map = {}  # nom -> type_id
        self.display_names_map = {}   # type_id -> nom d'affichage par défaut
        self.category_map = {}        # catégorie -> [type_ids]
        self.all_display_names = {}   # type_id -> {lang: nom}
        
        if property_types_data:
            self._build_mappings(property_types_data)
    
    @classmethod
    def create_from_mongodb(cls, database_name: str = "real_estate_db", 
                           connection_string: str = "mongodb://localhost:27017/",
                           default_language: str = 'fr'):
        """
        Crée un normalisateur en chargeant les types depuis MongoDB
        
        Args:
            database_name: Nom de la base de données
            connection_string: Chaîne de connexion MongoDB
            default_language: Langue par défaut pour l'affichage ('fr' ou 'en')
            
        Returns:
            PropertyTypeNormalizer: Instance configurée avec les données MongoDB
        """
        from .mongodb_loader import MongoDBLoader
        
        print(f"🔗 Connexion à MongoDB: {database_name}")
        loader = MongoDBLoader(connection_string)
        
        if not loader.connect(database_name):
            raise ConnectionError(f"Impossible de se connecter à MongoDB: {database_name}")
        
        try:
            property_types = loader.load_property_types()
            if not property_types:
                raise ValueError("Aucun type de propriété trouvé dans la collection property_types")
            
            normalizer = cls(property_types_data=property_types, default_language=default_language)
            logger.info(f"✅ Normalisateur créé avec {len(property_types)} types depuis MongoDB")
            return normalizer
            
        finally:
            loader.disconnect()
    
    def load_from_mongodb(self, database_name: str = "real_estate_db", 
                         connection_string: str = "mongodb://localhost:27017/"):
        """
        Charge les types de propriétés depuis MongoDB
        
        Args:
            database_name: Nom de la base de données
            connection_string: Chaîne de connexion MongoDB
        """
        from .mongodb_loader import MongoDBLoader
        
        print(f"🔗 Chargement des types depuis MongoDB: {database_name}")
        loader = MongoDBLoader(connection_string)
        
        if not loader.connect(database_name):
            raise ConnectionError(f"Impossible de se connecter à MongoDB: {database_name}")
        
        try:
            property_types = loader.load_property_types()
            if not property_types:
                raise ValueError("Aucun type de propriété trouvé dans la collection property_types")
            
            self._build_mappings(property_types)
            logger.info(f"✅ {len(property_types)} types chargés depuis MongoDB")
            
        finally:
            loader.disconnect()
    
    def _build_mappings(self, property_types_data: List[Dict]):
        """Construit les mappings pour la normalisation (toutes langues)"""
        logger.info("🔧 Construction des mappings de types (language-agnostic)...")
        
        # Réinitialiser les mappings
        self.property_types_map = {}
        self.display_names_map = {}
        self.category_map = {}
        self.all_display_names = {}
        
        for prop_type in property_types_data:
            type_id = prop_type.get('_id')
            if not type_id:
                continue
            
            # Stocker tous les noms d'affichage
            display_names = prop_type.get('display_names', {})
            self.all_display_names[type_id] = display_names
            
            # Nom d'affichage par défaut
            default_name = display_names.get(self.default_language, 
                                           display_names.get('en', type_id))
            self.display_names_map[type_id] = default_name
            
            # Créer des mappings pour TOUTES les langues disponibles
            for lang, name in display_names.items():
                if name and name.strip():
                    # Mapping nom -> type_id pour chaque langue
                    self.property_types_map[name] = type_id
                    self.property_types_map[name.strip()] = type_id
                    
                    # Ajouter des variations pour cette langue
                    self._add_variations(type_id, name, lang)
            
            # Si pas de display_names, utiliser l'ID
            if not display_names:
                self.property_types_map[type_id] = type_id
                self._add_variations(type_id, type_id, 'generic')
            
            # Mapping par catégorie
            category = prop_type.get('category', 'Autre')
            if category not in self.category_map:
                self.category_map[category] = []
            self.category_map[category].append(type_id)
        
        print(f"✅ Mappings construits: {len(self.property_types_map)} variations pour {len(self.display_names_map)} types")
        print(f"   🌐 Langues supportées: {self._get_supported_languages()}")
    
    def _add_variations(self, type_id: str, display_name: str, language: str = 'generic'):
        """Ajoute des variations courantes pour toutes les langues"""
        base_name = display_name.replace(' à vendre', '').replace(' for sale', '').strip()
        
        # Variations de base
        variations = [
            base_name,
            base_name.lower(),
            base_name.upper(),
            base_name.capitalize(),
            base_name.title(),
        ]
        
        # Variations sans accents (pour le français)
        if language == 'fr' or language == 'generic':
            variations.extend([
                base_name.replace('é', 'e').replace('è', 'e').replace('ê', 'e'),
                base_name.replace('à', 'a').replace('â', 'a'),
                base_name.replace('ç', 'c'),
                base_name.replace('ô', 'o').replace('ö', 'o'),
                base_name.replace('ü', 'u').replace('ù', 'u'),
            ])
        
        # Variations spécifiques par type (multilingue)
        base_lower = base_name.lower()
        
        # Maison/House
        if any(word in base_lower for word in ['maison', 'house', 'home']):
            variations.extend([
                'Maison', 'House', 'Home', 'maison', 'house', 'home',
                'Maison à vendre', 'House for sale', 'Home for sale',
                'Résidence', 'Residence', 'résidence', 'residence'
            ])
        
        # Condo/Condominium
        elif any(word in base_lower for word in ['condo', 'condominium']):
            variations.extend([
                'Condo', 'Condominium', 'condo', 'condominium',
                'Condo à vendre', 'Condo for sale','Loft', 'Studio for sale',
                'Condominium à vendre', 'Condominium for sale'
            ])
        
        # Duplex
        elif 'duplex' in base_lower:
            variations.extend([
                'Duplex', 'duplex', 'Duplex à vendre', 'Duplex for sale'
            ])
        
        # Triplex
        elif 'triplex' in base_lower:
            variations.extend([
                'Triplex', 'triplex', 'Triplex à vendre', 'Triplex for sale'
            ])
        
        # Quadruplex
        elif 'quadruplex' in base_lower:
            variations.extend([
                'Quadruplex', 'quadruplex', 'Quadruplex à vendre', 'Quadruplex for sale'
            ])
        
        # Appartement/Apartment
        elif any(word in base_lower for word in ['appartement', 'apartment', 'apt']):
            variations.extend([
                'Appartement', 'Apartment', 'appartement', 'apartment',
                'Apt', 'apt', 'Appt', 'appt'
            ])
        
        # Terrain/Land
        elif any(word in base_lower for word in ['terrain', 'land', 'lot']):
            variations.extend([
                'Terrain', 'Land', 'terrain', 'land','Terre','Terre à vendre',
                'Lot', 'lot', 'Terrain à vendre', 'Land for sale'
            ])
        
        # Ajouter toutes les variations uniques
        for variation in set(variations):
            if variation and variation.strip() and variation not in self.property_types_map:
                self.property_types_map[variation.strip()] = type_id
    
    def _get_supported_languages(self) -> List[str]:
        """Retourne la liste des langues supportées"""
        languages = set()
        for display_names in self.all_display_names.values():
            languages.update(display_names.keys())
        return sorted(list(languages))
    
    def normalize_property_types(self, df: pd.DataFrame, type_column: str = 'type') -> pd.DataFrame:
        """Normalise les types de propriétés (language-agnostic)"""
        if type_column not in df.columns:
            logger.warning(f"Colonne '{type_column}' non trouvée")
            return df
        
        logger.info(f"🏠 Normalisation des types de propriétés (toutes langues)...")
        
        df_normalized = df.copy()
        
        # Statistiques avant
        original_types = df_normalized[type_column].value_counts()
        print(f"\n📊 Types avant normalisation:")
        for prop_type, count in original_types.head(10).items():
            print(f"   📝 {prop_type}: {count} propriétés")
        
        # Normaliser
        normalized_types = []
        unrecognized_types = set()
        
        for prop_type in df_normalized[type_column]:
            if pd.isna(prop_type):
                normalized_types.append('unknown')
                continue
            
            normalized_type = self._normalize_single_type(str(prop_type))
            normalized_types.append(normalized_type)
            
            if normalized_type == 'unknown':
                unrecognized_types.add(str(prop_type))
        
        # Remplacer la colonne type par le type_id
        df_normalized[f'{type_column}_id'] = normalized_types
        
        # Ajouter colonne avec nom d'affichage
        df_normalized[f'{type_column}_display'] = df_normalized[f'{type_column}_id'].map(
            lambda x: self.display_names_map.get(x, x) if x != 'unknown' else 'unknown'
        )
        
        # Ajouter colonne catégorie
        df_normalized[f'{type_column}_category'] = df_normalized[f'{type_column}_id'].apply(
            self._get_category_for_type
        )
        
        # Statistiques après
        normalized_counts = df_normalized[f'{type_column}_id'].value_counts()
        print(f"\n✅ Types après normalisation:")
        for type_id, count in normalized_counts.head(10).items():
            display_name = self.display_names_map.get(type_id, type_id)
            print(f"   🏷️ {display_name} ({type_id}): {count} propriétés")
        
        # Types non reconnus
        if unrecognized_types:
            print(f"\n⚠️ Types non reconnus ({len(unrecognized_types)}):")
            for unrecognized in sorted(unrecognized_types)[:10]:
                print(f"   ❓ {unrecognized}")
        
        return df_normalized
    
    def _normalize_single_type(self, prop_type: str) -> str:
        """Normalise un seul type (language-agnostic)"""
        clean_type = str(prop_type).strip()
        
        # Correspondance exacte
        if clean_type in self.property_types_map:
            return self.property_types_map[clean_type]
        
        # Correspondance partielle
        for known_type, type_id in self.property_types_map.items():
            if self._fuzzy_match(clean_type, known_type):
                return type_id
        
        return 'unknown'
    
    def _fuzzy_match(self, input_type: str, known_type: str) -> bool:
        """Vérifie correspondance approximative (language-agnostic)"""
        input_clean = input_type.lower().replace(' ', '').replace('-', '').replace('_', '')
        known_clean = known_type.lower().replace(' ', '').replace('-', '').replace('_', '')
        
        # Correspondance exacte
        if input_clean == known_clean:
            return True
        
        # Correspondance par inclusion
        if input_clean in known_clean or known_clean in input_clean:
            return True
        
        # Correspondance par mots
        input_words = set(input_clean.split())
        known_words = set(known_clean.split())
        
        if input_words & known_words:
            return True
        
        return False
    
    def _get_category_for_type(self, type_id: str) -> str:
        """Retourne la catégorie pour un type donné"""
        for category, type_ids in self.category_map.items():
            if type_id in type_ids:
                return category
        return 'Autre'
    
    def get_property_categories(self) -> Dict[str, List[str]]:
        """Retourne les catégories avec leurs types"""
        return self.category_map.copy()
    
    def get_all_display_names(self) -> Dict[str, Dict[str, str]]:
        """Retourne tous les noms d'affichage par langue"""
        return self.all_display_names.copy()
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques détaillées"""
        return {
            'total_types': len(self.display_names_map),
            'total_variations': len(self.property_types_map),
            'categories': list(self.category_map.keys()),
            'category_counts': {cat: len(types) for cat, types in self.category_map.items()},
            'supported_languages': self._get_supported_languages(),
            'default_language': self.default_language
        } 