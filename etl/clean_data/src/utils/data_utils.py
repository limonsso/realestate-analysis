#!/usr/bin/env python3
"""
Utilitaires pour la manipulation des données
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DataUtils:
    """Utilitaires pour la manipulation et l'analyse des données"""
    
    @staticmethod
    def clean_numeric_column(series: pd.Series) -> pd.Series:
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
    
    @staticmethod
    def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Standardise les noms de colonnes en snake_case"""
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
        df = df.rename(columns=column_mapping)
        
        # Convertir en snake_case
        df.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in df.columns]
        
        return df
    
    @staticmethod
    def consolidate_revenue_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Consolide les colonnes de revenus"""
        revenue_columns = ['revenu', 'plex_revenue']
        existing_revenue_cols = [col for col in revenue_columns if col in df.columns]
        
        if len(existing_revenue_cols) > 1:
            # Créer une colonne consolidée de manière robuste
            consolidated_values = []
            for idx in range(len(df)):
                row_sum = 0
                for col in existing_revenue_cols:
                    try:
                        val = df.loc[idx, col]
                        if pd.notna(val) and str(val).replace('.', '').replace('-', '').isdigit():
                            row_sum += float(val)
                    except:
                        continue
                consolidated_values.append(row_sum)
            
            df['revenue_consolidated'] = consolidated_values
            # Supprimer les colonnes originales
            df = df.drop(columns=existing_revenue_cols)
        
        elif len(existing_revenue_cols) == 1:
            # Une seule colonne de revenu, la renommer
            col_name = existing_revenue_cols[0]
            df['revenue_consolidated'] = df[col_name]
            df = df.drop(columns=[col_name])
        
        return df
    
    @staticmethod
    def consolidate_date_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Consolide les colonnes de dates"""
        date_columns = ['created_at', 'updated_at', 'update_at', 'add_date']
        existing_date_cols = [col for col in date_columns if col in df.columns]
        
        if len(existing_date_cols) > 1:
            # Convertir en datetime et prendre la plus récente
            for col in existing_date_cols:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            
            df['date_consolidated'] = df[existing_date_cols].max(axis=1)
            # Garder seulement la date consolidée
            df = df.drop(columns=existing_date_cols)
        
        return df
    
    @staticmethod
    def remove_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Supprime les colonnes dupliquées"""
        duplicate_columns = df.columns[df.columns.duplicated()].tolist()
        if duplicate_columns:
            logger.warning(f"⚠️ Colonnes dupliquées détectées: {duplicate_columns}")
            # Supprimer les colonnes dupliquées (garder la première occurrence)
            df = df.loc[:, ~df.columns.duplicated()]
            logger.info(f"✅ Colonnes dupliquées supprimées: {len(duplicate_columns)} colonnes")
        
        return df
    
    @staticmethod
    def create_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Crée les métriques financières calculées"""
        # ROI brut (si revenus et prix disponibles)
        if 'revenue_consolidated' in df.columns and 'price' in df.columns:
            df['roi_brut'] = (
                df['revenue_consolidated'] / df['price']
            ) * 100
        
        # Prix par pied carré
        if 'price' in df.columns and 'surface' in df.columns:
            df['price_per_sqft'] = df['price'] / df['surface']
        
        # Potentiel de plus-value (écart évaluation/prix)
        if 'municipal_evaluation_total' in df.columns and 'price' in df.columns:
            df['plus_value_potential'] = (
                (df['municipal_evaluation_total'] - df['price']) / 
                df['price']
            ) * 100
        
        # Cash-flow mensuel
        if 'revenue_consolidated' in df.columns:
            df['monthly_cashflow'] = df['revenue_consolidated'] / 12
        
        return df
    
    @staticmethod
    def create_physical_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Crée les métriques physiques calculées"""
        from datetime import datetime
        
        # Âge du bâtiment
        if 'construction_year' in df.columns:
            current_year = datetime.now().year
            df['building_age'] = current_year - df['construction_year']
        
        # Ratio chambres/surface
        if 'bedrooms' in df.columns and 'surface' in df.columns:
            df['bedrooms_per_sqft'] = df['bedrooms'] / df['surface']
        
        return df
    
    @staticmethod
    def create_categories(df: pd.DataFrame) -> pd.DataFrame:
        """Crée les catégories et segments"""
        # Segments de prix
        if 'price' in df.columns:
            price_quantiles = df['price'].quantile([0.25, 0.5, 0.75])
            df['price_segment'] = pd.cut(
                df['price'],
                bins=[0, price_quantiles[0.25], price_quantiles[0.5], price_quantiles[0.75], float('inf')],
                labels=['Économique', 'Moyen', 'Élevé', 'Premium']
            )
        
        # Classes de ROI
        if 'roi_brut' in df.columns:
            df['roi_class'] = pd.cut(
                df['roi_brut'],
                bins=[-float('inf'), 0, 5, 10, 15, float('inf')],
                labels=['Négatif', 'Faible', 'Modéré', 'Élevé', 'Exceptionnel']
            )
        
        return df
    
    @staticmethod
    def create_completeness_score(df: pd.DataFrame) -> pd.DataFrame:
        """Crée un score de complétude des données par propriété"""
        # Calculer le pourcentage de données non-manquantes par ligne
        completeness_scores = []
        
        for idx, row in df.iterrows():
            non_null_count = row.notna().sum()
            total_columns = len(row)
            completeness_percent = (non_null_count / total_columns) * 100
            completeness_scores.append(completeness_percent)
        
        df['completeness_score'] = completeness_scores
        return df
    
    @staticmethod
    def optimize_dataframe_structure(df: pd.DataFrame) -> pd.DataFrame:
        """Optimise la structure finale du DataFrame"""
        # Colonnes finales organisées par catégorie
        final_columns = []
        
        # Identifiants et métadonnées
        id_cols = ['_id', 'type', 'company', 'version']
        final_columns.extend([col for col in id_cols if col in df.columns])
        
        # Géolocalisation
        geo_cols = ['address', 'full_address', 'city', 'region', 'longitude', 'latitude']
        final_columns.extend([col for col in geo_cols if col in df.columns])
        
        # Caractéristiques physiques
        physical_cols = ['surface', 'bedrooms', 'bathrooms', 'construction_year', 'building_style']
        final_columns.extend([col for col in physical_cols if col in df.columns])
        
        # Données financières
        financial_cols = ['price', 'revenue_consolidated', 'municipal_tax', 'school_tax']
        final_columns.extend([col for col in financial_cols if col in df.columns])
        
        # Métriques calculées
        metric_cols = ['roi_brut', 'price_per_sqft', 'plus_value_potential', 'building_age']
        final_columns.extend([col for col in metric_cols if col in df.columns])
        
        # Catégories
        category_cols = ['price_segment', 'roi_class', 'completeness_score']
        final_columns.extend([col for col in category_cols if col in df.columns])
        
        # Autres colonnes
        other_cols = [col for col in df.columns if col not in final_columns]
        final_columns.extend(other_cols)
        
        # Réorganiser le DataFrame
        df = df[final_columns]
        
        return df
