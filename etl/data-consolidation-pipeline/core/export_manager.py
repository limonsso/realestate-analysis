#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 GESTIONNAIRE D'EXPORT
========================

Gère l'export des données dans différents formats
"""

import logging
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import time

logger = logging.getLogger(__name__)

class ExportManager:
    """
    Gestionnaire d'export pour le pipeline ETL
    
    Responsable de l'export des données dans différents formats
    et de la gestion des fichiers de sortie
    """
    
    def __init__(self, pipeline_manager):
        """
        Initialise le gestionnaire d'export
        
        Args:
            pipeline_manager: Instance du gestionnaire de pipeline
        """
        self.pipeline_manager = pipeline_manager
        self.exported_files = {}
    
    def export_data(self, df: pd.DataFrame, pipeline_name: str, 
                    formats: List[str], output_dir: str) -> Dict[str, str]:
        """
        Exporte les données dans les formats spécifiés
        
        Args:
            df: DataFrame à exporter
            pipeline_name: Nom du pipeline pour l'export
            formats: Liste des formats d'export
            output_dir: Répertoire de sortie
            
        Returns:
            Dict avec les chemins des fichiers exportés
        """
        logger.info("💾 === PHASE 6: EXPORT MULTI-FORMATS ===")
        
        if self.pipeline_manager.exporter is None:
            logger.warning("⚠️ AdvancedExporter non disponible, export basique utilisé")
            return self._basic_export(df, pipeline_name, formats, output_dir)
        
        try:
            logger.info(f"💾 === EXPORT MULTI-FORMATS: {pipeline_name} ===")
            
            start_time = time.time()
            exported_files = self.pipeline_manager.exporter.export_dataset(
                df, pipeline_name, formats, output_dir
            )
            export_time = time.time() - start_time
            
            logger.info(f"🎯 Export terminé en {export_time:.2f}s")
            logger.info(f"📊 {len(exported_files)}/{len(formats)} formats exportés avec succès")
            
            self.exported_files = exported_files
            return exported_files
            
        except Exception as e:
            logger.error(f"❌ Erreur export avancé: {e}, fallback vers export basique")
            return self._basic_export(df, pipeline_name, formats, output_dir)
    
    def _basic_export(self, df: pd.DataFrame, pipeline_name: str,
                      formats: List[str], output_dir: str) -> Dict[str, str]:
        """Export basique en cas d'échec de l'exporteur avancé"""
        logger.info("📤 Export basique activé...")
        
        exported_files = {}
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        for format_type in formats:
            try:
                if format_type.lower() == "csv":
                    filename = f"real_estate_data_{pipeline_name}_{timestamp}.csv"
                    filepath = output_path / filename
                    df.to_csv(filepath, index=False, encoding='utf-8')
                    exported_files["csv"] = str(filepath)
                    logger.info(f"✅ CSV exporté: {filepath}")
                    
                elif format_type.lower() == "json":
                    filename = f"real_estate_data_{pipeline_name}_{timestamp}.json"
                    filepath = output_path / filename
                    df.to_json(filepath, orient='records', indent=2, force_ascii=False)
                    exported_files["json"] = str(filepath)
                    logger.info(f"✅ JSON exporté: {filepath}")
                    
                elif format_type.lower() == "parquet":
                    try:
                        filename = f"real_estate_data_{pipeline_name}_{timestamp}.parquet"
                        filepath = output_path / filename
                        df.to_parquet(filepath, index=False)
                        exported_files["parquet"] = str(filepath)
                        logger.info(f"✅ Parquet exporté: {filepath}")
                    except ImportError:
                        logger.warning("⚠️ PyArrow non disponible, export Parquet ignoré")
                        
                else:
                    logger.warning(f"⚠️ Format non supporté: {format_type}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur export {format_type}: {e}")
        
        logger.info(f"📊 {len(exported_files)}/{len(formats)} formats exportés avec succès")
        return exported_files
    
    def get_export_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des exports effectués"""
        return {
            "total_formats": len(self.exported_files),
            "exported_files": self.exported_files,
            "export_status": "success" if self.exported_files else "failed"
        }
    
    def cleanup_exports(self, keep_files: bool = True):
        """
        Nettoie les fichiers d'export temporaires
        
        Args:
            keep_files: Si False, supprime les fichiers exportés
        """
        if not keep_files and self.exported_files:
            logger.info("🧹 Nettoyage des fichiers d'export...")
            for format_type, filepath in self.exported_files.items():
                try:
                    Path(filepath).unlink(missing_ok=True)
                    logger.info(f"🗑️ Fichier supprimé: {filepath}")
                except Exception as e:
                    logger.warning(f"⚠️ Impossible de supprimer {filepath}: {e}")
            self.exported_files = {}
