"""
Interfaces abstraites pour le système d'analyse immobilière
Respecte les principes SOLID pour une meilleure maintenabilité
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import pandas as pd


class IDataProcessor(ABC):
    """Interface pour le traitement des données"""
    
    @abstractmethod
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Nettoie les données en supprimant les colonnes problématiques"""
        pass
    
    @abstractmethod
    def encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode les variables catégorielles"""
        pass
    
    @abstractmethod
    def impute_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute les valeurs manquantes"""
        pass


class IPropertyClassifier(ABC):
    """Interface pour la classification des propriétés"""
    
    @abstractmethod
    def classify_properties(self, df: pd.DataFrame) -> pd.DataFrame:
        """Classifie les propriétés selon différents critères"""
        pass
    
    @abstractmethod
    def get_classification_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Retourne les statistiques de classification"""
        pass


class IFeatureSelector(ABC):
    """Interface pour la sélection de variables"""
    
    @abstractmethod
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélectionne les variables importantes"""
        pass
    
    @abstractmethod
    def get_feature_importance(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Retourne l'importance des variables"""
        pass 