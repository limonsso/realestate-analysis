#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 DASHBOARD DE VALIDATION INTERACTIF - CONTRÔLE QUALITÉ VISUEL
===============================================================

Dashboard interactif pour la validation et le contrôle qualité des données
Basé sur les spécifications du real_estate_prompt.md
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
import json
import warnings
from datetime import datetime

# Imports conditionnels pour Plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    warnings.warn("Plotly non disponible - dashboard non fonctionnel")

# Imports conditionnels pour Seaborn
try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    warnings.warn("Seaborn non disponible - visualisations limitées")

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class ValidationDashboard:
    """
    Dashboard de validation interactif pour le pipeline ETL
    Intègre Plotly + Seaborn pour visualisations premium
    """
    
    def __init__(self, dashboard_config: Dict = None):
        """
        Initialise le dashboard de validation
        
        Args:
            dashboard_config: Configuration du dashboard
        """
        self.dashboard_config = dashboard_config or self._default_dashboard_config()
        self.dashboard_data = {}
        self.visualization_history = []
        
        logger.info("📊 === INITIALISATION DU DASHBOARD DE VALIDATION ===")
        logger.info(f"🎨 Plotly: {'✅' if PLOTLY_AVAILABLE else '❌'}")
        logger.info(f"📈 Seaborn: {'✅' if SEABORN_AVAILABLE else '❌'}")
        
        if not PLOTLY_AVAILABLE:
            logger.error("❌ Plotly requis pour le dashboard interactif")
            raise ImportError("Plotly non disponible")
    
    def _default_dashboard_config(self) -> Dict:
        """Configuration par défaut du dashboard"""
        return {
            "theme": "plotly_white",
            "colors": {
                "primary": "#1f77b4",
                "secondary": "#ff7f0e",
                "success": "#2ca02c",
                "warning": "#d62728",
                "info": "#9467bd"
            },
            "layout": {
                "width": 1200,
                "height": 800,
                "margin": {"l": 50, "r": 50, "t": 50, "b": 50}
            },
            "export": {
                "formats": ["html", "png", "pdf"],
                "directory": "dashboard_exports"
            }
        }
    
    def create_quality_overview_dashboard(self, df: pd.DataFrame, 
                                        quality_metrics: Dict) -> Dict[str, Any]:
        """
        Crée un dashboard de vue d'ensemble de la qualité
        
        Args:
            df: DataFrame à analyser
            quality_metrics: Métriques de qualité
            
        Returns:
            Dict avec les figures et métriques
        """
        logger.info("📊 === CRÉATION DU DASHBOARD QUALITÉ ===")
        
        if not PLOTLY_AVAILABLE:
            return {"error": "Plotly non disponible"}
        
        # === FIGURE 1: COMPLÉTUDE DES DONNÉES ===
        fig1 = self._create_completeness_chart(df)
        
        # === FIGURE 2: DISTRIBUTION DES VALEURS ===
        fig2 = self._create_value_distribution_chart(df)
        
        # === FIGURE 3: MÉTRIQUES DE QUALITÉ ===
        fig3 = self._create_quality_metrics_chart(quality_metrics)
        
        # === FIGURE 4: ANALYSE DES ANOMALIES ===
        fig4 = self._create_anomaly_analysis_chart(df)
        
        # === DASHBOARD COMPLET ===
        dashboard = {
            "figures": {
                "completeness": fig1,
                "distribution": fig2,
                "quality_metrics": fig3,
                "anomalies": fig4
            },
            "metrics": quality_metrics,
            "dataset_info": {
                "shape": df.shape,
                "memory_usage": df.memory_usage(deep=True).sum() / 1024**2,  # MB
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict()
            }
        }
        
        logger.info("✅ Dashboard qualité créé avec succès")
        return dashboard
    
    def _create_completeness_chart(self, df: pd.DataFrame) -> go.Figure:
        """Crée un graphique de complétude des données"""
        completeness = (1 - df.isna().sum() / len(df)) * 100
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(completeness.index),
                y=list(completeness.values),
                marker_color=[
                    'green' if val >= 80 else 'orange' if val >= 60 else 'red'
                    for val in completeness.values
                ],
                text=[f"{val:.1f}%" for val in completeness.values],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="📊 Complétude des Données par Colonne",
            xaxis_title="Colonnes",
            yaxis_title="Complétude (%)",
            yaxis_range=[0, 100],
            template=self.dashboard_config["theme"],
            **self.dashboard_config["layout"]
        )
        
        return fig
    
    def _create_value_distribution_chart(self, df: pd.DataFrame) -> go.Figure:
        """Crée un graphique de distribution des valeurs"""
        # Sélection des colonnes numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:6]  # Limite à 6 colonnes
        
        if len(numeric_cols) == 0:
            return go.Figure().add_annotation(
                text="Aucune colonne numérique disponible",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        # Création des sous-graphiques
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=[f"Distribution {col}" for col in numeric_cols],
            specs=[[{"type": "histogram"}, {"type": "histogram"}, {"type": "histogram"}],
                   [{"type": "histogram"}, {"type": "histogram"}, {"type": "histogram"}]]
        )
        
        for i, col in enumerate(numeric_cols):
            row = (i // 3) + 1
            col_pos = (i % 3) + 1
            
            fig.add_trace(
                go.Histogram(x=df[col].dropna(), name=col, showlegend=False),
                row=row, col=col_pos
            )
        
        fig.update_layout(
            title="📈 Distribution des Valeurs Numériques",
            template=self.dashboard_config["theme"],
            **self.dashboard_config["layout"]
        )
        
        return fig
    
    def _create_quality_metrics_chart(self, quality_metrics: Dict) -> go.Figure:
        """Crée un graphique des métriques de qualité"""
        if not quality_metrics:
            return go.Figure().add_annotation(
                text="Aucune métrique de qualité disponible",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        # Extraction des métriques principales
        metrics = {}
        for key, value in quality_metrics.items():
            if isinstance(value, (int, float)):
                metrics[key] = value
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        metrics[f"{key}_{sub_key}"] = sub_value
        
        if not metrics:
            return go.Figure().add_annotation(
                text="Aucune métrique numérique disponible",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                marker_color=self.dashboard_config["colors"]["primary"],
                text=[f"{val:.2f}" if isinstance(val, float) else str(val) for val in metrics.values()],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="🎯 Métriques de Qualité des Données",
            xaxis_title="Métriques",
            yaxis_title="Valeurs",
            template=self.dashboard_config["theme"],
            **self.dashboard_config["layout"]
        )
        
        return fig
    
    def _create_anomaly_analysis_chart(self, df: pd.DataFrame) -> go.Figure:
        """Crée un graphique d'analyse des anomalies"""
        # Sélection des colonnes numériques pour l'analyse des outliers
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:3]  # Limite à 3 colonnes
        
        if len(numeric_cols) == 0:
            return go.Figure().add_annotation(
                text="Aucune colonne numérique disponible pour l'analyse des anomalies",
                xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
            )
        
        fig = make_subplots(
            rows=1, cols=len(numeric_cols),
            subplot_titles=[f"Anomalies {col}" for col in numeric_cols],
            specs=[[{"type": "box"}] * len(numeric_cols)]
        )
        
        for i, col in enumerate(numeric_cols):
            fig.add_trace(
                go.Box(y=df[col].dropna(), name=col, showlegend=False),
                row=1, col=i+1
            )
        
        fig.update_layout(
            title="🚨 Analyse des Anomalies (Box Plots)",
            template=self.dashboard_config["theme"],
            **self.dashboard_config["layout"]
        )
        
        return fig
    
    def export_dashboard(self, dashboard: Dict, filename: str = None, 
                        format: str = "html") -> str:
        """
        Exporte le dashboard dans différents formats
        
        Args:
            dashboard: Dashboard à exporter
            filename: Nom du fichier (optionnel)
            format: Format d'export (html, png, pdf)
            
        Returns:
            Chemin du fichier exporté
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_dashboard_{timestamp}"
        
        export_dir = Path(self.dashboard_config["export"]["directory"])
        export_dir.mkdir(exist_ok=True)
        
        if format == "html":
            # Export HTML interactif
            html_content = self._create_html_dashboard(dashboard)
            filepath = export_dir / f"{filename}.html"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Dashboard exporté en HTML: {filepath}")
            return str(filepath)
        
        elif format == "png":
            # Export PNG (première figure)
            if dashboard.get("figures"):
                first_fig = list(dashboard["figures"].values())[0]
                filepath = export_dir / f"{filename}.png"
                first_fig.write_image(str(filepath))
                logger.info(f"✅ Dashboard exporté en PNG: {filepath}")
                return str(filepath)
        
        else:
            logger.warning(f"⚠️ Format {format} non supporté")
            return ""
    
    def _create_html_dashboard(self, dashboard: Dict) -> str:
        """Crée le contenu HTML du dashboard"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard de Validation - Pipeline ETL</title>
            <meta charset="utf-8">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
                .header { background-color: #1f77b4; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .section { background-color: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }
                .metric-card { background-color: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
                .metric-value { font-size: 24px; font-weight: bold; color: #1f77b4; }
                .metric-label { color: #666; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Dashboard de Validation - Pipeline ETL Ultra-Intelligent</h1>
                <p>Contrôle qualité et validation des données immobilières</p>
            </div>
            
            <div class="section">
                <h2>📊 Informations du Dataset</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{shape[0]}</div>
                        <div class="metric-label">Lignes</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{shape[1]}</div>
                        <div class="metric-label">Colonnes</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{memory:.1f} MB</div>
                        <div class="metric-label">Mémoire</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Complétude des Données</h2>
                <div id="completeness-chart"></div>
            </div>
            
            <div class="section">
                <h2>📊 Distribution des Valeurs</h2>
                <div id="distribution-chart"></div>
            </div>
            
            <div class="section">
                <h2>🎯 Métriques de Qualité</h2>
                <div id="quality-chart"></div>
            </div>
            
            <div class="section">
                <h2>🚨 Analyse des Anomalies</h2>
                <div id="anomaly-chart"></div>
            </div>
            
            <script>
                // Intégration des graphiques Plotly
                {plotly_scripts}
            </script>
        </body>
        </html>
        """
        
        # Préparation des données pour le template
        dataset_info = dashboard.get("dataset_info", {})
        shape = dataset_info.get("shape", [0, 0])
        memory = dataset_info.get("memory_usage", 0)
        
        # Génération des scripts Plotly
        plotly_scripts = ""
        for name, fig in dashboard.get("figures", {}).items():
            plotly_scripts += f"""
            var {name.replace('-', '_')} = {fig.to_json()};
            Plotly.newPlot('{name}-chart', {name.replace('-', '_')}.data, {name.replace('-', '_')}.layout);
            """
        
        return html_template.format(
            shape=shape,
            memory=memory,
            plotly_scripts=plotly_scripts
        )
