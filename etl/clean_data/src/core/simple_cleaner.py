#!/usr/bin/env python3
"""
Système de nettoyage simplifié pour les données immobilières
Version adaptée aux vraies données du marché québécois
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleRealEstateCleaner:
    """Nettoyeur simplifié pour les données immobilières"""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.df_original = None
        self.df_cleaned = None
        
    def load_data(self, data_path: str = None) -> bool:
        """Charge les données depuis un fichier CSV"""
        try:
            file_path = data_path or self.data_path
            if not file_path:
                raise ValueError("Aucun chemin de fichier spécifié")
            
            logger.info(f"📁 Chargement depuis le fichier: {file_path}")
            
            # Charger les données
            self.df_original = pd.read_csv(file_path)
            self.df_cleaned = self.df_original.copy()
            
            logger.info(f"✅ Données chargées: {self.df_cleaned.shape}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def clean_data(self) -> bool:
        """Nettoie les données de manière simplifiée"""
        try:
            logger.info("🛠️ DÉMARRAGE DU NETTOYAGE SIMPLIFIÉ")
            
            # 1. Nettoyage des colonnes problématiques
            self._fix_problematic_columns()
            
            # 2. Nettoyage des valeurs numériques
            self._clean_numeric_columns()
            
            # 3. Nettoyage des dates
            self._clean_date_columns()
            
            # 4. Suppression des doublons
            self._remove_duplicates()
            
            logger.info("✅ Nettoyage simplifié terminé")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage: {e}")
            return False
    
    def _fix_problematic_columns(self):
        """Corrige les colonnes qui posent problème"""
        logger.info("🔧 Correction des colonnes problématiques...")
        
        # Colonnes connues pour poser problème
        problematic_cols = ['bedrooms', 'bathrooms', 'surface', 'plex-revenue']
        
        for col in problematic_cols:
            if col in self.df_cleaned.columns:
                try:
                    # Vérifier le type de la colonne
                    if isinstance(self.df_cleaned[col], pd.DataFrame):
                        logger.warning(f"  Colonne {col} est un DataFrame, conversion en Series...")
                        
                        # Essayer de récupérer la première colonne
                        if self.df_cleaned[col].shape[1] > 0:
                            first_col = self.df_cleaned[col].iloc[:, 0]
                            # S'assurer que la longueur correspond
                            if len(first_col) == len(self.df_cleaned):
                                self.df_cleaned[col] = first_col.values
                                logger.info(f"    {col} converti en Series avec {len(first_col)} valeurs")
                            else:
                                # Ajuster la longueur
                                if len(first_col) > len(self.df_cleaned):
                                    self.df_cleaned[col] = first_col[:len(self.df_cleaned)].values
                                else:
                                    # Étendre avec des NaN
                                    extended_values = [first_col.iloc[i] if i < len(first_col) else np.nan for i in range(len(self.df_cleaned))]
                                    self.df_cleaned[col] = extended_values
                                logger.info(f"    {col} ajusté à {len(self.df_cleaned)} valeurs")
                        else:
                            logger.warning(f"    {col} est un DataFrame vide, remplacement par des NaN")
                            self.df_cleaned[col] = np.nan
                    
                    # Vérifier que c'est maintenant une Series
                    if not isinstance(self.df_cleaned[col], pd.Series):
                        self.df_cleaned[col] = pd.Series(self.df_cleaned[col])
                        
                except Exception as e:
                    logger.error(f"    Erreur lors de la correction de {col}: {e}")
                    # En cas d'erreur, remplacer par des NaN
                    self.df_cleaned[col] = np.nan
        
        logger.info("✅ Colonnes problématiques corrigées")
    
    def _clean_numeric_columns(self):
        """Nettoie les colonnes numériques"""
        logger.info("💰 Nettoyage des colonnes numériques...")
        
        # Colonnes numériques à nettoyer
        numeric_cols = ['price', 'revenu', 'plex-revenue', 'surface', 'bedrooms', 'bathrooms']
        
        for col in numeric_cols:
            if col in self.df_cleaned.columns:
                try:
                    # Convertir en numérique
                    self.df_cleaned[col] = pd.to_numeric(self.df_cleaned[col], errors='coerce')
                    
                    # Remplacer les valeurs aberrantes par la médiane
                    if col in ['bedrooms', 'bathrooms']:
                        median_val = self.df_cleaned[col].median()
                        if pd.notna(median_val):
                            self.df_cleaned[col] = self.df_cleaned[col].fillna(median_val)
                    
                    logger.info(f"    {col} nettoyé")
                    
                except Exception as e:
                    logger.error(f"    Erreur lors du nettoyage de {col}: {e}")
        
        logger.info("✅ Colonnes numériques nettoyées")
    
    def _clean_date_columns(self):
        """Nettoie les colonnes de dates"""
        logger.info("📅 Nettoyage des colonnes de dates...")
        
        # Colonnes de dates à nettoyer
        date_cols = ['created_at', 'updated_at', 'add_date']
        
        for col in date_cols:
            if col in self.df_cleaned.columns:
                try:
                    # Convertir en datetime
                    self.df_cleaned[col] = pd.to_datetime(self.df_cleaned[col], errors='coerce')
                    logger.info(f"    {col} converti en datetime")
                    
                except Exception as e:
                    logger.error(f"    Erreur lors du nettoyage de {col}: {e}")
        
        logger.info("✅ Colonnes de dates nettoyées")
    
    def _remove_duplicates(self):
        """Supprime les doublons"""
        logger.info("🔄 Suppression des doublons...")
        
        initial_count = len(self.df_cleaned)
        
        # Supprimer les doublons basés sur l'adresse et le prix
        if 'address' in self.df_cleaned.columns and 'price' in self.df_cleaned.columns:
            self.df_cleaned = self.df_cleaned.drop_duplicates(subset=['address', 'price'], keep='first')
        else:
            # Fallback: supprimer les doublons complets
            self.df_cleaned = self.df_cleaned.drop_duplicates(keep='first')
        
        final_count = len(self.df_cleaned)
        duplicates_removed = initial_count - final_count
        
        logger.info(f"✅ Doublons supprimés: {duplicates_removed} propriétés")
    
    def save_cleaned_data(self, output_path: str = None) -> bool:
        """Sauvegarde les données nettoyées"""
        try:
            if output_path is None:
                # Créer un nom de fichier automatique
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"cleaned_real_estate_data_{timestamp}.csv"
            
            # Sauvegarder en CSV
            self.df_cleaned.to_csv(output_path, index=False)
            logger.info(f"💾 Données nettoyées sauvegardées: {output_path}")
            
            # Sauvegarder aussi en Parquet
            parquet_path = output_path.replace('.csv', '.parquet')
            self.df_cleaned.to_parquet(parquet_path, index=False)
            logger.info(f"💾 Données nettoyées sauvegardées (Parquet): {parquet_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def get_summary(self) -> dict:
        """Retourne un résumé du nettoyage"""
        if self.df_cleaned is None:
            return {"error": "Aucune donnée disponible"}
        
        summary = {
            "original_shape": self.df_original.shape if self.df_original is not None else None,
            "cleaned_shape": self.df_cleaned.shape,
            "columns": list(self.df_cleaned.columns),
            "missing_values": self.df_cleaned.isnull().sum().to_dict(),
            "data_types": self.df_cleaned.dtypes.to_dict()
        }
        
        return summary

def main():
    """Fonction principale pour l'exécution en ligne de commande"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Nettoyage simplifié des données immobilières")
    parser.add_argument("input_file", help="Fichier CSV d'entrée")
    parser.add_argument("-o", "--output", help="Fichier de sortie (optionnel)")
    
    args = parser.parse_args()
    
    # Créer le nettoyeur
    cleaner = SimpleRealEstateCleaner()
    
    # Charger les données
    if not cleaner.load_data(args.input_file):
        logger.error("❌ Échec du chargement des données")
        return 1
    
    # Nettoyer les données
    if not cleaner.clean_data():
        logger.error("❌ Échec du nettoyage des données")
        return 1
    
    # Sauvegarder les données nettoyées
    if not cleaner.save_cleaned_data(args.output):
        logger.error("❌ Échec de la sauvegarde des données")
        return 1
    
    # Afficher le résumé
    summary = cleaner.get_summary()
    logger.info("📊 RÉSUMÉ DU NETTOYAGE:")
    logger.info(f"  Forme originale: {summary['original_shape']}")
    logger.info(f"  Forme nettoyée: {summary['cleaned_shape']}")
    logger.info(f"  Colonnes: {len(summary['columns'])}")
    
    logger.info("✅ NETTOYAGE TERMINÉ AVEC SUCCÈS!")
    return 0

if __name__ == "__main__":
    exit(main())
