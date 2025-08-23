"""
Gestionnaire de session HTTP pour Centris.ca
"""

import aiohttp
import structlog

logger = structlog.get_logger()


class CentrisSessionManager:
    """Gestionnaire de session HTTP pour Centris"""
    
    def __init__(self, centris_config):
        self.config = centris_config
        self.base_url = centris_config.base_url
        self.session = None
        self._setup_session()
    
    def _setup_session(self):
        """Configure la session HTTP avec les headers appropriés"""
        # Utiliser la configuration passée ou une valeur par défaut
        timeout = getattr(self.config, 'request_timeout', 30)
        
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-CA,fr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def close(self):
        """Ferme la session HTTP"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def get_session(self) -> aiohttp.ClientSession:
        """Retourne la session HTTP active"""
        return self.session
    
    def update_headers(self, headers: dict):
        """Met à jour les headers de la session"""
        if self.session:
            self.session.headers.update(headers)

