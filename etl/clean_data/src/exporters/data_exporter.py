#!/usr/bin/env python3
"""
Exporteur de données pour différents formats
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    """Gère l'export des données dans différents formats"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """S'assure que le dossier de sortie existe"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_data(self, df: pd.DataFrame, base_filename: str = None) -> dict:
        """
        Exporte les données dans tous les formats supportés
        
        Args:
            df: DataFrame à exporter
            base_filename: Nom de base pour les fichiers (sans extension)
            
        Returns:
            Dict avec les chemins des fichiers exportés
        """
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"real_estate_cleaned_{timestamp}"
        
        exported_files = {}
        
        # Export Parquet (performance optimale)
        parquet_file = self.export_parquet(df, base_filename)
        if parquet_file:
            exported_files['parquet'] = parquet_file
        
        # Export CSV (compatibilité universelle)
        csv_file = self.export_csv(df, base_filename)
        if csv_file:
            exported_files['csv'] = csv_file
        
        # Export JSON (pour applications web)
        json_file = self.export_json(df, base_filename)
        if json_file:
            exported_files['json'] = json_file
        
        # Export GeoJSON si coordonnées disponibles
        if 'longitude' in df.columns and 'latitude' in df.columns:
            geojson_file = self.export_geojson(df, base_filename)
            if geojson_file:
                exported_files['geojson'] = geojson_file
        
        logger.info(f"✅ Export terminé: {len(exported_files)} formats")
        return exported_files
    
    def export_parquet(self, df: pd.DataFrame, base_filename: str) -> Path:
        """Exporte en format Parquet"""
        try:
            output_file = self.output_dir / f"{base_filename}.parquet"
            df.to_parquet(output_file, index=False)
            logger.info(f"✅ Export Parquet: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"❌ Erreur export Parquet: {e}")
            return None
    
    def export_csv(self, df: pd.DataFrame, base_filename: str) -> Path:
        """Exporte en format CSV"""
        try:
            output_file = self.output_dir / f"{base_filename}.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"✅ Export CSV: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"❌ Erreur export CSV: {e}")
            return None
    
    def export_json(self, df: pd.DataFrame, base_filename: str) -> Path:
        """Exporte en format JSON"""
        try:
            output_file = self.output_dir / f"{base_filename}.json"
            df.to_json(output_file, orient='records', indent=2)
            logger.info(f"✅ Export JSON: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"❌ Erreur export JSON: {e}")
            return None
    
    def export_geojson(self, df: pd.DataFrame, base_filename: str) -> Path:
        """Exporte en format GeoJSON pour cartes interactives"""
        try:
            output_file = self.output_dir / f"{base_filename}.geojson"
            
            # Créer un GeoDataFrame
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(
                    df['longitude'], 
                    df['latitude']
                ),
                crs="EPSG:4326"
            )
            
            # Exporter
            gdf.to_file(output_file, driver='GeoJSON')
            logger.info(f"✅ Export GeoJSON: {output_file}")
            return output_file
            
        except Exception as e:
            logger.warning(f"⚠️ Export GeoJSON échoué: {e}")
            return None
