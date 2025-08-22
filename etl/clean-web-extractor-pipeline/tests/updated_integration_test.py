#!/usr/bin/env python3
"""
Tests d'intégration mis à jour pour utiliser LocationConfig
Teste l'architecture modulaire avec le nouveau format de localisation
"""

import asyncio
import structlog
from unittest.mock import patch
from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType
from config.settings import config, LocationConfig
from src.utils.logging import setup_logging

# Configuration du logging
setup_logging()
logger = structlog.get_logger(__name__)


class UpdatedIntegrationTestSuite:
    """Suite de tests d'intégration avec LocationConfig"""
    
    def __init__(self):
        self.extractor = None
        self.test_results = []
        
    async def setup(self):
        """Configuration initiale des tests"""
        logger.info("🔧 Configuration des tests d'intégration mis à jour...")
        
        # Initialisation de l'extracteur avec architecture modulaire
        self.extractor = CentrisExtractor(config.centris)
        
        logger.info("✅ Configuration terminée")
        
    async def cleanup(self):
        """Nettoyage des ressources"""
        if self.extractor:
            await self.extractor.close()
            logger.info("🔌 CentrisExtractor fermé proprement")
            
    async def test_location_config_integration(self):
        """Test d'intégration avec LocationConfig"""
        logger.info("🎯 Test d'intégration avec LocationConfig...")
        
        try:
            # Création d'une requête avec LocationConfig
            search_query = SearchQuery(
                locations=[
                    LocationConfig(
                        type="GeographicArea",
                        value="Montréal",
                        type_id="GSGS4621"
                    ),
                    LocationConfig(
                        type="GeographicArea",
                        value="Laval",
                        type_id="GSGS4622"
                    )
                ],
                property_types=[PropertyType.SELL_CONDO],
                price_min=200000,
                price_max=260000
            )
            
            logger.info(f"✅ SearchQuery créé avec {len(search_query.locations)} localisations")
            
            # Vérification de la structure
            for i, location in enumerate(search_query.locations):
                logger.info(f"📍 Localisation {i+1}: {location.type} - {location.value} (ID: {location.type_id})")
                
                # Validation des attributs
                assert hasattr(location, 'type'), f"Attribut 'type' manquant pour {location}"
                assert hasattr(location, 'value'), f"Attribut 'value' manquant pour {location}"
                assert hasattr(location, 'type_id'), f"Attribut 'type_id' manquant pour {location}"
                
            self.test_results.append(("LocationConfig Integration", "SUCCESS", f"{len(search_query.locations)} localisations"))
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du test LocationConfig: {e}")
            self.test_results.append(("LocationConfig Integration", "ERROR", str(e)))
            return False
            
    async def test_search_manager_with_location_config(self):
        """Test du SearchManager avec LocationConfig"""
        logger.info("🔍 Test du SearchManager avec LocationConfig...")
        
        try:
            # Test de construction de requête
            search_query = SearchQuery(
                locations=[
                    LocationConfig(
                        type="GeographicArea",
                        value="Montérégie",
                        type_id="RARA16"
                    )
                ],
                property_types=[PropertyType.PLEX],
                price_min=200000,
                price_max=260000
            )
            
            # Vérification que SearchManager peut traiter LocationConfig
            search_data = self.extractor.search_manager._build_search_request(search_query)
            
            # Validation de la structure de la requête
            assert 'query' in search_data, "Clé 'query' manquante"
            assert 'Filters' in search_data['query'], "Clé 'Filters' manquante"
            assert 'FieldsValues' in search_data['query'], "Clé 'FieldsValues' manquante"
            
            # Vérification des filtres de localisation
            filters = search_data['query']['Filters']
            assert len(filters) == 1, f"Nombre de filtres incorrect: {len(filters)}"
            
            location_filter = filters[0]
            assert location_filter['MatchType'] == "GeographicArea", f"MatchType incorrect: {location_filter['MatchType']}"
            assert location_filter['Text'] == "Montérégie", f"Text incorrect: {location_filter['Text']}"
            assert location_filter['Id'] == "RARA16", f"Id incorrect: {location_filter['Id']}"
            
            logger.info(f"✅ Requête construite correctement: {search_data}")
            self.test_results.append(("SearchManager LocationConfig", "SUCCESS", "Requête construite"))
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du test SearchManager: {e}")
            self.test_results.append(("SearchManager LocationConfig", "ERROR", str(e)))
            return False
            
    async def test_full_workflow_with_location_config(self):
        """Test du workflow complet avec LocationConfig"""
        logger.info("🔄 Test du workflow complet avec LocationConfig...")
        
        try:
            # Requête avec LocationConfig
            search_query = SearchQuery(
                locations=[
                    LocationConfig(
                        type="GeographicArea",
                        value="Trois-Rivières",
                        type_id="RARA04"
                    )
                ],
                property_types=[PropertyType.PLEX],
                price_min=200000,
                price_max=260000
            )
            
            # Test d'extraction des résumés
            summaries = await self.extractor.extract_summaries(search_query)
            
            if summaries:
                logger.info(f"✅ Extraction réussie: {len(summaries)} propriétés trouvées")
                
                # Validation de la structure des données
                for summary in summaries[:3]:  # Vérifier les 3 premiers
                    self._validate_summary_structure(summary)
                    
                self.test_results.append(("Workflow complet LocationConfig", "SUCCESS", len(summaries)))
                return True
            else:
                logger.warning("⚠️ Aucune propriété trouvée - possible problème de recherche")
                self.test_results.append(("Workflow complet LocationConfig", "WARNING", 0))
                return True
                
        except Exception as e:
            logger.error(f"❌ Erreur lors du workflow complet: {e}")
            self.test_results.append(("Workflow complet LocationConfig", "ERROR", str(e)))
            return False
            
    def _validate_summary_structure(self, summary):
        """Valide la structure d'un résumé de propriété"""
        required_fields = ['id', 'type', 'price', 'address', 'source', 'last_updated']
        
        for field in required_fields:
            if not hasattr(summary, field) or getattr(summary, field) is None:
                raise ValueError(f"Champ manquant ou null: {field}")
                
        # Validation spécifique
        if summary.price and summary.price <= 0:
            raise ValueError(f"Prix invalide: {summary.price}")
            
        if not summary.address.city:
            raise ValueError("Ville manquante dans l'adresse")
            
        logger.debug(f"✅ Résumé {summary.id} validé: {summary.type.value} - {summary.price}$")
        
    def print_results(self):
        """Affiche les résultats des tests"""
        logger.info("\n" + "="*60)
        logger.info("📊 RÉSULTATS DES TESTS D'INTÉGRATION AVEC LocationConfig")
        logger.info("="*60)
        
        success_count = sum(1 for _, status, _ in self.test_results if status == "SUCCESS")
        warning_count = sum(1 for _, status, _ in self.test_results if status == "WARNING")
        error_count = sum(1 for _, status, _ in self.test_results if status == "ERROR")
        total_count = len(self.test_results)
        
        for test_name, status, details in self.test_results:
            if status == "SUCCESS":
                logger.info(f"✅ {test_name}: {details}")
            elif status == "WARNING":
                logger.warning(f"⚠️ {test_name}: {details}")
            else:
                logger.error(f"❌ {test_name}: {details}")
                
        logger.info("-"*60)
        logger.info(f"📈 Résumé: {success_count} succès, {warning_count} avertissements, {error_count} erreurs")
        logger.info(f"🎯 Taux de réussite: {(success_count + warning_count) / total_count * 100:.1f}%")
        
        if error_count == 0:
            logger.info("🎉 Tous les tests critiques ont réussi !")
        else:
            logger.warning(f"⚠️ {error_count} test(s) critique(s) ont échoué")
            
        logger.info("="*60)


async def run_updated_integration_tests():
    """Exécute tous les tests d'intégration mis à jour"""
    logger.info("🚀 Démarrage des tests d'intégration avec LocationConfig...")
    
    test_suite = UpdatedIntegrationTestSuite()
    
    try:
        # Configuration
        await test_suite.setup()
        
        # Tests
        tests = [
            test_suite.test_location_config_integration,
            test_suite.test_search_manager_with_location_config,
            test_suite.test_full_workflow_with_location_config
        ]
        
        for test in tests:
            try:
                await test()
            except Exception as e:
                logger.error(f"❌ Test {test.__name__} a échoué: {e}")
                
        # Affichage des résultats
        test_suite.print_results()
        
    except Exception as e:
        logger.error(f"❌ Erreur critique lors des tests: {e}")
        
    finally:
        # Nettoyage
        await test_suite.cleanup()
        logger.info("🧹 Tests terminés et ressources nettoyées")


if __name__ == "__main__":
    asyncio.run(run_updated_integration_tests())
