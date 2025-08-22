#!/usr/bin/env python3
"""
Script de débogage pour identifier le problème dans SearchManager
"""

import asyncio
import structlog
from src.extractors.centris.search_manager import CentrisSearchManager
from src.extractors.centris.session_manager import CentrisSessionManager
from src.models.property import SearchQuery, PropertyType
from config.settings import config

# Configuration du logging
structlog.configure(processors=[structlog.processors.TimeStamper(fmt="iso"), structlog.processors.add_log_level, structlog.dev.ConsoleRenderer()])
logger = structlog.get_logger(__name__)


async def debug_search_manager():
    """Débogue le SearchManager étape par étape"""
    logger.info("🔍 Démarrage du débogage du SearchManager...")
    
    try:
        # 1. Initialisation du SessionManager
        logger.info("1️⃣ Initialisation du SessionManager...")
        session_manager = CentrisSessionManager(config.centris)
        logger.info("✅ SessionManager initialisé")
        
        # 2. Initialisation du SearchManager
        logger.info("2️⃣ Initialisation du SearchManager...")
        search_manager = CentrisSearchManager(session_manager)
        logger.info("✅ SearchManager initialisé")
        
        # 3. Test de construction de requête
        logger.info("3️⃣ Test de construction de requête...")
        search_query = SearchQuery(
            locations=["Montréal"],
            property_types=[PropertyType.SELL_CONDO],
            price_min=200000,
            price_max=500000
        )
        
        search_data = search_manager._build_search_request(search_query)
        logger.info(f"✅ Requête construite: {search_data}")
        
        # 4. Test de l'API UpdateQuery
        logger.info("4️⃣ Test de l'API UpdateQuery...")
        try:
            async with session_manager.session.post(
                f"{session_manager.base_url}/api/property/UpdateQuery",
                json=search_data
            ) as response:
                logger.info(f"📡 Statut UpdateQuery: {response.status}")
                logger.info(f"📡 Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    response_text = await response.text()
                    logger.info(f"📄 Réponse UpdateQuery (premiers 500 chars): {response_text[:500]}")
                    
                    # Essayer de parser comme JSON
                    try:
                        response_json = await response.json()
                        logger.info(f"✅ Réponse JSON: {response_json}")
                    except Exception as json_error:
                        logger.warning(f"⚠️ Impossible de parser comme JSON: {json_error}")
                        logger.info(f"📄 Contenu complet: {response_text}")
                else:
                    logger.error(f"❌ Échec UpdateQuery: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'appel UpdateQuery: {e}")
            
        # 5. Test de l'API UserContext/Lock
        logger.info("5️⃣ Test de l'API UserContext/Lock...")
        try:
            async with session_manager.session.post(
                f"{session_manager.base_url}/UserContext/Lock",
                json={'uc': 0}
            ) as lock_response:
                logger.info(f"📡 Statut Lock: {lock_response.status}")
                logger.info(f"📡 Headers: {dict(lock_response.headers)}")
                
                if lock_response.status == 200:
                    response_text = await lock_response.text()
                    logger.info(f"📄 Réponse Lock (premiers 500 chars): {response_text[:500]}")
                    
                    # Essayer de parser comme JSON
                    try:
                        response_json = await lock_response.json()
                        logger.info(f"✅ Réponse JSON: {response_json}")
                        
                        # Tester l'accès à 'uck'
                        uck = response_json.get('uck', '')
                        logger.info(f"🔑 UCK extrait: '{uck}'")
                        
                    except Exception as json_error:
                        logger.warning(f"⚠️ Impossible de parser comme JSON: {json_error}")
                        logger.info(f"📄 Contenu complet: {response_text}")
                else:
                    logger.error(f"❌ Échec Lock: {lock_response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'appel Lock: {e}")
            
    except Exception as e:
        logger.error(f"❌ Erreur critique: {e}")
        
    finally:
        # Nettoyage
        if 'session_manager' in locals():
            await session_manager.close()
            logger.info("🔌 SessionManager fermé")


if __name__ == "__main__":
    asyncio.run(debug_search_manager())
