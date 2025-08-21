#!/usr/bin/env python3
"""
🧠 CONSOLIDATION INTELLIGENTE DES STRUCTURES COMPLEXES
=====================================================

Script pour consolider intelligemment les colonnes avec des structures JSON complexes
comme unites et residential_units.
"""

import pandas as pd
import numpy as np
import json
import ast
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple, Union

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartConsolidator:
    """Consolidateur intelligent pour les structures de données complexes."""
    
    def __init__(self):
        self.consolidation_rules = {
            'units': {
                'source_columns': ['unites', 'residential_units', 'commercial_units'],
                'target_columns': {
                    'total_units': 'total_units_final',
                    'unit_types': 'unit_types_final',
                    'unit_details': 'unit_details_final'
                },
                'strategy': 'smart_units_consolidation'
            },
            'address': {
                'source_columns': ['address', 'full_address', 'location'],
                'target_columns': {
                    'street': 'street_final',
                    'city': 'city_final',
                    'postal_code': 'postal_code_final'
                },
                'strategy': 'smart_address_consolidation'
            },
            'evaluation': {
                'source_columns': ['municipal_evaluation_building', 'municipal_evaluation_land', 'municipal_evaluation_total'],
                'target_columns': {
                    'building_value': 'building_value_final',
                    'land_value': 'land_value_final',
                    'total_value': 'total_value_final'
                },
                'strategy': 'smart_evaluation_consolidation'
            }
        }
    
    def load_test_data(self, csv_file: str) -> pd.DataFrame:
        """Charge les données de test depuis le CSV."""
        logger.info(f"📁 Chargement des données: {csv_file}")
        df = pd.read_csv(csv_file)
        logger.info(f"✅ Données chargées: {df.shape[0]} lignes × {df.shape[1]} colonnes")
        return df
    
    def parse_json_string(self, value: str) -> Union[List, Dict, str]:
        """Parse une chaîne JSON de manière sécurisée."""
        if pd.isna(value) or value == '':
            return None
        
        try:
            # Essayer d'abord json.loads
            return json.loads(value)
        except json.JSONDecodeError:
            try:
                # Fallback: ast.literal_eval pour les structures Python
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                # Dernier fallback: traiter comme string
                return value
    
    def consolidate_units_intelligently(self, df: pd.DataFrame) -> pd.DataFrame:
        """Consolidation intelligente des colonnes d'unités."""
        logger.info("🏠 === CONSOLIDATION INTELLIGENTE DES UNITÉS ===")
        
        df_consolidated = df.copy()
        
        # Colonnes sources pour les unités
        unit_columns = ['unites', 'residential_units', 'commercial_units']
        available_columns = [col for col in unit_columns if col in df.columns]
        
        if len(available_columns) > 1:
            logger.info(f"🔄 Consolidation des colonnes d'unités: {available_columns}")
            
            # Créer les colonnes consolidées
            df_consolidated['total_units_final'] = self._calculate_total_units(df, available_columns)
            df_consolidated['unit_types_final'] = self._extract_unit_types(df, available_columns)
            df_consolidated['unit_details_final'] = self._create_unit_details(df, available_columns)
            
            # Supprimer les colonnes sources
            df_consolidated = df_consolidated.drop(columns=available_columns)
            
            logger.info(f"✅ {len(available_columns)} colonnes d'unités consolidées")
        
        return df_consolidated
    
    def _calculate_total_units(self, df: pd.DataFrame, unit_columns: List[str]) -> pd.Series:
        """Calcule le nombre total d'unités."""
        total_units = pd.Series(0, index=df.index)
        
        for col in unit_columns:
            if col in df.columns:
                for idx, value in df[col].items():
                    if pd.notna(value):
                        parsed_value = self.parse_json_string(value)
                        if isinstance(parsed_value, list):
                            # Compter les unités dans la liste
                            count = 0
                            for item in parsed_value:
                                if isinstance(item, dict):
                                    # Extraire le count ou nb_unite
                                    if 'count' in item:
                                        count += int(item['count'])
                                    elif 'nb_unite' in item:
                                        count += int(item['nb_unite'])
                                    else:
                                        count += 1
                                else:
                                    count += 1
                            total_units[idx] += count
                        elif isinstance(parsed_value, dict):
                            # Structure simple
                            if 'count' in parsed_value:
                                total_units[idx] += int(parsed_value['count'])
                            elif 'nb_unite' in parsed_value:
                                total_units[idx] += int(parsed_value['nb_unite'])
        
        return total_units
    
    def _extract_unit_types(self, df: pd.DataFrame, unit_columns: List[str]) -> pd.Series:
        """Extrait les types d'unités uniques."""
        unit_types = pd.Series('', index=df.index)
        
        for col in unit_columns:
            if col in df.columns:
                for idx, value in df[col].items():
                    if pd.notna(value) and unit_types[idx] == '':
                        parsed_value = self.parse_json_string(value)
                        if isinstance(parsed_value, list):
                            types = []
                            for item in parsed_value:
                                if isinstance(item, dict):
                                    # Extraire le type ou unite
                                    if 'type' in item:
                                        types.append(str(item['type']))
                                    elif 'unite' in item:
                                        types.append(str(item['unite']))
                            if types:
                                unit_types[idx] = ', '.join(set(types))
                        elif isinstance(parsed_value, dict):
                            if 'type' in parsed_value:
                                unit_types[idx] = str(parsed_value['type'])
                            elif 'unite' in parsed_value:
                                unit_types[idx] = str(parsed_value['unite'])
        
        return unit_types
    
    def _create_unit_details(self, df: pd.DataFrame, unit_columns: List[str]) -> pd.Series:
        """Crée une structure détaillée des unités."""
        unit_details = pd.Series('', index=df.index)
        
        for col in unit_columns:
            if col in df.columns:
                for idx, value in df[col].items():
                    if pd.notna(value) and unit_details[idx] == '':
                        parsed_value = self.parse_json_string(value)
                        if isinstance(parsed_value, list):
                            details = []
                            for item in parsed_value:
                                if isinstance(item, dict):
                                    detail = {}
                                    if 'type' in item:
                                        detail['type'] = item['type']
                                    elif 'unite' in item:
                                        detail['type'] = item['unite']
                                    
                                    if 'count' in item:
                                        detail['count'] = item['count']
                                    elif 'nb_unite' in item:
                                        detail['count'] = item['nb_unite']
                                    
                                    if detail:
                                        details.append(detail)
                            
                            if details:
                                unit_details[idx] = json.dumps(details, ensure_ascii=False)
                        elif isinstance(parsed_value, dict):
                            detail = {}
                            if 'type' in parsed_value:
                                detail['type'] = parsed_value['type']
                            elif 'unite' in parsed_value:
                                detail['type'] = parsed_value['unite']
                            
                            if 'count' in parsed_value:
                                detail['count'] = parsed_value['count']
                            elif 'nb_unite' in parsed_value:
                                detail['count'] = parsed_value['nb_unite']
                            
                            if detail:
                                unit_details[idx] = json.dumps([detail], ensure_ascii=False)
        
        return unit_details
    
    def consolidate_address_intelligently(self, df: pd.DataFrame) -> pd.DataFrame:
        """Consolidation intelligente des adresses."""
        logger.info("🏠 === CONSOLIDATION INTELLIGENTE DES ADRESSES ===")
        
        df_consolidated = df.copy()
        
        # Colonnes sources pour les adresses
        address_columns = ['address', 'full_address', 'location']
        available_columns = [col for col in address_columns if col in df.columns]
        
        if len(available_columns) > 1:
            logger.info(f"🔄 Consolidation des colonnes d'adresses: {available_columns}")
            
            # Créer les colonnes consolidées
            df_consolidated['street_final'] = self._extract_street(df, available_columns)
            df_consolidated['city_final'] = self._extract_city(df, available_columns)
            df_consolidated['postal_code_final'] = self._extract_postal_code(df, available_columns)
            
            # Supprimer les colonnes sources
            df_consolidated = df_consolidated.drop(columns=available_columns)
            
            logger.info(f"✅ {len(available_columns)} colonnes d'adresses consolidées")
        
        return df_consolidated
    
    def _extract_street(self, df: pd.DataFrame, address_columns: List[str]) -> pd.Series:
        """Extrait la rue depuis les colonnes d'adresse."""
        street = pd.Series('', index=df.index)
        
        for col in address_columns:
            if col in df.columns:
                for idx, value in df[col].items():
                    if pd.notna(value) and street[idx] == '':
                        parsed_value = self.parse_json_string(value)
                        if isinstance(parsed_value, dict):
                            if 'street' in parsed_value:
                                street[idx] = str(parsed_value['street'])
                        elif isinstance(parsed_value, str):
                            # Essayer d'extraire la rue d'une adresse complète
                            if ',' in parsed_value:
                                street[idx] = parsed_value.split(',')[0].strip()
                            else:
                                street[idx] = parsed_value
        
        return street
    
    def _extract_city(self, df: pd.DataFrame, address_columns: List[str]) -> pd.Series:
        """Extrait la ville depuis les colonnes d'adresse."""
        city = pd.Series('', index=df.index)
        
        for col in address_columns:
            if col in address_columns:
                for idx, value in df[col].items():
                    if pd.notna(value) and city[idx] == '':
                        parsed_value = self.parse_json_string(value)
                        if isinstance(parsed_value, dict):
                            if 'locality' in parsed_value:
                                city[idx] = str(parsed_value['locality'])
                        elif isinstance(parsed_value, str):
                            # Essayer d'extraire la ville d'une adresse complète
                            if ',' in parsed_value:
                                parts = parsed_value.split(',')
                                if len(parts) > 1:
                                    city[idx] = parts[1].strip()
        
        return city
    
    def _extract_postal_code(self, df: pd.DataFrame, address_columns: List[str]) -> pd.Series:
        """Extrait le code postal depuis les colonnes d'adresse."""
        postal_code = pd.Series('', index=df.index)
        
        for col in address_columns:
            if col in address_columns:
                for idx, value in df[col].items():
                    if pd.notna(value) and postal_code[idx] == '':
                        parsed_value = self.parse_json_string(value)
                        if isinstance(parsed_value, dict):
                            if 'postal_code' in parsed_value:
                                postal_code[idx] = str(parsed_value['postal_code'])
        
        return postal_code
    
    def run_smart_consolidation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exécute la consolidation intelligente complète."""
        logger.info("🧠 === DÉMARRAGE DE LA CONSOLIDATION INTELLIGENTE ===")
        
        df_consolidated = df.copy()
        original_columns = len(df.columns)
        
        # 1. Consolidation des unités
        df_consolidated = self.consolidate_units_intelligently(df_consolidated)
        
        # 2. Consolidation des adresses
        df_consolidated = self.consolidate_address_intelligently(df_consolidated)
        
        # 3. Autres consolidations...
        
        final_columns = len(df_consolidated.columns)
        reduction = original_columns - final_columns
        
        logger.info("📊 === RÉSULTATS DE LA CONSOLIDATION INTELLIGENTE ===")
        logger.info(f"Colonnes originales: {original_columns}")
        logger.info(f"Colonnes finales: {final_columns}")
        logger.info(f"Réduction: {reduction} colonnes")
        
        return df_consolidated
    
    def generate_consolidation_report(self, df_original: pd.DataFrame, df_consolidated: pd.DataFrame) -> str:
        """Génère un rapport de consolidation intelligente."""
        report = []
        report.append("# 🧠 RAPPORT DE CONSOLIDATION INTELLIGENTE")
        report.append("")
        
        report.append("## 📊 Métriques de Consolidation")
        report.append(f"- **Colonnes originales:** {df_original.shape[1]}")
        report.append(f"- **Colonnes après consolidation:** {df_consolidated.shape[1]}")
        report.append(f"- **Réduction:** {df_original.shape[1] - df_consolidated.shape[1]} colonnes")
        report.append("")
        
        report.append("## 🔗 Consolidations Intelligentes")
        report.append("")
        
        # Unités
        if 'total_units_final' in df_consolidated.columns:
            report.append("### 🏠 Consolidation des Unités")
            report.append("- **Colonnes sources:** unites, residential_units, commercial_units")
            report.append("- **Colonnes cibles:** total_units_final, unit_types_final, unit_details_final")
            report.append("- **Stratégie:** Parsing JSON intelligent + agrégation")
            report.append("")
        
        # Adresses
        if 'street_final' in df_consolidated.columns:
            report.append("### 🏠 Consolidation des Adresses")
            report.append("- **Colonnes sources:** address, full_address, location")
            report.append("- **Colonnes cibles:** street_final, city_final, postal_code_final")
            report.append("- **Stratégie:** Extraction intelligente des composants")
            report.append("")
        
        report.append("## 📋 Colonnes Finales")
        for col in df_consolidated.columns:
            if col.endswith('_final'):
                report.append(f"- **{col}** ← Colonne consolidée")
            else:
                report.append(f"- {col}")
        
        return "\n".join(report)

def main():
    """Fonction principale de consolidation intelligente."""
    logger.info("🚀 === DÉMARRAGE CONSOLIDATION INTELLIGENTE ===")
    
    # Créer le consolidateur intelligent
    consolidator = SmartConsolidator()
    
    # Fichier CSV à tester
    csv_file = "exports/trois_rivieres_plex_consolidated/real_estate_data_modular_pipeline_20250820_203204.csv"
    
    if Path(csv_file).exists():
        # Charger les données
        df_original = consolidator.load_test_data(csv_file)
        
        # Exécuter la consolidation intelligente
        df_consolidated = consolidator.run_smart_consolidation(df_original)
        
        # Générer le rapport
        report = consolidator.generate_consolidation_report(df_original, df_consolidated)
        
        # Sauvegarder le rapport
        report_file = "exports/trois_rivieres_plex_consolidated/smart_consolidation_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"📄 Rapport de consolidation intelligente sauvegardé: {report_file}")
        
        # Sauvegarder les données consolidées
        consolidated_file = "exports/trois_rivieres_plex_consolidated/smart_consolidated_data.csv"
        df_consolidated.to_csv(consolidated_file, index=False)
        logger.info(f"💾 Données consolidées intelligemment sauvegardées: {consolidated_file}")
        
        # Affichage du rapport
        print("\n" + "="*80)
        print(report)
        print("="*80)
        
    else:
        logger.error(f"❌ Fichier non trouvé: {csv_file}")

if __name__ == "__main__":
    main()
