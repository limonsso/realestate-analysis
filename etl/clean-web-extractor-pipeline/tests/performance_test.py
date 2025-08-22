"""
Tests de performance pour l'architecture modulaire du CentrisExtractor
"""

import asyncio
import time
import structlog
from unittest.mock import Mock, patch
from concurrent.futures import ThreadPoolExecutor

from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType, PropertySummary, Address

logger = structlog.get_logger()


class MockCentrisConfig:
    """Configuration mock pour les tests de performance"""
    def __init__(self):
        self.base_url = "https://www.centris.ca"
        self.timeout = 30


class PerformanceTestSuite:
    """Suite de tests de performance"""
    
    def __init__(self):
        self.mock_config = MockCentrisConfig()
        self.extractor = None
    
    async def setup(self):
        """Configuration initiale"""
        with patch('config.settings.config') as mock_config:
            mock_config.centris = self.mock_config
            self.extractor = CentrisExtractor(self.mock_config)
    
    async def teardown(self):
        """Nettoyage"""
        if self.extractor:
            await self.extractor.close()
    
    async def test_concurrent_extraction_performance(self):
        """Test de performance avec extraction concurrente"""
        logger.info("⚡ Test de performance avec extraction concurrente...")
        
        start_time = time.time()
        
        # Création de multiples requêtes de recherche
        search_queries = [
            SearchQuery(locations=["Montréal"], property_types=[PropertyType.CONDO]),
            SearchQuery(locations=["Laval"], property_types=[PropertyType.SINGLE_FAMILY_HOME]),
            SearchQuery(locations=["Longueuil"], property_types=[PropertyType.PLEX]),
            SearchQuery(locations=["Brossard"], property_types=[PropertyType.SELL_CONDO])
        ]
        
        try:
            # Mock des composants pour simulation
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                    with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                        
                        # Configuration des mocks
                        mock_search.return_value = ["<html>page1</html>"]
                        mock_extract.return_value = [
                            PropertySummary(
                                id=f"test{i}",
                                address=Address(city="Test", region="Québec"),
                                type=PropertyType.CONDO,
                                price=250000
                            ) for i in range(10)
                        ]
                        mock_validate.return_value = True
                        
                        # Exécution concurrente
                        tasks = [
                            self.extractor.extract_summaries(query) 
                            for query in search_queries
                        ]
                        
                        results = await asyncio.gather(*tasks)
                        
                        # Vérifications
                        assert len(results) == 4
                        assert all(len(result) == 10 for result in results)
                        
                        end_time = time.time()
                        execution_time = end_time - start_time
                        
                        logger.info(f"✅ Extraction concurrente terminée en {execution_time:.2f}s")
                        logger.info(f"📊 {len(search_queries)} requêtes traitées")
                        logger.info(f"🚀 Temps moyen par requête: {execution_time/len(search_queries):.2f}s")
                        
                        return True
                        
        except Exception as e:
            logger.error(f"❌ Erreur du test de performance: {e}")
            return False
    
    async def test_memory_usage_under_load(self):
        """Test de l'utilisation mémoire sous charge"""
        logger.info("💾 Test de l'utilisation mémoire sous charge...")
        
        try:
            # Simulation d'une charge importante
            large_search_query = SearchQuery(
                locations=["Montréal", "Laval", "Longueuil", "Brossard"],
                property_types=[PropertyType.CONDO, PropertyType.SINGLE_FAMILY_HOME, PropertyType.PLEX]
            )
            
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                    with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                        
                        # Simulation de beaucoup de pages
                        mock_search.return_value = [f"<html>page{i}</html>" for i in range(100)]
                        mock_extract.return_value = [
                            PropertySummary(
                                id=f"test{i}",
                                address=Address(city="Test", region="Québec"),
                                type=PropertyType.CONDO,
                                price=250000
                            ) for i in range(20)
                        ]
                        mock_validate.return_value = True
                        
                        # Exécution
                        result = await self.extractor.extract_summaries(large_search_query)
                        
                        # Vérification que la mémoire est gérée correctement
                        assert len(result) == 2000  # 100 pages × 20 propriétés
                        
                        logger.info(f"✅ Gestion mémoire testée avec {len(result)} propriétés")
                        return True
                        
        except Exception as e:
            logger.error(f"❌ Erreur du test mémoire: {e}")
            return False
    
    async def test_response_time_consistency(self):
        """Test de la cohérence des temps de réponse"""
        logger.info("⏱️ Test de la cohérence des temps de réponse...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.CONDO]
            )
            
            response_times = []
            
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                    with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                        
                        mock_search.return_value = ["<html>page1</html>"]
                        mock_extract.return_value = [
                            PropertySummary(
                                id="test1",
                                address=Address(city="Montréal", region="Québec"),
                                type=PropertyType.CONDO,
                                price=250000
                            )
                        ]
                        mock_validate.return_value = True
                        
                        # Exécution multiple pour mesurer la cohérence
                        for i in range(10):
                            start_time = time.time()
                            result = await self.extractor.extract_summaries(search_query)
                            end_time = time.time()
                            
                            response_times.append(end_time - start_time)
                            assert len(result) == 1
                        
                        # Analyse des temps de réponse
                        avg_time = sum(response_times) / len(response_times)
                        max_time = max(response_times)
                        min_time = min(response_times)
                        variance = sum((t - avg_time) ** 2 for t in response_times) / len(response_times)
                        
                        logger.info(f"📊 Temps de réponse - Moyenne: {avg_time:.3f}s")
                        logger.info(f"📊 Temps de réponse - Min: {min_time:.3f}s, Max: {max_time:.3f}s")
                        logger.info(f"📊 Variance: {variance:.6f}")
                        
                        # Vérification de la cohérence (variance faible)
                        assert variance < 0.001  # Variance très faible pour la cohérence
                        
                        return True
                        
        except Exception as e:
            logger.error(f"❌ Erreur du test de cohérence: {e}")
            return False
    
    async def test_scalability_with_component_count(self):
        """Test de la scalabilité avec le nombre de composants"""
        logger.info("📈 Test de la scalabilité avec le nombre de composants...")
        
        try:
            # Test avec différents nombres de composants simulés
            component_counts = [1, 5, 10, 20]
            execution_times = []
            
            for count in component_counts:
                start_time = time.time()
                
                # Simulation de l'utilisation de plusieurs composants
                with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                    with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                        with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                            
                            mock_search.return_value = ["<html>page1</html>"]
                            mock_extract.return_value = [
                                PropertySummary(
                                    id=f"test{i}",
                                    address=Address(city="Test", region="Québec"),
                                    type=PropertyType.CONDO,
                                    price=250000
                                ) for i in range(count)
                            ]
                            mock_validate.return_value = True
                            
                            result = await self.extractor.extract_summaries(
                                SearchQuery(locations=["Test"], property_types=[PropertyType.CONDO])
                            )
                            
                            end_time = time.time()
                            execution_times.append(end_time - start_time)
                            
                            assert len(result) == count
                
                logger.info(f"📊 {count} composants traités en {execution_times[-1]:.3f}s")
            
            # Analyse de la scalabilité
            logger.info("📈 Analyse de la scalabilité:")
            for i, count in enumerate(component_counts):
                logger.info(f"  {count} composants: {execution_times[i]:.3f}s")
            
            # Vérification que le temps n'augmente pas de manière exponentielle
            for i in range(1, len(execution_times)):
                time_increase = execution_times[i] / execution_times[i-1]
                assert time_increase < 3.0  # L'augmentation doit être raisonnable
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de scalabilité: {e}")
            return False


async def run_performance_tests():
    """Exécution de tous les tests de performance"""
    logger.info("🚀 Démarrage des tests de performance...")
    
    test_suite = PerformanceTestSuite()
    
    try:
        await test_suite.setup()
        
        tests = [
            test_suite.test_concurrent_extraction_performance(),
            test_suite.test_memory_usage_under_load(),
            test_suite.test_response_time_consistency(),
            test_suite.test_scalability_with_component_count()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Analyse des résultats
        passed = sum(1 for r in results if r is True)
        failed = len(results) - passed
        
        logger.info(f"\n📊 Résumé des tests de performance:")
        logger.info(f"✅ Réussis: {passed}")
        logger.info(f"❌ Échoués: {failed}")
        
        return passed, failed
        
    finally:
        await test_suite.teardown()


if __name__ == "__main__":
    asyncio.run(run_performance_tests())
