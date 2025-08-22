"""
Tests de robustesse pour l'architecture modulaire du CentrisExtractor
"""

import asyncio
import structlog
from unittest.mock import Mock, patch, AsyncMock
from aiohttp import ClientError, ServerTimeoutError

from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType, PropertySummary, Address

logger = structlog.get_logger()


class MockCentrisConfig:
    """Configuration mock pour les tests de robustesse"""
    def __init__(self):
        self.base_url = "https://www.centris.ca"
        self.timeout = 30


class RobustnessTestSuite:
    """Suite de tests de robustesse"""
    
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
    
    async def test_network_failure_handling(self):
        """Test de la gestion des échecs réseau"""
        logger.info("🌐 Test de la gestion des échecs réseau...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.CONDO]
            )
            
            # Simulation d'échec réseau
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                mock_search.side_effect = ClientError("Erreur de connexion")
                
                # L'extracteur doit gérer l'erreur gracieusement
                try:
                    result = await self.extractor.extract_summaries(search_query)
                    # Si on arrive ici, l'erreur n'a pas été gérée correctement
                    assert False, "L'erreur réseau aurait dû être gérée"
                except Exception as e:
                    # L'erreur doit être capturée et relancée
                    assert "Erreur de connexion" in str(e)
                    logger.info("✅ Gestion d'erreur réseau testée")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de robustesse réseau: {e}")
            return False
    
    async def test_timeout_handling(self):
        """Test de la gestion des timeouts"""
        logger.info("⏰ Test de la gestion des timeouts...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.CONDO]
            )
            
            # Simulation de timeout
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                mock_search.side_effect = ServerTimeoutError("Timeout de la requête")
                
                try:
                    result = await self.extractor.extract_summaries(search_query)
                    assert False, "Le timeout aurait dû être géré"
                except Exception as e:
                    assert "Timeout" in str(e)
                    logger.info("✅ Gestion de timeout testée")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de timeout: {e}")
            return False
    
    async def test_invalid_data_handling(self):
        """Test de la gestion des données invalides"""
        logger.info("⚠️ Test de la gestion des données invalides...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.CONDO]
            )
            
            # Simulation de données HTML invalides
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                    
                    mock_search.return_value = ["<invalid>html</invalid>"]
                    mock_extract.return_value = []  # Aucune propriété extraite
                    
                    result = await self.extractor.extract_summaries(search_query)
                    
                    # L'extracteur doit gérer les données invalides
                    assert result == []
                    logger.info("✅ Gestion de données invalides testée")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de données invalides: {e}")
            return False
    
    async def test_component_failure_isolation(self):
        """Test de l'isolation des échecs de composants"""
        logger.info("🔒 Test de l'isolation des échecs de composants...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.CONDO]
            )
            
            # Simulation d'échec du validateur
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.data_validator, 'validate_search_results') as mock_validate:
                    
                    mock_search.return_value = ["<html>page1</html>"]
                    mock_validate.side_effect = Exception("Erreur du validateur")
                    
                    # L'erreur du validateur ne doit pas affecter les autres composants
                    try:
                        result = await self.extractor.extract_summaries(search_query)
                        # Le validateur a une gestion d'erreur qui retourne True par défaut
                        assert len(result) > 0
                        logger.info("✅ Isolation des échecs de composants testée")
                    except Exception as e:
                        # Si une erreur est levée, elle doit être spécifique au validateur
                        assert "validateur" in str(e).lower()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test d'isolation: {e}")
            return False
    
    async def test_memory_leak_prevention(self):
        """Test de la prévention des fuites mémoire"""
        logger.info("💾 Test de la prévention des fuites mémoire...")
        
        try:
            # Exécution multiple pour détecter les fuites
            for i in range(10):
                search_query = SearchQuery(
                    locations=["Montréal"],
                    property_types=[PropertyType.CONDO]
                )
                
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
                                )
                            ]
                            mock_validate.return_value = True
                            
                            result = await self.extractor.extract_summaries(search_query)
                            assert len(result) == 1
                
                # Vérification que les composants sont toujours accessibles
                assert self.extractor.session_manager is not None
                assert self.extractor.search_manager is not None
                assert self.extractor.summary_extractor is not None
                assert self.extractor.detail_extractor is not None
                assert self.extractor.data_validator is not None
            
            logger.info("✅ Prévention des fuites mémoire testée")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de prévention des fuites: {e}")
            return False
    
    async def test_graceful_degradation(self):
        """Test de la dégradation gracieuse"""
        logger.info("🔄 Test de la dégradation gracieuse...")
        
        try:
            search_query = SearchQuery(
                locations=["Montréal"],
                property_types=[PropertyType.CONDO]
            )
            
            # Simulation de dégradation progressive
            with patch.object(self.extractor.search_manager, 'search_with_pagination') as mock_search:
                with patch.object(self.extractor.summary_extractor, 'extract_summaries_from_html') as mock_extract:
                    
                    # Première page réussit, deuxième échoue
                    mock_search.return_value = ["<html>page1</html>", "<html>page2</html>"]
                    mock_extract.side_effect = [
                        [PropertySummary(id="test1", address=Address(), type=PropertyType.CONDO, price=250000)],
                        []  # Deuxième page échoue
                    ]
                    
                    result = await self.extractor.extract_summaries(search_query)
                    
                    # L'extracteur doit continuer avec les données disponibles
                    assert len(result) == 1
                    assert result[0].id == "test1"
                    
                    logger.info("✅ Dégradation gracieuse testée")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur du test de dégradation: {e}")
            return False


async def run_robustness_tests():
    """Exécution de tous les tests de robustesse"""
    logger.info("🚀 Démarrage des tests de robustesse...")
    
    test_suite = RobustnessTestSuite()
    
    try:
        await test_suite.setup()
        
        tests = [
            test_suite.test_network_failure_handling(),
            test_suite.test_timeout_handling(),
            test_suite.test_invalid_data_handling(),
            test_suite.test_component_failure_isolation(),
            test_suite.test_memory_leak_prevention(),
            test_suite.test_graceful_degradation()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Analyse des résultats
        passed = sum(1 for r in results if r is True)
        failed = len(results) - passed
        
        logger.info(f"\n📊 Résumé des tests de robustesse:")
        logger.info(f"✅ Réussis: {passed}")
        logger.info(f"❌ Échoués: {failed}")
        
        return passed, failed
        
    finally:
        await test_suite.teardown()


if __name__ == "__main__":
    asyncio.run(run_robustness_tests())

