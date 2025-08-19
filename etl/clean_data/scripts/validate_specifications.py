#!/usr/bin/env python3
"""
Script de validation des spécifications du projet de nettoyage immobilier
Vérifie que toutes les exigences du real_estate_prompt.md sont respectées
"""

import sys
from pathlib import Path
import importlib
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpecificationValidator:
    """Valide que toutes les spécifications sont respectées"""
    
    def __init__(self):
        self.validation_results = {}
        self.passed_checks = 0
        self.total_checks = 0
        self.failed_checks = []
    
    def validate_all_specifications(self):
        """Valide toutes les spécifications"""
        logger.info("🔍 VALIDATION COMPLÈTE DES SPÉCIFICATIONS")
        logger.info("=" * 60)
        
        # Validation de la structure du projet
        self._validate_project_structure()
        
        # Validation de la stack technologique
        self._validate_tech_stack()
        
        # Validation des phases de nettoyage
        self._validate_cleaning_phases()
        
        # Validation des fonctionnalités
        self._validate_functionality()
        
        # Validation des livrables
        self._validate_deliverables()
        
        # Affichage du résumé
        self._display_summary()
        
        return self.passed_checks == self.total_checks
    
    def _validate_project_structure(self):
        """Valide la structure du projet"""
        logger.info("📁 VALIDATION DE LA STRUCTURE DU PROJET")
        
        # Vérifier les dossiers requis
        required_dirs = [
            "inputs", "outputs", "src", "tests", "docs", "examples"
        ]
        
        for directory in required_dirs:
            self.total_checks += 1
            if Path(directory).exists():
                logger.info(f"  ✅ Dossier {directory} présent")
                self.passed_checks += 1
            else:
                logger.error(f"  ❌ Dossier {directory} manquant")
                self.failed_checks.append(f"Dossier {directory} manquant")
        
        # Vérifier la structure src
        src_structure = [
            "src/__init__.py",
            "src/core/__init__.py",
            "src/core/cleaner.py",
            "src/core/simple_cleaner.py",
            "src/core/config.py",
            "src/exporters/__init__.py",
            "src/exporters/data_exporter.py",
            "src/exporters/report_exporter.py",
            "src/validators/__init__.py",
            "src/validators/data_validator.py",
            "src/utils/__init__.py",
            "src/utils/data_utils.py"
        ]
        
        for file_path in src_structure:
            self.total_checks += 1
            if Path(file_path).exists():
                logger.info(f"  ✅ Fichier {file_path} présent")
                self.passed_checks += 1
            else:
                logger.error(f"  ❌ Fichier {file_path} manquant")
                self.failed_checks.append(f"Fichier {file_path} manquant")
        
        # Vérifier les fichiers principaux
        main_files = [
            "main.py", "requirements.txt", "README.md"
        ]
        
        for file_path in main_files:
            self.total_checks += 1
            if Path(file_path).exists():
                logger.info(f"  ✅ Fichier {file_path} présent")
                self.passed_checks += 1
            else:
                logger.error(f"  ❌ Fichier {file_path} manquant")
                self.failed_checks.append(f"Fichier {file_path} manquant")
    
    def _validate_tech_stack(self):
        """Valide la stack technologique requise"""
        logger.info("🛠️ VALIDATION DE LA STACK TECHNOLOGIQUE")
        
        # Technologies Python requises
        required_packages = [
            "pandas", "numpy", "geopandas", "folium", "geopy",
            "matplotlib", "seaborn", "plotly", "scipy", "sklearn"
        ]
        
        for package in required_packages:
            self.total_checks += 1
            try:
                importlib.import_module(package)
                logger.info(f"  ✅ Package {package} disponible")
                self.passed_checks += 1
            except ImportError:
                logger.error(f"  ❌ Package {package} non disponible")
                self.failed_checks.append(f"Package {package} non disponible")
        
        # Vérifier Python 3.9+
        self.total_checks += 1
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 9:
            logger.info(f"  ✅ Python {python_version.major}.{python_version.minor} compatible")
            self.passed_checks += 1
        else:
            logger.error(f"  ❌ Python {python_version.major}.{python_version.minor} non compatible (3.9+ requis)")
            self.failed_checks.append(f"Python {python_version.major}.{python_version.minor} non compatible")
    
    def _validate_cleaning_phases(self):
        """Valide que toutes les phases de nettoyage sont implémentées"""
        logger.info("🔍 VALIDATION DES PHASES DE NETTOYAGE")
        
        # Phase 1: Audit et diagnostic
        self.total_checks += 1
        if self._check_phase1_implementation():
            logger.info("  ✅ Phase 1: Audit et diagnostic implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Phase 1: Audit et diagnostic manquante")
            self.failed_checks.append("Phase 1: Audit et diagnostic manquante")
        
        # Phase 2: Nettoyage intelligent
        self.total_checks += 1
        if self._check_phase2_implementation():
            logger.info("  ✅ Phase 2: Nettoyage intelligent implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Phase 2: Nettoyage intelligent manquante")
            self.failed_checks.append("Phase 2: Nettoyage intelligent manquante")
        
        # Phase 3: Enrichissement intelligent
        self.total_checks += 1
        if self._check_phase3_implementation():
            logger.info("  ✅ Phase 3: Enrichissement intelligent implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Phase 3: Enrichissement intelligent manquante")
            self.failed_checks.append("Phase 3: Enrichissement intelligent manquante")
        
        # Phase 4: Validation et contrôle qualité
        self.total_checks += 1
        if self._check_phase4_implementation():
            logger.info("  ✅ Phase 4: Validation et contrôle qualité implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Phase 4: Validation et contrôle qualité manquante")
            self.failed_checks.append("Phase 4: Validation et contrôle qualité manquante")
        
        # Phase 5: Préparation pour l'analyse
        self.total_checks += 1
        if self._check_phase5_implementation():
            logger.info("  ✅ Phase 5: Préparation pour l'analyse implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Phase 5: Préparation pour l'analyse manquante")
            self.failed_checks.append("Phase 5: Préparation pour l'analyse manquante")
    
    def _check_phase1_implementation(self):
        """Vérifie l'implémentation de la Phase 1"""
        try:
            # Vérifier que la classe RealEstateDataCleaner a la méthode phase1_audit_diagnostic
            from src.core.cleaner import RealEstateDataCleaner
            return hasattr(RealEstateDataCleaner, 'phase1_audit_diagnostic')
        except:
            return False
    
    def _check_phase2_implementation(self):
        """Vérifie l'implémentation de la Phase 2"""
        try:
            from src.core.cleaner import RealEstateDataCleaner
            return hasattr(RealEstateDataCleaner, 'phase2_cleaning_intelligent')
        except:
            return False
    
    def _check_phase3_implementation(self):
        """Vérifie l'implémentation de la Phase 3"""
        try:
            from src.core.cleaner import RealEstateDataCleaner
            return hasattr(RealEstateDataCleaner, 'phase3_enrichment_intelligent')
        except:
            return False
    
    def _check_phase4_implementation(self):
        """Vérifie l'implémentation de la Phase 4"""
        try:
            from src.core.cleaner import RealEstateDataCleaner
            return hasattr(RealEstateDataCleaner, 'phase4_validation_quality_control')
        except:
            return False
    
    def _check_phase5_implementation(self):
        """Vérifie l'implémentation de la Phase 5"""
        try:
            from src.core.cleaner import RealEstateDataCleaner
            return hasattr(RealEstateDataCleaner, 'phase5_preparation_analysis')
        except:
            return False
    
    def _validate_functionality(self):
        """Valide les fonctionnalités spécifiques"""
        logger.info("⚡ VALIDATION DES FONCTIONNALITÉS")
        
        # Vérifier la gestion des colonnes problématiques
        self.total_checks += 1
        if self._check_problematic_columns_handling():
            logger.info("  ✅ Gestion des colonnes problématiques implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Gestion des colonnes problématiques manquante")
            self.failed_checks.append("Gestion des colonnes problématiques manquante")
        
        # Vérifier la consolidation des colonnes redondantes
        self.total_checks += 1
        if self._check_column_consolidation():
            logger.info("  ✅ Consolidation des colonnes redondantes implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Consolidation des colonnes redondantes manquante")
            self.failed_checks.append("Consolidation des colonnes redondantes manquante")
        
        # Vérifier la gestion géospatiale
        self.total_checks += 1
        if self._check_geospatial_handling():
            logger.info("  ✅ Gestion géospatiale implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Gestion géospatiale manquante")
            self.failed_checks.append("Gestion géospatiale manquante")
        
        # Vérifier la création de métriques
        self.total_checks += 1
        if self._check_metrics_creation():
            logger.info("  ✅ Création de métriques implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Création de métriques manquante")
            self.failed_checks.append("Création de métriques manquante")
    
    def _check_problematic_columns_handling(self):
        """Vérifie la gestion des colonnes problématiques"""
        try:
            # Ajouter le dossier src au path Python
            import sys
            from pathlib import Path
            src_path = Path(__file__).parent / "src"
            sys.path.insert(0, str(src_path))
            
            from src.utils.data_utils import DataUtils
            return hasattr(DataUtils, 'standardize_column_names')
        except Exception as e:
            logger.error(f"Erreur lors de la vérification: {e}")
            return False
    
    def _check_column_consolidation(self):
        """Vérifie la consolidation des colonnes"""
        try:
            from src.utils.data_utils import DataUtils
            return (hasattr(DataUtils, 'consolidate_revenue_columns') and 
                   hasattr(DataUtils, 'consolidate_date_columns'))
        except:
            return False
    
    def _check_geospatial_handling(self):
        """Vérifie la gestion géospatiale"""
        try:
            from src.exporters.data_exporter import DataExporter
            return hasattr(DataExporter, 'export_geojson')
        except:
            return False
    
    def _check_metrics_creation(self):
        """Vérifie la création de métriques"""
        try:
            from src.utils.data_utils import DataUtils
            return (hasattr(DataUtils, 'create_financial_metrics') and 
                   hasattr(DataUtils, 'create_physical_metrics'))
        except:
            return False
    
    def _validate_deliverables(self):
        """Valide les livrables finaux"""
        logger.info("📦 VALIDATION DES LIVRABLES")
        
        # Vérifier l'export multi-format
        self.total_checks += 1
        if self._check_multi_format_export():
            logger.info("  ✅ Export multi-format implémenté")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Export multi-format manquant")
            self.failed_checks.append("Export multi-format manquant")
        
        # Vérifier la génération de rapports
        self.total_checks += 1
        if self._check_report_generation():
            logger.info("  ✅ Génération de rapports implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Génération de rapports manquante")
            self.failed_checks.append("Génération de rapports manquante")
        
        # Vérifier la validation des données
        self.total_checks += 1
        if self._check_data_validation():
            logger.info("  ✅ Validation des données implémentée")
            self.passed_checks += 1
        else:
            logger.error("  ❌ Validation des données manquante")
            self.failed_checks.append("Validation des données manquante")
    
    def _check_multi_format_export(self):
        """Vérifie l'export multi-format"""
        try:
            from src.exporters.data_exporter import DataExporter
            exporter = DataExporter(Path("outputs/cleaned_data"))
            return (hasattr(exporter, 'export_csv') and 
                   hasattr(exporter, 'export_parquet') and
                   hasattr(exporter, 'export_json') and
                   hasattr(exporter, 'export_geojson'))
        except:
            return False
    
    def _check_report_generation(self):
        """Vérifie la génération de rapports"""
        try:
            from src.exporters.report_exporter import ReportExporter
            return hasattr(ReportExporter, 'export_quality_report')
        except:
            return False
    
    def _check_data_validation(self):
        """Vérifie la validation des données"""
        try:
            # Ajouter le dossier src au path Python
            import sys
            from pathlib import Path
            src_path = Path(__file__).parent / "src"
            sys.path.insert(0, str(src_path))
            
            from src.validators.data_validator import DataValidator
            return hasattr(DataValidator, 'validate_dataset')
        except Exception as e:
            logger.error(f"Erreur lors de la vérification: {e}")
            return False
    
    def _display_summary(self):
        """Affiche le résumé de la validation"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 RÉSUMÉ DE LA VALIDATION DES SPÉCIFICATIONS")
        logger.info("=" * 60)
        
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        
        logger.info(f"✅ Tests réussis: {self.passed_checks}/{self.total_checks}")
        logger.info(f"📈 Taux de succès: {success_rate:.1f}%")
        
        if self.failed_checks:
            logger.error(f"❌ Échecs détectés: {len(self.failed_checks)}")
            for failure in self.failed_checks:
                logger.error(f"  - {failure}")
        else:
            logger.info("🎉 Toutes les spécifications sont respectées !")
        
        logger.info("=" * 60)

def main():
    """Fonction principale"""
    logger.info("🚀 DÉMARRAGE DE LA VALIDATION DES SPÉCIFICATIONS")
    
    validator = SpecificationValidator()
    success = validator.validate_all_specifications()
    
    if success:
        logger.info("🎉 VALIDATION RÉUSSIE - Toutes les spécifications sont respectées !")
        return 0
    else:
        logger.error("❌ VALIDATION ÉCHOUÉE - Certaines spécifications ne sont pas respectées")
        return 1

if __name__ == "__main__":
    exit(main())
