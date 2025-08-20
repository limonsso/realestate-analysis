#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
✅ VALIDATEUR DE DONNÉES - Composant de validation
==================================================

Module spécialisé dans la validation complète des données après traitement
Validation de qualité, cohérence et règles métier
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
import warnings
from datetime import datetime
import json

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Composant spécialisé dans la validation complète des données
    Applique des règles de validation métier et génère des rapports de qualité
    """
    
    def __init__(self):
        """Initialise le validateur de données"""
        self.validation_results = {}
        self.validation_stats = {}
        self.quality_thresholds = self._initialize_quality_thresholds()
        self.business_rules = self._initialize_business_rules()
        logger.info("✅ DataValidator initialisé")
    
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Point d'entrée principal pour la validation des données
        
        Args:
            df: DataFrame à valider
            
        Returns:
            Dict avec les résultats de validation complets
        """
        logger.info("✅ === DÉBUT VALIDATION COMPLÈTE DES DONNÉES ===")
        
        try:
            if df is None or df.empty:
                raise ValueError("❌ DataFrame vide pour la validation")
            
            start_time = datetime.now()
            
            # === PHASE 1: VALIDATION DE BASE ===
            logger.info("✅ Phase 1: Validation de base")
            basic_validation = self._validate_basic_data_quality(df)
            
            # === PHASE 2: VALIDATION DES RÈGLES MÉTIER ===
            logger.info("✅ Phase 2: Validation des règles métier")
            business_validation = self._validate_business_rules(df)
            
            # === PHASE 3: VALIDATION DE LA COHÉRENCE ===
            logger.info("✅ Phase 3: Validation de la cohérence")
            consistency_validation = self._validate_data_consistency(df)
            
            # === PHASE 4: VALIDATION DES MÉTRIQUES DE CONSOLIDATION ===
            logger.info("✅ Phase 4: Validation des métriques de consolidation")
            consolidation_validation = self._validate_consolidation_metrics(df)
            
            # === PHASE 5: VALIDATION DES DONNÉES ENRICHIES ===
            logger.info("✅ Phase 5: Validation des données enrichies")
            enrichment_validation = self._validate_enriched_data(df)
            
            # === PHASE 6: DÉTERMINATION DU STATUT GLOBAL ===
            logger.info("✅ Phase 6: Détermination du statut global")
            overall_status = self._determine_overall_validation_status({
                'basic': basic_validation,
                'business': business_validation,
                'consistency': consistency_validation,
                'consolidation': consolidation_validation,
                'enrichment': enrichment_validation
            })
            
            # Compilation des résultats
            self.validation_results = {
                'basic_validation': basic_validation,
                'business_rules_validation': business_validation,
                'consistency_validation': consistency_validation,
                'consolidation_validation': consolidation_validation,
                'enrichment_validation': enrichment_validation,
                'overall_status': overall_status
            }
            
            # Statistiques de validation
            self.validation_stats = {
                'total_validations': len(self.validation_results),
                'passed_validations': sum(1 for v in self.validation_results.values() if isinstance(v, dict) and v.get('status') == 'PASSED'),
                'failed_validations': sum(1 for v in self.validation_results.values() if isinstance(v, dict) and v.get('status') == 'FAILED'),
                'warning_validations': sum(1 for v in self.validation_results.values() if isinstance(v, dict) and v.get('status') == 'WARNING'),
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'data_shape': df.shape,
                'overall_quality_score': overall_status.get('quality_score', 0.0)
            }
            
            logger.info(f"✅ Validation terminée en {self.validation_stats['processing_time']:.2f}s")
            logger.info(f"📊 Statut global: {overall_status['status']}")
            logger.info(f"⭐ Score de qualité: {overall_status['quality_score']:.1%}")
            
            return self.validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            raise
    
    def _initialize_quality_thresholds(self) -> Dict[str, Any]:
        """Initialisation des seuils de qualité"""
        return {
            'completeness': 0.8,      # 80% de complétude minimum
            'uniqueness': 0.9,        # 90% d'unicité minimum
            'consistency': 0.85,      # 85% de cohérence minimum
            'accuracy': 0.9,          # 90% de précision minimum
            'timeliness': 0.95,       # 95% de fraîcheur minimum
            'validity': 0.9           # 90% de validité minimum
        }
    
    def _initialize_business_rules(self) -> Dict[str, Any]:
        """Initialisation des règles métier"""
        return {
            'price': {
                'required': True,
                'min_value': 0,
                'max_value': 10000000,
                'data_type': 'numeric',
                'business_logic': 'Le prix doit être positif et raisonnable'
            },
            'surface': {
                'required': True,
                'min_value': 0,
                'max_value': 10000,
                'data_type': 'numeric',
                'business_logic': 'La surface doit être positive et réaliste'
            },
            'city': {
                'required': True,
                'allowed_values': ['Montréal', 'Trois-Rivières', 'Québec', 'Laval', 'Gatineau', 'Sherbrooke'],
                'data_type': 'categorical',
                'business_logic': 'La ville doit être dans la liste des villes supportées'
            },
            'type': {
                'required': True,
                'allowed_values': ['maison', 'appartement', 'duplex', 'triplex', 'condo', 'loft', 'terrain', 'commercial'],
                'data_type': 'categorical',
                'business_logic': 'Le type de propriété doit être valide'
            },
            'year_built': {
                'required': False,
                'min_value': 1800,
                'max_value': 2030,
                'data_type': 'integer',
                'business_logic': "L'année de construction doit être réaliste"
            }
        }
    
    def _validate_basic_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation de base de la qualité des données"""
        try:
            validation_results = {}
            
            # 1. Complétude des données
            completeness_scores = {}
            for col in df.columns:
                missing_count = df[col].isna().sum()
                total_count = len(df)
                completeness = 1 - (missing_count / total_count)
                completeness_scores[col] = {
                    'score': round(completeness, 3),
                    'missing_count': missing_count,
                    'missing_percentage': round((missing_count / total_count) * 100, 1)
                }
            
            overall_completeness = np.mean([score['score'] for score in completeness_scores.values()])
            validation_results['completeness'] = {
                'score': round(overall_completeness, 3),
                'threshold': self.quality_thresholds['completeness'],
                'passed': overall_completeness >= self.quality_thresholds['completeness'],
                'details': completeness_scores
            }
            
            # 2. Unicité des données
            uniqueness_scores = {}
            for col in df.columns:
                unique_count = df[col].nunique()
                total_count = len(df)
                uniqueness = unique_count / total_count if total_count > 0 else 0
                uniqueness_scores[col] = {
                    'score': round(uniqueness, 3),
                    'unique_count': unique_count,
                    'duplicate_percentage': round((1 - uniqueness) * 100, 1)
                }
            
            overall_uniqueness = np.mean([score['score'] for score in uniqueness_scores.values()])
            validation_results['uniqueness'] = {
                'score': round(overall_uniqueness, 3),
                'threshold': self.quality_thresholds['uniqueness'],
                'passed': overall_uniqueness >= self.quality_thresholds['uniqueness'],
                'details': uniqueness_scores
            }
            
            # 3. Types de données
            type_validation = {}
            for col in df.columns:
                expected_type = self.business_rules.get(col, {}).get('data_type', 'any')
                actual_type = str(df[col].dtype)
                
                type_valid = True
                if expected_type == 'numeric':
                    type_valid = pd.api.types.is_numeric_dtype(df[col])
                elif expected_type == 'categorical':
                    type_valid = pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col])
                elif expected_type == 'integer':
                    type_valid = pd.api.types.is_integer_dtype(df[col])
                
                type_validation[col] = {
                    'expected': expected_type,
                    'actual': actual_type,
                    'valid': type_valid
                }
            
            overall_type_validity = sum(1 for v in type_validation.values() if v['valid']) / len(type_validation)
            validation_results['type_consistency'] = {
                'score': round(overall_type_validity, 3),
                'threshold': self.quality_thresholds['consistency'],
                'passed': overall_type_validity >= self.quality_thresholds['consistency'],
                'details': type_validation
            }
            
            # Détermination du statut global
            passed_checks = sum(1 for v in validation_results.values() if v['passed'])
            total_checks = len(validation_results)
            overall_score = passed_checks / total_checks
            
            validation_results['overall'] = {
                'score': round(overall_score, 3),
                'passed_checks': passed_checks,
                'total_checks': total_checks,
                'status': 'PASSED' if overall_score >= 0.8 else 'WARNING' if overall_score >= 0.6 else 'FAILED'
            }
            
            logger.info(f"✅ Validation de base: {passed_checks}/{total_checks} tests réussis")
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur validation de base: {e}")
            return {'error': str(e), 'status': 'FAILED'}
    
    def _validate_business_rules(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des règles métier"""
        try:
            validation_results = {}
            rule_violations = {}
            
            for field, rule in self.business_rules.items():
                if field not in df.columns:
                    if rule.get('required', False):
                        rule_violations[field] = ['Champ requis manquant']
                    continue
                
                field_violations = []
                
                # Vérification des valeurs requises
                if rule.get('required', False):
                    missing_count = df[field].isna().sum()
                    if missing_count > 0:
                        field_violations.append(f"Valeurs manquantes: {missing_count}")
                
                # Vérification des limites numériques
                if 'min_value' in rule:
                    below_limit = (df[field] < rule['min_value']).sum()
                    if below_limit > 0:
                        field_violations.append(f"Valeurs < {rule['min_value']}: {below_limit}")
                
                if 'max_value' in rule:
                    above_limit = (df[field] > rule['max_value']).sum()
                    if above_limit > 0:
                        field_violations.append(f"Valeurs > {rule['max_value']}: {above_limit}")
                
                # Vérification des valeurs autorisées
                if 'allowed_values' in rule:
                    invalid_values = ~df[field].isin(rule['allowed_values'])
                    invalid_count = invalid_values.sum()
                    if invalid_count > 0:
                        field_violations.append(f"Valeurs invalides: {invalid_count}")
                
                # Vérification des types de données
                if 'data_type' in rule:
                    type_valid = True
                    if rule['data_type'] == 'numeric':
                        type_valid = pd.api.types.is_numeric_dtype(df[field])
                    elif rule['data_type'] == 'categorical':
                        type_valid = pd.api.types.is_categorical_dtype(df[field]) or pd.api.types.is_object_dtype(df[field])
                    elif rule['data_type'] == 'integer':
                        type_valid = pd.api.types.is_integer_dtype(df[field])
                    
                    if not type_valid:
                        field_violations.append(f"Type invalide: attendu {rule['data_type']}")
                
                if field_violations:
                    rule_violations[field] = field_violations
            
            # Calcul du score de validation des règles métier
            total_fields = len(self.business_rules)
            valid_fields = total_fields - len(rule_violations)
            business_rule_score = valid_fields / total_fields if total_fields > 0 else 0
            
            validation_results = {
                'score': round(business_rule_score, 3),
                'threshold': self.quality_thresholds['validity'],
                'passed': business_rule_score >= self.quality_thresholds['validity'],
                'total_fields': total_fields,
                'valid_fields': valid_fields,
                'violations': rule_violations,
                'status': 'PASSED' if business_rule_score >= 0.9 else 'WARNING' if business_rule_score >= 0.7 else 'FAILED'
            }
            
            if rule_violations:
                logger.warning(f"⚠️ Violations des règles métier détectées: {len(rule_violations)} champs")
            else:
                logger.info("✅ Toutes les règles métier respectées")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur validation règles métier: {e}")
            return {'error': str(e), 'status': 'FAILED'}
    
    def _validate_data_consistency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation de la cohérence des données"""
        try:
            consistency_checks = {}
            
            # 1. Cohérence prix/surface
            if 'price' in df.columns and 'surface' in df.columns:
                price_surface_ratio = df['price'] / df['surface']
                median_ratio = price_surface_ratio.median()
                
                # Détection des anomalies (ratio > 3x la médiane)
                threshold = median_ratio * 3
                anomalies = (price_surface_ratio > threshold).sum()
                
                consistency_checks['price_surface_ratio'] = {
                    'median_ratio': round(median_ratio, 2),
                    'anomalies_detected': int(anomalies),
                    'anomaly_percentage': round((anomalies / len(df)) * 100, 1),
                    'status': 'PASSED' if anomalies / len(df) < 0.1 else 'WARNING'
                }
            
            # 2. Cohérence géographique
            if 'latitude' in df.columns and 'longitude' in df.columns:
                # Vérification des coordonnées dans des plages raisonnables pour le Québec
                lat_valid = ((df['latitude'] >= 45.0) & (df['latitude'] <= 46.0)).sum()
                lon_valid = ((df['longitude'] >= -74.0) & (df['longitude'] <= -73.0)).sum()
                
                consistency_checks['geographic_coordinates'] = {
                    'latitude_valid': int(lat_valid),
                    'longitude_valid': int(lon_valid),
                    'total_records': len(df),
                    'coordinate_validity': round(min(lat_valid, lon_valid) / len(df), 3),
                    'status': 'PASSED' if min(lat_valid, lon_valid) / len(df) >= 0.95 else 'WARNING'
                }
            
            # 3. Cohérence temporelle
            if 'year_built' in df.columns:
                current_year = datetime.now().year
                age_valid = ((df['year_built'] >= 1800) & (df['year_built'] <= current_year)).sum()
                
                consistency_checks['temporal_consistency'] = {
                    'valid_years': int(age_valid),
                    'total_records': len(df),
                    'year_validity': round(age_valid / len(df), 3),
                    'status': 'PASSED' if age_valid / len(df) >= 0.95 else 'WARNING'
                }
            
            # Score global de cohérence
            if consistency_checks:
                consistency_scores = [check.get('coordinate_validity', check.get('year_validity', 1.0)) 
                                   for check in consistency_checks.values()]
                overall_consistency = np.mean(consistency_scores)
                
                validation_results = {
                    'score': round(overall_consistency, 3),
                    'threshold': self.quality_thresholds['consistency'],
                    'passed': overall_consistency >= self.quality_thresholds['consistency'],
                    'checks': consistency_checks,
                    'status': 'PASSED' if overall_consistency >= 0.85 else 'WARNING' if overall_consistency >= 0.7 else 'FAILED'
                }
            else:
                validation_results = {
                    'score': 1.0,
                    'threshold': self.quality_thresholds['consistency'],
                    'passed': True,
                    'checks': {},
                    'status': 'PASSED'
                }
            
            logger.info(f"✅ Validation de cohérence: score {validation_results['score']:.1%}")
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur validation cohérence: {e}")
            return {'error': str(e), 'status': 'FAILED'}
    
    def _validate_consolidation_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des métriques de consolidation"""
        try:
            consolidation_checks = {}
            
            # 1. Vérification des colonnes consolidées
            expected_consolidated_columns = [
                'price_final', 'surface_final', 'type_final', 'city_final',
                'rooms_final', 'bathrooms_final', 'year_built_final'
            ]
            
            available_consolidated = [col for col in expected_consolidated_columns if col in df.columns]
            consolidation_coverage = len(available_consolidated) / len(expected_consolidated_columns)
            
            consolidation_checks['consolidation_coverage'] = {
                'expected_columns': expected_consolidated_columns,
                'available_columns': available_consolidated,
                'coverage_percentage': round(consolidation_coverage * 100, 1),
                'status': 'PASSED' if consolidation_coverage >= 0.8 else 'WARNING'
            }
            
            # 2. Qualité des colonnes consolidées
            if available_consolidated:
                quality_scores = {}
                for col in available_consolidated:
                    if col in df.columns:
                        completeness = 1 - (df[col].isna().sum() / len(df))
                        quality_scores[col] = round(completeness, 3)
                
                avg_quality = np.mean(list(quality_scores.values())) if quality_scores else 0
                
                consolidation_checks['consolidated_quality'] = {
                    'quality_scores': quality_scores,
                    'average_quality': round(avg_quality, 3),
                    'status': 'PASSED' if avg_quality >= 0.9 else 'WARNING' if avg_quality >= 0.7 else 'FAILED'
                }
            
            # Score global de consolidation
            if consolidation_checks:
                coverage_score = consolidation_checks['consolidation_coverage']['coverage_percentage'] / 100
                quality_score = consolidation_checks['consolidated_quality']['average_quality'] if 'consolidated_quality' in consolidation_checks else 1.0
                overall_score = (coverage_score + quality_score) / 2
                
                validation_results = {
                    'score': round(overall_score, 3),
                    'threshold': 0.8,
                    'passed': overall_score >= 0.8,
                    'checks': consolidation_checks,
                    'status': 'PASSED' if overall_score >= 0.8 else 'WARNING' if overall_score >= 0.6 else 'FAILED'
                }
            else:
                validation_results = {
                    'score': 0.0,
                    'threshold': 0.8,
                    'passed': False,
                    'checks': {},
                    'status': 'FAILED'
                }
            
            logger.info(f"✅ Validation consolidation: score {validation_results['score']:.1%}")
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur validation consolidation: {e}")
            return {'error': str(e), 'status': 'FAILED'}
    
    def _validate_enriched_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validation des données enrichies"""
        try:
            enrichment_checks = {}
            
            # 1. Vérification des métriques financières
            financial_metrics = ['price_per_sqm', 'price_surface_ratio', 'roi_estimate']
            available_financial = [col for col in financial_metrics if col in df.columns]
            
            if available_financial:
                financial_quality = {}
                for col in available_financial:
                    if col in df.columns:
                        # Vérification que les valeurs sont dans des plages raisonnables
                        if col == 'price_per_sqm':
                            valid_range = (100, 10000)  # 100$ à 10k$ par m²
                        elif col == 'price_surface_ratio':
                            valid_range = (100, 10000)
                        elif col == 'roi_estimate':
                            valid_range = (0, 0.5)  # 0% à 50%
                        
                        if 'valid_range' in locals():
                            min_val, max_val = valid_range
                            valid_count = ((df[col] >= min_val) & (df[col] <= max_val)).sum()
                            quality_score = valid_count / len(df)
                            financial_quality[col] = round(quality_score, 3)
                
                avg_financial_quality = np.mean(list(financial_quality.values())) if financial_quality else 0
                
                enrichment_checks['financial_metrics'] = {
                    'available_metrics': available_financial,
                    'quality_scores': financial_quality,
                    'average_quality': round(avg_financial_quality, 3),
                    'status': 'PASSED' if avg_financial_quality >= 0.9 else 'WARNING'
                }
            
            # 2. Vérification des métriques géographiques
            geographic_metrics = ['city_density', 'region', 'distance_to_center', 'zone_type']
            available_geographic = [col for col in geographic_metrics if col in df.columns]
            
            if available_geographic:
                geographic_coverage = len(available_geographic) / len(geographic_metrics)
                
                enrichment_checks['geographic_metrics'] = {
                    'available_metrics': available_geographic,
                    'coverage_percentage': round(geographic_coverage * 100, 1),
                    'status': 'PASSED' if geographic_coverage >= 0.75 else 'WARNING'
                }
            
            # 3. Vérification des scores d'opportunité
            opportunity_metrics = ['opportunity_score', 'opportunity_level', 'quality_index']
            available_opportunity = [col for col in opportunity_metrics if col in df.columns]
            
            if available_opportunity:
                opportunity_quality = {}
                for col in available_opportunity:
                    if col in df.columns:
                        if col == 'opportunity_score':
                            # Vérification que le score est entre 0 et 1
                            valid_count = ((df[col] >= 0) & (df[col] <= 1)).sum()
                            quality_score = valid_count / len(df)
                            opportunity_quality[col] = round(quality_score, 3)
                
                avg_opportunity_quality = np.mean(list(opportunity_quality.values())) if opportunity_quality else 0
                
                enrichment_checks['opportunity_metrics'] = {
                    'available_metrics': available_opportunity,
                    'quality_scores': opportunity_quality,
                    'average_quality': round(avg_opportunity_quality, 3),
                    'status': 'PASSED' if avg_opportunity_quality >= 0.9 else 'WARNING'
                }
            
            # Score global d'enrichissement
            if enrichment_checks:
                enrichment_scores = []
                for check in enrichment_checks.values():
                    if 'average_quality' in check:
                        enrichment_scores.append(check['average_quality'])
                    elif 'coverage_percentage' in check:
                        enrichment_scores.append(check['coverage_percentage'] / 100)
                
                overall_enrichment = np.mean(enrichment_scores) if enrichment_scores else 0
                
                validation_results = {
                    'score': round(overall_enrichment, 3),
                    'threshold': 0.8,
                    'passed': overall_enrichment >= 0.8,
                    'checks': enrichment_checks,
                    'status': 'PASSED' if overall_enrichment >= 0.8 else 'WARNING' if overall_enrichment >= 0.6 else 'FAILED'
                }
            else:
                validation_results = {
                    'score': 0.0,
                    'threshold': 0.8,
                    'passed': False,
                    'checks': {},
                    'status': 'FAILED'
                }
            
            logger.info(f"✅ Validation enrichissement: score {validation_results['score']:.1%}")
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur validation enrichissement: {e}")
            return {'error': str(e), 'status': 'FAILED'}
    
    def _determine_overall_validation_status(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Détermination du statut global de validation"""
        try:
            # Calcul des scores par catégorie
            category_scores = {}
            for category, result in validation_results.items():
                if isinstance(result, dict) and 'score' in result:
                    category_scores[category] = result['score']
            
            # Score global pondéré
            weights = {
                'basic': 0.25,
                'business': 0.25,
                'consistency': 0.20,
                'consolidation': 0.15,
                'enrichment': 0.15
            }
            
            weighted_score = 0
            total_weight = 0
            
            for category, weight in weights.items():
                if category in category_scores:
                    weighted_score += category_scores[category] * weight
                    total_weight += weight
            
            overall_score = weighted_score / total_weight if total_weight > 0 else 0
            
            # Détermination du statut global
            if overall_score >= 0.9:
                status = 'PASSED'
                message = 'Excellente qualité des données'
            elif overall_score >= 0.8:
                status = 'PASSED'
                message = 'Bonne qualité des données'
            elif overall_score >= 0.7:
                status = 'WARNING'
                message = 'Qualité acceptable avec quelques points d\'attention'
            elif overall_score >= 0.6:
                status = 'WARNING'
                message = 'Qualité modérée nécessitant des améliorations'
            else:
                status = 'FAILED'
                message = 'Qualité insuffisante, rejet des données'
            
            overall_status = {
                'status': status,
                'quality_score': round(overall_score, 3),
                'message': message,
                'category_scores': category_scores,
                'weighted_score': round(overall_score, 3),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"📊 Statut global: {status} - Score: {overall_score:.1%}")
            logger.info(f"💬 Message: {message}")
            
            return overall_status
            
        except Exception as e:
            logger.error(f"❌ Erreur détermination statut global: {e}")
            return {
                'status': 'ERROR',
                'quality_score': 0.0,
                'message': f'Erreur lors de la validation: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_validation_results(self) -> Dict[str, Any]:
        """Retourne les résultats de validation"""
        return self.validation_results.copy()
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de validation"""
        return self.validation_stats.copy()
    
    def generate_validation_report(self) -> str:
        """Génération d'un rapport de validation en format texte"""
        try:
            report = []
            report.append("=" * 60)
            report.append("📊 RAPPORT DE VALIDATION DES DONNÉES")
            report.append("=" * 60)
            report.append(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"📊 Forme des données: {self.validation_stats.get('data_shape', 'N/A')}")
            report.append("")
            
            # Résumé global
            overall = self.validation_results.get('overall_status', {})
            report.append("🎯 RÉSUMÉ GLOBAL")
            report.append("-" * 30)
            report.append(f"Statut: {overall.get('status', 'N/A')}")
            report.append(f"Score de qualité: {overall.get('quality_score', 0):.1%}")
            report.append(f"Message: {overall.get('message', 'N/A')}")
            report.append("")
            
            # Détails par catégorie
            for category, result in self.validation_results.items():
                if category == 'overall_status':
                    continue
                
                if isinstance(result, dict) and 'status' in result:
                    report.append(f"🔍 {category.upper().replace('_', ' ')}")
                    report.append("-" * 30)
                    report.append(f"Statut: {result.get('status', 'N/A')}")
                    report.append(f"Score: {result.get('score', 0):.1%}")
                    
                    if 'passed' in result:
                        report.append(f"Test réussi: {'✅' if result['passed'] else '❌'}")
                    
                    report.append("")
            
            # Statistiques
            report.append("📈 STATISTIQUES")
            report.append("-" * 30)
            report.append(f"Tests réussis: {self.validation_stats.get('passed_validations', 0)}")
            report.append(f"Tests échoués: {self.validation_stats.get('failed_validations', 0)}")
            report.append(f"Tests avec avertissement: {self.validation_stats.get('warning_validations', 0)}")
            report.append(f"Temps de traitement: {self.validation_stats.get('processing_time', 0):.2f}s")
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport: {e}")
            return f"Erreur lors de la génération du rapport: {str(e)}"
