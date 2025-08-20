#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ENRICHEUR DE DONNÉES - Composant d'enrichissement
=====================================================

Module spécialisé dans l'enrichissement des données avec des métriques dérivées
Calculs financiers, géographiques et métriques d'opportunité
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
import warnings
from datetime import datetime
import math

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class DataEnricher:
    """
    Composant spécialisé dans l'enrichissement des données
    Calcule des métriques dérivées et ajoute des informations contextuelles
    """
    
    def __init__(self):
        """Initialise l'enricheur de données"""
        self.enrichment_results = {}
        self.enrichment_stats = {}
        self.metric_calculators = self._initialize_metric_calculators()
        logger.info("🚀 DataEnricher initialisé")
    
    def enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Point d'entrée principal pour l'enrichissement des données
        
        Args:
            df: DataFrame à enrichir
            
        Returns:
            DataFrame enrichi avec de nouvelles colonnes
        """
        logger.info("🚀 === DÉBUT ENRICHISSEMENT DES DONNÉES ===")
        
        try:
            if df is None or df.empty:
                raise ValueError("❌ DataFrame vide pour l'enrichissement")
            
            start_time = datetime.now()
            initial_columns = len(df.columns)
            
            # Copie des données pour éviter la modification de l'original
            df_enriched = df.copy()
            
            # === PHASE 1: MÉTRIQUES FINANCIÈRES ===
            logger.info("🚀 Phase 1: Calcul des métriques financières")
            df_enriched = self._calculate_financial_metrics(df_enriched)
            
            # === PHASE 2: MÉTRIQUES GÉOGRAPHIQUES ===
            logger.info("🚀 Phase 2: Enrichissement géographique")
            df_enriched = self._enrich_geographic_data(df_enriched)
            
            # === PHASE 3: MÉTRIQUES D'OPPORTUNITÉ ===
            logger.info("🚀 Phase 3: Calcul des métriques d'opportunité")
            df_enriched = self._calculate_opportunity_metrics(df_enriched)
            
            # === PHASE 4: CATÉGORISATION AUTOMATIQUE ===
            logger.info("🚀 Phase 4: Catégorisation automatique")
            df_enriched = self._apply_automatic_categorization(df_enriched)
            
            # === PHASE 5: MÉTRIQUES DÉRIVÉES ===
            logger.info("🚀 Phase 5: Métriques dérivées")
            df_enriched = self._calculate_derived_metrics(df_enriched)
            
            # Statistiques d'enrichissement
            final_columns = len(df_enriched.columns)
            self.enrichment_stats = {
                'initial_columns': initial_columns,
                'final_columns': final_columns,
                'columns_added': final_columns - initial_columns,
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'enrichment_phases': len(self.enrichment_results)
            }
            
            logger.info(f"✅ Enrichissement terminé: {initial_columns} → {final_columns} colonnes")
            logger.info(f"➕ Colonnes ajoutées: {final_columns - initial_columns}")
            logger.info(f"⏱️ Temps de traitement: {self.enrichment_stats['processing_time']:.2f}s")
            
            return df_enriched
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'enrichissement: {e}")
            raise
    
    def _initialize_metric_calculators(self) -> Dict[str, Any]:
        """Initialisation des calculateurs de métriques"""
        return {
            'financial': self._calculate_financial_metrics,
            'geographic': self._enrich_geographic_data,
            'opportunity': self._calculate_opportunity_metrics,
            'categorization': self._apply_automatic_categorization,
            'derived': self._calculate_derived_metrics
        }
    
    def _calculate_financial_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcul des métriques financières"""
        try:
            # Prix au m²
            if 'price' in df.columns and 'surface' in df.columns:
                df['price_per_sqm'] = (df['price'] / df['surface']).round(2)
                logger.info("💰 Prix au m² calculé")
            
            # Ratio prix/surface
            if 'price' in df.columns and 'surface' in df.columns:
                df['price_surface_ratio'] = (df['price'] / df['surface']).round(4)
                logger.info("📊 Ratio prix/surface calculé")
            
            # Catégorisation des prix
            if 'price' in df.columns:
                df['price_category'] = pd.cut(
                    df['price'],
                    bins=[0, 300000, 500000, 750000, 1000000, float('inf')],
                    labels=['Économique', 'Abordable', 'Moyen', 'Élevé', 'Premium'],
                    include_lowest=True
                )
                logger.info("🏷️ Catégories de prix créées")
            
            # ROI estimé (basé sur des hypothèses)
            if 'price' in df.columns and 'year_built' in df.columns:
                current_year = datetime.now().year
                df['age'] = current_year - df['year_built']
                df['roi_estimate'] = self._estimate_roi(df['price'], df['age'])
                logger.info("📈 ROI estimé calculé")
            
            self.enrichment_results['financial_metrics'] = {
                'metrics_added': ['price_per_sqm', 'price_surface_ratio', 'price_category', 'roi_estimate'],
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur métriques financières: {e}")
            self.enrichment_results['financial_metrics'] = {'success': False, 'error': str(e)}
            return df
    
    def _enrich_geographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrichissement des données géographiques"""
        try:
            # Calcul de la densité de population (simulée)
            if 'city' in df.columns:
                city_density = {
                    'Montréal': 4700,
                    'Trois-Rivières': 1200,
                    'Québec': 1100,
                    'Laval': 2100,
                    'Gatineau': 800,
                    'Sherbrooke': 900
                }
                df['city_density'] = df['city'].map(city_density)
                logger.info("🌍 Densité de population ajoutée")
            
            # Région administrative
            if 'city' in df.columns:
                region_mapping = {
                    'Montréal': 'Montréal',
                    'Laval': 'Montréal',
                    'Gatineau': 'Outaouais',
                    'Québec': 'Capitale-Nationale',
                    'Trois-Rivières': 'Mauricie',
                    'Sherbrooke': 'Estrie'
                }
                df['region'] = df['city'].map(region_mapping)
                logger.info("🗺️ Régions administratives ajoutées")
            
            # Distance au centre-ville (simulée)
            if 'latitude' in df.columns and 'longitude' in df.columns:
                # Coordonnées approximatives des centres-villes
                city_centers = {
                    'Montréal': (45.5017, -73.5673),
                    'Trois-Rivières': (46.3508, -72.5447),
                    'Québec': (46.8139, -71.2080),
                    'Laval': (45.5698, -73.7241)
                }
                
                df['distance_to_center'] = df.apply(
                    lambda row: self._calculate_distance(
                        row['latitude'], row['longitude'],
                        city_centers.get(row.get('city', 'Montréal'), (45.5017, -73.5673))
                    ) if pd.notna(row.get('latitude')) and pd.notna(row.get('longitude')) else np.nan,
                    axis=1
                )
                logger.info("📍 Distances au centre-ville calculées")
            
            # Zone géographique (urbain/suburbain/rural)
            if 'distance_to_center' in df.columns:
                df['zone_type'] = pd.cut(
                    df['distance_to_center'],
                    bins=[0, 5, 15, float('inf')],
                    labels=['Urbain', 'Suburbain', 'Rural'],
                    include_lowest=True
                )
                logger.info("🏘️ Types de zones définis")
            
            self.enrichment_results['geographic_enrichment'] = {
                'metrics_added': ['city_density', 'region', 'distance_to_center', 'zone_type'],
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur enrichissement géographique: {e}")
            self.enrichment_results['geographic_enrichment'] = {'success': False, 'error': str(e)}
            return df
    
    def _calculate_opportunity_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcul des métriques d'opportunité"""
        try:
            # Score d'opportunité global
            opportunity_score = np.zeros(len(df))
            
            # Facteur prix (plus bas = meilleur)
            if 'price' in df.columns:
                price_score = 1 - (df['price'] / df['price'].max())
                opportunity_score += price_score * 0.3
            
            # Facteur surface (plus grand = meilleur)
            if 'surface' in df.columns:
                surface_score = df['surface'] / df['surface'].max()
                opportunity_score += surface_score * 0.25
            
            # Facteur âge (plus récent = meilleur)
            if 'age' in df.columns:
                age_score = 1 - (df['age'] / df['age'].max())
                opportunity_score += age_score * 0.2
            
            # Facteur localisation (densité = meilleur)
            if 'city_density' in df.columns:
                density_score = df['city_density'] / df['city_density'].max()
                opportunity_score += density_score * 0.15
            
            # Facteur ROI
            if 'roi_estimate' in df.columns:
                roi_score = df['roi_estimate'] / df['roi_estimate'].max()
                opportunity_score += roi_score * 0.1
            
            df['opportunity_score'] = opportunity_score.round(3)
            
            # Catégorisation des opportunités
            df['opportunity_level'] = pd.cut(
                df['opportunity_score'],
                bins=[0, 0.3, 0.6, 0.8, 1.0],
                labels=['Faible', 'Moyenne', 'Bonne', 'Excellente'],
                include_lowest=True
            )
            
            logger.info("🎯 Scores d'opportunité calculés")
            
            # Indicateur de bon rapport qualité-prix
            if 'price_per_sqm' in df.columns:
                median_price_sqm = df['price_per_sqm'].median()
                df['good_value_indicator'] = (df['price_per_sqm'] < median_price_sqm).astype(int)
                logger.info("💎 Indicateurs de bon rapport qualité-prix créés")
            
            self.enrichment_results['opportunity_metrics'] = {
                'metrics_added': ['opportunity_score', 'opportunity_level', 'good_value_indicator'],
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur métriques d'opportunité: {e}")
            self.enrichment_results['opportunity_metrics'] = {'success': False, 'error': str(e)}
            return df
    
    def _apply_automatic_categorization(self, df: pd.DataFrame) -> pd.DataFrame:
        """Application de la catégorisation automatique"""
        try:
            # Catégorisation par type de propriété
            if 'type' in df.columns:
                df['property_category'] = df['type'].map({
                    'maison': 'Résidentiel',
                    'appartement': 'Résidentiel',
                    'duplex': 'Résidentiel',
                    'triplex': 'Résidentiel',
                    'condo': 'Résidentiel',
                    'loft': 'Résidentiel',
                    'terrain': 'Terrain',
                    'commercial': 'Commercial'
                }).fillna('Autre')
                logger.info("🏷️ Catégories de propriétés créées")
            
            # Catégorisation par taille
            if 'surface' in df.columns:
                df['size_category'] = pd.cut(
                    df['surface'],
                    bins=[0, 1000, 1500, 2500, float('inf')],
                    labels=['Petit', 'Moyen', 'Grand', 'Très grand'],
                    include_lowest=True
                )
                logger.info("📏 Catégories de taille créées")
            
            # Catégorisation par budget
            if 'price' in df.columns:
                df['budget_category'] = pd.cut(
                    df['price'],
                    bins=[0, 400000, 600000, 800000, float('inf')],
                    labels=['Budget', 'Moyen budget', 'Haut budget', 'Luxe'],
                    include_lowest=True
                )
                logger.info("💰 Catégories de budget créées")
            
            # Catégorisation par investisseur
            if 'opportunity_score' in df.columns:
                df['investor_type'] = df['opportunity_score'].apply(
                    lambda x: 'Conservateur' if x < 0.4 else 'Modéré' if x < 0.7 else 'Agressif'
                )
                logger.info("👥 Types d'investisseurs définis")
            
            self.enrichment_results['automatic_categorization'] = {
                'categories_added': ['property_category', 'size_category', 'budget_category', 'investor_type'],
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur catégorisation automatique: {e}")
            self.enrichment_results['automatic_categorization'] = {'success': False, 'error': str(e)}
            return df
    
    def _calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcul des métriques dérivées finales"""
        try:
            # Indice de qualité global
            quality_indicators = []
            
            if 'price_per_sqm' in df.columns:
                # Normalisation du prix au m²
                price_sqm_norm = (df['price_per_sqm'] - df['price_per_sqm'].mean()) / df['price_per_sqm'].std()
                quality_indicators.append(price_sqm_norm)
            
            if 'surface' in df.columns:
                # Normalisation de la surface
                surface_norm = (df['surface'] - df['surface'].mean()) / df['surface'].std()
                quality_indicators.append(surface_norm)
            
            if 'opportunity_score' in df.columns:
                # Normalisation du score d'opportunité
                opp_norm = (df['opportunity_score'] - df['opportunity_score'].mean()) / df['opportunity_score'].std()
                quality_indicators.append(opp_norm)
            
            if quality_indicators:
                df['quality_index'] = np.mean(quality_indicators, axis=0).round(3)
                logger.info("⭐ Indice de qualité global calculé")
            
            # Score de recommandation
            if 'opportunity_score' in df.columns and 'price_per_sqm' in df.columns:
                # Combinaison pondérée des facteurs
                recommendation_score = (
                    df['opportunity_score'] * 0.4 +
                    (1 - df['price_per_sqm'] / df['price_per_sqm'].max()) * 0.3 +
                    (df['surface'] / df['surface'].max()) * 0.3
                )
                df['recommendation_score'] = recommendation_score.round(3)
                logger.info("👍 Scores de recommandation calculés")
            
            # Indicateur de tendance
            if 'year_built' in df.columns:
                current_year = datetime.now().year
                df['trend_indicator'] = df['year_built'].apply(
                    lambda x: 'Moderne' if x >= 2000 else 'Récent' if x >= 1980 else 'Classique' if x >= 1960 else 'Ancien'
                )
                logger.info("📈 Indicateurs de tendance créés")
            
            self.enrichment_results['derived_metrics'] = {
                'metrics_added': ['quality_index', 'recommendation_score', 'trend_indicator'],
                'success': True
            }
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erreur métriques dérivées: {e}")
            self.enrichment_results['derived_metrics'] = {'success': False, 'error': str(e)}
            return df
    
    def _estimate_roi(self, price: pd.Series, age: pd.Series) -> pd.Series:
        """Estimation du ROI basée sur le prix et l'âge"""
        try:
            # Formule simplifiée pour l'estimation du ROI
            # ROI = (Appréciation annuelle + Revenus locatifs) / Prix d'achat
            
            # Appréciation annuelle estimée (2-5% selon l'âge)
            appreciation_rate = np.where(age < 10, 0.05, np.where(age < 25, 0.03, 0.02))
            annual_appreciation = price * appreciation_rate
            
            # Revenus locatifs estimés (4-6% du prix)
            rental_rate = np.where(age < 15, 0.06, 0.04)
            annual_rental = price * rental_rate
            
            # ROI total
            total_roi = (annual_appreciation + annual_rental) / price
            
            return total_roi.round(3)
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul ROI: {e}")
            return pd.Series([0.05] * len(price))  # ROI par défaut 5%
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcul de la distance entre deux points géographiques (formule de Haversine)"""
        try:
            # Conversion en radians
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            
            # Différences
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            # Formule de Haversine
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            # Rayon de la Terre en km
            r = 6371
            
            return c * r
            
        except Exception:
            return np.nan
    
    def get_enrichment_results(self) -> Dict[str, Any]:
        """Retourne les résultats de l'enrichissement"""
        return self.enrichment_results.copy()
    
    def get_enrichment_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'enrichissement"""
        return self.enrichment_stats.copy()
    
    def get_enriched_columns(self) -> List[str]:
        """Retourne la liste des colonnes ajoutées par l'enrichissement"""
        enriched_columns = []
        for result in self.enrichment_results.values():
            if result.get('success') and 'metrics_added' in result:
                enriched_columns.extend(result['metrics_added'])
            elif result.get('success') and 'categories_added' in result:
                enriched_columns.extend(result['categories_added'])
        return enriched_columns
