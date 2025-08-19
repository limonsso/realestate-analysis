"""
Classes de validation pour le système d'analyse immobilière
"""

from typing import List
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Classe pour valider les données"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Valide qu'un DataFrame contient les colonnes requises"""
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            logger.error(f"Colonnes manquantes: {missing_columns}")
            return False
        return True
    
    @staticmethod
    def validate_target_column(df: pd.DataFrame, target_column: str) -> bool:
        """Valide que la colonne cible existe et n'est pas vide"""
        if target_column not in df.columns:
            logger.error(f"Colonne cible '{target_column}' manquante")
            return False
        
        if df[target_column].isna().all():
            logger.error(f"Colonne cible '{target_column}' entièrement vide")
            return False
        
        return True 