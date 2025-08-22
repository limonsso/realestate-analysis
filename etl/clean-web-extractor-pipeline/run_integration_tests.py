"""
Script principal pour exécuter tous les tests d'intégration
"""

import asyncio
import structlog
from datetime import datetime

# Import des suites de tests
from tests.integration_test import run_integration_tests
from tests.performance_test import run_performance_tests
from tests.robustness_test import run_robustness_tests

logger = structlog.get_logger()


async def run_all_integration_tests():
    """Exécution de tous les tests d'intégration"""
    logger.info("🚀 DÉMARRAGE DES TESTS D'INTÉGRATION COMPLETS")
    logger.info("=" * 80)
    
    start_time = datetime.now()
    
    # Résultats des tests
    results = {}
    
    try:
        # 1. Tests d'intégration de base
        logger.info("\n🔗 PHASE 1: Tests d'Intégration de Base")
        logger.info("-" * 50)
        passed, failed = await run_integration_tests()
        results['integration'] = {'passed': passed, 'failed': failed}
        
        # 2. Tests de performance
        logger.info("\n⚡ PHASE 2: Tests de Performance")
        logger.info("-" * 50)
        passed, failed = await run_performance_tests()
        results['performance'] = {'passed': passed, 'failed': failed}
        
        # 3. Tests de robustesse
        logger.info("\n🛡️ PHASE 3: Tests de Robustesse")
        logger.info("-" * 50)
        passed, failed = await run_robustness_tests()
        results['robustness'] = {'passed': passed, 'failed': failed}
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors des tests: {e}")
        return False
    
    finally:
        end_time = datetime.now()
        execution_time = end_time - start_time
    
    # Résumé final
    logger.info("\n" + "=" * 80)
    logger.info("📊 RÉSUMÉ FINAL DES TESTS D'INTÉGRATION")
    logger.info("=" * 80)
    
    total_passed = sum(r['passed'] for r in results.values())
    total_failed = sum(r['failed'] for r in results.values())
    total_tests = total_passed + total_failed
    
    # Détail par catégorie
    for category, result in results.items():
        success_rate = (result['passed'] / (result['passed'] + result['failed'])) * 100 if (result['passed'] + result['failed']) > 0 else 0
        logger.info(f"📋 {category.upper()}: {result['passed']}/{result['passed'] + result['failed']} ({success_rate:.1f}%)")
    
    # Résumé global
    logger.info("-" * 50)
    global_success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    logger.info(f"🎯 TOTAL: {total_passed}/{total_tests} ({global_success_rate:.1f}%)")
    logger.info(f"⏱️ Temps d'exécution: {execution_time}")
    
    # Statut final
    if total_failed == 0:
        logger.info("🎉 TOUS LES TESTS D'INTÉGRATION ONT RÉUSSI !")
        logger.info("✅ L'architecture modulaire est prête pour la production")
        return True
    else:
        logger.warning(f"⚠️ {total_failed} test(s) ont échoué")
        logger.warning("🔧 Vérifiez les composants défaillants")
        return False


def main():
    """Fonction principale"""
    try:
        success = asyncio.run(run_all_integration_tests())
        exit_code = 0 if success else 1
        exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n⏹️ Tests interrompus par l'utilisateur")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        exit(1)


if __name__ == "__main__":
    main()

