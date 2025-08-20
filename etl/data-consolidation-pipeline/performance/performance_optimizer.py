#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 OPTIMISEUR DE PERFORMANCE - ACCÉLÉRATION ET OPTIMISATION
===========================================================

Module d'optimisation des performances avec Dask, Modin, Numba, Cython
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Union, Callable
import warnings
import time
import psutil
import gc
import os
from pathlib import Path
import json
from datetime import datetime

# Imports conditionnels pour les bibliothèques d'optimisation
try:
    import dask.dataframe as dd
    import dask.array as da
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
    warnings.warn("Dask non disponible - parallélisation limitée")

try:
    import modin.pandas as mpd
    MODIN_AVAILABLE = True
except ImportError:
    MODIN_AVAILABLE = False
    warnings.warn("Modin non disponible - parallélisation pandas limitée")

try:
    import numba
    from numba import jit, prange
    NUMBA_AVAILABLE = True
    JIT_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    JIT_AVAILABLE = False
    warnings.warn("Numba non disponible - compilation JIT limitée")

try:
    import pyarrow as pa
    PYARROW_AVAILABLE = True
except ImportError:
    PYARROW_AVAILABLE = False
    warnings.warn("PyArrow non disponible - optimisations mémoire limitées")

try:
    from memory_profiler import profile
    MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    MEMORY_PROFILER_AVAILABLE = False
    warnings.warn("Memory Profiler non disponible - profilage mémoire limité")

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """
    Optimiseur de performance pour le pipeline ETL
    Intègre Dask + Modin + Numba + PyArrow + Memory Profiler
    """
    
    def __init__(self, performance_config: Dict = None):
        """
        Initialise l'optimiseur de performance
        
        Args:
            performance_config: Configuration de performance
        """
        self.performance_config = performance_config or self._default_performance_config()
        self.performance_metrics = {}
        self.optimization_history = []
        self.memory_usage_history = []
        
        logger.info("🚀 PerformanceOptimizer initialisé")
        logger.info(f"⚡ Dask: {'✅' if DASK_AVAILABLE else '❌'}")
        logger.info(f"🔄 Modin: {'✅' if MODIN_AVAILABLE else '❌'}")
        logger.info(f"⚙️ Numba: {'✅' if NUMBA_AVAILABLE else '❌'}")
        logger.info(f"🏹 PyArrow: {'✅' if PYARROW_AVAILABLE else '❌'}")
        logger.info(f"💾 Memory Profiler: {'✅' if MEMORY_PROFILER_AVAILABLE else '❌'}")
    
    def _default_performance_config(self) -> Dict:
        """Configuration de performance par défaut"""
        return {
            "parallel_processing": {
                "enabled": True,
                "n_workers": min(8, os.cpu_count() or 1),  # Augmenté pour performance maximale
                "chunk_size": 10000,
                "memory_limit": "4GB"  # Augmenté pour gros datasets
            },
            "dask_optimization": {
                "enabled": True,  # Activé par défaut comme spécifié
                "partition_size": "100MB",
                "npartitions": None,  # Auto-détection
                "persist_intermediate": True
            },
            "modin_optimization": {
                "enabled": True,  # Activé par défaut comme spécifié
                "engine": "ray",  # Utilise Ray pour parallélisation
                "partition_size": "100MB"
            },
            "memory_optimization": {
                "enabled": True,
                "dtype_optimization": True,
                "categorical_optimization": True,
                "chunk_processing": True,
                "garbage_collection": True
            },
            "numba_optimization": {
                "enabled": True,
                "parallel": True,
                "fastmath": True
            },
            "pyarrow_optimization": {
                "enabled": True,
                "use_pyarrow": True,
                "compression": "snappy"
            }
        }
    
    def optimize_dataframe(self, df: pd.DataFrame, optimization_level: str = "medium") -> pd.DataFrame:
        """
        Optimise un DataFrame selon le niveau spécifié
        
        Args:
            df: DataFrame à optimiser
            optimization_level: Niveau d'optimisation (light, medium, aggressive)
            
        Returns:
            DataFrame optimisé
        """
        logger.info(f"🚀 === OPTIMISATION DATAFRAME: {optimization_level.upper()} ===")
        
        optimization_start = time.time()
        initial_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        
        # === OPTIMISATION MÉMOIRE ===
        if self.performance_config["memory_optimization"]["enabled"]:
            logger.info("💾 Optimisation mémoire...")
            df = self._optimize_memory_usage(df, optimization_level)
        
        # === OPTIMISATION DES TYPES ===
        if self.performance_config["memory_optimization"]["dtype_optimization"]:
            logger.info("🔧 Optimisation des types de données...")
            df = self._optimize_data_types(df, optimization_level)
        
        # === OPTIMISATION CATÉGORIELLE ===
        if self.performance_config["memory_optimization"]["categorical_optimization"]:
            logger.info("📊 Optimisation catégorielle...")
            df = self._optimize_categorical_columns(df, optimization_level)
        
        # === OPTIMISATION PYARROW ===
        if self.performance_config["pyarrow_optimization"]["enabled"] and PYARROW_AVAILABLE:
            logger.info("🏹 Optimisation PyArrow...")
            df = self._apply_pyarrow_optimizations(df)
        
        # === CALCUL DES MÉTRIQUES ===
        optimization_end = time.time()
        final_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        
        memory_reduction = ((initial_memory - final_memory) / initial_memory) * 100
        optimization_time = optimization_end - optimization_start
        
        # Enregistrement des métriques
        optimization_record = {
            "timestamp": datetime.now().isoformat(),
            "optimization_level": optimization_level,
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_reduction_percent": memory_reduction,
            "optimization_time_seconds": optimization_time,
            "shape": df.shape
        }
        
        self.optimization_history.append(optimization_record)
        
        logger.info(f"✅ Optimisation terminée en {optimization_time:.2f}s")
        logger.info(f"💾 Mémoire: {initial_memory:.2f} MB → {final_memory:.2f} MB")
        logger.info(f"📉 Réduction: {memory_reduction:.1f}%")
        
        return df
    
    def _optimize_memory_usage(self, df: pd.DataFrame, level: str) -> pd.DataFrame:
        """Optimise l'utilisation mémoire du DataFrame"""
        optimized_df = df.copy()
        
        # === OPTIMISATION DES TYPES NUMÉRIQUES ===
        if level in ["medium", "aggressive"]:
            for col in optimized_df.select_dtypes(include=[np.number]).columns:
                col_type = optimized_df[col].dtype
                
                if col_type == 'int64':
                    # Conversion en int32 ou int16 si possible
                    c_min = optimized_df[col].min()
                    c_max = optimized_df[col].max()
                    
                    if c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        optimized_df[col] = optimized_df[col].astype(np.int32)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        optimized_df[col] = optimized_df[col].astype(np.int16)
                
                elif col_type == 'float64':
                    # Conversion en float32 si possible
                    if optimized_df[col].notna().all():
                        c_min = optimized_df[col].min()
                        c_max = optimized_df[col].max()
                        
                        if c_min >= -3.4e38 and c_max <= 3.4e38:
                            optimized_df[col] = optimized_df[col].astype(np.float32)
        
        # === OPTIMISATION DES TYPES OBJET ===
        if level in ["medium", "aggressive"]:
            for col in optimized_df.select_dtypes(include=['object']).columns:
                # Conversion en string[pyarrow] si disponible
                if PYARROW_AVAILABLE and self.performance_config["pyarrow_optimization"]["use_pyarrow"]:
                    optimized_df[col] = optimized_df[col].astype(self.performance_config["pyarrow_optimization"]["string_dtype"])
        
        return optimized_df
    
    def _optimize_data_types(self, df: pd.DataFrame, level: str) -> pd.DataFrame:
        """Optimise les types de données pour la performance"""
        optimized_df = df.copy()
        
        # === DÉTECTION AUTOMATIQUE DES TYPES ===
        for col in optimized_df.columns:
            if optimized_df[col].dtype == 'object':
                # Tentative de conversion en numérique
                try:
                    pd.to_numeric(optimized_df[col], errors='raise')
                    optimized_df[col] = pd.to_numeric(optimized_df[col], errors='coerce')
                    logger.debug(f"🔢 Colonne '{col}' convertie en numérique")
                except:
                    # Tentative de conversion en datetime
                    try:
                        pd.to_datetime(optimized_df[col], errors='raise')
                        optimized_df[col] = pd.to_datetime(optimized_df[col], errors='coerce')
                        logger.debug(f"📅 Colonne '{col}' convertie en datetime")
                    except:
                        pass
        
        return optimized_df
    
    def _optimize_categorical_columns(self, df: pd.DataFrame, level: str) -> pd.DataFrame:
        """Optimise les colonnes catégorielles"""
        optimized_df = df.copy()
        
        # Seuil pour la conversion en catégorie
        categorical_threshold = 0.5 if level == "light" else 0.7 if level == "medium" else 0.9
        
        for col in optimized_df.select_dtypes(include=['object']).columns:
            try:
                # Vérifier si la colonne peut être convertie en catégorie
                # en testant si les valeurs sont hashables
                sample_values = optimized_df[col].dropna().head(100)
                hashable_values = []
                
                for val in sample_values:
                    try:
                        hash(val)  # Test si la valeur est hashable
                        hashable_values.append(val)
                    except TypeError:
                        # Valeur non-hashable, la traiter comme une chaîne
                        hashable_values.append(str(val))
                
                if len(hashable_values) > 0:
                    # Calculer le ratio d'unicité sur les valeurs hashables
                    unique_count = len(set(hashable_values))
                    unique_ratio = unique_count / len(optimized_df)
                    
                    if unique_ratio < categorical_threshold:
                        # Convertir en catégorie en gérant les valeurs non-hashables
                        safe_series = optimized_df[col].apply(
                            lambda x: str(x) if x is not None else None
                        )
                        optimized_df[col] = safe_series.astype('category')
                        logger.debug(f"📊 Colonne '{col}' convertie en catégorie (ratio: {unique_ratio:.2f})")
                else:
                    logger.debug(f"⚠️ Colonne '{col}' ignorée - aucune valeur hashable")
                    
            except Exception as e:
                logger.warning(f"⚠️ Impossible d'optimiser la colonne '{col}' en catégorie: {e}")
                continue
        
        return optimized_df
    
    def _apply_pyarrow_optimizations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique les optimisations PyArrow"""
        if not PYARROW_AVAILABLE:
            return df
        
        try:
            # Conversion en format PyArrow
            optimized_df = df.copy()
            
            # Optimisation des colonnes string
            for col in optimized_df.select_dtypes(include=['object']).columns:
                if self.performance_config["pyarrow_optimization"]["use_pyarrow"]:
                    optimized_df[col] = optimized_df[col].astype(self.performance_config["pyarrow_optimization"]["string_dtype"])
            
            return optimized_df
            
        except Exception as e:
            logger.warning(f"⚠️ Optimisation PyArrow échouée: {e}")
            return df
    
    def parallelize_operation(self, df: pd.DataFrame, operation: Callable, 
                             operation_name: str = "operation", **kwargs) -> pd.DataFrame:
        """
        Parallélise une opération sur le DataFrame
        
        Args:
            df: DataFrame à traiter
            operation: Fonction à appliquer
            operation_name: Nom de l'opération pour le logging
            **kwargs: Arguments supplémentaires pour l'opération
            
        Returns:
            DataFrame traité
        """
        if not self.performance_config["parallel_processing"]["enabled"]:
            logger.info(f"⚡ Parallélisation désactivée - exécution séquentielle")
            return operation(df, **kwargs)
        
        if not DASK_AVAILABLE:
            logger.warning("⚠️ Dask non disponible - exécution séquentielle")
            return operation(df, **kwargs)
        
        logger.info(f"⚡ === PARALLÉLISATION: {operation_name} ===")
        
        # === CONVERSION EN DASK DATAFRAME ===
        logger.info("🔄 Conversion en Dask DataFrame...")
        ddf = dd.from_pandas(df, npartitions=self._calculate_optimal_partitions(df))
        
        # === APPLICATION DE L'OPÉRATION ===
        logger.info(f"🚀 Application de {operation_name} en parallèle...")
        start_time = time.time()
        
        try:
            # Application de l'opération
            result_ddf = operation(ddf, **kwargs)
            
            # Conversion de retour en pandas
            result_df = result_ddf.compute()
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            logger.info(f"✅ Opération parallélisée terminée en {processing_time:.2f}s")
            
            return result_df
            
        except Exception as e:
            logger.error(f"❌ Erreur parallélisation: {e}")
            logger.info("🔄 Retour à l'exécution séquentielle...")
            return operation(df, **kwargs)
    
    def _calculate_optimal_partitions(self, df: pd.DataFrame) -> int:
        """Calcule le nombre optimal de partitions pour Dask"""
        config = self.performance_config["parallel_processing"]
        n_workers = config["n_workers"]
        
        # Calcul basé sur la taille du DataFrame
        total_rows = len(df)
        chunk_size = config["chunk_size"]
        
        optimal_partitions = max(1, min(n_workers * 2, total_rows // chunk_size))
        
        return optimal_partitions
    
    def optimize_numeric_operations(self, df: pd.DataFrame, operations: List[str]) -> pd.DataFrame:
        """
        Optimise les opérations numériques avec Numba
        
        Args:
            df: DataFrame à optimiser
            operations: Liste des opérations à optimiser
            
        Returns:
            DataFrame avec opérations optimisées
        """
        if not NUMBA_AVAILABLE or not self.performance_config["numba_optimization"]["enabled"]:
            logger.info("⚠️ Numba non disponible - opérations standard")
            return df
        
        logger.info("⚙️ === OPTIMISATION NUMÉRIQUE AVEC NUMBA ===")
        
        optimized_df = df.copy()
        
        for operation in operations:
            if operation == "rolling_mean":
                optimized_df = self._apply_numba_rolling_mean(optimized_df)
            elif operation == "rolling_std":
                optimized_df = self._apply_numba_rolling_std(optimized_df)
            elif operation == "z_score":
                optimized_df = self._apply_numba_z_score(optimized_df)
            elif operation == "outlier_detection":
                optimized_df = self._apply_numba_outlier_detection(optimized_df)
        
        return optimized_df
    
    @staticmethod
    def _numba_rolling_mean(arr, window):
        if JIT_AVAILABLE:
            return jit(nopython=True, parallel=True, fastmath=True, cache=True)(_numba_rolling_mean_impl)(arr, window)
        else:
            return _numba_rolling_mean_impl(arr, window)
    
    @staticmethod
    def _numba_rolling_mean_impl(arr, window):
        """Calcul de moyenne mobile optimisé avec Numba"""
        n = len(arr)
        result = np.empty(n)
        result[:window-1] = np.nan
        
        for i in range(window-1, n):
            result[i] = np.mean(arr[i-window+1:i+1])
        
        return result
    
    @staticmethod
    def _numba_rolling_std(arr, window):
        if JIT_AVAILABLE:
            return jit(nopython=True, parallel=True, fastmath=True, cache=True)(_numba_rolling_std_impl)(arr, window)
        else:
            return _numba_rolling_std_impl(arr, window)
    
    @staticmethod
    def _numba_rolling_std_impl(arr, window):
        """Calcul d'écart-type mobile optimisé avec Numba"""
        n = len(arr)
        result = np.empty(n)
        result[:window-1] = np.nan
        
        for i in range(window-1, n):
            result[i] = np.std(arr[i-window+1:i+1])
        
        return result
    
    @staticmethod
    def _numba_z_score(arr):
        if JIT_AVAILABLE:
            return jit(nopython=True, parallel=True, fastmath=True, cache=True)(_numba_z_score_impl)(arr)
        else:
            return _numba_z_score_impl(arr)
    
    @staticmethod
    def _numba_z_score_impl(arr):
        """Calcul de Z-score optimisé avec Numba"""
        mean = np.mean(arr)
        std = np.std(arr)
        
        if std == 0:
            return np.zeros_like(arr)
        
        return (arr - mean) / std
    
    @staticmethod
    def _numba_outlier_detection(arr, threshold=3.0):
        if JIT_AVAILABLE:
            return jit(nopython=True, parallel=True, fastmath=True, cache=True)(_numba_outlier_detection_impl)(arr, threshold)
        else:
            return _numba_outlier_detection_impl(arr, threshold)
    
    @staticmethod
    def _numba_outlier_detection_impl(arr, threshold=3.0):
        """Détection d'outliers optimisée avec Numba"""
        z_scores = np.abs((arr - np.mean(arr)) / np.std(arr))
        return z_scores > threshold
    
    def _apply_numba_rolling_mean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique la moyenne mobile optimisée par Numba"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].notna().sum() > 10:  # Au moins 10 valeurs non-nulles
                window = min(10, len(df) // 10)  # Fenêtre adaptative
                df[f"{col}_rolling_mean"] = self._numba_rolling_mean(
                    df[col].fillna(0).values, window
                )
        
        return df
    
    def _apply_numba_rolling_std(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique l'écart-type mobile optimisé par Numba"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].notna().sum() > 10:
                window = min(10, len(df) // 10)
                df[f"{col}_rolling_std"] = self._numba_rolling_std(
                    df[col].fillna(0).values, window
                )
        
        return df
    
    def _apply_numba_z_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique le Z-score optimisé par Numba"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].notna().sum() > 10:
                df[f"{col}_z_score"] = self._numba_z_score(df[col].fillna(0).values)
        
        return df
    
    def _apply_numba_outlier_detection(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applique la détection d'outliers optimisée par Numba"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].notna().sum() > 10:
                df[f"{col}_is_outlier"] = self._numba_outlier_detection(
                    df[col].fillna(0).values, threshold=3.0
                )
        
        return df
    
    def monitor_memory_usage(self, df: pd.DataFrame, operation_name: str = "operation") -> Dict[str, float]:
        """
        Surveille l'utilisation mémoire
        
        Args:
            df: DataFrame à surveiller
            operation_name: Nom de l'opération
            
        Returns:
            Dict avec les métriques mémoire
        """
        if not self.performance_config["monitoring"]["memory_tracking"]:
            return {}
        
        # === UTILISATION MÉMOIRE DU DATAFRAME ===
        df_memory = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        
        # === UTILISATION MÉMOIRE SYSTÈME ===
        process = psutil.Process()
        process_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # === UTILISATION MÉMOIRE SYSTÈME ===
        system_memory = psutil.virtual_memory()
        system_used = system_memory.used / 1024 / 1024 / 1024  # GB
        system_total = system_memory.total / 1024 / 1024 / 1024  # GB
        system_percent = system_memory.percent
        
        memory_metrics = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation_name,
            "dataframe_memory_mb": df_memory,
            "process_memory_mb": process_memory,
            "system_memory_used_gb": system_used,
            "system_memory_total_gb": system_total,
            "system_memory_percent": system_percent
        }
        
        self.memory_usage_history.append(memory_metrics)
        
        logger.info(f"💾 Mémoire - DataFrame: {df_memory:.2f} MB, Process: {process_memory:.2f} MB")
        logger.info(f"💾 Système: {system_percent:.1f}% ({system_used:.2f}/{system_total:.2f} GB)")
        
        return memory_metrics
    
    def optimize_garbage_collection(self, force: bool = False) -> Dict[str, Any]:
        """
        Optimise la gestion de la mémoire avec garbage collection
        
        Args:
            force: Force la collecte des déchets
            
        Returns:
            Dict avec les métriques de GC
        """
        if not self.performance_config["monitoring"]["gc_optimization"]:
            return {}
        
        logger.info("🗑️ === OPTIMISATION GARBAGE COLLECTION ===")
        
        # === MÉTRIQUES AVANT GC ===
        before_memory = psutil.virtual_memory().used / 1024 / 1024 / 1024  # GB
        before_objects = len(gc.get_objects())
        
        # === COLLECTE DES DÉCHETS ===
        start_time = time.time()
        
        if force:
            collected = gc.collect()
        else:
            collected = gc.collect()
        
        end_time = time.time()
        gc_time = end_time - start_time
        
        # === MÉTRIQUES APRÈS GC ===
        after_memory = psutil.virtual_memory().used / 1024 / 1024 / 1024  # GB
        after_objects = len(gc.get_objects())
        
        # === CALCUL DES AMÉLIORATIONS ===
        memory_freed = before_memory - after_memory
        objects_freed = before_objects - after_objects
        
        gc_metrics = {
            "timestamp": datetime.now().isoformat(),
            "before_memory_gb": before_memory,
            "after_memory_gb": after_memory,
            "memory_freed_gb": memory_freed,
            "before_objects": before_objects,
            "after_objects": after_objects,
            "objects_freed": objects_freed,
            "gc_time_seconds": gc_time,
            "collected": collected
        }
        
        logger.info(f"✅ GC terminé en {gc_time:.3f}s")
        logger.info(f"💾 Mémoire libérée: {memory_freed:.3f} GB")
        logger.info(f"🗑️ Objets libérés: {objects_freed}")
        
        return gc_metrics
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des performances"""
        if not self.optimization_history:
            return {"message": "Aucune optimisation effectuée"}
        
        # === MÉTRIQUES D'OPTIMISATION ===
        total_optimizations = len(self.optimization_history)
        total_memory_saved = sum(
            record["memory_reduction_percent"] * record["initial_memory_mb"] / 100
            for record in self.optimization_history
        )
        avg_optimization_time = np.mean([
            record["optimization_time_seconds"] for record in self.optimization_history
        ])
        
        # === MÉTRIQUES MÉMOIRE ===
        memory_records = len(self.memory_usage_history)
        avg_dataframe_memory = np.mean([
            record["dataframe_memory_mb"] for record in self.memory_usage_history
        ]) if memory_records > 0 else 0
        
        # === MÉTRIQUES SYSTÈME ===
        avg_system_memory = np.mean([
            record["system_memory_percent"] for record in self.memory_usage_history
        ]) if memory_records > 0 else 0
        
        return {
            "optimization_summary": {
                "total_optimizations": total_optimizations,
                "total_memory_saved_mb": total_memory_saved,
                "average_optimization_time_seconds": avg_optimization_time
            },
            "memory_summary": {
                "memory_tracking_records": memory_records,
                "average_dataframe_memory_mb": avg_dataframe_memory,
                "average_system_memory_percent": avg_system_memory
            },
            "capabilities": {
                "dask_available": DASK_AVAILABLE,
                "modin_available": MODIN_AVAILABLE,
                "numba_available": NUMBA_AVAILABLE,
                "pyarrow_available": PYARROW_AVAILABLE,
                "memory_profiler_available": MEMORY_PROFILER_AVAILABLE
            },
            "configuration": self.performance_config
        }
    
    def generate_performance_report(self, output_path: str = None) -> str:
        """
        Génère un rapport de performance complet
        
        Args:
            output_path: Chemin de sauvegarde (optionnel)
            
        Returns:
            Contenu du rapport
        """
        logger.info("📊 === GÉNÉRATION RAPPORT PERFORMANCE ===")
        
        # Récupération du résumé
        summary = self.get_performance_summary()
        
        # Génération du rapport
        report_content = []
        report_content.append("# " + "="*80)
        report_content.append("# RAPPORT DE PERFORMANCE ET OPTIMISATION")
        report_content.append("# " + "="*80)
        report_content.append(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append("# " + "="*80 + "\n")
        
        # Résumé exécutif
        report_content.append("## RÉSUMÉ EXÉCUTIF")
        if "optimization_summary" in summary:
            opt_summary = summary["optimization_summary"]
            report_content.append(f"**Optimisations effectuées:** {opt_summary['total_optimizations']}")
            report_content.append(f"**Mémoire totale économisée:** {opt_summary['total_memory_saved_mb']:.2f} MB")
            report_content.append(f"**Temps moyen d'optimisation:** {opt_summary['average_optimization_time_seconds']:.3f}s")
        else:
            report_content.append("**Aucune optimisation effectuée**")
        report_content.append("")
        
        # Capacités disponibles
        report_content.append("## CAPACITÉS D'OPTIMISATION")
        capabilities = summary.get("capabilities", {})
        for capability, available in capabilities.items():
            status = "✅ Disponible" if available else "❌ Non disponible"
            report_content.append(f"**{capability}:** {status}")
        report_content.append("")
        
        # Historique des optimisations
        if self.optimization_history:
            report_content.append("## HISTORIQUE DES OPTIMISATIONS")
            for i, record in enumerate(self.optimization_history[-5:], 1):  # 5 dernières
                report_content.append(f"### Optimisation {i}")
                report_content.append(f"**Niveau:** {record['optimization_level']}")
                report_content.append(f"**Mémoire initiale:** {record['initial_memory_mb']:.2f} MB")
                report_content.append(f"**Mémoire finale:** {record['final_memory_mb']:.2f} MB")
                report_content.append(f"**Réduction:** {record['memory_reduction_percent']:.1f}%")
                report_content.append(f"**Temps:** {record['optimization_time_seconds']:.3f}s")
                report_content.append("")
        
        # Configuration
        report_content.append("## CONFIGURATION")
        config = summary.get("configuration", {})
        for section, settings in config.items():
            report_content.append(f"### {section.replace('_', ' ').title()}")
            for key, value in settings.items():
                report_content.append(f"**{key}:** {value}")
            report_content.append("")
        
        report_content.append("# " + "="*80)
        report_content.append("# FIN DU RAPPORT")
        report_content.append("# " + "="*80)
        
        report_text = "\n".join(report_content)
        
        # Sauvegarde si un chemin est fourni
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                logger.info(f"📄 Rapport de performance sauvegardé: {output_path}")
            except Exception as e:
                logger.error(f"❌ Erreur sauvegarde rapport: {e}")
        
        return report_text
    
    def benchmark_operation(self, df: pd.DataFrame, operation: Callable, 
                           operation_name: str = "operation", iterations: int = 3, **kwargs) -> Dict[str, Any]:
        """
        Benchmark d'une opération pour mesurer les performances
        
        Args:
            df: DataFrame à traiter
            operation: Fonction à benchmarker
            operation_name: Nom de l'opération
            iterations: Nombre d'itérations pour le benchmark
            **kwargs: Arguments supplémentaires pour l'opération
            
        Returns:
            Dict avec les métriques de benchmark
        """
        logger.info(f"⏱️ === BENCHMARK: {operation_name} ===")
        
        # === MÉTRIQUES AVANT ===
        before_memory = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        before_shape = df.shape
        
        # === EXÉCUTION DU BENCHMARK ===
        execution_times = []
        memory_usage = []
        
        for i in range(iterations):
            logger.info(f"🔄 Itération {i+1}/{iterations}...")
            
            # Mesure du temps
            start_time = time.time()
            result_df = operation(df, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            
            # Mesure de la mémoire
            result_memory = result_df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
            memory_usage.append(result_memory)
            
            logger.info(f"⏱️ Itération {i+1}: {execution_time:.3f}s, {result_memory:.2f} MB")
        
        # === CALCUL DES MÉTRIQUES ===
        avg_execution_time = np.mean(execution_times)
        std_execution_time = np.std(execution_times)
        avg_memory_usage = np.mean(memory_usage)
        
        # === MÉTRIQUES FINALES ===
        after_shape = result_df.shape
        memory_change = ((avg_memory_usage - before_memory) / before_memory) * 100
        
        benchmark_results = {
            "operation_name": operation_name,
            "iterations": iterations,
            "execution_times": execution_times,
            "average_execution_time_seconds": avg_execution_time,
            "std_execution_time_seconds": std_execution_time,
            "memory_usage_mb": memory_usage,
            "average_memory_usage_mb": avg_memory_usage,
            "memory_change_percent": memory_change,
            "before_shape": before_shape,
            "after_shape": after_shape,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"📊 === RÉSULTATS BENCHMARK ===")
        logger.info(f"⏱️ Temps moyen: {avg_execution_time:.3f}s ± {std_execution_time:.3f}s")
        logger.info(f"💾 Mémoire moyenne: {avg_memory_usage:.2f} MB")
        logger.info(f"📉 Changement mémoire: {memory_change:.1f}%")
        logger.info(f"📐 Forme: {before_shape} → {after_shape}")
        
        return benchmark_results

    def enable_all_optimizations(self) -> Dict[str, bool]:
        """
        Active toutes les optimisations disponibles pour performance maximale
        Respecte les spécifications du real_estate_prompt.md
        """
        logger.info("🚀 === ACTIVATION DE TOUTES LES OPTIMISATIONS ===")
        
        optimizations_status = {}
        
        # === DASK OPTIMIZATION ===
        if DASK_AVAILABLE and self.performance_config["dask_optimization"]["enabled"]:
            try:
                import dask.dataframe as dd
                self.use_dask = True
                self.dask_config = self.performance_config["dask_optimization"]
                optimizations_status["dask"] = True
                logger.info("✅ Dask activé pour traitement parallèle")
            except Exception as e:
                logger.warning(f"⚠️ Dask non activé: {e}")
                optimizations_status["dask"] = False
        else:
            optimizations_status["dask"] = False
        
        # === MODIN OPTIMIZATION ===
        if MODIN_AVAILABLE and self.performance_config["modin_optimization"]["enabled"]:
            try:
                import modin.pandas as mpd
                self.use_modin = True
                self.modin_config = self.performance_config["modin_optimization"]
                optimizations_status["modin"] = True
                logger.info("✅ Modin activé pour pandas parallèle")
            except Exception as e:
                logger.warning(f"⚠️ Modin non activé: {e}")
                optimizations_status["modin"] = False
        else:
            optimizations_status["modin"] = False
        
        # === NUMBA OPTIMIZATION ===
        if NUMBA_AVAILABLE and self.performance_config["numba_optimization"]["enabled"]:
            try:
                self.use_numba = True
                self.numba_config = self.performance_config["numba_optimization"]
                optimizations_status["numba"] = True
                logger.info("✅ Numba activé pour compilation JIT")
            except Exception as e:
                logger.warning(f"⚠️ Numba non activé: {e}")
                optimizations_status["numba"] = False
        else:
            optimizations_status["numba"] = False
        
        # === PYARROW OPTIMIZATION ===
        if PYARROW_AVAILABLE and self.performance_config["pyarrow_optimization"]["enabled"]:
            try:
                self.use_pyarrow = True
                self.pyarrow_config = self.performance_config["pyarrow_optimization"]
                optimizations_status["pyarrow"] = True
                logger.info("✅ PyArrow activé pour optimisations mémoire")
            except Exception as e:
                logger.warning(f"⚠️ PyArrow non activé: {e}")
                optimizations_status["pyarrow"] = False
        else:
            optimizations_status["pyarrow"] = False
        
        # === MEMORY OPTIMIZATION ===
        if self.performance_config["memory_optimization"]["enabled"]:
            self.use_memory_optimization = True
            optimizations_status["memory"] = True
            logger.info("✅ Optimisations mémoire activées")
        else:
            optimizations_status["memory"] = False
        
        # === RÉSUMÉ DES OPTIMISATIONS ===
        active_count = sum(optimizations_status.values())
        total_count = len(optimizations_status)
        
        logger.info(f"🎯 Optimisations activées: {active_count}/{total_count}")
        logger.info(f"📊 Status: {optimizations_status}")
        
        return optimizations_status
