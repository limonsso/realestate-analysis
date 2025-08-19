#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 NETTOYAGE EXPERT DU DATASET IMMOBILIER
==========================================

Script de nettoyage complet selon les spécifications real_estate_prompt.md
Implémente toutes les phases : Audit, Nettoyage, Enrichissement, Validation
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime, date
import re
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealEstateDataCleaner:
    """Classe principale pour le nettoyage des données immobilières"""
    
    def __init__(self, input_file: str = None, mongodb_connection: str = None):
        """
        Initialise le nettoyeur de données
        
        Args:
            input_file: Chemin vers le fichier CSV/Excel à nettoyer
            mongodb_connection: Chaîne de connexion MongoDB
        """
        self.input_file = input_file
        self.mongodb_connection = mongodb_connection
        self.df = None
        self.df_cleaned = None
        self.quality_report = {}
        
    def load_data(self, source: str = "mongodb") -> bool:
        """
        Charge les données depuis la source spécifiée
        
        Args:
            source: "mongodb" ou "file"
        """
        try:
            if source == "mongodb" and self.mongodb_connection:
                logger.info("🔄 Chargement depuis MongoDB...")
                # TODO: Implémenter chargement MongoDB
                return False
            elif self.input_file:
                logger.info(f"📁 Chargement depuis le fichier: {self.input_file}")
                if self.input_file.endswith('.csv'):
                    self.df = pd.read_csv(self.input_file)
                elif self.input_file.endswith('.xlsx'):
                    self.df = pd.read_excel(self.input_file)
                elif self.input_file.endswith('.json'):
                    self.df = pd.read_json(self.input_file)
                else:
                    logger.error("❌ Format de fichier non supporté")
                    return False
                
                logger.info(f"✅ Données chargées: {self.df.shape}")
                return True
            else:
                logger.error("❌ Aucune source de données spécifiée")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def phase1_audit_diagnostic(self) -> Dict:
        """
        PHASE 1: AUDIT & DIAGNOSTIC COMPLET
        Analyse exploratoire et détection des problèmes
        """
        logger.info("🔍 PHASE 1: AUDIT & DIAGNOSTIC COMPLET")
        
        if self.df is None:
            logger.error("❌ Aucune donnée chargée")
            return {}
        
        audit_results = {}
        
        # 1. Dimensions et utilisation mémoire
        audit_results['dimensions'] = {
            'shape': self.df.shape,
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'dtypes': self.df.dtypes.value_counts().to_dict()
        }
        
        # 2. Analyse des valeurs manquantes
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        
        audit_results['missing_data'] = {
            'total_missing': missing_data.sum(),
            'missing_percent': missing_percent.to_dict(),
            'columns_with_missing': missing_data[missing_data > 0].to_dict()
        }
        
        # 3. Détection des doublons
        duplicates = self.df.duplicated().sum()
        audit_results['duplicates'] = {
            'total_duplicates': duplicates,
            'duplicate_percent': (duplicates / len(self.df)) * 100
        }
        
        # 4. Analyse des colonnes problématiques identifiées
        problematic_columns = {
            'revenu_variants': ['revenu', 'plex-revenue', 'plex-revenu'],
            'date_columns': ['created_at', 'updated_at', 'update_at', 'add_date'],
            'surface_columns': ['surface', 'living_area'],
            'year_columns': ['construction_year', 'year_built'],
            'tax_columns': ['municipal_taxes', 'municipal_tax'],
            'bedroom_columns': ['bedrooms', 'nb_bedroom']
        }
        
        audit_results['problematic_columns'] = {}
        for category, cols in problematic_columns.items():
            existing_cols = [col for col in cols if col in self.df.columns]
            if existing_cols:
                audit_results['problematic_columns'][category] = existing_cols
        
        # 5. Statistiques descriptives de base
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            audit_results['numeric_stats'] = self.df[numeric_columns].describe().to_dict()
        
        logger.info(f"✅ Audit terminé: {len(audit_results)} analyses effectuées")
        return audit_results
    
    def phase2_cleaning_intelligent(self) -> bool:
        """
        PHASE 2: NETTOYAGE INTELLIGENT
        Déduplication, consolidation et standardisation
        """
        logger.info("🛠️ PHASE 2: NETTOYAGE INTELLIGENT")
        
        if self.df is None:
            logger.error("❌ Aucune donnée chargée")
            return False
        
        try:
            self.df_cleaned = self.df.copy()
            
            # 1. Standardisation des noms de colonnes
            self._standardize_column_names()
            
            # 2. Consolidation des colonnes redondantes
            self._consolidate_redundant_columns()
            
            # 3. Nettoyage des variables financières
            self._clean_financial_variables()
            
            # 4. Nettoyage des caractéristiques physiques
            self._clean_physical_characteristics()
            
            # 5. Nettoyage de la géolocalisation
            self._clean_geolocation()
            
            # 6. Élimination des doublons
            self._remove_duplicates()
            
            logger.info("✅ Nettoyage intelligent terminé")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage: {e}")
            return False
    
    def _standardize_column_names(self):
        """Standardise les noms de colonnes en snake_case"""
        logger.info("🔄 Standardisation des noms de colonnes...")
        
        # Règles de standardisation
        column_mapping = {
            'nb_bedroom': 'bedrooms',
            'nb_bathroom': 'bathrooms',
            'plex-revenue': 'plex_revenue',
            'plex-revenu': 'plex_revenue',
            'municipal_taxes': 'municipal_tax',
            'school_taxes': 'school_tax',
            'year_built': 'construction_year',
            'living_area': 'surface',
            'unites': 'units',
            'residential_units': 'residential_units',
            'commercial_units': 'commercial_units'
        }
        
        # Appliquer le mapping
        self.df_cleaned = self.df_cleaned.rename(columns=column_mapping)
        
        # Convertir en snake_case
        self.df_cleaned.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in self.df_cleaned.columns]
        
        logger.info(f"✅ Colonnes standardisées: {len(self.df_cleaned.columns)}")
    
    def _consolidate_redundant_columns(self):
        """Consolide les colonnes redondantes"""
        logger.info("🔄 Consolidation des colonnes redondantes...")
        
        # Consolidation des revenus - utiliser les noms après standardisation
        revenue_columns = ['revenu', 'plex_revenue']
        existing_revenue_cols = [col for col in revenue_columns if col in self.df_cleaned.columns]
        
        if len(existing_revenue_cols) > 1:
            # Créer une colonne consolidée de manière plus robuste
            try:
                # Vérifier que les colonnes existent et sont des Series
                for col in existing_revenue_cols:
                    if col in self.df_cleaned.columns:
                        if not isinstance(self.df_cleaned[col], pd.Series):
                            logger.warning(f"Colonne {col} n'est pas une Series: {type(self.df_cleaned[col])}")
                            # Forcer la conversion en Series
                            self.df_cleaned[col] = pd.Series(self.df_cleaned[col].values.flatten() if hasattr(self.df_cleaned[col], 'values') else self.df_cleaned[col])
                
                # Créer la colonne consolidée
                self.df_cleaned['revenue_consolidated'] = self.df_cleaned[existing_revenue_cols].fillna(0).sum(axis=1)
                # Supprimer les colonnes originales
                self.df_cleaned = self.df_cleaned.drop(columns=existing_revenue_cols)
                logger.info("✅ Colonnes de revenus consolidées")
            except Exception as e:
                logger.error(f"Erreur lors de la consolidation des revenus: {e}")
                # Fallback: garder seulement la première colonne
                if existing_revenue_cols:
                    self.df_cleaned['revenue_consolidated'] = self.df_cleaned[existing_revenue_cols[0]]
                    self.df_cleaned = self.df_cleaned.drop(columns=existing_revenue_cols[1:])
                    logger.info("✅ Fallback: première colonne de revenu conservée")
        elif len(existing_revenue_cols) == 1:
            # Une seule colonne de revenu, la renommer
            col_name = existing_revenue_cols[0]
            self.df_cleaned['revenue_consolidated'] = self.df_cleaned[col_name]
            self.df_cleaned = self.df_cleaned.drop(columns=[col_name])
            logger.info(f"✅ Colonne de revenu {col_name} renommée en revenue_consolidated")
        else:
            logger.warning("Aucune colonne de revenu trouvée")
        
        # Consolidation des dates
        date_columns = ['created_at', 'updated_at', 'update_at', 'add_date']
        existing_date_cols = [col for col in date_columns if col in self.df_cleaned.columns]
        
        if len(existing_date_cols) > 1:
            # Convertir en datetime et prendre la plus récente
            for col in existing_date_cols:
                self.df_cleaned[col] = pd.to_datetime(self.df_cleaned[col], errors='coerce')
            
            self.df_cleaned['date_consolidated'] = self.df_cleaned[existing_date_cols].max(axis=1)
            # Garder seulement la date consolidée
            self.df_cleaned = self.df_cleaned.drop(columns=existing_date_cols)
            logger.info("✅ Colonnes de dates consolidées")
    
    def _clean_financial_variables(self):
        """Nettoie les variables financières"""
        logger.info("💰 Nettoyage des variables financières...")
        
        # Nettoyage des prix
        if 'price' in self.df_cleaned.columns:
            self.df_cleaned['price'] = self._clean_numeric_column(self.df_cleaned['price'])
        
        # Nettoyage des revenus
        if 'revenue_consolidated' in self.df_cleaned.columns:
            self.df_cleaned['revenue_consolidated'] = self._clean_numeric_column(self.df_cleaned['revenue_consolidated'])
        
        # Nettoyage des taxes
        tax_columns = ['municipal_tax', 'school_tax']
        for col in tax_columns:
            if col in self.df_cleaned.columns:
                self.df_cleaned[col] = self._clean_numeric_column(self.df_cleaned[col])
        
        # Nettoyage des évaluations municipales
        eval_columns = ['municipal_evaluation_building', 'municipal_evaluation_land', 'municipal_evaluation_total']
        for col in eval_columns:
            if col in self.df_cleaned.columns:
                self.df_cleaned[col] = self._clean_numeric_column(self.df_cleaned[col])
        
        logger.info("✅ Variables financières nettoyées")
    
    def _clean_numeric_column(self, series: pd.Series) -> pd.Series:
        """Nettoie une colonne numérique"""
        try:
            if hasattr(series, 'dtype') and str(series.dtype) == 'object':
                # Supprimer les symboles monétaires et caractères spéciaux
                cleaned = series.astype(str).str.replace(r'[\$,€£¥\s,]', '', regex=True)
                # Convertir en numérique
                cleaned = pd.to_numeric(cleaned, errors='coerce')
            else:
                cleaned = series
        except Exception as e:
            # Fallback: essayer de convertir directement
            cleaned = pd.to_numeric(series, errors='coerce')
        
        return cleaned
    
    def _clean_physical_characteristics(self):
        """Nettoie les caractéristiques physiques"""
        logger.info("🏠 Nettoyage des caractéristiques physiques...")
        
        try:
            # Nettoyage des surfaces
            if 'surface' in self.df_cleaned.columns:
                logger.info("  - Nettoyage de surface...")
                try:
                    # Vérifier et corriger le type de la colonne
                    if not isinstance(self.df_cleaned['surface'], pd.Series):
                        logger.warning(f"    Colonne surface n'est pas une Series: {type(self.df_cleaned['surface'])}")
                        # Forcer la conversion en Series
                        self.df_cleaned['surface'] = pd.Series(self.df_cleaned['surface'].values.flatten() if hasattr(self.df_cleaned['surface'], 'values') else self.df_cleaned['surface'])
                        logger.info("    Colonne surface convertie en Series")
                    
                    self.df_cleaned['surface'] = self._clean_numeric_column(self.df_cleaned['surface'])
                    logger.info("    Surface nettoyée avec succès")
                except Exception as e:
                    logger.error(f"    Erreur lors du nettoyage de surface: {e}")
                    raise
            
            # Nettoyage des chambres et salles de bain
            bedroom_cols = ['bedrooms', 'bathrooms']
            for col in bedroom_cols:
                if col in self.df_cleaned.columns:
                    logger.info(f"  - Nettoyage de {col}...")
                    try:
                        logger.info(f"    Type de {col} avant conversion: {type(self.df_cleaned[col])}")
                        
                        # Vérifier et corriger le type de la colonne
                        if not isinstance(self.df_cleaned[col], pd.Series):
                            logger.warning(f"    Colonne {col} n'est pas une Series: {type(self.df_cleaned[col])}")
                            
                            # Méthode plus robuste pour convertir en Series
                            try:
                                if hasattr(self.df_cleaned[col], 'values'):
                                    if hasattr(self.df_cleaned[col].values, 'flatten'):
                                        # DataFrame avec valeurs multidimensionnelles
                                        values = self.df_cleaned[col].values.flatten()
                                    else:
                                        # DataFrame simple
                                        values = self.df_cleaned[col].values
                                else:
                                    # Autre type d'objet
                                    values = self.df_cleaned[col]
                                
                                # Créer une nouvelle Series
                                self.df_cleaned[col] = pd.Series(values, index=self.df_cleaned.index)
                                logger.info(f"    Colonne {col} convertie en Series avec {len(self.df_cleaned[col])} valeurs")
                                
                            except Exception as conv_error:
                                logger.error(f"    Erreur lors de la conversion: {conv_error}")
                                # Fallback: essayer de récupérer la première colonne si c'est un DataFrame
                                if hasattr(self.df_cleaned[col], 'iloc'):
                                    try:
                                        # Récupérer la première colonne et s'assurer qu'elle a la bonne longueur
                                        first_col = self.df_cleaned[col].iloc[:, 0]
                                        if len(first_col) == len(self.df_cleaned):
                                            # S'assurer que c'est bien une Series et l'assigner correctement
                                            if isinstance(first_col, pd.Series):
                                                self.df_cleaned[col] = first_col.values
                                            else:
                                                self.df_cleaned[col] = pd.Series(first_col.values, index=self.df_cleaned.index)
                                            logger.info(f"    Fallback: première colonne de {col} utilisée avec {len(first_col)} valeurs")
                                        else:
                                            # Ajuster la longueur si nécessaire
                                            if len(first_col) > len(self.df_cleaned):
                                                truncated_values = first_col[:len(self.df_cleaned)].values
                                                self.df_cleaned[col] = pd.Series(truncated_values, index=self.df_cleaned.index)
                                                logger.info(f"    Fallback: première colonne de {col} tronquée à {len(self.df_cleaned)} valeurs")
                                            else:
                                                # Étendre avec des valeurs NaN si nécessaire
                                                extended_values = [first_col.iloc[i] if i < len(first_col) else pd.NA for i in range(len(self.df_cleaned))]
                                                self.df_cleaned[col] = pd.Series(extended_values, index=self.df_cleaned.index)
                                                logger.info(f"    Fallback: première colonne de {col} étendue à {len(self.df_cleaned)} valeurs")
                                    except Exception as fallback_error:
                                        logger.error(f"    Erreur lors du fallback: {fallback_error}")
                                        raise ValueError(f"Impossible de convertir {col} en Series")
                                else:
                                    raise ValueError(f"Impossible de convertir {col} en Series")
                        
                        # Vérifier à nouveau après conversion
                        if not isinstance(self.df_cleaned[col], pd.Series):
                            logger.error(f"    Échec de la conversion de {col} en Series")
                            raise ValueError(f"Impossible de convertir {col} en Series")
                        
                        logger.info(f"    Valeurs de {col} avant conversion: {self.df_cleaned[col].head().tolist()}")
                        
                        # Vérifier si c'est déjà numérique
                        if pd.api.types.is_numeric_dtype(self.df_cleaned[col]):
                            logger.info(f"    {col} est déjà numérique, pas de conversion nécessaire")
                        else:
                            self.df_cleaned[col] = pd.to_numeric(self.df_cleaned[col], errors='coerce')
                            logger.info(f"    {col} converti en numérique")
                        
                        # Remplacer les valeurs aberrantes par la médiane
                        median_val = self.df_cleaned[col].median()
                        if pd.notna(median_val):
                            self.df_cleaned[col] = self.df_cleaned[col].fillna(median_val)
                            logger.info(f"    Valeurs manquantes remplacées par la médiane: {median_val}")
                        else:
                            logger.warning(f"    Médiane non disponible pour {col}")
                    except Exception as e:
                        logger.error(f"    Erreur lors du nettoyage de {col}: {e}")
                        logger.error(f"    Type de {col}: {type(self.df_cleaned[col])}")
                        logger.error(f"    Valeurs de {col}: {self.df_cleaned[col].head().tolist() if hasattr(self.df_cleaned[col], 'head') else 'Pas de méthode head'}")
                        raise
            
            # Nettoyage des années de construction
            if 'construction_year' in self.df_cleaned.columns:
                logger.info("  - Nettoyage de construction_year...")
                try:
                    # Convertir en numérique
                    self.df_cleaned['construction_year'] = pd.to_numeric(self.df_cleaned['construction_year'], errors='coerce')
                    logger.info(f"    Converti en numérique: {self.df_cleaned['construction_year'].dtype}")
                    
                    # Filtrer les années réalistes (1800-2024) de manière plus robuste
                    try:
                        self.df_cleaned['construction_year'] = self.df_cleaned['construction_year'].clip(1800, 2024)
                        logger.info("    Clip appliqué avec succès")
                    except Exception as clip_error:
                        logger.warning(f"    Clip échoué: {clip_error}, utilisation du fallback")
                        # Fallback: filtrer manuellement
                        mask = (self.df_cleaned['construction_year'] >= 1800) & (self.df_cleaned['construction_year'] <= 2024)
                        self.df_cleaned.loc[~mask, 'construction_year'] = np.nan
                        logger.info("    Fallback appliqué")
                except Exception as e:
                    logger.error(f"    Erreur lors du nettoyage de construction_year: {e}")
                    raise
            
            logger.info("✅ Caractéristiques physiques nettoyées")
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage des caractéristiques physiques: {e}")
            raise
    
    def _clean_geolocation(self):
        """Nettoie la géolocalisation"""
        logger.info("📍 Nettoyage de la géolocalisation...")
        
        # Nettoyage des coordonnées
        coord_columns = ['longitude', 'latitude']
        for col in coord_columns:
            if col in self.df_cleaned.columns:
                self.df_cleaned[col] = pd.to_numeric(self.df_cleaned[col], errors='coerce')
        
        # Filtrer les coordonnées valides pour le Québec
        if 'longitude' in self.df_cleaned.columns and 'latitude' in self.df_cleaned.columns:
            # Coordonnées approximatives du Québec
            mask = (
                (self.df_cleaned['longitude'] >= -80) & 
                (self.df_cleaned['longitude'] <= -55) &
                (self.df_cleaned['latitude'] >= 45) & 
                (self.df_cleaned['latitude'] <= 63)
            )
            self.df_cleaned = self.df_cleaned[mask]
            logger.info(f"✅ Géolocalisation filtrée: {len(self.df_cleaned)} propriétés valides")
        
        # Nettoyage des adresses
        address_columns = ['address', 'full_address', 'city', 'region']
        for col in address_columns:
            if col in self.df_cleaned.columns:
                self.df_cleaned[col] = self.df_cleaned[col].astype(str).str.strip()
    
    def _remove_duplicates(self):
        """Élimine les doublons"""
        logger.info("🔄 Suppression des doublons...")
        
        initial_count = len(self.df_cleaned)
        
        # Supprimer les doublons basés sur l'adresse et le prix
        duplicate_columns = ['address', 'price']
        existing_dup_cols = [col for col in duplicate_columns if col in self.df_cleaned.columns]
        
        if len(existing_dup_cols) >= 2:
            self.df_cleaned = self.df_cleaned.drop_duplicates(subset=existing_dup_cols, keep='first')
        else:
            # Fallback: supprimer les doublons complets
            self.df_cleaned = self.df_cleaned.drop_duplicates(keep='first')
        
        final_count = len(self.df_cleaned)
        duplicates_removed = initial_count - final_count
        
        logger.info(f"✅ Doublons supprimés: {duplicates_removed} propriétés")
    
    def phase3_enrichment_intelligent(self) -> bool:
        """
        PHASE 3: ENRICHISSEMENT INTELLIGENT
        Création de variables calculées et catégorisation
        """
        logger.info("⚡ PHASE 3: ENRICHISSEMENT INTELLIGENT")
        
        if self.df_cleaned is None:
            logger.error("❌ Aucune donnée nettoyée disponible")
            return False
        
        try:
            # 1. Variables calculées financières
            self._create_financial_metrics()
            
            # 2. Variables calculées physiques
            self._create_physical_metrics()
            
            # 3. Catégorisation
            self._create_categories()
            
            # 4. Score de complétude
            self._create_completeness_score()
            
            logger.info("✅ Enrichissement intelligent terminé")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'enrichissement: {e}")
            return False
    
    def _create_financial_metrics(self):
        """Crée les métriques financières calculées"""
        logger.info("💰 Création des métriques financières...")
        
        # ROI brut (si revenus et prix disponibles)
        if 'revenue_consolidated' in self.df_cleaned.columns and 'price' in self.df_cleaned.columns:
            self.df_cleaned['roi_brut'] = (
                self.df_cleaned['revenue_consolidated'] / self.df_cleaned['price']
            ) * 100
        
        # Prix par pied carré
        if 'price' in self.df_cleaned.columns and 'surface' in self.df_cleaned.columns:
            self.df_cleaned['price_per_sqft'] = self.df_cleaned['price'] / self.df_cleaned['surface']
        
        # Potentiel de plus-value (écart évaluation/prix)
        if 'municipal_evaluation_total' in self.df_cleaned.columns and 'price' in self.df_cleaned.columns:
            self.df_cleaned['plus_value_potential'] = (
                (self.df_cleaned['municipal_evaluation_total'] - self.df_cleaned['price']) / 
                self.df_cleaned['price']
            ) * 100
        
        # Cash-flow mensuel
        if 'revenue_consolidated' in self.df_cleaned.columns:
            self.df_cleaned['monthly_cashflow'] = self.df_cleaned['revenue_consolidated'] / 12
        
        logger.info("✅ Métriques financières créées")
    
    def _create_physical_metrics(self):
        """Crée les métriques physiques calculées"""
        logger.info("🏠 Création des métriques physiques...")
        
        # Âge du bâtiment
        if 'construction_year' in self.df_cleaned.columns:
            current_year = datetime.now().year
            self.df_cleaned['building_age'] = current_year - self.df_cleaned['construction_year']
        
        # Ratio chambres/surface
        if 'bedrooms' in self.df_cleaned.columns and 'surface' in self.df_cleaned.columns:
            self.df_cleaned['bedrooms_per_sqft'] = self.df_cleaned['bedrooms'] / self.df_cleaned['surface']
        
        logger.info("✅ Métriques physiques créées")
    
    def _create_categories(self):
        """Crée les catégories et segments"""
        logger.info("🏷️ Création des catégories...")
        
        # Segments de prix
        if 'price' in self.df_cleaned.columns:
            price_quantiles = self.df_cleaned['price'].quantile([0.25, 0.5, 0.75])
            self.df_cleaned['price_segment'] = pd.cut(
                self.df_cleaned['price'],
                bins=[0, price_quantiles[0.25], price_quantiles[0.5], price_quantiles[0.75], float('inf')],
                labels=['Économique', 'Moyen', 'Élevé', 'Premium']
            )
        
        # Classes de ROI
        if 'roi_brut' in self.df_cleaned.columns:
            self.df_cleaned['roi_class'] = pd.cut(
                self.df_cleaned['roi_brut'],
                bins=[-float('inf'), 0, 5, 10, 15, float('inf')],
                labels=['Négatif', 'Faible', 'Modéré', 'Élevé', 'Exceptionnel']
            )
        
        # Types d'opportunité
        opportunity_conditions = []
        opportunity_labels = []
        
        if 'plus_value_potential' in self.df_cleaned.columns:
            opportunity_conditions.append(self.df_cleaned['plus_value_potential'] > 20)
            opportunity_labels.append('Sous-évalué')
        
        if 'roi_brut' in self.df_cleaned.columns:
            opportunity_conditions.append(self.df_cleaned['roi_brut'] > 10)
            opportunity_labels.append('ROI Élevé')
        
        if opportunity_conditions:
            self.df_cleaned['opportunity_type'] = np.select(
                opportunity_conditions,
                opportunity_labels,
                default='Standard'
            )
        
        logger.info("✅ Catégories créées")
    
    def _create_completeness_score(self):
        """Crée un score de complétude des données"""
        logger.info("📊 Création du score de complétude...")
        
        # Calculer le pourcentage de données non-manquantes par propriété
        completeness = (self.df_cleaned.notna().sum(axis=1) / len(self.df_cleaned.columns)) * 100
        self.df_cleaned['completeness_score'] = completeness
        
        # Catégoriser la qualité des données
        self.df_cleaned['data_quality'] = pd.cut(
            completeness,
            bins=[0, 50, 75, 90, 100],
            labels=['Faible', 'Moyenne', 'Bonne', 'Excellente']
        )
        
        logger.info("✅ Score de complétude créé")
    
    def phase4_validation_quality_control(self) -> Dict:
        """
        PHASE 4: VALIDATION & CONTRÔLE QUALITÉ
        Tests automatiques et validation des données
        """
        logger.info("🚨 PHASE 4: VALIDATION & CONTRÔLE QUALITÉ")
        
        if self.df_cleaned is None:
            logger.error("❌ Aucune donnée nettoyée disponible")
            return {}
        
        validation_results = {}
        
        try:
            # 1. Tests de cohérence financière
            financial_validation = self._validate_financial_consistency()
            validation_results['financial_validation'] = financial_validation
            
            # 2. Tests de cohérence physique
            physical_validation = self._validate_physical_consistency()
            validation_results['physical_validation'] = physical_validation
            
            # 3. Tests de géolocalisation
            geo_validation = self._validate_geolocation()
            validation_results['geo_validation'] = geo_validation
            
            # 4. Tests généraux
            general_validation = self._validate_general_consistency()
            validation_results['general_validation'] = general_validation
            
            # 5. Résumé des validations
            validation_results['summary'] = self._create_validation_summary(validation_results)
            
            logger.info("✅ Validation et contrôle qualité terminés")
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            return {}
    
    def _validate_financial_consistency(self) -> Dict:
        """Valide la cohérence financière"""
        validation = {'passed': 0, 'failed': 0, 'issues': []}
        
        # ROI réaliste (0% à 50%)
        if 'roi_brut' in self.df_cleaned.columns:
            roi_mask = (self.df_cleaned['roi_brut'] >= 0) & (self.df_cleaned['roi_brut'] <= 50)
            validation['passed'] += roi_mask.sum()
            validation['failed'] += (~roi_mask).sum()
            
            if (~roi_mask).sum() > 0:
                validation['issues'].append(f"ROI aberrant: {(~roi_mask).sum()} propriétés")
        
        # Prix vs évaluation municipale (écart ±50%)
        if 'plus_value_potential' in self.df_cleaned.columns:
            price_eval_mask = (self.df_cleaned['plus_value_potential'] >= -50) & (self.df_cleaned['plus_value_potential'] <= 50)
            validation['passed'] += price_eval_mask.sum()
            validation['failed'] += (~price_eval_mask).sum()
            
            if (~price_eval_mask).sum() > 0:
                validation['issues'].append(f"Écart prix/évaluation aberrant: {(~price_eval_mask).sum()} propriétés")
        
        return validation
    
    def _validate_physical_consistency(self) -> Dict:
        """Valide la cohérence physique"""
        validation = {'passed': 0, 'failed': 0, 'issues': []}
        
        # Surface positive
        if 'surface' in self.df_cleaned.columns:
            surface_mask = self.df_cleaned['surface'] > 0
            validation['passed'] += surface_mask.sum()
            validation['failed'] += (~surface_mask).sum()
        
        # Chambres et SDB positives
        for col in ['bedrooms', 'bathrooms']:
            if col in self.df_cleaned.columns:
                positive_mask = self.df_cleaned[col] >= 0
                validation['passed'] += positive_mask.sum()
                validation['failed'] += (~positive_mask).sum()
        
        # Âge du bâtiment réaliste
        if 'building_age' in self.df_cleaned.columns:
            age_mask = (self.df_cleaned['building_age'] >= 0) & (self.df_cleaned['building_age'] <= 200)
            validation['passed'] += age_mask.sum()
            validation['failed'] += (~age_mask).sum()
        
        return validation
    
    def _validate_geolocation(self) -> Dict:
        """Valide la géolocalisation"""
        validation = {'passed': 0, 'failed': 0, 'issues': []}
        
        # Coordonnées dans les limites du Québec
        if 'longitude' in self.df_cleaned.columns and 'latitude' in self.df_cleaned.columns:
            geo_mask = (
                (self.df_cleaned['longitude'] >= -80) & 
                (self.df_cleaned['longitude'] <= -55) &
                (self.df_cleaned['latitude'] >= 45) & 
                (self.df_cleaned['latitude'] <= 63)
            )
            validation['passed'] += geo_mask.sum()
            validation['failed'] += (~geo_mask).sum()
        
        return validation
    
    def _validate_general_consistency(self) -> Dict:
        """Valide la cohérence générale"""
        validation = {'passed': 0, 'failed': 0, 'issues': []}
        
        # Pas de valeurs négatives pour les variables physiques
        physical_cols = ['surface', 'bedrooms', 'bathrooms']
        for col in physical_cols:
            if col in self.df_cleaned.columns:
                positive_mask = self.df_cleaned[col] >= 0
                validation['passed'] += positive_mask.sum()
                validation['failed'] += (~positive_mask).sum()
        
        return validation
    
    def _create_validation_summary(self, validation_results: Dict) -> Dict:
        """Crée un résumé des validations"""
        total_passed = sum(v.get('passed', 0) for v in validation_results.values() if isinstance(v, dict))
        total_failed = sum(v.get('failed', 0) for v in validation_results.values() if isinstance(v, dict))
        total_records = len(self.df_cleaned) if self.df_cleaned is not None else 0
        
        return {
            'total_records': total_records,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'success_rate': (total_passed / total_records * 100) if total_records > 0 else 0
        }
    
    def phase5_preparation_analysis(self) -> bool:
        """
        PHASE 5: PRÉPARATION POUR L'ANALYSE
        Export et structure finale
        """
        logger.info("🎯 PHASE 5: PRÉPARATION POUR L'ANALYSE")
        
        if self.df_cleaned is None:
            logger.error("❌ Aucune donnée nettoyée disponible")
            return False
        
        try:
            # 1. Structure finale optimisée
            self._optimize_final_structure()
            
            # 2. Export multi-format
            self._export_data()
            
            # 3. Création du rapport de qualité
            self._create_quality_report()
            
            logger.info("✅ Préparation pour l'analyse terminée")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la préparation: {e}")
            return False
    
    def _optimize_final_structure(self):
        """Optimise la structure finale des données"""
        logger.info("🔄 Optimisation de la structure finale...")
        
        # Réorganiser les colonnes par catégorie
        column_categories = {
            'identifiants': ['_id', 'link', 'company', 'version'],
            'geolocalisation': ['address', 'full_address', 'city', 'region', 'longitude', 'latitude'],
            'financier': ['price', 'revenue_consolidated', 'roi_brut', 'price_per_sqft', 'plus_value_potential'],
            'physique': ['surface', 'bedrooms', 'bathrooms', 'construction_year', 'building_age'],
            'evaluations': ['municipal_evaluation_building', 'municipal_evaluation_land', 'municipal_evaluation_total'],
            'taxes': ['municipal_tax', 'school_tax'],
            'categorisation': ['price_segment', 'roi_class', 'opportunity_type', 'data_quality'],
            'metadonnees': ['completeness_score', 'date_consolidated']
        }
        
        # Créer l'ordre final des colonnes
        final_columns = []
        for category, cols in column_categories.items():
            existing_cols = [col for col in cols if col in self.df_cleaned.columns]
            final_columns.extend(existing_cols)
        
        # Ajouter les colonnes restantes
        remaining_cols = [col for col in self.df_cleaned.columns if col not in final_columns]
        final_columns.extend(remaining_cols)
        
        # Réorganiser
        self.df_cleaned = self.df_cleaned[final_columns]
        
        logger.info(f"✅ Structure optimisée: {len(final_columns)} colonnes organisées")
    
    def _export_data(self):
        """Exporte les données dans différents formats"""
        logger.info("💾 Export des données...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"real_estate_cleaned_{timestamp}"
        
        # Export Parquet (performance optimale)
        parquet_file = f"{base_filename}.parquet"
        self.df_cleaned.to_parquet(parquet_file, index=False)
        logger.info(f"✅ Export Parquet: {parquet_file}")
        
        # Export CSV (compatibilité universelle)
        csv_file = f"{base_filename}.csv"
        self.df_cleaned.to_csv(csv_file, index=False)
        logger.info(f"✅ Export CSV: {csv_file}")
        
        # Export JSON (pour applications web)
        json_file = f"{base_filename}.json"
        self.df_cleaned.to_json(json_file, orient='records', indent=2)
        logger.info(f"✅ Export JSON: {json_file}")
        
        # Export GeoJSON si coordonnées disponibles
        if 'longitude' in self.df_cleaned.columns and 'latitude' in self.df_cleaned.columns:
            geojson_file = f"{base_filename}.geojson"
            self._export_geojson(geojson_file)
            logger.info(f"✅ Export GeoJSON: {geojson_file}")
    
    def _export_geojson(self, filename: str):
        """Exporte en format GeoJSON pour cartes interactives"""
        try:
            # Créer un GeoDataFrame
            gdf = gpd.GeoDataFrame(
                self.df_cleaned,
                geometry=gpd.points_from_xy(
                    self.df_cleaned['longitude'], 
                    self.df_cleaned['latitude']
                ),
                crs="EPSG:4326"
            )
            
            # Exporter
            gdf.to_file(filename, driver='GeoJSON')
            
        except Exception as e:
            logger.warning(f"⚠️ Export GeoJSON échoué: {e}")
    
    def _create_quality_report(self):
        """Crée un rapport de qualité des données"""
        logger.info("📊 Création du rapport de qualité...")
        
        # Statistiques générales
        self.quality_report = {
            'timestamp': datetime.now().isoformat(),
            'dataset_info': {
                'total_records': len(self.df_cleaned),
                'total_columns': len(self.df_cleaned.columns),
                'memory_usage_mb': self.df_cleaned.memory_usage(deep=True).sum() / 1024**2
            },
            'data_quality': {
                'completeness_score_mean': self.df_cleaned['completeness_score'].mean() if 'completeness_score' in self.df_cleaned.columns else 0,
                'missing_data_percentage': (self.df_cleaned.isnull().sum().sum() / (len(self.df_cleaned) * len(self.df_cleaned.columns))) * 100
            },
            'validation_summary': getattr(self, 'validation_results', {}).get('summary', {})
        }
        
        # Sauvegarder le rapport
        import json
        report_file = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.quality_report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Rapport de qualité créé: {report_file}")
    
    def run_complete_cleaning_pipeline(self, input_file: str = None) -> bool:
        """
        Exécute le pipeline complet de nettoyage
        
        Args:
            input_file: Chemin vers le fichier à nettoyer
            
        Returns:
            True si le nettoyage s'est bien déroulé
        """
        logger.info("🚀 DÉMARRAGE DU PIPELINE COMPLET DE NETTOYAGE")
        
        try:
            # Configuration
            if input_file:
                self.input_file = input_file
            
            # Phase 1: Audit et diagnostic
            if not self.load_data():
                return False
            
            audit_results = self.phase1_audit_diagnostic()
            logger.info(f"📊 Audit terminé: {len(audit_results)} analyses effectuées")
            
            # Phase 2: Nettoyage intelligent
            if not self.phase2_cleaning_intelligent():
                return False
            
            # Phase 3: Enrichissement intelligent
            if not self.phase3_enrichment_intelligent():
                return False
            
            # Phase 4: Validation et contrôle qualité
            validation_results = self.phase4_validation_quality_control()
            self.validation_results = validation_results
            logger.info(f"✅ Validation terminée: {validation_results.get('summary', {}).get('success_rate', 0):.1f}% de succès")
            
            # Phase 5: Préparation pour l'analyse
            if not self.phase5_preparation_analysis():
                return False
            
            logger.info("🎉 PIPELINE DE NETTOYAGE TERMINÉ AVEC SUCCÈS!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur dans le pipeline: {e}")
            return False
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Retourne les données nettoyées"""
        return self.df_cleaned if self.df_cleaned is not None else pd.DataFrame()
    
    def get_quality_report(self) -> Dict:
        """Retourne le rapport de qualité"""
        return self.quality_report


def main():
    """Fonction principale pour exécuter le nettoyage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Nettoyage expert du dataset immobilier')
    parser.add_argument('--input', '-i', help='Fichier d\'entrée (CSV, Excel, JSON)')
    parser.add_argument('--mongodb', '-m', help='Chaîne de connexion MongoDB')
    parser.add_argument('--output-dir', '-o', default='.', help='Répertoire de sortie')
    
    args = parser.parse_args()
    
    # Créer le nettoyeur
    cleaner = RealEstateDataCleaner(
        input_file=args.input,
        mongodb_connection=args.mongodb
    )
    
    # Exécuter le pipeline
    success = cleaner.run_complete_cleaning_pipeline()
    
    if success:
        logger.info("✅ Nettoyage terminé avec succès!")
        logger.info(f"📊 Données nettoyées: {len(cleaner.get_cleaned_data())} propriétés")
        
        # Afficher le rapport de qualité
        quality_report = cleaner.get_quality_report()
        if quality_report:
            logger.info("📋 Rapport de qualité généré")
    else:
        logger.error("❌ Échec du nettoyage")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

