"""
Module principal d'analyse immobilière
Point d'entrée unifié pour tous les composants d'analyse
"""

import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imports des composants modulaires
from .interfaces import IDataProcessor, IPropertyClassifier, IFeatureSelector
from .validators import DataValidator
from .data_processors import PropertyDataProcessor
from .classifiers import PropertyClassifier
from .feature_selectors import FeatureSelector
from .analyzers import PropertyAnalyzer

# Exposer les classes principales pour une utilisation directe
__all__ = [
    'PropertyAnalyzer',
    'PropertyDataProcessor', 
    'PropertyClassifier',
    'FeatureSelector',
    'DataValidator',
    'IDataProcessor',
    'IPropertyClassifier', 
    'IFeatureSelector'
]

"""
Analyse avancée des propriétés immobilières avec optimisations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
import time

from .analyzers import PropertyAnalyzer as BasePropertyAnalyzer
from .data_processors import PropertyDataProcessor
from .feature_selectors import AdaptiveFeatureSelector, FastFeatureSelector, HybridFeatureSelector
from .classifiers import PropertyClassifier

logger = logging.getLogger(__name__)


class OptimizedPropertyAnalyzer(BasePropertyAnalyzer):
    """
    Analyseur de propriétés optimisé avec sélection adaptative automatique
    Hérite de PropertyAnalyzer mais utilise les nouveaux sélecteurs optimisés
    """
    
    def __init__(self, 
                 data_processor: Optional[PropertyDataProcessor] = None,
                 property_classifier: Optional[PropertyClassifier] = None,
                 feature_selector: Optional[Any] = None,
                 use_adaptive_selection: bool = True,
                 random_state: int = 42):
        
        # Initialiser le parent avec le processeur fourni ou par défaut
        super().__init__(
            data_processor=data_processor,
            property_classifier=property_classifier,
            feature_selector=feature_selector
        )
        
        self.use_adaptive_selection = use_adaptive_selection
        self.random_state = random_state
        self.analysis_metadata = {}
        
        # Remplacer le feature_selector par le sélecteur adaptatif si demandé
        if use_adaptive_selection:
            try:
                self.feature_selector = AdaptiveFeatureSelector(random_state=random_state)
                logger.info("🤖 Sélecteur adaptatif activé")
            except Exception as e:
                logger.warning(f"⚠️ Impossible d'activer le sélecteur adaptatif: {e}")
    
    def analyze_properties_optimized(self, 
                                   df: pd.DataFrame, 
                                   target_column: str = 'price',
                                   enable_classification_analysis: bool = True,
                                   max_processing_time: Optional[int] = None) -> Dict[str, Any]:
        """
        Analyse optimisée avec gestion du temps et adaptation automatique
        
        Args:
            df: DataFrame des propriétés
            target_column: Colonne cible pour la prédiction
            enable_classification_analysis: Activer l'analyse par classification
            max_processing_time: Temps maximum en secondes (None = pas de limite)
        
        Returns:
            Dictionnaire avec résultats d'analyse optimisés
        """
        start_time = time.time()
        data_size = len(df)
        
        logger.info(f"🚀 Analyse optimisée: {data_size:,} propriétés")
        print(f"\n🚀 === ANALYSE OPTIMISÉE DES PROPRIÉTÉS ===")
        print(f"📊 Volume: {data_size:,} propriétés")
        print(f"🎯 Variable cible: '{target_column}'")
        print(f"⏱️ Limite temps: {max_processing_time}s" if max_processing_time else "⏱️ Pas de limite de temps")
        
        # Déterminer la stratégie optimale
        strategy = self._determine_strategy(data_size, max_processing_time)
        print(f"🤖 Stratégie sélectionnée: {strategy}")
        
        self.analysis_metadata = {
            'start_time': start_time,
            'data_size': data_size,
            'strategy': strategy,
            'target_column': target_column,
            'max_processing_time': max_processing_time
        }
        
        try:
            # Analyse selon la stratégie choisie
            if strategy == "ultra_fast":
                results = self._ultra_fast_analysis(df, target_column)
            elif strategy == "fast":
                results = self._fast_analysis(df, target_column)
            elif strategy == "balanced":
                results = self._balanced_analysis(df, target_column, enable_classification_analysis)
            else:  # strategy == "complete"
                results = self._complete_analysis(df, target_column, enable_classification_analysis)
            
            # Ajouter métadonnées
            elapsed_time = time.time() - start_time
            results['analysis_metadata'] = self.analysis_metadata
            results['analysis_metadata']['elapsed_time'] = elapsed_time
            results['analysis_metadata']['success'] = True
            
            print(f"\n✅ Analyse terminée en {elapsed_time:.1f}s")
            print(f"🎯 Variables sélectionnées: {len(results.get('selected_features', []))}")
            
            return results
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"❌ Erreur analyse optimisée: {e}")
            
            # Fallback vers analyse basique
            print(f"\n⚠️ Fallback vers analyse basique...")
            return self._fallback_analysis(df, target_column, elapsed_time, str(e))
    
    def _determine_strategy(self, data_size: int, max_time: Optional[int]) -> str:
        """Détermine la stratégie optimale selon les contraintes"""
        
        if max_time and max_time < 300:  # Moins de 5 minutes
            return "ultra_fast"
        elif data_size > 100000:
            return "ultra_fast"
        elif data_size > 50000:
            return "fast"
        elif data_size > 20000:
            return "balanced"
        else:
            return "complete"
    
    def _ultra_fast_analysis(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Analyse ultra-rapide pour très gros volumes"""
        print(f"\n⚡ === ANALYSE ULTRA-RAPIDE ===")
        
        # Nettoyage minimal
        print(f"🧹 Nettoyage rapide...")
        df_clean = self.data_processor.clean_data(df)
        
        # Échantillonnage agressif pour sélection
        sample_size = min(5000, len(df_clean))
        print(f"📊 Échantillonnage pour sélection: {sample_size:,}")
        
        df_sample = df_clean.sample(n=sample_size, random_state=self.random_state)
        
        # Préparation rapide
        df_encoded = self.data_processor.encode_features(df_sample)
        if target_column not in df_encoded.columns:
            raise ValueError(f"Variable cible '{target_column}' non disponible")
        
        X = df_encoded.select_dtypes(include=[np.number]).drop(columns=[target_column])
        y = df_encoded[target_column]
        
        # Nettoyage valeurs manquantes
        mask = X.isnull().any(axis=1) | y.isnull()
        X = X[~mask]
        y = y[~mask]
        
        # Sélection ultra-rapide (corrélation seulement)
        print(f"🔍 Sélection par corrélation...")
        correlations = X.corrwith(y).abs().sort_values(ascending=False)
        selected_features = correlations.head(10).index.tolist()
        
        return {
            'selected_features': selected_features,
            'df_cleaned': df_clean,
            'feature_importance': dict(zip(selected_features, correlations[selected_features])),
            'strategy_used': 'ultra_fast',
            'sample_size': sample_size
        }
    
    def _fast_analysis(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Analyse rapide avec FastFeatureSelector"""
        print(f"\n⚡ === ANALYSE RAPIDE ===")
        
        # Nettoyage
        df_clean = self.data_processor.clean_data(df)
        
        # Classification rapide
        print(f"🏠 Classification rapide...")
        df_classified = self.property_classifier.classify_properties(df_clean)
        classification_stats = self.property_classifier.get_classification_stats(df_classified)
        
        # Préparation
        df_prepared = self.data_processor.impute_missing_values(df_classified)
        df_encoded = self.data_processor.encode_features(df_prepared)
        
        if target_column not in df_encoded.columns:
            raise ValueError(f"Variable cible '{target_column}' non disponible")
        
        X = df_encoded.select_dtypes(include=[np.number]).drop(columns=[target_column])
        y = df_encoded[target_column]
        
        # Sélection rapide
        fast_selector = FastFeatureSelector(
            sample_size=min(10000, len(X)),
            rf_estimators=20
        )
        selected_features = fast_selector.select_features(X, y)
        
        return {
            'selected_features': selected_features,
            'df_cleaned': df_classified,
            'df_prepared': df_encoded,
            'classification_stats': classification_stats,
            'feature_importance': fast_selector.get_feature_importance(X, y),
            'strategy_used': 'fast',
            'X': X[selected_features] if selected_features else X,
            'y': y
        }
    
    def _balanced_analysis(self, df: pd.DataFrame, target_column: str, 
                          enable_classification_analysis: bool) -> Dict[str, Any]:
        """Analyse équilibrée avec HybridFeatureSelector"""
        print(f"\n🎯 === ANALYSE ÉQUILIBRÉE ===")
        
        # Analyse standard mais avec sélecteur hybride
        df_clean = self.data_processor.clean_data(df)
        df_classified = self.property_classifier.classify_properties(df_clean)
        classification_stats = self.property_classifier.get_classification_stats(df_classified)
        
        df_prepared = self.data_processor.impute_missing_values(df_classified)
        df_encoded = self.data_processor.encode_features(df_prepared)
        
        if target_column not in df_encoded.columns:
            raise ValueError(f"Variable cible '{target_column}' non disponible")
        
        X = df_encoded.select_dtypes(include=[np.number]).drop(columns=[target_column])
        y = df_encoded[target_column]
        
        # Sélection hybride
        hybrid_selector = HybridFeatureSelector(
            sample_size=min(15000, len(X)),
            rf_estimators=40
        )
        selected_features = hybrid_selector.select_features(X, y)
        
        results = {
            'selected_features': selected_features,
            'df_cleaned': df_classified,
            'df_prepared': df_encoded,
            'classification_stats': classification_stats,
            'feature_importance': hybrid_selector.get_feature_importance(X, y),
            'strategy_used': 'balanced',
            'X': X[selected_features] if selected_features else X,
            'y': y
        }
        
        # Analyse par classification si demandée
        if enable_classification_analysis and 'classification_immobiliere' in df_classified.columns:
            print(f"🏠 Analyse par type de propriété...")
            classification_features = hybrid_selector.select_features_by_classification(
                X, y, df_classified.loc[X.index, 'classification_immobiliere']
            )
            results['classification_features'] = classification_features
        
        return results
    
    def _complete_analysis(self, df: pd.DataFrame, target_column: str,
                          enable_classification_analysis: bool) -> Dict[str, Any]:
        """Analyse complète avec sélecteur adaptatif"""
        print(f"\n🔬 === ANALYSE COMPLÈTE ===")
        
        # Utiliser la méthode parent mais avec notre sélecteur adaptatif
        return self.analyze_properties(df, target_column)
    
    def _fallback_analysis(self, df: pd.DataFrame, target_column: str, 
                          elapsed_time: float, error_msg: str) -> Dict[str, Any]:
        """Analyse de fallback minimaliste"""
        print(f"🔄 Analyse basique de sauvetage...")
        
        try:
            df_clean = self.data_processor.clean_data(df)
            
            # Sélection minimale par corrélation
            if target_column in df_clean.columns:
                numeric_cols = df_clean.select_dtypes(include=[np.number])
                if target_column in numeric_cols.columns:
                    correlations = numeric_cols.corrwith(numeric_cols[target_column]).abs()
                    correlations = correlations.sort_values(ascending=False)
                    selected_features = correlations.head(5).index.tolist()
                    if target_column in selected_features:
                        selected_features.remove(target_column)
                else:
                    selected_features = []
            else:
                selected_features = []
            
            return {
                'selected_features': selected_features,
                'df_cleaned': df_clean,
                'strategy_used': 'fallback',
                'error_message': error_msg,
                'analysis_metadata': {
                    'elapsed_time': elapsed_time,
                    'success': False,
                    'fallback_used': True
                }
            }
            
        except Exception as e2:
            logger.error(f"❌ Erreur critique fallback: {e2}")
            return {
                'selected_features': [],
                'df_cleaned': df,
                'strategy_used': 'critical_fallback',
                'error_message': f"Erreur principale: {error_msg}, Erreur fallback: {str(e2)}",
                'analysis_metadata': {
                    'elapsed_time': elapsed_time,
                    'success': False,
                    'critical_fallback_used': True
                }
            }
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Génère un rapport sur les optimisations utilisées"""
        if not self.analysis_metadata:
            return {"error": "Aucune analyse effectuée"}
        
        metadata = self.analysis_metadata
        
        report = {
            "volume_data": metadata.get('data_size', 0),
            "strategie_utilisee": metadata.get('strategy', 'unknown'),
            "temps_execution": metadata.get('elapsed_time', 0),
            "succes": metadata.get('success', False),
            "optimisations": {
                "selecteur_adaptatif": self.use_adaptive_selection,
                "echantillonnage": metadata.get('sample_size') is not None,
                "fallback_utilise": metadata.get('fallback_used', False)
            }
        }
        
        # Recommandations
        data_size = metadata.get('data_size', 0)
        elapsed_time = metadata.get('elapsed_time', 0)
        
        recommendations = []
        if data_size > 100000 and elapsed_time > 600:
            recommendations.append("Considérer l'échantillonnage pour futures analyses")
        if not metadata.get('success', False):
            recommendations.append("Vérifier la qualité des données d'entrée")
        if metadata.get('fallback_used', False):
            recommendations.append("Optimiser les paramètres de nettoyage")
        
        report["recommandations"] = recommendations
        
        return report

# Code de test pour démontrer les améliorations
if __name__ == "__main__":
    # Créer des données de test
    print("🔧 === TEST DU SYSTÈME MODULAIRE ===")
    print("Création de données de test...")
    
    import pandas as pd
    import numpy as np
    
    # Générer des données factices
    np.random.seed(42)
    n_samples = 1000
    
    test_data = {
        'price': np.random.normal(500000, 200000, n_samples),
        'surface': np.random.normal(150, 50, n_samples),
        'longitude': np.random.normal(-73.6, 0.1, n_samples),
        'latitude': np.random.normal(45.5, 0.1, n_samples),
        'construction_year': np.random.randint(1950, 2025, n_samples),
        'type': np.random.choice(['Maison', 'Condo', 'Duplex', 'Triplex'], n_samples),
        'revenu': np.random.normal(2000, 1000, n_samples),
        'nb_bathroom': np.random.randint(1, 4, n_samples),
        'municipal_evaluation_total': np.random.normal(400000, 150000, n_samples),
        'school_taxes': np.random.normal(3000, 1000, n_samples),
        # Colonnes problématiques pour tester le nettoyage
        '_id': range(n_samples),
        'link': ['http://example.com'] * n_samples,
        'images': [None] * n_samples,  # Colonne entièrement vide
        'useless_col': ['same_value'] * n_samples,  # Une seule valeur
        # Colonnes avec beaucoup de valeurs manquantes
        'mostly_missing': [np.nan] * int(n_samples * 0.97) + [1] * int(n_samples * 0.03)
    }
    
    # Introduire quelques valeurs manquantes
    for col in ['surface', 'construction_year', 'revenu']:
        missing_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
        for idx in missing_indices:
            test_data[col][idx] = np.nan
    
    # Créer le DataFrame
    df_test = pd.DataFrame(test_data)
    
    print(f"✅ Données de test créées: {df_test.shape}")
    print("🚀 Lancement du test complet...\n")
    
    # Tester le pipeline complet
    try:
        analyzer = PropertyAnalyzer()
        results = analyzer.analyze_properties(df_test, target_column='price')
        
        print(f"\n🎉 === TEST RÉUSSI! ===")
        print(f"Variables sélectionnées: {results['selected_features']}")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc() 