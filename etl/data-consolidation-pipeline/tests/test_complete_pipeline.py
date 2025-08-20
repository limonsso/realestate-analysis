#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST COMPLET DU PIPELINE AVEC REQUÊTE MONGODB
=================================================

Test complet du pipeline ETL avec l'architecture modulaire
Utilise une requête MongoDB d'exemple pour valider le fonctionnement
"""

import sys
import logging
import json
from pathlib import Path
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_test_query_file():
    """Crée un fichier de requête MongoDB de test"""
    logger.info("📝 Création du fichier de requête de test...")
    
    # Requête de test : triplex à Trois-Rivières
    test_query = {
        "city": "Trois-Rivières",
        "type": {
            "$regex": "triplex",
            "$options": "i"
        }
    }
    
    # Création du répertoire examples s'il n'existe pas
    examples_dir = Path('examples')
    examples_dir.mkdir(exist_ok=True)
    
    # Fichier de requête de test
    query_file_path = examples_dir / 'test_query_trois_rivieres_triplex.json'
    
    with open(query_file_path, 'w', encoding='utf-8') as f:
        json.dump(test_query, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Fichier de requête créé: {query_file_path}")
    return str(query_file_path)

def test_pipeline_with_mongodb_query():
    """Test du pipeline complet avec une requête MongoDB"""
    logger.info("🧪 === TEST DU PIPELINE COMPLET AVEC REQUÊTE MONGODB ===")
    
    try:
        # Création du fichier de requête
        query_file_path = create_test_query_file()
        
        # Configuration du pipeline
        input_config = {
            "database": "real_estate_db",
            "collection": "properties",
            "limit": 50,  # Limite pour le test
            "query_file": query_file_path
        }
        
        output_config = {
            "output_dir": "exports/test_pipeline/",
            "formats": ["csv", "json"],
            "filename_prefix": "test_pipeline_trois_rivieres_triplex"
        }
        
        logger.info("🔧 Configuration du pipeline:")
        logger.info(f"   📥 Source: MongoDB")
        logger.info(f"   🗄️ Base: {input_config['database']}")
        logger.info(f"   📚 Collection: {input_config['collection']}")
        logger.info(f"   📊 Limite: {input_config['limit']} documents")
        logger.info(f"   🔍 Requête: {query_file_path}")
        logger.info(f"   📤 Sortie: {output_config['output_dir']}")
        
        # Import de l'orchestrateur
        logger.info("📦 Import de l'orchestrateur principal...")
        sys.path.insert(0, 'core')
        
        from main_pipeline_orchestrator import MainPipelineOrchestrator
        
        # Initialisation de l'orchestrateur
        logger.info("🎼 Initialisation de l'orchestrateur...")
        orchestrator = MainPipelineOrchestrator(
            config=input_config,
            use_external_modules=True  # Tente d'utiliser tous les modules disponibles
        )
        
        # Test des composants individuels
        logger.info("🧪 Test des composants individuels...")
        component_tests = orchestrator.test_individual_components()
        logger.info(f"📊 Tests des composants: {component_tests}")
        
        # Vérification du statut des modules externes
        logger.info("🔧 Statut des modules externes...")
        external_status = orchestrator.get_external_modules_status()
        available_modules = sum(1 for s in external_status.values() if s['available'])
        total_modules = len(external_status)
        logger.info(f"📊 Modules externes: {available_modules}/{total_modules} disponibles")
        
        # Exécution du pipeline complet
        logger.info("🚀 === DÉMARRAGE DU PIPELINE COMPLET ===")
        
        start_time = datetime.now()
        
        try:
            results = orchestrator.run_complete_pipeline(
                input_source="mongodb",
                input_config=input_config,
                output_config=output_config
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("🎉 === PIPELINE COMPLET TERMINÉ AVEC SUCCÈS ===")
            logger.info(f"⏱️ Durée totale: {duration:.2f}s")
            
            # Analyse des résultats
            logger.info("📊 === ANALYSE DES RÉSULTATS ===")
            
            if results.get('success'):
                logger.info("✅ Statut: Succès")
                logger.info(f"📊 Forme d'entrée: {results.get('input_shape', 'N/A')}")
                logger.info(f"📊 Forme de sortie: {results.get('output_shape', 'N/A')}")
                logger.info(f"📉 Réduction: {results.get('reduction_percentage', 0):.1f}%")
                logger.info(f"⭐ Score qualité: {results.get('overall_quality_score', 0):.1%}")
                
                # Résultats du clustering spatial
                spatial_results = results.get('spatial_clustering', {})
                if spatial_results.get('success'):
                    logger.info(f"🌍 Clustering spatial: {spatial_results.get('n_clusters', 0)} zones créées")
                else:
                    logger.info(f"🌍 Clustering spatial: {spatial_results.get('message', 'Non exécuté')}")
                
                # Résultats de catégorisation
                categorization_stats = results.get('categorization_stats', {})
                logger.info(f"🏷️ Catégorisation: {categorization_stats}")
                
                # Résultats de validation
                validation_results = results.get('validation_results', {})
                if 'overall_status' in validation_results:
                    overall_status = validation_results['overall_status']
                    logger.info(f"✅ Validation: {overall_status.get('status', 'N/A')} - Score: {overall_status.get('quality_score', 0):.1%}")
                
                # Résultats d'export
                export_results = results.get('export_results', {})
                if export_results.get('success'):
                    logger.info(f"📤 Export: {export_results.get('files_generated', 0)} fichiers générés")
                    logger.info(f"📁 Formats: {export_results.get('formats', [])}")
                
                # Métriques modulaires
                modular_results = results.get('modular_pipeline_results', {})
                if modular_results:
                    logger.info("🎼 Résultats du pipeline modulaire disponibles")
                    
                    # Statistiques des composants
                    component_stats = results.get('component_stats', {})
                    if component_stats:
                        logger.info("📊 Statistiques des composants:")
                        for component, stats in component_stats.items():
                            logger.info(f"   • {component}: {stats}")
                
                return True, results
                
            else:
                logger.error("❌ Pipeline échoué")
                return False, results
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'exécution du pipeline: {e}")
            return False, {"error": str(e)}
            
    except ImportError as e:
        logger.error(f"❌ Erreur d'import: {e}")
        return False, {"error": f"Import error: {str(e)}"}
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        return False, {"error": f"Unexpected error: {str(e)}"}

def test_pipeline_modular_only():
    """Test du pipeline modulaire uniquement (sans phases spécialisées)"""
    logger.info("🧪 === TEST DU PIPELINE MODULAIRE UNIQUEMENT ===")
    
    try:
        # Configuration simple pour le test modulaire
        input_config = {
            "source": "test",
            "limit": 100
        }
        
        output_config = {
            "output_dir": "exports/test_modular/",
            "formats": ["csv"],
            "filename_prefix": "test_modular_pipeline"
        }
        
        logger.info("🔧 Configuration du pipeline modulaire:")
        logger.info(f"   📥 Source: {input_config['source']}")
        logger.info(f"   📊 Limite: {input_config['limit']} documents")
        logger.info(f"   📤 Sortie: {output_config['output_dir']}")
        
        # Import de l'orchestrateur
        from core.main_pipeline_orchestrator import MainPipelineOrchestrator
        
        # Initialisation de l'orchestrateur
        orchestrator = MainPipelineOrchestrator(
            config=input_config,
            use_external_modules=False  # Uniquement les composants modulaires
        )
        
        # Exécution du pipeline modulaire
        logger.info("🎼 Exécution du pipeline modulaire...")
        
        start_time = datetime.now()
        
        results = orchestrator.run_modular_pipeline_only(
            input_source="test",
            input_config=input_config,
            output_config=output_config
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("✅ Pipeline modulaire exécuté avec succès")
        logger.info(f"⏱️ Durée: {duration:.2f}s")
        logger.info(f"📊 Résultats: {results}")
        
        return True, results
        
    except Exception as e:
        logger.error(f"❌ Erreur pipeline modulaire: {e}")
        return False, {"error": str(e)}

def run_all_tests():
    """Exécution de tous les tests"""
    logger.info("🚀 === DÉMARRAGE DES TESTS COMPLETS DU PIPELINE ===")
    
    tests = [
        ("Pipeline complet avec MongoDB", test_pipeline_with_mongodb_query),
        ("Pipeline modulaire uniquement", test_pipeline_modular_only)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Test: {test_name}")
        logger.info("=" * 50)
        
        try:
            success, test_results = test_func()
            results.append((test_name, success, test_results))
            
            if success:
                logger.info(f"✅ {test_name}: SUCCÈS")
            else:
                logger.error(f"❌ {test_name}: ÉCHEC")
                if isinstance(test_results, dict) and 'error' in test_results:
                    logger.error(f"   Erreur: {test_results['error']}")
                    
        except Exception as e:
            logger.error(f"❌ {test_name}: ERREUR - {e}")
            results.append((test_name, False, {"error": str(e)}))
    
    # Résumé des tests
    logger.info("\n📊 === RÉSUMÉ DES TESTS ===")
    successful_tests = sum(1 for _, success, _ in results if success)
    total_tests = len(results)
    
    for test_name, success, test_results in results:
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        logger.info(f"{test_name}: {status}")
        
        if success and isinstance(test_results, dict):
            # Affichage des métriques clés
            if 'pipeline_duration' in test_results:
                logger.info(f"   ⏱️ Durée: {test_results['pipeline_duration']:.2f}s")
            if 'overall_quality_score' in test_results:
                logger.info(f"   ⭐ Qualité: {test_results['overall_quality_score']:.1%}")
    
    logger.info(f"\n🎯 Résultat global: {successful_tests}/{total_tests} tests réussis")
    
    if successful_tests == total_tests:
        logger.info("🎉 Tous les tests sont passés avec succès !")
        logger.info("🎯 Le pipeline complet fonctionne parfaitement !")
        return True
    else:
        logger.warning(f"⚠️ {total_tests - successful_tests} test(s) ont échoué")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("⏹️ Tests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur fatale lors des tests: {e}")
        sys.exit(1)
