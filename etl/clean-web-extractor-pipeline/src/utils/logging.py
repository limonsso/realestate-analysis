"""
Configuration du système de logging
Utilise structlog pour un logging structuré et moderne
"""

import sys
import logging
from pathlib import Path
from typing import Optional

import structlog
from structlog.stdlib import LoggerFactory
from structlog.processors import (
    TimeStamper, add_log_level, format_exc_info,
    JSONRenderer
)


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "json"
):
    """
    Configure le système de logging avec structlog
    
    Args:
        log_level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Chemin vers le fichier de log (optionnel)
        log_format: Format des logs (json ou console)
    """
    # Configuration des niveaux de logging
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    log_level_num = level_map.get(log_level.upper(), logging.INFO)
    
    # Configuration de structlog
    structlog.configure(
        processors=[
            # Ajout du timestamp
            TimeStamper(fmt="iso"),
            
            # Ajout du niveau de log
            add_log_level,
            
            # Gestion des exceptions
            format_exc_info,
            
            # Formatage final
            JSONRenderer() if log_format == "json" else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configuration du logging standard Python
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level_num
    )
    
    # Configuration du fichier de log si spécifié
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level_num)
        
        # Formatter pour le fichier
        if log_format == "json":
            file_formatter = logging.Formatter('%(message)s')
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        
        # Ajout du handler au logger racine
        logging.getLogger().addHandler(file_handler)
    
    # Configuration des loggers tiers
    _configure_third_party_loggers(log_level_num)
    
    # Log de démarrage
    logger = structlog.get_logger()
    logger.info(
        "🚀 Système de logging initialisé",
        log_level=log_level,
        log_file=log_file,
        log_format=log_format
    )


def _configure_third_party_loggers(log_level: int):
    """Configure les loggers des bibliothèques tierces"""
    # Réduction du bruit des bibliothèques externes
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # Configuration des niveaux
    for logger_name in [
        "urllib3", "requests", "aiohttp", "motor", "pymongo", "asyncio"
    ]:
        logging.getLogger(logger_name).setLevel(log_level)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """
    Retourne un logger configuré
    
    Args:
        name: Nom du logger (optionnel)
        
    Returns:
        Logger structlog configuré
    """
    return structlog.get_logger(name)


def log_function_call(func_name: str = None):
    """
    Décorateur pour logger les appels de fonction
    
    Args:
        func_name: Nom de la fonction (optionnel, utilise le nom de la fonction décorée par défaut)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            function_name = func_name or func.__name__
            
            logger.debug(
                "🔍 Appel de fonction",
                function=function_name,
                args_count=len(args),
                kwargs_count=len(kwargs)
            )
            
            try:
                result = func(*args, **kwargs)
                logger.debug(
                    "✅ Fonction terminée avec succès",
                    function=function_name
                )
                return result
            except Exception as e:
                logger.error(
                    "❌ Erreur dans la fonction",
                    function=function_name,
                    error=str(e),
                    error_type=type(e).__name__
                )
                raise
        
        return wrapper
    return decorator


def log_execution_time(func_name: str = None):
    """
    Décorateur pour logger le temps d'exécution des fonctions
    
    Args:
        func_name: Nom de la fonction (optionnel)
    """
    import time
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            function_name = func_name or func.__name__
            
            start_time = time.time()
            
            logger.debug(
                "⏱️ Début d'exécution",
                function=function_name
            )
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.info(
                    "✅ Exécution terminée",
                    function=function_name,
                    execution_time_seconds=execution_time,
                    execution_time_ms=execution_time * 1000
                )
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                
                logger.error(
                    "❌ Erreur d'exécution",
                    function=function_name,
                    execution_time_seconds=execution_time,
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator


class LogContext:
    """Contexte de logging pour tracer les opérations"""
    
    def __init__(self, operation: str, **context_data):
        self.operation = operation
        self.context_data = context_data
        self.logger = get_logger()
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(
            "🚀 Début d'opération",
            operation=self.operation,
            **self.context_data
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info(
                "✅ Opération terminée avec succès",
                operation=self.operation,
                execution_time_seconds=execution_time,
                **self.context_data
            )
        else:
            self.logger.error(
                "❌ Opération échouée",
                operation=self.operation,
                execution_time_seconds=execution_time,
                error=str(exc_val),
                error_type=exc_type.__name__,
                **self.context_data
            )
    
    def log_step(self, step: str, **step_data):
        """Log une étape de l'opération"""
        self.logger.debug(
            "📋 Étape d'opération",
            operation=self.operation,
            step=step,
            **step_data
        )
    
    def log_progress(self, current: int, total: int, **progress_data):
        """Log le progrès de l'opération"""
        percentage = (current / total) * 100 if total > 0 else 0
        
        self.logger.info(
            "📊 Progrès de l'opération",
            operation=self.operation,
            progress_current=current,
            progress_total=total,
            progress_percentage=percentage,
            **progress_data
        )


# Import time pour le contexte de logging
import time
