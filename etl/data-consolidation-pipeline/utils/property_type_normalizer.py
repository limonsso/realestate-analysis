#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏠 NORMALISATEUR DE TYPES DE PROPRIÉTÉ - Pipeline ETL Ultra-Intelligent
========================================================================

Module de normalisation intelligente des types de propriété immobilière
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
import warnings
import re
from datetime import datetime

# Import conditionnel de MongoDB
try:
    import pymongo
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    warnings.warn("PyMongo non disponible - fonctionnalités MongoDB limitées")

# Import conditionnel de FuzzyWuzzy
try:
    from fuzzywuzzy import fuzz, process
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False
    warnings.warn("FuzzyWuzzy non disponible - similarité limitée")

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class PropertyTypeNormalizer:
    """
    Normalisateur intelligent des types de propriété immobilière
    Supporte français et anglais avec détection automatique
    """
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/",
                 database_name: str = "real_estate_db",
                 collection_name: str = "property_types"):
        """
        Initialise le normalisateur de types de propriété
        
        Args:
            connection_string: Chaîne de connexion MongoDB
            database_name: Nom de la base de données
            collection_name: Nom de la collection des types
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        
        # Mappings par défaut
        self.default_mappings = self._initialize_default_mappings()
        
        # Mappings depuis MongoDB
        self.mongodb_mappings = self._load_mongodb_mappings()
        
        # Configuration de normalisation
        self.normalization_config = {
            "similarity_threshold": 80,
            "case_sensitive": False,
            "fuzzy_matching": FUZZYWUZZY_AVAILABLE,
            "language_detection": True
        }
        
        logger.info("🏠 PropertyTypeNormalizer initialisé")
        logger.info(f"🗄️ MongoDB: {'✅' if MONGODB_AVAILABLE else '❌'}")
        logger.info(f"🧠 FuzzyWuzzy: {'✅' if FUZZYWUZZY_AVAILABLE else '❌'}")
        logger.info(f"📊 Mappings chargés: {len(self.default_mappings) + len(self.mongodb_mappings)}")
    
    def _initialize_default_mappings(self) -> Dict[str, str]:
        """Initialise les mappings par défaut"""
        return {
            # === FRANÇAIS ===
            "maison": "Maison",
            "maison unifamiliale": "Maison",
            "maison de ville": "Maison",
            "maison jumelée": "Maison",
            "maison en rangée": "Maison",
            "maison mobile": "Maison mobile",
            "maison préfabriquée": "Maison préfabriquée",
            
            "appartement": "Appartement",
            "apt": "Appartement",
            "appt": "Appartement",
            "studio": "Studio",
            "loft": "Loft",
            "duplex": "Duplex",
            "triplex": "Triplex",
            "quadruplex": "Quadruplex",
            
            "condo": "Condo",
            "condominium": "Condo",
            "copropriété": "Condo",
            "copropriete": "Condo",
            
            "terrain": "Terrain",
            "lot": "Terrain",
            "parcelle": "Terrain",
            "propriété commerciale": "Commercial",
            "propriete commerciale": "Commercial",
            "bureau": "Commercial",
            "bureaux": "Commercial",
            "entrepôt": "Commercial",
            "entrepot": "Commercial",
            "entrepôt": "Commercial",
            
            # === ANGLAIS ===
            "house": "Maison",
            "single family": "Maison",
            "single-family": "Maison",
            "townhouse": "Maison de ville",
            "town house": "Maison de ville",
            "detached": "Maison",
            "semi-detached": "Maison jumelée",
            "semi detached": "Maison jumelée",
            "row house": "Maison en rangée",
            "mobile home": "Maison mobile",
            "prefabricated": "Maison préfabriquée",
            
            "apartment": "Appartement",
            "flat": "Appartement",
            "unit": "Unité",
            "penthouse": "Penthouse",
            "garden apartment": "Appartement avec jardin",
            "basement apartment": "Appartement sous-sol",
            
            "condominium": "Condo",
            "strata": "Condo",
            "co-op": "Coopérative",
            "cooperative": "Coopérative",
            
            "land": "Terrain",
            "vacant land": "Terrain vacant",
            "building lot": "Terrain constructible",
            "commercial property": "Commercial",
            "office": "Bureau",
            "warehouse": "Entrepôt",
            "retail": "Commerce de détail",
            "industrial": "Industriel",
            
            # === VARIANTES ===
            "1 bedroom": "Appartement 1 chambre",
            "2 bedroom": "Appartement 2 chambres",
            "3 bedroom": "Appartement 3 chambres",
            "4 bedroom": "Appartement 4 chambres",
            "5+ bedroom": "Appartement 5+ chambres",
            
            "1 chambre": "Appartement 1 chambre",
            "2 chambres": "Appartement 2 chambres",
            "3 chambres": "Appartement 3 chambres",
            "4 chambres": "Appartement 4 chambres",
            "5+ chambres": "Appartement 5+ chambres"
        }
    
    def _load_mongodb_mappings(self) -> Dict[str, str]:
        """Charge les mappings depuis MongoDB"""
        if not MONGODB_AVAILABLE:
            return {}
        
        try:
            client = MongoClient(self.connection_string)
            db = client[self.database_name]
            collection = db[self.collection_name]
            
            # Vérification de la connexion
            client.admin.command('ping')
            
            # Récupération des mappings
            mappings = {}
            cursor = collection.find({})
            
            for doc in cursor:
                if 'original' in doc and 'normalized' in doc:
                    mappings[doc['original'].lower()] = doc['normalized']
            
            client.close()
            
            logger.info(f"📊 {len(mappings)} mappings chargés depuis MongoDB")
            return mappings
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur chargement MongoDB: {e}")
            return {}
    
    def normalize_property_type(self, property_type: str) -> str:
        """
        Normalise un type de propriété
        
        Args:
            property_type: Type de propriété à normaliser
            
        Returns:
            Type normalisé
        """
        if pd.isna(property_type) or property_type == "":
            return "Non spécifié"
        
        # Conversion en string et nettoyage
        property_type_str = str(property_type).strip()
        
        if not property_type_str:
            return "Non spécifié"
        
        # Recherche exacte dans les mappings
        normalized = self._exact_match(property_type_str)
        if normalized:
            return normalized
        
        # Recherche par similarité
        normalized = self._fuzzy_match(property_type_str)
        if normalized:
            return normalized
        
        # Normalisation par règles
        normalized = self._rule_based_normalization(property_type_str)
        if normalized:
            return normalized
        
        # Retour du type original si aucune normalisation trouvée
        return property_type_str
    
    def _exact_match(self, property_type: str) -> Optional[str]:
        """Recherche de correspondance exacte"""
        # Recherche dans les mappings par défaut
        if property_type.lower() in self.default_mappings:
            return self.default_mappings[property_type.lower()]
        
        # Recherche dans les mappings MongoDB
        if property_type.lower() in self.mongodb_mappings:
            return self.mongodb_mappings[property_type.lower()]
        
        return None
    
    def _fuzzy_match(self, property_type: str) -> Optional[str]:
        """Recherche par similarité floue"""
        if not FUZZYWUZZY_AVAILABLE:
            return None
        
        try:
            # Recherche dans les mappings par défaut
            best_match = process.extractOne(
                property_type.lower(),
                self.default_mappings.keys(),
                scorer=fuzz.ratio
            )
            
            if best_match and best_match[1] >= self.normalization_config["similarity_threshold"]:
                return self.default_mappings[best_match[0]]
            
            # Recherche dans les mappings MongoDB
            if self.mongodb_mappings:
                best_match = process.extractOne(
                    property_type.lower(),
                    self.mongodb_mappings.keys(),
                    scorer=fuzz.ratio
                )
                
                if best_match and best_match[1] >= self.normalization_config["similarity_threshold"]:
                    return self.mongodb_mappings[best_match[0]]
            
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur fuzzy matching: {e}")
            return None
    
    def _rule_based_normalization(self, property_type: str) -> Optional[str]:
        """Normalisation basée sur des règles"""
        property_type_lower = property_type.lower()
        
        # Détection de la langue
        is_french = self._detect_french(property_type_lower)
        is_english = self._detect_english(property_type_lower)
        
        # Règles de normalisation
        if is_french:
            return self._apply_french_rules(property_type_lower)
        elif is_english:
            return self._apply_english_rules(property_type_lower)
        else:
            return self._apply_generic_rules(property_type_lower)
    
    def _detect_french(self, text: str) -> bool:
        """Détecte si le texte est en français"""
        french_indicators = [
            "maison", "appartement", "chambre", "propriété", "propriete",
            "terrain", "commercial", "bureau", "entrepôt", "entrepot"
        ]
        
        return any(indicator in text for indicator in french_indicators)
    
    def _detect_english(self, text: str) -> bool:
        """Détecte si le texte est en anglais"""
        english_indicators = [
            "house", "apartment", "bedroom", "property", "land",
            "commercial", "office", "warehouse", "condo", "condominium"
        ]
        
        return any(indicator in text for indicator in english_indicators)
    
    def _apply_french_rules(self, text: str) -> str:
        """Applique les règles de normalisation françaises"""
        if "maison" in text:
            if "unifamiliale" in text:
                return "Maison unifamiliale"
            elif "ville" in text:
                return "Maison de ville"
            elif "jumelée" in text or "jumelée" in text:
                return "Maison jumelée"
            else:
                return "Maison"
        
        elif "appartement" in text or "apt" in text:
            if "studio" in text:
                return "Studio"
            elif "duplex" in text:
                return "Duplex"
            elif "loft" in text:
                return "Loft"
            else:
                return "Appartement"
        
        elif "condo" in text or "condominium" in text:
            return "Condo"
        
        elif "terrain" in text or "lot" in text:
            return "Terrain"
        
        elif "commercial" in text or "bureau" in text:
            return "Commercial"
        
        return text.title()
    
    def _apply_english_rules(self, text: str) -> str:
        """Applique les règles de normalisation anglaises"""
        if "house" in text:
            if "single" in text and "family" in text:
                return "Single Family House"
            elif "town" in text:
                return "Townhouse"
            elif "detached" in text:
                return "Detached House"
            elif "semi" in text and "detached" in text:
                return "Semi-Detached House"
            else:
                return "House"
        
        elif "apartment" in text or "apt" in text:
            if "studio" in text:
                return "Studio"
            elif "penthouse" in text:
                return "Penthouse"
            else:
                return "Apartment"
        
        elif "condo" in text or "condominium" in text:
            return "Condominium"
        
        elif "land" in text:
            return "Land"
        
        elif "commercial" in text or "office" in text:
            return "Commercial"
        
        return text.title()
    
    def _apply_generic_rules(self, text: str) -> str:
        """Applique des règles génériques de normalisation"""
        # Suppression des caractères spéciaux
        cleaned = re.sub(r'[^\w\s]', ' ', text)
        
        # Normalisation des espaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Capitalisation
        return cleaned.title()
    
    def normalize_dataframe(self, df: pd.DataFrame, column_name: str = "property_type") -> pd.DataFrame:
        """
        Normalise une colonne de types de propriété dans un DataFrame
        
        Args:
            df: DataFrame à normaliser
            column_name: Nom de la colonne à normaliser
            
        Returns:
            DataFrame avec la colonne normalisée
        """
        if column_name not in df.columns:
            logger.warning(f"⚠️ Colonne '{column_name}' non trouvée")
            return df
        
        logger.info(f"🔄 Normalisation de la colonne '{column_name}'")
        
        # Sauvegarde de la colonne originale
        original_column = f"{column_name}_original"
        df[original_column] = df[column_name].copy()
        
        # Application de la normalisation
        df[column_name] = df[column_name].apply(self.normalize_property_type)
        
        # Statistiques de normalisation
        unique_original = df[original_column].nunique()
        unique_normalized = df[column_name].nunique()
        reduction = ((unique_original - unique_normalized) / unique_original) * 100
        
        logger.info(f"✅ Normalisation terminée:")
        logger.info(f"   Types originaux: {unique_original}")
        logger.info(f"   Types normalisés: {unique_normalized}")
        logger.info(f"   Réduction: {reduction:.1f}%")
        
        return df
    
    def get_normalization_stats(self, df: pd.DataFrame, column_name: str = "property_type") -> Dict[str, Any]:
        """
        Génère des statistiques de normalisation
        
        Args:
            df: DataFrame analysé
            column_name: Nom de la colonne analysée
            
        Returns:
            Dict avec les statistiques
        """
        if column_name not in df.columns:
            return {"error": f"Colonne '{column_name}' non trouvée"}
        
        # Statistiques de base
        total_values = len(df[column_name])
        null_values = df[column_name].isnull().sum()
        unique_values = df[column_name].nunique()
        
        # Distribution des types
        type_distribution = df[column_name].value_counts().head(10).to_dict()
        
        # Valeurs les plus fréquentes
        most_common = df[column_name].mode().tolist()
        
        stats = {
            "total_values": total_values,
            "null_values": null_values,
            "non_null_values": total_values - null_values,
            "unique_values": unique_values,
            "type_distribution": type_distribution,
            "most_common": most_common,
            "normalization_ratio": unique_values / (total_values - null_values) if (total_values - null_values) > 0 else 0
        }
        
        return stats
    
    def add_property_type_mapping(self, original: str, normalized: str, 
                                  source: str = "manual") -> bool:
        """
        Ajoute un nouveau mapping de type de propriété
        
        Args:
            original: Type original
            normalized: Type normalisé
            source: Source du mapping
            
        Returns:
            True si ajouté avec succès
        """
        try:
            # Ajout au mapping par défaut
            self.default_mappings[original.lower()] = normalized
            
            # Sauvegarde dans MongoDB si disponible
            if MONGODB_AVAILABLE:
                self._save_mapping_to_mongodb(original, normalized, source)
            
            logger.info(f"✅ Mapping ajouté: '{original}' → '{normalized}'")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur ajout mapping: {e}")
            return False
    
    def _save_mapping_to_mongodb(self, original: str, normalized: str, source: str):
        """Sauvegarde un mapping dans MongoDB"""
        try:
            client = MongoClient(self.connection_string)
            db = client[self.database_name]
            collection = db[self.collection_name]
            
            # Vérification si le mapping existe déjà
            existing = collection.find_one({"original": original})
            
            if existing:
                # Mise à jour
                collection.update_one(
                    {"original": original},
                    {"$set": {"normalized": normalized, "source": source, "updated_at": datetime.now()}}
                )
            else:
                # Insertion
                collection.insert_one({
                    "original": original,
                    "normalized": normalized,
                    "source": source,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })
            
            client.close()
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur sauvegarde MongoDB: {e}")
    
    def export_mappings(self, output_file: str = "property_type_mappings.json") -> bool:
        """
        Exporte tous les mappings dans un fichier JSON
        
        Args:
            output_file: Fichier de sortie
            
        Returns:
            True si export réussi
        """
        try:
            all_mappings = {}
            all_mappings.update(self.default_mappings)
            all_mappings.update(self.mongodb_mappings)
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_mappings": len(all_mappings),
                "default_mappings": self.default_mappings,
                "mongodb_mappings": self.mongodb_mappings,
                "normalization_config": self.normalization_config
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"💾 Mappings exportés: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur export mappings: {e}")
            return False
