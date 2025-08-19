#!/usr/bin/env python3
"""
Utilitaires pour la gestion des logs
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import os

class LoggingUtils:
    """Utilitaires pour la configuration des logs"""
    
    @staticmethod
    def setup_logging(
        log_level: str = "INFO",
        log_file: Path = None,
        log_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    ) -> logging.Logger:
        """Configure le système de logging"""
        
        # Créer le logger principal
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Supprimer les handlers existants
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Handler pour la console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # Handler pour le fichier si spécifié
        if log_file:
            try:
                # Créer le dossier des logs si nécessaire
                log_file.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(getattr(logging, log_level.upper()))
                file_formatter = logging.Formatter(log_format)
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
                
                logger.info(f"Logs sauvegardés dans: {log_file}")
            except Exception as e:
                logger.warning(f"Impossible de configurer le fichier de log: {e}")
        
        return logger
    
    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        """Retourne un logger configuré"""
        if name:
            return logging.getLogger(name)
        return logging.getLogger()
    
    @staticmethod
    def log_execution_time(func):
        """Décorateur pour logger le temps d'exécution d'une fonction"""
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger = LoggingUtils.get_logger()
            
            logger.info(f"🚀 Démarrage de {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                execution_time = datetime.now() - start_time
                logger.info(f"✅ {func.__name__} terminé en {execution_time.total_seconds():.2f}s")
                return result
            except Exception as e:
                execution_time = datetime.now() - start_time
                logger.error(f"❌ {func.__name__} échoué après {execution_time.total_seconds():.2f}s: {e}")
                raise
        
        return wrapper
