#!/usr/bin/env python3
"""
Utilitaires pour la gestion des fichiers
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    """Utilitaires pour la gestion des fichiers"""
    
    @staticmethod
    def ensure_directory(directory_path: Path) -> bool:
        """S'assure qu'un dossier existe"""
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la création du dossier {directory_path}: {e}")
            return False
    
    @staticmethod
    def cleanup_old_files(directory_path: Path, days_to_keep: int = 30) -> int:
        """Nettoie les anciens fichiers d'un dossier"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cleaned_count = 0
            
            for file_path in directory_path.glob("*"):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_date:
                        file_path.unlink()
                        cleaned_count += 1
            
            return cleaned_count
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage de {directory_path}: {e}")
            return 0
    
    @staticmethod
    def get_file_size_mb(file_path: Path) -> float:
        """Retourne la taille d'un fichier en MB"""
        try:
            return file_path.stat().st_size / (1024 * 1024)
        except Exception:
            return 0.0
    
    @staticmethod
    def get_directory_info(directory_path: Path) -> dict:
        """Retourne les informations d'un dossier"""
        try:
            if not directory_path.exists():
                return {"exists": False}
            
            files = list(directory_path.glob("*"))
            total_size = sum(
                FileUtils.get_file_size_mb(f) for f in files if f.is_file()
            )
            
            return {
                "exists": True,
                "file_count": len(files),
                "total_size_mb": total_size,
                "last_modified": datetime.fromtimestamp(
                    directory_path.stat().st_mtime
                ).isoformat()
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de {directory_path}: {e}")
            return {"exists": False, "error": str(e)}
