"""
Classes de sélection de variables pour l'analyse immobilière
Optimisées pour tous les volumes de données
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging
import time

from .interfaces import IFeatureSelector

logger = logging.getLogger(__name__)


class FastFeatureSelector(IFeatureSelector):
    """Sélecteur de variables optimisé pour très gros volumes (>100K)"""
    
    def __init__(self, 
                 sample_size: int = 8000,
                 random_state: int = 42,
                 correlation_threshold: float = 0.1,
                 univariate_k: int = 20,
                 rf_estimators: int = 20,
                 rf_max_depth: int = 10):
        self.sample_size = sample_size
        self.random_state = random_state
        self.correlation_threshold = correlation_threshold
        self.univariate_k = univariate_k
        self.rf_estimators = rf_estimators
        self.rf_max_depth = rf_max_depth
        self.selected_features_ = []
        self.feature_scores_ = {}
        
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection rapide optimisée pour gros volumes"""
        start_time = time.time()
        
        print(f"\n⚡ === SÉLECTION RAPIDE POUR GROS VOLUMES ===")
        print(f"📊 Données: {X.shape[0]:,} × {X.shape[1]}")
        
        # Échantillonnage stratifié si nécessaire
        X_work, y_work = self._create_sample(X, y)
        
        # 1. Sélection par corrélation (très rapide)
        corr_features = self._select_by_correlation(X_work, y_work)
        
        # 2. Sélection univariée (rapide)
        univariate_features = self._select_univariate(X_work, y_work)
        
        # 3. Random Forest léger (modéré)
        rf_features = self._select_rf_light(X_work, y_work)
        
        # 4. Combinaison intelligente
        selected = self._combine_methods(corr_features, univariate_features, rf_features)
        
        elapsed = time.time() - start_time
        print(f"\n✅ Sélection terminée en {elapsed:.1f}s")
        print(f"🎯 Variables sélectionnées: {len(selected)}")
        
        self.selected_features_ = selected
        return selected
    
    def _create_sample(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
        """Crée un échantillon stratifié"""
        if len(X) <= self.sample_size:
            print(f"✅ Données complètes utilisées: {len(X):,}")
            return X, y
            
        print(f"📊 Échantillonnage stratifié: {len(X):,} → {self.sample_size:,}")
        
        # Échantillonnage stratifié par quantiles de y
        try:
            stratify = pd.qcut(y, q=5, duplicates='drop')
            X_sample, _, y_sample, _ = train_test_split(
                X, y, train_size=self.sample_size, 
                random_state=self.random_state, stratify=stratify
            )
        except:
            # Fallback: échantillonnage simple
            X_sample, _, y_sample, _ = train_test_split(
                X, y, train_size=self.sample_size, 
                random_state=self.random_state
            )
        
        print(f"   ✅ Échantillon créé: {X_sample.shape}")
        return X_sample, y_sample
    
    def _select_by_correlation(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection par corrélation (instantané)"""
        print(f"\n📊 1. Sélection par corrélation...")
        start = time.time()
        
        correlations = X.corrwith(y).abs().sort_values(ascending=False)
        selected = correlations[correlations >= self.correlation_threshold].index.tolist()
        
        # Garder au minimum les 10 meilleures
        if len(selected) < 10:
            selected = correlations.head(10).index.tolist()
        
        elapsed = time.time() - start
        print(f"   ⚡ {len(selected)} variables en {elapsed:.2f}s")
        print(f"   🏆 Top 3: {selected[:3]}")
        
        # Stocker les scores
        for feature in selected:
            self.feature_scores_[feature] = correlations[feature]
        
        return selected
    
    def _select_univariate(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection univariée rapide"""
        print(f"\n🔬 2. Sélection univariée (f_regression)...")
        start = time.time()
        
        k = min(self.univariate_k, X.shape[1])
        selector = SelectKBest(score_func=f_regression, k=k)
        
        try:
            selector.fit(X, y)
            selected = X.columns[selector.get_support()].tolist()
            scores = selector.scores_
            
            elapsed = time.time() - start
            print(f"   ⚡ {len(selected)} variables en {elapsed:.2f}s")
            print(f"   🏆 Top 3: {selected[:3]}")
            
            # Stocker les scores normalisés
            max_score = max(scores) if len(scores) > 0 else 1
            for i, feature in enumerate(X.columns):
                if feature in selected:
                    self.feature_scores_[feature] = scores[i] / max_score
            
            return selected
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return []
    
    def _select_rf_light(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Random Forest léger et rapide"""
        print(f"\n🌲 3. Random Forest léger...")
        start = time.time()
        
        try:
            rf = RandomForestRegressor(
                n_estimators=self.rf_estimators,
                max_depth=self.rf_max_depth,
                random_state=self.random_state,
                n_jobs=-1,
                min_samples_split=5,
                min_samples_leaf=2
            )
            
            rf.fit(X, y)
            
            # Sélection basée sur l'importance médiane
            importances = rf.feature_importances_
            threshold = np.median(importances)
            selected = [X.columns[i] for i, imp in enumerate(importances) if imp >= threshold]
            
            elapsed = time.time() - start
            print(f"   ⚡ {len(selected)} variables en {elapsed:.2f}s")
            print(f"   📊 Seuil: {threshold:.4f}")
            print(f"   🏆 Top 3: {selected[:3]}")
            
            # Stocker les scores
            for i, feature in enumerate(X.columns):
                if feature in selected:
                    self.feature_scores_[feature] = importances[i]
            
            return selected
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return []
    
    def _combine_methods(self, corr_features: List[str], 
                        univariate_features: List[str], 
                        rf_features: List[str]) -> List[str]:
        """Combine intelligemment les résultats"""
        print(f"\n🔗 4. Combinaison des méthodes...")
        
        # Compter les votes pour chaque variable
        feature_votes = {}
        all_features = set(corr_features + univariate_features + rf_features)
        
        for feature in all_features:
            votes = 0
            if feature in corr_features:
                votes += 1
            if feature in univariate_features:
                votes += 1
            if feature in rf_features:
                votes += 1
            feature_votes[feature] = votes
        
        # Variables avec au moins 2 votes
        consensus_features = [f for f, v in feature_votes.items() if v >= 2]
        
        # Ajouter les meilleures variables de chaque méthode
        top_from_each = set()
        top_from_each.update(corr_features[:5])
        top_from_each.update(univariate_features[:5])
        top_from_each.update(rf_features[:5])
        
        # Combinaison finale
        final_features = list(set(consensus_features + list(top_from_each)))
        
        print(f"   📊 Corrélation: {len(corr_features)}")
        print(f"   📊 Univariée: {len(univariate_features)}")
        print(f"   📊 Random Forest: {len(rf_features)}")
        print(f"   🤝 Consensus (≥2 votes): {len(consensus_features)}")
        print(f"   🏆 Top de chaque: {len(top_from_each)}")
        print(f"   ✅ Final: {len(final_features)}")
        
        return final_features

    def get_feature_importance(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Retourne l'importance des variables sélectionnées"""
        return self.feature_scores_


class HybridFeatureSelector(IFeatureSelector):
    """Sélecteur hybride pour volumes moyens (20K-100K)"""
    
    def __init__(self, 
                 sample_size: int = 15000,
                 random_state: int = 42,
                 use_lasso: bool = True,
                 rf_estimators: int = 50):
        self.sample_size = sample_size
        self.random_state = random_state
        self.use_lasso = use_lasso
        self.rf_estimators = rf_estimators
        self.selected_features_ = []
        
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection hybride équilibrée"""
        start_time = time.time()
        
        print(f"\n🎯 === SÉLECTION HYBRIDE ÉQUILIBRÉE ===")
        print(f"📊 Données: {X.shape[0]:,} × {X.shape[1]}")
        
        # Échantillonnage si nécessaire
        X_work, y_work = self._create_sample(X, y)
        
        selected_features = []
        
        # 1. Méthodes rapides
        fast_selector = FastFeatureSelector(
            sample_size=min(8000, len(X_work)),
            rf_estimators=30
        )
        fast_features = fast_selector.select_features(X_work, y_work)
        selected_features.extend(fast_features)
        
        # 2. Lasso si demandé et faisable
        if self.use_lasso and len(X_work) <= 15000:
            lasso_features = self._select_lasso(X_work, y_work)
            selected_features.extend(lasso_features)
        
        # 3. Random Forest plus sophistiqué
        rf_features = self._select_rf_advanced(X_work, y_work)
        selected_features.extend(rf_features)
        
        # Déduplication et finalisation
        final_features = list(set(selected_features))
        
        elapsed = time.time() - start_time
        print(f"\n✅ Sélection hybride terminée en {elapsed:.1f}s")
        print(f"🎯 Variables finales: {len(final_features)}")
        
        self.selected_features_ = final_features
        return final_features
    
    def _create_sample(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
        """Crée un échantillon si nécessaire"""
        if len(X) <= self.sample_size:
            return X, y
            
        print(f"📊 Échantillonnage: {len(X):,} → {self.sample_size:,}")
        X_sample, _, y_sample, _ = train_test_split(
            X, y, train_size=self.sample_size, 
            random_state=self.random_state
        )
        return X_sample, y_sample
    
    def _select_lasso(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection Lasso optimisée"""
        print(f"\n🔍 Sélection Lasso...")
        start = time.time()
        
        try:
            # Standardisation pour Lasso
            scaler = StandardScaler()
            X_scaled = pd.DataFrame(
                scaler.fit_transform(X), 
                columns=X.columns, 
                index=X.index
            )
            
            lasso = LassoCV(cv=3, random_state=self.random_state, max_iter=2000)
            lasso.fit(X_scaled, y)
            
            selected = [X.columns[i] for i, coef in enumerate(lasso.coef_) if abs(coef) > 1e-6]
            
            elapsed = time.time() - start
            print(f"   ⚡ {len(selected)} variables en {elapsed:.2f}s")
            
            return selected
            
        except Exception as e:
            print(f"   ❌ Erreur Lasso: {e}")
            return []
    
    def _select_rf_advanced(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Random Forest plus sophistiqué"""
        print(f"\n🌲 Random Forest avancé...")
        start = time.time()
        
        try:
            rf = RandomForestRegressor(
                n_estimators=self.rf_estimators,
                random_state=self.random_state,
                n_jobs=-1,
                oob_score=True
            )
            
            rf.fit(X, y)
            
            # Sélection basée on importance > percentile 75
            importances = rf.feature_importances_
            threshold = np.percentile(importances, 75)
            selected = [X.columns[i] for i, imp in enumerate(importances) if imp >= threshold]
            
            elapsed = time.time() - start
            print(f"   ⚡ {len(selected)} variables en {elapsed:.2f}s")
            print(f"   📊 OOB Score: {rf.oob_score_:.3f}")
            
            return selected
            
        except Exception as e:
            print(f"   ❌ Erreur RF avancé: {e}")
            return []

    def get_feature_importance(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Placeholder pour compatibilité"""
        return {}


class AdaptiveFeatureSelector(IFeatureSelector):
    """Sélecteur adaptatif qui choisit automatiquement la stratégie optimale"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.strategy_used_ = ""
        self.selector_ = None
        
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection adaptative selon la taille des données"""
        data_size = len(X)
        
        print(f"\n🤖 === SÉLECTION ADAPTATIVE ===")
        print(f"📊 Analyse du volume: {data_size:,} propriétés")
        
        # Choisir la stratégie optimale
        if data_size > 100000:
            print(f"🚀 Stratégie: ULTRA-RAPIDE (>100K)")
            self.selector_ = FastFeatureSelector(
                sample_size=8000,
                rf_estimators=15,
                rf_max_depth=8
            )
            self.strategy_used_ = "ultra_fast"
            
        elif data_size > 50000:
            print(f"⚡ Stratégie: RAPIDE (50K-100K)")
            self.selector_ = FastFeatureSelector(
                sample_size=12000,
                rf_estimators=25,
                rf_max_depth=12
            )
            self.strategy_used_ = "fast"
            
        elif data_size > 20000:
            print(f"🎯 Stratégie: HYBRIDE (20K-50K)")
            self.selector_ = HybridFeatureSelector(
                sample_size=15000,
                rf_estimators=40
            )
            self.strategy_used_ = "hybrid"
            
        else:
            print(f"🔬 Stratégie: STANDARD (<20K)")
            self.selector_ = FeatureSelector(rf_n_estimators=75)
            self.strategy_used_ = "standard"
        
        # Exécuter la sélection
        selected = self.selector_.select_features(X, y)
        
        print(f"\n📈 Stratégie '{self.strategy_used_}' utilisée")
        print(f"✅ {len(selected)} variables sélectionnées")
        
        return selected
    
    def get_feature_importance(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Délègue au sélecteur utilisé"""
        if self.selector_:
            return self.selector_.get_feature_importance(X, y)
        return {}

    def select_features_by_classification(self, 
                                        X: pd.DataFrame, 
                                        y: pd.Series,
                                        classification: pd.Series) -> Dict[str, List[str]]:
        """Sélection adaptative par classification"""
        print(f"\n🏠 === SÉLECTION ADAPTATIVE PAR TYPE ===")
        
        results = {}
        unique_categories = classification.unique()
        
        for category in unique_categories:
            if category == 'non_classifie':
                continue
                
            mask = classification == category
            X_cat = X[mask]
            y_cat = y[mask]
            
            if len(X_cat) < 50:
                print(f"   ⚠️ {category}: données insuffisantes ({len(X_cat)})")
                continue
            
            print(f"\n   🏷️ {category}: {len(X_cat)} propriétés")
            
            # Adapter selon la taille de chaque catégorie
            if len(X_cat) > 5000:
                selector = FastFeatureSelector(sample_size=3000, rf_estimators=15)
            elif len(X_cat) > 1000:
                selector = FastFeatureSelector(sample_size=len(X_cat), rf_estimators=25)
            else:
                # Sélection simple pour petites catégories
                try:
                    correlations = X_cat.corrwith(y_cat).abs().sort_values(ascending=False)
                    results[category] = correlations.head(min(10, len(correlations))).index.tolist()
                    print(f"      📊 {len(results[category])} variables (corrélation)")
                    continue
                except:
                    results[category] = []
                    continue
            
            try:
                selected = selector.select_features(X_cat, y_cat)
                results[category] = selected[:15]  # Limiter à 15 max
                print(f"      📊 {len(results[category])} variables sélectionnées")
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
                results[category] = []
        
        return results


class FeatureSelector(IFeatureSelector):
    """Classe pour la sélection de variables importantes (version améliorée)"""
    
    def __init__(self, 
                 cv_folds: int = 5, 
                 random_state: int = 42,
                 max_iter: int = 10000,
                 tolerance: float = 1e-3,
                 rf_n_estimators: int = 100,
                 rf_threshold: float = 0.01,
                 enable_optimizations: bool = True):
        self.cv_folds = cv_folds
        self.random_state = random_state
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.rf_n_estimators = rf_n_estimators
        self.rf_threshold = rf_threshold
        self.enable_optimizations = enable_optimizations
        self.lasso_model = None
        self.rf_model = None
    
    def select_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélectionne les variables importantes en combinant Lasso et Random Forest"""
        logger.info("🎯 Sélection de variables...")
        
        print(f"\n🎯 === SÉLECTION DE VARIABLES ===")
        print(f"📊 Variables disponibles: {X.shape[1]}")
        
        # Optimisation automatique pour gros volumes
        if self.enable_optimizations and len(X) > 50000:
            print(f"⚡ Optimisation activée pour {len(X):,} propriétés")
            adaptive_selector = AdaptiveFeatureSelector(self.random_state)
            return adaptive_selector.select_features(X, y)
        
        print(f"📝 Variables: {list(X.columns)}")
        
        # Sélection par Lasso
        print(f"\n🔍 Sélection par Lasso (régularisation L1):")
        lasso_features = self._select_lasso_features(X, y)
        
        # Sélection par Random Forest
        print(f"\n🌲 Sélection par Random Forest:")
        rf_features = self._select_rf_features(X, y)
        
        # Combiner les résultats
        all_selected = list(set(lasso_features + rf_features))
        
        print(f"\n🔗 === COMBINAISON DES MÉTHODES ===")
        print(f"📊 Variables sélectionnées par Lasso: {len(lasso_features)}")
        print(f"📊 Variables sélectionnées par Random Forest: {len(rf_features)}")
        print(f"📊 Variables uniques sélectionnées: {len(all_selected)}")
        
        if all_selected:
            print(f"\n✅ Variables finales sélectionnées:")
            for i, feature in enumerate(all_selected, 1):
                print(f"   {i:2d}. {feature}")
        else:
            print(f"⚠️ Aucune variable sélectionnée")
        
        return all_selected
    
    def _select_lasso_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection de variables par Lasso"""
        try:
            # Configuration du modèle Lasso
            lasso = LassoCV(
                cv=self.cv_folds,
                random_state=self.random_state,
                max_iter=self.max_iter,
                tol=self.tolerance
            )
            
            # Entraînement
            lasso.fit(X, y)
            self.lasso_model = lasso
            
            # Identifier les variables avec coefficient non-nul
            selected_features = []
            for i, coef in enumerate(lasso.coef_):
                if abs(coef) > 0:
                    selected_features.append(X.columns[i])
            
            print(f"   📈 Alpha optimal: {lasso.alpha_:.6f}")
            print(f"   📊 Variables sélectionnées: {len(selected_features)}")
            print(f"   📝 Variables: {selected_features}")
            
            return selected_features
            
        except Exception as e:
            print(f"   ❌ Erreur Lasso: {e}")
            return []
    
    def _select_rf_features(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Sélection de variables par Random Forest"""
        try:
            # Configuration du modèle Random Forest
            rf = RandomForestRegressor(
                n_estimators=self.rf_n_estimators,
                random_state=self.random_state,
                n_jobs=-1
            )
            
            # Entraînement
            rf.fit(X, y)
            self.rf_model = rf
            
            # Calculer l'importance des variables
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': rf.feature_importances_
            }).sort_values('importance', ascending=False)
            
            # Sélectionner les variables importantes
            threshold = self.rf_threshold
            important_features = feature_importance[feature_importance['importance'] >= threshold]['feature'].tolist()
            
            print(f"   📊 Seuil d'importance: {threshold}")
            print(f"   📈 Variables importantes: {len(important_features)}")
            print(f"   📝 Variables: {important_features}")
            
            # Afficher les 5 variables les plus importantes
            print(f"   🏆 Top 5 variables importantes:")
            for i, (_, row) in enumerate(feature_importance.head().iterrows(), 1):
                print(f"      {i}. {row['feature']}: {row['importance']:.4f}")
            
            return important_features
            
        except Exception as e:
            print(f"   ❌ Erreur Random Forest: {e}")
            return []
    
    def get_feature_importance(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Retourne l'importance des variables"""
        if self.rf_model is None:
            # Entraîner un modèle si nécessaire
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            rf.fit(X, y)
        else:
            rf = self.rf_model
        
        return dict(zip(X.columns, rf.feature_importances_))
    
    def select_features_by_classification(self, 
                                        X: pd.DataFrame, 
                                        y: pd.Series,
                                        classification: pd.Series) -> Dict[str, List[str]]:
        """Sélectionne les variables importantes par type de propriété"""
        logger.info("🏠 Sélection de variables par classification...")
        
        # Utiliser le sélecteur adaptatif pour gros volumes
        if self.enable_optimizations and len(X) > 20000:
            adaptive_selector = AdaptiveFeatureSelector(self.random_state)
            return adaptive_selector.select_features_by_classification(X, y, classification)
        
        print(f"\n🏠 === SÉLECTION PAR TYPE DE PROPRIÉTÉ ===")
        
        classification_features = {}
        unique_categories = classification.unique()
        
        for category in unique_categories:
            if category == 'non_classifie':
                continue
                
            # Filtrer les données pour cette catégorie
            mask = classification == category
            X_cat = X[mask]
            y_cat = y[mask]
            
            if len(X_cat) < 10:  # Trop peu de données
                print(f"   ⚠️ {category}: données insuffisantes ({len(X_cat)} échantillons)")
                continue
            
            print(f"\n   🏷️ {category}: {len(X_cat)} propriétés")
            
            # Sélection de variables pour cette catégorie
            try:
                # Utiliser Random Forest pour cette catégorie
                rf_cat = RandomForestRegressor(
                    n_estimators=50,
                    random_state=42,
                    n_jobs=-1
                )
                rf_cat.fit(X_cat, y_cat)
                
                # Sélectionner les variables importantes
                feature_importance = pd.DataFrame({
                    'feature': X_cat.columns,
                    'importance': rf_cat.feature_importances_
                }).sort_values('importance', ascending=False)
                
                # Prendre les 10 variables les plus importantes
                top_features = feature_importance.head(10)['feature'].tolist()
                classification_features[category] = top_features
                
                print(f"      📊 Variables sélectionnées: {len(top_features)}")
                print(f"      📝 Top 3: {top_features[:3]}")
                
            except Exception as e:
                print(f"      ❌ Erreur pour {category}: {e}")
                classification_features[category] = []
        
        return classification_features 