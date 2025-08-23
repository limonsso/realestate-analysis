#!/usr/bin/env python3
import sys, asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from src.services.database_service import DatabaseService
from config.settings import DatabaseConfig

async def main():
    print("🔍 Vérification de la nouvelle collection")
    db_config = DatabaseConfig(server_url="mongodb://localhost:27017", connection_string="mongodb://localhost:27017", database_name="real_estate_analytics")
    db_service = DatabaseService(db_config)
    await db_service.connect()
    db_service.set_collection_names(properties_collection="chambly_plex_test_20250822_160419")
    property_data = await db_service.get_property_by_id("21002530")
    if property_data:
        print(f"✅ Propriété trouvée: {property_data.residential_units_detail}")
    await db_service.close()
asyncio.run(main())
