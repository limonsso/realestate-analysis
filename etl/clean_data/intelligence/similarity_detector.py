#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 DÉTECTEUR D'INTELLIGENCE - SIMILARITÉ ET PATTERNS
=====================================================

Module d'intelligence pour la détection automatique des similarités
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Tuple, Optional, Set, Any
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class SimilarityDetector:
    """
    Détecteur intelligent de similarités entre colonnes
    Utilise FuzzyWuzzy + Regex + Difflib comme spécifié
    """
    
    def __init__(self, similarity_threshold: float = 80.0):
        """
        Initialise le détecteur de similarités
        
        Args:
            similarity_threshold: Seuil de similarité (0-100)
        """
        self.similarity_threshold = similarity_threshold
        self.patterns = self._initialize_patterns()
        logger.info(f"🧠 SimilarityDetector initialisé - Seuil: {similarity_threshold}%")
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        """Initialise les patterns regex pour la détection"""
        return {
            # === PATTERNS PRIX ===
            "price_patterns": [
                r"price", r"prix", r"valeur", r"montant", r"asking", r"list", r"sale",
                r"cost", r"value", r"amount", r"asking_price", r"list_price", r"sale_price"
            ],
            
            # === PATTERNS SURFACE ===
            "surface_patterns": [
                r"surface", r"superficie", r"area", r"living_area", r"floor_area",
                r"sqft", r"m2", r"square_feet", r"square_meters", r"footage"
            ],
            
            # === PATTERNS CHAMBRES ===
            "bedroom_patterns": [
                r"bedroom", r"chambre", r"bed", r"br", r"room", r"chambres"
            ],
            
            # === PATTERNS SALLES DE BAIN ===
            "bathroom_patterns": [
                r"bathroom", r"salle_bain", r"bath", r"ba", r"toilet", r"wc"
            ],
            
            # === PATTERNS COORDONNÉES ===
            "coordinate_patterns": [
                r"lat", r"latitude", r"lng", r"longitude", r"long", r"lon",
                r"coord", r"geo", r"x", r"y", r"position"
            ],
            
            # === PATTERNS ADRESSES ===
            "address_patterns": [
                r"address", r"adresse", r"street", r"rue", r"location", r"addr"
            ],
            
            # === PATTERNS DATES ===
            "date_patterns": [
                r"date", r"created", r"updated", r"modified", r"add", r"listing",
                r"creation", r"modification", r"maj"
            ],
            
            # === PATTERNS TAXES ===
            "tax_patterns": [
                r"tax", r"taxe", r"municipal", r"school", r"education", r"city", r"town"
            ],
            
            # === PATTERNS REVENUS ===
            "revenue_patterns": [
                r"revenue", r"revenu", r"plex", r"income", r"rental", r"rent"
            ],
            
            # === PATTERNS ÉVALUATIONS ===
            "evaluation_patterns": [
                r"evaluation", r"assessment", r"valuation", r"assessed", r"municipal"
            ],
            
            # === PATTERNS PARKING ===
            "parking_patterns": [
                r"parking", r"garage", r"car", r"vehicle", r"space", r"nb_parking"
            ],
            
            # === PATTERNS UNITÉS ===
            "unit_patterns": [
                r"unit", r"unite", r"residential", r"commercial", r"nb_unit"
            ],
            
            # === PATTERNS DÉPENSES ===
            "expense_patterns": [
                r"expense", r"depense", r"cost", r"maintenance", r"charge"
            ],
            
            # === PATTERNS TERRAIN ===
            "land_patterns": [
                r"lot", r"terrain", r"land", r"ground", r"parcel"
            ],
            
            # === PATTERNS GÉOGRAPHIQUES ===
            "geographic_patterns": [
                r"city", r"ville", r"region", r"province", r"state", r"municipality"
            ]
        }
    
    def detect_similar_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Détecte automatiquement les colonnes similaires
        
        Args:
            df: DataFrame à analyser
            
        Returns:
            Dict des groupes de colonnes similaires
        """
        logger.info("🔍 === DÉTECTION AUTOMATIQUE DES SIMILARITÉS ===")
        
        columns = list(df.columns)
        similarity_groups = {}
        
        # === DÉTECTION PAR PATTERNS REGEX ===
        logger.info("📋 Détection par patterns regex...")
        pattern_groups = self._detect_by_patterns(columns)
        
        # === DÉTECTION PAR SIMILARITÉ SÉMANTIQUE ===
        logger.info("🧠 Détection par similarité sémantique (FuzzyWuzzy)...")
        semantic_groups = self._detect_by_semantic_similarity(columns)
        
        # === DÉTECTION PAR CONTENU ===
        logger.info("📊 Détection par analyse du contenu...")
        content_groups = self._detect_by_content_similarity(df)
        
        # === FUSION DES GROUPES ===
        logger.info("🔗 Fusion des groupes détectés...")
        merged_groups = self._merge_similarity_groups(
            pattern_groups, semantic_groups, content_groups
        )
        
        # === VALIDATION ET NETTOYAGE ===
        logger.info("✅ Validation et nettoyage des groupes...")
        final_groups = self._validate_and_clean_groups(merged_groups, df)
        
        logger.info(f"🎯 {len(final_groups)} groupes de similarités détectés")
        return final_groups
    
    def _detect_by_patterns(self, columns: List[str]) -> Dict[str, List[str]]:
        """Détection par patterns regex"""
        pattern_groups = {}
        
        for pattern_name, patterns in self.patterns.items():
            matching_columns = []
            
            for column in columns:
                column_lower = column.lower()
                
                for pattern in patterns:
                    if re.search(pattern, column_lower):
                        matching_columns.append(column)
                        break
            
            if len(matching_columns) > 1:
                pattern_groups[pattern_name] = matching_columns
        
        return pattern_groups
    
    def _detect_by_semantic_similarity(self, columns: List[str]) -> Dict[str, List[str]]:
        """Détection par similarité sémantique avec FuzzyWuzzy"""
        semantic_groups = {}
        processed_columns = set()
        
        for i, col1 in enumerate(columns):
            if col1 in processed_columns:
                continue
                
            similar_columns = [col1]
            processed_columns.add(col1)
            
            for col2 in columns[i+1:]:
                if col2 in processed_columns:
                    continue
                
                # Calcul de similarité avec FuzzyWuzzy
                ratio = fuzz.ratio(col1.lower(), col2.lower())
                partial_ratio = fuzz.partial_ratio(col1.lower(), col2.lower())
                token_sort_ratio = fuzz.token_sort_ratio(col1.lower(), col2.lower())
                token_set_ratio = fuzz.token_set_ratio(col1.lower(), col2.lower())
                
                # Score composite
                composite_score = (ratio + partial_ratio + token_sort_ratio + token_set_ratio) / 4
                
                if composite_score >= self.similarity_threshold:
                    similar_columns.append(col2)
                    processed_columns.add(col2)
            
            if len(similar_columns) > 1:
                group_name = f"semantic_group_{len(semantic_groups) + 1}"
                semantic_groups[group_name] = similar_columns
        
        return semantic_groups
    
    def _detect_by_content_similarity(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Détection par analyse du contenu des colonnes"""
        content_groups = {}
        columns = list(df.columns)
        
        # Analyse des types de données
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Groupes par type de données
        if len(numeric_columns) > 1:
            content_groups["numeric_group"] = numeric_columns
        
        if len(categorical_columns) > 1:
            content_groups["categorical_group"] = categorical_columns
        
        if len(datetime_columns) > 1:
            content_groups["datetime_group"] = datetime_columns
        
        # Analyse des distributions pour colonnes numériques
        numeric_similarities = self._analyze_numeric_distributions(df, numeric_columns)
        content_groups.update(numeric_similarities)
        
        return content_groups
    
    def _analyze_numeric_distributions(self, df: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, List[str]]:
        """Analyse des distributions pour détecter des colonnes similaires"""
        distribution_groups = {}
        
        if len(numeric_columns) < 2:
            return distribution_groups
        
        # Calcul des statistiques descriptives
        stats_df = df[numeric_columns].describe()
        
        # Groupes par similarité de distribution
        for i, col1 in enumerate(numeric_columns):
            if col1 in [col for group in distribution_groups.values() for col in group]:
                continue
                
            similar_columns = [col1]
            
            for col2 in numeric_columns[i+1:]:
                if col2 in [col for group in distribution_groups.values() for col in group]:
                    continue
                
                # Comparaison des distributions
                similarity_score = self._compare_distributions(
                    df[col1], df[col2], stats_df[col1], stats_df[col2]
                )
                
                if similarity_score >= 0.7:  # Seuil de similarité de distribution
                    similar_columns.append(col2)
            
            if len(similar_columns) > 1:
                group_name = f"distribution_group_{len(distribution_groups) + 1}"
                distribution_groups[group_name] = similar_columns
        
        return distribution_groups
    
    def _compare_distributions(self, series1: pd.Series, series2: pd.Series, 
                              stats1: pd.Series, stats2: pd.Series) -> float:
        """Compare deux distributions numériques"""
        try:
            # Similarité des statistiques descriptives
            mean_similarity = 1 - abs(stats1['mean'] - stats2['mean']) / max(abs(stats1['mean']), abs(stats2['mean']), 1)
            std_similarity = 1 - abs(stats1['std'] - stats2['std']) / max(abs(stats1['std']), abs(stats2['std']), 1)
            
            # Similarité des percentiles
            percentile_similarity = 1 - abs(stats1['75%'] - stats2['75%']) / max(abs(stats1['75%']), abs(stats2['75%']), 1)
            
            # Score composite
            composite_score = (mean_similarity + std_similarity + percentile_similarity) / 3
            
            return max(0, min(1, composite_score))
            
        except Exception:
            return 0.0
    
    def _merge_similarity_groups(self, pattern_groups: Dict, semantic_groups: Dict, 
                                content_groups: Dict) -> Dict[str, List[str]]:
        """Fusion des groupes détectés par différentes méthodes"""
        all_groups = {}
        all_groups.update(pattern_groups)
        all_groups.update(semantic_groups)
        all_groups.update(content_groups)
        
        # Fusion des groupes qui partagent des colonnes
        merged_groups = self._merge_overlapping_groups(all_groups)
        
        return merged_groups
    
    def _merge_overlapping_groups(self, groups: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Fusion des groupes qui partagent des colonnes"""
        if not groups:
            return {}
        
        # Création d'un graphe de connectivité
        column_to_groups = {}
        for group_name, columns in groups.items():
            for column in columns:
                if column not in column_to_groups:
                    column_to_groups[column] = []
                column_to_groups[column].append(group_name)
        
        # Fusion des groupes connectés
        merged_groups = {}
        processed_groups = set()
        
        for group_name, columns in groups.items():
            if group_name in processed_groups:
                continue
            
            # Recherche de tous les groupes connectés
            connected_groups = self._find_connected_groups(group_name, groups, column_to_groups)
            
            # Fusion des colonnes
            all_columns = set()
            for connected_group in connected_groups:
                all_columns.update(groups[connected_group])
                processed_groups.add(connected_group)
            
            if all_columns:
                merged_groups[f"merged_group_{len(merged_groups) + 1}"] = list(all_columns)
        
        return merged_groups
    
    def _find_connected_groups(self, start_group: str, groups: Dict[str, List[str]], 
                              column_to_groups: Dict[str, List[str]]) -> Set[str]:
        """Trouve tous les groupes connectés via des colonnes partagées"""
        connected = {start_group}
        to_process = {start_group}
        
        while to_process:
            current_group = to_process.pop()
            current_columns = groups[current_group]
            
            for column in current_columns:
                if column in column_to_groups:
                    for related_group in column_to_groups[column]:
                        if related_group not in connected:
                            connected.add(related_group)
                            to_process.add(related_group)
        
        return connected
    
    def _validate_and_clean_groups(self, groups: Dict[str, List[str]], 
                                  df: pd.DataFrame) -> Dict[str, List[str]]:
        """Valide et nettoie les groupes détectés"""
        validated_groups = {}
        
        for group_name, columns in groups.items():
            # Vérification que les colonnes existent
            existing_columns = [col for col in columns if col in df.columns]
            
            if len(existing_columns) >= 2:
                # Suppression des doublons
                unique_columns = list(dict.fromkeys(existing_columns))
                validated_groups[group_name] = unique_columns
        
        return validated_groups
    
    def get_similarity_matrix(self, columns: List[str]) -> pd.DataFrame:
        """
        Génère une matrice de similarité entre toutes les colonnes
        
        Args:
            columns: Liste des colonnes à comparer
            
        Returns:
            DataFrame avec la matrice de similarité
        """
        logger.info("📊 Génération de la matrice de similarité...")
        
        n_cols = len(columns)
        similarity_matrix = pd.DataFrame(
            np.zeros((n_cols, n_cols)),
            index=columns,
            columns=columns
        )
        
        for i, col1 in enumerate(columns):
            for j, col2 in enumerate(columns):
                if i == j:
                    similarity_matrix.loc[col1, col2] = 100.0
                else:
                    # Calcul de similarité avec FuzzyWuzzy
                    ratio = fuzz.ratio(col1.lower(), col2.lower())
                    partial_ratio = fuzz.partial_ratio(col1.lower(), col2.lower())
                    token_sort_ratio = fuzz.token_sort_ratio(col1.lower(), col2.lower())
                    token_set_ratio = fuzz.token_set_ratio(col1.lower(), col2.lower())
                    
                    # Score composite
                    composite_score = (ratio + partial_ratio + token_sort_ratio + token_set_ratio) / 4
                    similarity_matrix.loc[col1, col2] = composite_score
        
        return similarity_matrix
    
    def suggest_consolidation_groups(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Suggère des groupes de consolidation basés sur l'analyse
        
        Args:
            df: DataFrame à analyser
            
        Returns:
            Dict avec les suggestions de consolidation
        """
        logger.info("💡 === SUGGESTIONS DE CONSOLIDATION ===")
        
        # Détection des similarités
        similarity_groups = self.detect_similar_columns(df)
        
        # Analyse des suggestions
        suggestions = {}
        
        for group_name, columns in similarity_groups.items():
            if len(columns) >= 2:
                # Analyse de la qualité des colonnes
                quality_analysis = self._analyze_column_quality(df, columns)
                
                suggestions[group_name] = {
                    "columns": columns,
                    "count": len(columns),
                    "quality_analysis": quality_analysis,
                    "consolidation_score": self._calculate_consolidation_score(quality_analysis),
                    "suggested_final_column": self._suggest_final_column_name(columns)
                }
        
        # Tri par score de consolidation
        sorted_suggestions = dict(
            sorted(suggestions.items(), 
                   key=lambda x: x[1]["consolidation_score"], 
                   reverse=True)
        )
        
        logger.info(f"💡 {len(sorted_suggestions)} suggestions de consolidation générées")
        return sorted_suggestions
    
    def _analyze_column_quality(self, df: pd.DataFrame, columns: List[str]) -> Dict:
        """Analyse la qualité des colonnes d'un groupe"""
        quality_analysis = {}
        
        for column in columns:
            if column in df.columns:
                series = df[column]
                
                quality_analysis[column] = {
                    "data_type": str(series.dtype),
                    "non_null_count": series.count(),
                    "null_percentage": (series.isnull().sum() / len(series)) * 100,
                    "unique_count": series.nunique(),
                    "memory_usage": series.memory_usage(deep=True),
                    "sample_values": series.dropna().head(3).tolist()
                }
        
        return quality_analysis
    
    def _calculate_consolidation_score(self, quality_analysis: Dict) -> float:
        """Calcule un score de consolidation pour un groupe"""
        if not quality_analysis:
            return 0.0
        
        scores = []
        
        for col_quality in quality_analysis.values():
            # Score basé sur la complétude
            completeness_score = 1 - (col_quality["null_percentage"] / 100)
            
            # Score basé sur la diversité (pas trop de valeurs uniques)
            diversity_score = 1 - min(col_quality["unique_count"] / 1000, 1)
            
            # Score composite
            col_score = (completeness_score + diversity_score) / 2
            scores.append(col_score)
        
        return sum(scores) / len(scores)
    
    def _suggest_final_column_name(self, columns: List[str]) -> str:
        """Suggère un nom pour la colonne finale consolidée"""
        if not columns:
            return "unknown_final"
        
        # Recherche du nom le plus court et le plus descriptif
        shortest_column = min(columns, key=len)
        
        # Ajout du suffixe _final
        if shortest_column.endswith("_final"):
            return shortest_column
        else:
            return f"{shortest_column}_final"
    
    def generate_similarity_report(self, df: pd.DataFrame, output_path: str = None) -> str:
        """
        Génère un rapport complet d'analyse des similarités
        
        Args:
            df: DataFrame analysé
            output_path: Chemin de sauvegarde (optionnel)
            
        Returns:
            Contenu du rapport
        """
        logger.info("📊 === GÉNÉRATION RAPPORT SIMILARITÉS ===")
        
        # Détection des similarités
        similarity_groups = self.detect_similar_columns(df)
        
        # Suggestions de consolidation
        consolidation_suggestions = self.suggest_consolidation_groups(df)
        
        # Matrice de similarité
        similarity_matrix = self.get_similarity_matrix(list(df.columns))
        
        # Génération du rapport
        report_content = []
        report_content.append("# " + "="*80)
        report_content.append("# RAPPORT D'ANALYSE DES SIMILARITÉS")
        report_content.append("# " + "="*80)
        report_content.append(f"# Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append(f"# Dataset: {df.shape[0]} lignes × {df.shape[1]} colonnes")
        report_content.append("# " + "="*80 + "\n")
        
        # Résumé exécutif
        report_content.append("## RÉSUMÉ EXÉCUTIF")
        report_content.append(f"Colonnes analysées: {len(df.columns)}")
        report_content.append(f"Groupes de similarités détectés: {len(similarity_groups)}")
        report_content.append(f"Suggestions de consolidation: {len(consolidation_suggestions)}")
        report_content.append("")
        
        # Groupes de similarités
        report_content.append("## GROUPES DE SIMILARITÉS DÉTECTÉS")
        for group_name, columns in similarity_groups.items():
            report_content.append(f"### {group_name}")
            report_content.append(f"Colonnes: {', '.join(columns)}")
            report_content.append(f"Nombre: {len(columns)}")
            report_content.append("")
        
        # Suggestions de consolidation
        report_content.append("## SUGGESTIONS DE CONSOLIDATION")
        for group_name, suggestion in consolidation_suggestions.items():
            report_content.append(f"### {group_name}")
            report_content.append(f"Colonnes: {', '.join(suggestion['columns'])}")
            report_content.append(f"Score de consolidation: {suggestion['consolidation_score']:.2f}")
            report_content.append(f"Colonne finale suggérée: {suggestion['suggested_final_column']}")
            report_content.append("")
        
        # Statistiques de qualité
        report_content.append("## ANALYSE DE QUALITÉ PAR GROUPE")
        for group_name, suggestion in consolidation_suggestions.items():
            report_content.append(f"### {group_name}")
            for col, quality in suggestion['quality_analysis'].items():
                report_content.append(f"**{col}**:")
                report_content.append(f"  - Type: {quality['data_type']}")
                report_content.append(f"  - Complétude: {100 - quality['null_percentage']:.1f}%")
                report_content.append(f"  - Valeurs uniques: {quality['unique_count']}")
                report_content.append(f"  - Échantillon: {quality['sample_values']}")
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
                logger.info(f"📄 Rapport sauvegardé: {output_path}")
            except Exception as e:
                logger.error(f"❌ Erreur sauvegarde rapport: {e}")
        
        return report_text

    def spatial_clustering(self, df: pd.DataFrame, eps: float = 0.01, min_samples: int = 5) -> Dict[str, Any]:
        """
        Clustering spatial DBSCAN pour création de zones géographiques
        Respecte les spécifications du real_estate_prompt.md
        
        Args:
            df: DataFrame avec colonnes latitude/longitude
            eps: Distance maximale entre points (degrés)
            min_samples: Nombre minimum de points pour former un cluster
            
        Returns:
            Dict avec résultats du clustering spatial
        """
        logger.info("🌍 === CLUSTERING SPATIAL DBSCAN ===")
        
        try:
            from sklearn.cluster import DBSCAN
            from sklearn.preprocessing import StandardScaler
        except ImportError:
            logger.error("❌ Scikit-learn requis pour clustering spatial")
            return {"success": False, "error": "scikit-learn non disponible"}
        
        # === VÉRIFICATION DES COLONNES GÉOGRAPHIQUES ===
        geo_columns = self._find_geographic_columns(df)
        if not geo_columns:
            logger.warning("⚠️ Aucune colonne géographique trouvée")
            return {"success": False, "error": "colonnes géographiques manquantes"}
        
        logger.info(f"📍 Colonnes géographiques détectées: {geo_columns}")
        
        # === PRÉPARATION DES DONNÉES ===
        geo_data = df[geo_columns].copy()
        geo_data = geo_data.dropna()
        
        if len(geo_data) < min_samples:
            logger.warning(f"⚠️ Données insuffisantes: {len(geo_data)} < {min_samples}")
            return {"success": False, "error": "données insuffisantes"}
        
        # === NORMALISATION DES COORDONNÉES ===
        scaler = StandardScaler()
        geo_scaled = scaler.fit_transform(geo_data)
        
        # === CLUSTERING DBSCAN ===
        logger.info(f"🔍 Clustering avec eps={eps}, min_samples={min_samples}")
        clustering = DBSCAN(eps=eps, min_samples=min_samples, random_state=42)
        cluster_labels = clustering.fit_predict(geo_scaled)
        
        # === ANALYSE DES RÉSULTATS ===
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        n_noise = list(cluster_labels).count(-1)
        
        logger.info(f"🎯 Clusters détectés: {n_clusters}")
        logger.info(f"🔍 Points de bruit: {n_noise}")
        
        # === AJOUT DES LABELS AU DATAFRAME ===
        df_result = df.copy()
        df_result['spatial_cluster'] = cluster_labels
        df_result['spatial_zone'] = df_result['spatial_cluster'].apply(
            lambda x: f"Zone_{x}" if x >= 0 else "Zone_Isolée"
        )
        
        # === STATISTIQUES PAR ZONE ===
        zone_stats = df_result.groupby('spatial_zone').agg({
            'spatial_cluster': 'count',
            geo_columns[0]: ['mean', 'std'],
            geo_columns[1]: ['mean', 'std']
        }).round(6)
        
        zone_stats.columns = ['nb_proprietes', 'lat_moy', 'lat_std', 'lng_moy', 'lng_std']
        
        # === MÉTRIQUES DE QUALITÉ ===
        cluster_quality = {
            'silhouette_score': None,
            'calinski_harabasz_score': None
        }
        
        try:
            from sklearn.metrics import silhouette_score, calinski_harabasz_score
            if n_clusters > 1:
                # Calcul des scores de qualité (excluant les points de bruit)
                valid_mask = cluster_labels >= 0
                if valid_mask.sum() > 1:
                    cluster_quality['silhouette_score'] = silhouette_score(
                        geo_scaled[valid_mask], cluster_labels[valid_mask]
                    )
                    cluster_quality['calinski_harabasz_score'] = calinski_harabasz_score(
                        geo_scaled[valid_mask], cluster_labels[valid_mask]
                    )
        except Exception as e:
            logger.warning(f"⚠️ Calcul des scores de qualité échoué: {e}")
        
        # === RÉSULTATS COMPLETS ===
        results = {
            "success": True,
            "n_clusters": n_clusters,
            "n_noise": n_noise,
            "total_points": len(geo_data),
            "cluster_quality": cluster_quality,
            "zone_statistics": zone_stats.to_dict(),
            "eps_used": eps,
            "min_samples_used": min_samples,
            "geographic_columns": geo_columns,
            "df_with_clusters": df_result
        }
        
        logger.info(f"✅ Clustering spatial réussi: {n_clusters} zones créées")
        return results
        
    def _find_geographic_columns(self, df: pd.DataFrame) -> List[str]:
        """Trouve les colonnes géographiques dans le DataFrame"""
        geo_patterns = [
            r"lat", r"latitude", r"lng", r"longitude", r"long", r"lon",
            r"coord", r"geo", r"x", r"y", r"position"
        ]
        
        geo_columns = []
        for col in df.columns:
            col_lower = col.lower()
            for pattern in geo_patterns:
                if re.search(pattern, col_lower):
                    geo_columns.append(col)
                    break
        
        # Vérification que nous avons au moins lat et lng
        if len(geo_columns) >= 2:
            return geo_columns[:2]  # Retourne les 2 premières colonnes géographiques
        elif len(geo_columns) == 1:
            return geo_columns
        else:
            return []
