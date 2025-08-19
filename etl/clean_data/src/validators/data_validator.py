#!/usr/bin/env python3
"""
Validateur de données immobilières
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    """Valide la qualité et la cohérence des données immobilières"""
    
    def __init__(self):
        self.validation_results = {}
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_dataset(self, df: pd.DataFrame) -> Dict:
        """
        Valide l'ensemble du dataset
        
        Args:
            df: DataFrame à valider
            
        Returns:
            Résultats de validation
        """
        logger.info("🚨 Validation du dataset...")
        
        validation_results = {
            'financial_validation': self._validate_financial_data(df),
            'physical_validation': self._validate_physical_data(df),
            'geographic_validation': self._validate_geographic_data(df),
            'consistency_validation': self._validate_data_consistency(df),
            'summary': {}
        }
        
        # Calculer le taux de succès global
        total_checks = 0
        passed_checks = 0
        
        for category, results in validation_results.items():
            if category != 'summary':
                total_checks += results.get('total_checks', 0)
                passed_checks += results.get('passed_checks', 0)
        
        if total_checks > 0:
            success_rate = (passed_checks / total_checks) * 100
        else:
            success_rate = 0
        
        validation_results['summary'] = {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': total_checks - passed_checks,
            'success_rate': success_rate,
            'errors': self.validation_errors,
            'warnings': self.validation_warnings
        }
        
        self.validation_results = validation_results
        logger.info(f"✅ Validation terminée: {success_rate:.1f}% de succès")
        
        return validation_results
    
    def _validate_financial_data(self, df: pd.DataFrame) -> Dict:
        """Valide les données financières"""
        results = {'total_checks': 0, 'passed_checks': 0, 'checks': []}
        
        # Validation des prix
        if 'price' in df.columns:
            results['total_checks'] += 1
            price_check = self._check_price_validity(df['price'])
            results['checks'].append(price_check)
            if price_check['passed']:
                results['passed_checks'] += 1
        
        # Validation des revenus
        if 'revenue_consolidated' in df.columns:
            results['total_checks'] += 1
            revenue_check = self._check_revenue_validity(df['revenue_consolidated'])
            results['checks'].append(revenue_check)
            if revenue_check['passed']:
                results['passed_checks'] += 1
        
        # Validation du ROI
        if 'roi_brut' in df.columns:
            results['total_checks'] += 1
            roi_check = self._check_roi_validity(df['roi_brut'])
            results['checks'].append(roi_check)
            if roi_check['passed']:
                results['passed_checks'] += 1
        
        return results
    
    def _validate_physical_data(self, df: pd.DataFrame) -> Dict:
        """Valide les données physiques"""
        results = {'total_checks': 0, 'passed_checks': 0, 'checks': []}
        
        # Validation des surfaces
        if 'surface' in df.columns:
            results['total_checks'] += 1
            surface_check = self._check_surface_validity(df['surface'])
            results['checks'].append(surface_check)
            if surface_check['passed']:
                results['passed_checks'] += 1
        
        # Validation des chambres
        if 'bedrooms' in df.columns:
            results['total_checks'] += 1
            bedrooms_check = self._check_bedrooms_validity(df['bedrooms'])
            results['checks'].append(bedrooms_check)
            if bedrooms_check['passed']:
                results['passed_checks'] += 1
        
        # Validation des années de construction
        if 'construction_year' in df.columns:
            results['total_checks'] += 1
            year_check = self._check_construction_year_validity(df['construction_year'])
            results['checks'].append(year_check)
            if year_check['passed']:
                results['passed_checks'] += 1
        
        return results
    
    def _validate_geographic_data(self, df: pd.DataFrame) -> Dict:
        """Valide les données géographiques"""
        results = {'total_checks': 0, 'passed_checks': 0, 'checks': []}
        
        # Validation des coordonnées
        if 'longitude' in df.columns and 'latitude' in df.columns:
            results['total_checks'] += 1
            coords_check = self._check_coordinates_validity(df['longitude'], df['latitude'])
            results['checks'].append(coords_check)
            if coords_check['passed']:
                results['passed_checks'] += 1
        
        # Validation des villes
        if 'city' in df.columns:
            results['total_checks'] += 1
            city_check = self._check_city_validity(df['city'])
            results['checks'].append(city_check)
            if city_check['passed']:
                results['passed_checks'] += 1
        
        return results
    
    def _validate_data_consistency(self, df: pd.DataFrame) -> Dict:
        """Valide la cohérence générale des données"""
        results = {'total_checks': 0, 'passed_checks': 0, 'checks': []}
        
        # Vérification des doublons
        results['total_checks'] += 1
        duplicates_check = self._check_duplicates(df)
        results['checks'].append(duplicates_check)
        if duplicates_check['passed']:
            results['passed_checks'] += 1
        
        # Vérification de la complétude
        results['total_checks'] += 1
        completeness_check = self._check_completeness(df)
        results['checks'].append(completeness_check)
        if completeness_check['passed']:
            results['passed_checks'] += 1
        
        return results
    
    def _check_price_validity(self, price_series: pd.Series) -> Dict:
        """Vérifie la validité des prix"""
        valid_prices = price_series.dropna()
        valid_prices = valid_prices[valid_prices > 0]
        
        passed = len(valid_prices) == len(price_series.dropna())
        
        return {
            'check_name': 'Prix valides',
            'passed': passed,
            'details': {
                'total_prices': len(price_series),
                'valid_prices': len(valid_prices),
                'invalid_prices': len(price_series.dropna()) - len(valid_prices)
            }
        }
    
    def _check_revenue_validity(self, revenue_series: pd.Series) -> Dict:
        """Vérifie la validité des revenus"""
        valid_revenues = revenue_series.dropna()
        valid_revenues = valid_revenues[valid_revenues >= 0]
        
        passed = len(valid_revenues) == len(revenue_series.dropna())
        
        return {
            'check_name': 'Revenus valides',
            'passed': passed,
            'details': {
                'total_revenues': len(revenue_series),
                'valid_revenues': len(valid_revenues),
                'negative_revenues': len(revenue_series.dropna()) - len(valid_revenues)
            }
        }
    
    def _check_roi_validity(self, roi_series: pd.Series) -> Dict:
        """Vérifie la validité du ROI"""
        valid_roi = roi_series.dropna()
        valid_roi = valid_roi[(valid_roi >= 0) & (valid_roi <= 50)]  # ROI entre 0% et 50%
        
        passed = len(valid_roi) == len(roi_series.dropna())
        
        return {
            'check_name': 'ROI valide',
            'passed': passed,
            'details': {
                'total_roi': len(roi_series),
                'valid_roi': len(valid_roi),
                'out_of_range_roi': len(roi_series.dropna()) - len(valid_roi)
            }
        }
    
    def _check_surface_validity(self, surface_series: pd.Series) -> Dict:
        """Vérifie la validité des surfaces"""
        valid_surfaces = surface_series.dropna()
        valid_surfaces = valid_surfaces[valid_surfaces > 0]
        
        passed = len(valid_surfaces) == len(surface_series.dropna())
        
        return {
            'check_name': 'Surfaces valides',
            'passed': passed,
            'details': {
                'total_surfaces': len(surface_series),
                'valid_surfaces': len(valid_surfaces),
                'invalid_surfaces': len(surface_series.dropna()) - len(valid_surfaces)
            }
        }
    
    def _check_bedrooms_validity(self, bedrooms_series: pd.Series) -> Dict:
        """Vérifie la validité des chambres"""
        valid_bedrooms = bedrooms_series.dropna()
        valid_bedrooms = valid_bedrooms[(valid_bedrooms >= 0) & (valid_bedrooms <= 20)]
        
        passed = len(valid_bedrooms) == len(bedrooms_series.dropna())
        
        return {
            'check_name': 'Chambres valides',
            'passed': passed,
            'details': {
                'total_bedrooms': len(bedrooms_series),
                'valid_bedrooms': len(valid_bedrooms),
                'out_of_range_bedrooms': len(bedrooms_series.dropna()) - len(valid_bedrooms)
            }
        }
    
    def _check_construction_year_validity(self, year_series: pd.Series) -> Dict:
        """Vérifie la validité des années de construction"""
        valid_years = year_series.dropna()
        valid_years = valid_years[(valid_years >= 1800) & (valid_years <= 2024)]
        
        passed = len(valid_years) == len(year_series.dropna())
        
        return {
            'check_name': 'Années de construction valides',
            'passed': passed,
            'details': {
                'total_years': len(year_series),
                'valid_years': len(valid_years),
                'out_of_range_years': len(year_series.dropna()) - len(valid_years)
            }
        }
    
    def _check_coordinates_validity(self, lon_series: pd.Series, lat_series: pd.Series) -> Dict:
        """Vérifie la validité des coordonnées"""
        valid_coords = pd.DataFrame({'lon': lon_series, 'lat': lat_series}).dropna()
        
        # Coordonnées du Québec
        quebec_mask = (
            (valid_coords['lon'] >= -80) & (valid_coords['lon'] <= -55) &
            (valid_coords['lat'] >= 45) & (valid_coords['lat'] <= 63)
        )
        
        valid_quebec_coords = valid_coords[quebec_mask]
        passed = len(valid_quebec_coords) == len(valid_coords)
        
        return {
            'check_name': 'Coordonnées valides (Québec)',
            'passed': passed,
            'details': {
                'total_coordinates': len(valid_coords),
                'valid_quebec_coordinates': len(valid_quebec_coords),
                'out_of_quebec_coordinates': len(valid_coords) - len(valid_quebec_coords)
            }
        }
    
    def _check_city_validity(self, city_series: pd.Series) -> Dict:
        """Vérifie la validité des villes"""
        valid_cities = city_series.dropna()
        valid_cities = valid_cities[valid_cities.str.strip() != '']
        
        passed = len(valid_cities) == len(city_series.dropna())
        
        return {
            'check_name': 'Villes valides',
            'passed': passed,
            'details': {
                'total_cities': len(city_series),
                'valid_cities': len(valid_cities),
                'empty_cities': len(city_series.dropna()) - len(valid_cities)
            }
        }
    
    def _check_duplicates(self, df: pd.DataFrame) -> Dict:
        """Vérifie la présence de doublons"""
        duplicates_count = df.duplicated().sum()
        passed = duplicates_count == 0
        
        return {
            'check_name': 'Pas de doublons',
            'passed': passed,
            'details': {
                'total_records': len(df),
                'duplicates_count': duplicates_count
            }
        }
    
    def _check_completeness(self, df: pd.DataFrame) -> Dict:
        """Vérifie la complétude des données"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        completeness_percent = ((total_cells - missing_cells) / total_cells) * 100
        
        passed = completeness_percent >= 80  # Au moins 80% de complétude
        
        return {
            'check_name': 'Complétude des données',
            'passed': passed,
            'details': {
                'total_cells': total_cells,
                'missing_cells': missing_cells,
                'completeness_percent': completeness_percent
            }
        }
