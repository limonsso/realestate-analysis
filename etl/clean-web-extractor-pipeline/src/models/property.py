"""
Modèles de données pour les propriétés immobilières
Utilise Pydantic pour la validation et la sérialisation
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union, TYPE_CHECKING
from pydantic import BaseModel, Field, validator, computed_field
from enum import Enum

from config.settings import LocationConfig


class PropertyType(str, Enum):
    """Types de propriétés supportés"""
    PLEX = "Plex"
    SINGLE_FAMILY_HOME = "SingleFamilyHome"
    SELL_CONDO = "SellCondo"
    RESIDENTIAL_LOT = "ResidentialLot"


class PropertyStatus(str, Enum):
    """Statuts des propriétés"""
    FOR_SALE = "for_sale"
    SOLD = "sold"
    PENDING = "pending"
    OFF_MARKET = "off_market"


class Address(BaseModel):
    """Adresse d'une propriété"""
    street: Optional[str] = Field(None, description="Rue et numéro")
    city: Optional[str] = Field(None, description="Ville")
    region: Optional[str] = Field(None, description="Région/Province")
    postal_code: Optional[str] = Field(None, description="Code postal")
    country: str = Field("Canada", description="Pays")
    
    @computed_field
    @property
    def full_address(self) -> str:
        """Adresse complète formatée"""
        parts = [self.street, self.city, self.region, self.postal_code]
        return ", ".join(filter(None, parts))


class Location(BaseModel):
    """Coordonnées géographiques"""
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude")
    
    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v):
        if v is not None and not isinstance(v, (int, float)):
            raise ValueError("Les coordonnées doivent être des nombres")
        return v


class FinancialInfo(BaseModel):
    """Informations financières"""
    price: Optional[float] = Field(None, ge=0, description="Prix de vente")
    municipal_evaluation_land: Optional[float] = Field(None, ge=0, description="Évaluation municipale du terrain")
    municipal_evaluation_building: Optional[float] = Field(None, ge=0, description="Évaluation municipale du bâtiment")
    municipal_evaluation_total: Optional[float] = Field(None, ge=0, description="Évaluation municipale totale")
    municipal_evaluation_year: Optional[int] = Field(None, ge=1900, le=2100, description="Année d'évaluation")
    municipal_tax: Optional[float] = Field(None, ge=0, description="Taxe municipale")
    school_tax: Optional[float] = Field(None, ge=0, description="Taxe scolaire")
    potential_gross_revenue: Optional[float] = Field(None, ge=0, description="Revenus bruts potentiels")
    
    @computed_field
    @property
    def total_taxes(self) -> Optional[float]:
        """Total des taxes"""
        if self.municipal_tax is not None or self.school_tax is not None:
            return (self.municipal_tax or 0) + (self.school_tax or 0)
        return None


class PropertyFeatures(BaseModel):
    """Caractéristiques physiques de la propriété"""
    rooms: Optional[int] = Field(None, ge=0, description="Nombre total de pièces")
    bedrooms: Optional[int] = Field(None, ge=0, description="Nombre de chambres")
    bedrooms_basement: Optional[int] = Field(None, ge=0, description="Chambres au sous-sol")
    bathrooms: Optional[int] = Field(None, ge=0, description="Nombre de salles de bain")
    
    @computed_field
    @property
    def total_bedrooms(self) -> Optional[int]:
        """Total des chambres (rez-de-chaussée + sous-sol)"""
        if self.bedrooms is not None or self.bedrooms_basement is not None:
            return (self.bedrooms or 0) + (self.bedrooms_basement or 0)
        return None


class PropertyDimensions(BaseModel):
    """Dimensions et surfaces"""
    lot_size: Optional[float] = Field(None, ge=0, description="Taille du terrain (pieds carrés)")
    living_area: Optional[float] = Field(None, ge=0, description="Surface habitable (pieds carrés)")
    year_built: Optional[int] = Field(None, ge=1600, le=2100, description="Année de construction")
    
    @computed_field
    @property
    def lot_size_acres(self) -> Optional[float]:
        """Taille du terrain en acres"""
        if self.lot_size:
            return self.lot_size / 43560  # 1 acre = 43,560 pieds carrés
        return None


class PropertyMedia(BaseModel):
    """Médias associés à la propriété"""
    main_image: Optional[str] = Field(None, description="Image principale")
    images: List[str] = Field(default_factory=list, description="Liste des images")
    virtual_tour_url: Optional[str] = Field(None, description="URL de la visite virtuelle")
    
    @computed_field
    @property
    def image_count(self) -> int:
        """Nombre total d'images"""
        count = len(self.images)
        if self.main_image:
            count += 1
        return count


class PropertyDescription(BaseModel):
    """Descriptions de la propriété"""
    short_description: Optional[str] = Field(None, description="Description courte")
    long_description: Optional[str] = Field(None, description="Description détaillée")
    features: List[str] = Field(default_factory=list, description="Liste des caractéristiques")
    amenities: List[str] = Field(default_factory=list, description="Liste des commodités")


class PropertyMetadata(BaseModel):
    """Métadonnées de la propriété"""
    source: str = Field(..., description="Source des données (ex: Centris, DuProprio)")
    source_id: Optional[str] = Field(None, description="ID dans la source originale")
    url: Optional[str] = Field(None, description="URL de la propriété sur la source")
    last_updated: datetime = Field(default_factory=datetime.now, description="Dernière mise à jour")
    extraction_date: datetime = Field(default_factory=datetime.now, description="Date d'extraction")
    
    @validator('last_updated', 'extraction_date', pre=True)
    def parse_datetime(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return datetime.now()
        return v


class Property(BaseModel):
    """Modèle principal d'une propriété immobilière"""
    # Identifiant unique
    id: Optional[str] = Field(None, description="ID unique de la propriété")
    
    # Informations de base
    type: str = Field(..., description="Type spécifique de la propriété (ex: Triplex, Duplex)")
    category: PropertyType = Field(..., description="Catégorie générale de la propriété (ex: Plex)")
    status: PropertyStatus = Field(PropertyStatus.FOR_SALE, description="Statut de la propriété")
    
    # Adresse et localisation
    address: Address = Field(..., description="Adresse de la propriété")
    location: Optional[Location] = Field(None, description="Coordonnées géographiques")
    
    # Informations financières
    financial: FinancialInfo = Field(..., description="Informations financières")
    
    # Caractéristiques physiques
    features: PropertyFeatures = Field(..., description="Caractéristiques physiques")
    dimensions: PropertyDimensions = Field(..., description="Dimensions et surfaces")
    
    # Médias et descriptions
    media: PropertyMedia = Field(..., description="Médias de la propriété")
    description: PropertyDescription = Field(..., description="Descriptions de la propriété")
    
    # Informations détaillées supplémentaires
    property_usage: Optional[str] = Field(None, description="Utilisation de la propriété (ex: Résidentielle)")
    building_style: Optional[str] = Field(None, description="Style de bâtiment (ex: Jumelé)")
    parking_info: Optional[str] = Field(None, description="Informations de stationnement (ex: Garage (1))")
    # units_info supprimé car redondant avec residential_units_detail et units_count
    # main_unit_info supprimé car redondant avec main_unit_detail
    move_in_date: Optional[str] = Field(None, description="Date d'emménagement (ex: Selon les baux)")
    
    # Nouvelles informations numériques extraites
    construction_year: Optional[int] = Field(None, ge=1600, le=2100, description="Année de construction")
    terrain_area_sqft: Optional[int] = Field(None, ge=0, description="Superficie du terrain en pieds carrés")
    parking_count: Optional[int] = Field(None, ge=0, description="Nombre total de stationnements")
    units_count: Optional[int] = Field(None, ge=0, description="Nombre total d'unités")
    walk_score: Optional[int] = Field(None, ge=0, le=100, description="Walk Score (0-100)")
    
    # Informations détaillées des unités
    residential_units_detail: Optional[str] = Field(None, description="Détail des unités résidentielles (ex: 1 x 4 ½, 2 x 5 ½)")
    main_unit_detail: Optional[str] = Field(None, description="Détail de l'unité principale (ex: 5 pièces, 3 chambres, 1 salle de bain)")
    
    # Nouvelles informations numériques détaillées des unités
    # Champs dynamiques pour les unités (ex: units_2_half_count, units_3_half_count, etc.)
    units_2_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 2 ½")
    units_3_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 3 ½")
    units_4_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 4 ½")
    units_5_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 5 ½")
    units_6_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 6 ½")
    units_7_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 7 ½")
    units_8_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 8 ½")
    units_9_half_count: Optional[int] = Field(None, ge=0, description="Nombre d'unités 9 ½")
    
    # Informations de l'unité principale
    main_unit_rooms: Optional[int] = Field(None, ge=0, description="Nombre de pièces de l'unité principale")
    main_unit_bedrooms: Optional[int] = Field(None, ge=0, description="Nombre de chambres de l'unité principale")
    main_unit_bathrooms: Optional[int] = Field(None, ge=0, description="Nombre de salles de bain de l'unité principale")
    
    # Champs dynamiques supplémentaires
    # units_breakdown supprimé car redondant avec units_X_half_count
    
    # Métadonnées
    metadata: PropertyMetadata = Field(..., description="Métadonnées de la propriété")
    
    # Champs calculés
    @computed_field
    @property
    def price_per_sqft(self) -> Optional[float]:
        """Prix par pied carré"""
        if self.financial.price and self.dimensions.living_area:
            return self.financial.price / self.dimensions.living_area
        return None
    
    @computed_field
    @property
    def is_new_construction(self) -> bool:
        """Indique si c'est une construction récente (moins de 5 ans)"""
        if self.dimensions.year_built:
            current_year = datetime.now().year
            return current_year - self.dimensions.year_built <= 5
        return False
    
    @computed_field
    @property
    def is_luxury(self) -> bool:
        """Indique si c'est une propriété de luxe (prix > 1M$ ou > 500$ par pied carré)"""
        if self.financial.price:
            return (self.financial.price > 1000000 or 
                   (self.price_per_sqft and self.price_per_sqft > 500))
        return False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True


class PropertySummary(BaseModel):
    """Résumé d'une propriété pour la recherche et la comparaison"""
    id: str = Field(..., description="ID unique de la propriété")
    type: PropertyType = Field(..., description="Type de propriété")
    price: Optional[float] = Field(None, description="Prix de vente")
    address: Address = Field(..., description="Adresse de la propriété")
    main_image: Optional[str] = Field(None, description="Image principale")
    url: Optional[str] = Field(None, description="URL de la propriété")
    source: str = Field(..., description="Source des données")
    last_updated: datetime = Field(default_factory=datetime.now, description="Dernière mise à jour")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True


class SearchQuery(BaseModel):
    """Paramètres de recherche de propriétés"""
    locations: List['LocationConfig'] = Field(..., description="Localisations à rechercher")
    property_types: List[PropertyType] = Field(..., description="Types de propriétés")
    price_min: Optional[float] = Field(None, ge=0, description="Prix minimum")
    price_max: Optional[float] = Field(None, ge=0, description="Prix maximum")
    bedrooms_min: Optional[int] = Field(None, ge=0, description="Nombre minimum de chambres")
    bathrooms_min: Optional[int] = Field(None, ge=0, description="Nombre minimum de salles de bain")
    living_area_min: Optional[float] = Field(None, ge=0, description="Surface habitable minimum")
    year_built_min: Optional[int] = Field(None, ge=1900, description="Année de construction minimum")
    
    @validator('price_max')
    def validate_price_range(cls, v, values):
        if v is not None and 'price_min' in values and values['price_min'] is not None:
            if v <= values['price_min']:
                raise ValueError("Le prix maximum doit être supérieur au prix minimum")
        return v
