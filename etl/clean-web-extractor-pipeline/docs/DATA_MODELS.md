# 📊 Modèles de Données du Pipeline

## 📋 Vue d'Ensemble

Le pipeline utilise des modèles de données Pydantic pour garantir la validation, la sérialisation et la cohérence des données extraites. Tous les modèles sont définis dans `src/models/property.py`.

## 🎯 **Distinction Type vs Catégorie**

Le pipeline implémente maintenant une **distinction claire** entre :

- **`type`** : Type spécifique de la propriété (ex: "Triplex", "Duplex")
- **`category`** : Catégorie générale de la propriété (ex: "Plex")

Cette distinction est **validée automatiquement** par le `TypeCategoryValidator` pour assurer la cohérence des données.

## 🏗️ Structure des Modèles

### **Hiérarchie des Modèles**

```
📦 BaseModel (Pydantic)
├── 🏠 Property (Propriété complète)
├── 📋 PropertySummary (Résumé de propriété)
├── 🔍 SearchQuery (Requête de recherche)
├── 📍 LocationConfig (Configuration de localisation)
├── 🏘️ Address (Adresse)
├── 💰 FinancialInfo (Informations financières)
├── 🏠 PropertyFeatures (Caractéristiques)
└── 📊 PropertyStatus (Statut de propriété)
```

## 🏠 Property (Propriété Complète)

### **Description**

Modèle principal représentant une propriété immobilière complète avec tous ses détails.

### **Structure**

```python
class Property(BaseModel):
    id: str                           # Identifiant unique
    type: PropertyType               # Type de propriété
    status: PropertyStatus           # Statut (vente, location)
    address: Address                 # Adresse complète
    financial: FinancialInfo         # Informations financières
    features: PropertyFeatures       # Caractéristiques physiques
    description: Optional[str]       # Description
    images: List[str]                # URLs des images
    url: Optional[str]               # URL de la page
    source: str = "Centris"          # Source des données
    last_updated: datetime           # Dernière mise à jour
    coordinates: Optional[Coordinates] # Coordonnées GPS
```

### **Exemple d'Instance**

```python
property_data = Property(
    id="MLS123456",
    type=PropertyType.SINGLE_FAMILY_HOME,
    status=PropertyStatus.FOR_SALE,
    address=Address(
        street="123 Rue Principale",
        city="Saint-Hyacinthe",
        region="Montérégie",
        postal_code="J2S 1M1"
    ),
    financial=FinancialInfo(
        price=450000,
        municipal_tax=2500,
        school_tax=800
    ),
    features=PropertyFeatures(
        bedrooms=3,
        bathrooms=2,
        area_sqft=1500
    ),
    source="Centris",
    last_updated=datetime.now()
)
```

## 📋 PropertySummary (Résumé de Propriété)

### **Description**

Modèle léger pour les résumés de propriétés extraits des pages de résultats de recherche.

### **Structure**

```python
class PropertySummary(BaseModel):
    id: str                           # Identifiant unique
    address: Address                  # Adresse de base
    price: Optional[float]            # Prix
    type: PropertyType               # Type de propriété
    image_url: Optional[str]          # URL de l'image principale
    url: Optional[str]                # URL de la page
    source: str = "Centris"           # Source des données
    last_updated: datetime            # Dernière mise à jour
    main_image: Optional[str]         # Image principale
```

### **Exemple d'Instance**

```python
summary = PropertySummary(
    id="16871982",
    address=Address(
        street="123 Rue Principale",
        city="Saint-Hyacinthe",
        region="Montérégie"
    ),
    price=245000.0,
    type=PropertyType.PLEX,
    image_url="https://example.com/image.jpg",
    source="Centris",
    last_updated=datetime.now()
)
```

## 🔍 SearchQuery (Requête de Recherche)

### **Description**

Modèle pour définir les critères de recherche des propriétés.

### **Structure**

```python
class SearchQuery(BaseModel):
    locations: List[LocationConfig]   # Localisations de recherche
    property_types: List[PropertyType] # Types de propriétés
    price_min: Optional[float]        # Prix minimum
    price_max: Optional[float]        # Prix maximum
    bedrooms_min: Optional[int]       # Nombre minimum de chambres
    bathrooms_min: Optional[int]      # Nombre minimum de salles de bain
    area_min: Optional[float]         # Surface minimum
```

### **Exemple d'Instance**

```python
search_query = SearchQuery(
    locations=[
        LocationConfig(
            type="GeographicArea",
            value="Montérégie",
            type_id="RARA16"
        ),
        LocationConfig(
            type="CityDistrict",
            value="Vieux-Montréal",
            type_id=449
        )
    ],
    property_types=[PropertyType.PLEX, PropertyType.SELL_CONDO],
    price_min=200000,
    price_max=500000,
    bedrooms_min=2
)
```

## 📍 LocationConfig (Configuration de Localisation)

### **Description**

Modèle pour configurer les localisations de recherche avec leurs identifiants Centris.

### **Structure**

```python
class LocationConfig(BaseModel):
    type: str                         # Type de localisation
    value: str                        # Nom de la localisation
    type_id: Union[str, int]          # ID Centris (string ou int)

    class Config:
        validate_by_name = True       # Validation par nom de champ
```

### **Types de Localisation Supportés**

#### **1. GeographicArea (Régions)**

```python
LocationConfig(
    type="GeographicArea",
    value="Montérégie",
    type_id="RARA16"  # ID string
)
```

**Régions disponibles** :

- `"RARA16"` : Montérégie
- `"RARA15"` : Laurentides
- `"RARA14"` : Lanaudière
- `"RARA13"` : Laval
- `"RARA12"` : Montréal (Île)
- `"RARA11"` : Mauricie
- `"RARA10"` : Estrie

#### **2. CityDistrict (Districts de ville)**

```python
LocationConfig(
    type="CityDistrict",
    value="Vieux-Montréal",
    type_id=449  # ID numérique
)
```

**Districts populaires** :

- `730` : Chambly
- `449` : Vieux-Montréal
- `450` : Plateau-Mont-Royal
- `451` : Mile-End
- `452` : Outremont

### **Exemple d'Instance**

```python
# Recherche dans plusieurs localisations
locations = [
    LocationConfig(
        type="GeographicArea",
        value="Montérégie",
        type_id="RARA16"
    ),
    LocationConfig(
        type="CityDistrict",
        value="Vieux-Montréal",
        type_id=449
    )
]
```

## 🏘️ Address (Adresse)

### **Description**

Modèle pour représenter les adresses des propriétés.

### **Structure**

```python
class Address(BaseModel):
    street: str                       # Rue et numéro
    city: str                         # Ville
    region: str                       # Région/Province
    postal_code: Optional[str]        # Code postal
    country: str = "Canada"           # Pays (défaut: Canada)
```

### **Exemple d'Instance**

```python
address = Address(
    street="123 Rue Principale",
    city="Saint-Hyacinthe",
    region="Montérégie",
    postal_code="J2S 1M1"
)
```

## 💰 FinancialInfo (Informations Financières)

### **Description**

Modèle pour les informations financières des propriétés.

### **Structure**

```python
class FinancialInfo(BaseModel):
    price: float                      # Prix de vente/location
    municipal_tax: Optional[float]    # Taxe municipale
    school_tax: Optional[float]       # Taxe scolaire
    maintenance_fee: Optional[float]  # Frais de maintenance (condos)
    utilities: Optional[float]        # Coûts des services publics
```

### **Exemple d'Instance**

```python
financial = FinancialInfo(
    price=450000,
    municipal_tax=2500,
    school_tax=800,
    maintenance_fee=200
)
```

## 🏠 PropertyFeatures (Caractéristiques)

### **Description**

Modèle pour les caractéristiques physiques des propriétés.

### **Structure**

```python
class PropertyFeatures(BaseModel):
    bedrooms: Optional[int]           # Nombre de chambres
    bathrooms: Optional[int]          # Nombre de salles de bain
    area_sqft: Optional[float]        # Surface en pieds carrés
    area_sqm: Optional[float]         # Surface en mètres carrés
    lot_size: Optional[float]         # Taille du terrain
    year_built: Optional[int]         # Année de construction
    parking_spaces: Optional[int]     # Places de stationnement
```

### **Exemple d'Instance**

```python
features = PropertyFeatures(
    bedrooms=3,
    bathrooms=2,
    area_sqft=1500,
    area_sqm=139.35,
    lot_size=5000,
    year_built=1995,
    parking_spaces=2
)
```

## 📊 PropertyType (Types de Propriétés)

### **Description**

Enumération des types de propriétés supportés par le pipeline.

### **Valeurs Disponibles**

```python
class PropertyType(str, Enum):
    SINGLE_FAMILY_HOME = "SingleFamilyHome"    # Maison unifamiliale
    PLEX = "Plex"                              # Plex (duplex, triplex, etc.)
    SELL_CONDO = "SellCondo"                   # Condo à vendre
    RENTAL_CONDO = "RentalCondo"               # Condo à louer
    RESIDENTIAL_LOT = "ResidentialLot"         # Terrain résidentiel
    COMMERCIAL = "Commercial"                   # Commercial
    INDUSTRIAL = "Industrial"                   # Industriel
```

### **Exemple d'Utilisation**

```python
# Filtrage par type de propriété
search_query = SearchQuery(
    locations=[montreal_location],
    property_types=[PropertyType.PLEX, PropertyType.SELL_CONDO],
    price_min=200000,
    price_max=500000
)
```

## 📊 PropertyStatus (Statut des Propriétés)

### **Description**

Enumération des statuts possibles des propriétés.

### **Valeurs Disponibles**

```python
class PropertyStatus(str, Enum):
    FOR_SALE = "ForSale"              # À vendre
    FOR_RENT = "ForRent"              # À louer
    SOLD = "Sold"                     # Vendue
    RENTED = "Rented"                 # Louée
    PENDING = "Pending"               # En attente
    OFF_MARKET = "OffMarket"          # Hors marché
```

## 🔄 Sérialisation et Validation

### **Validation Pydantic**

```python
# Validation automatique lors de la création
try:
    property_data = Property(
        id="MLS123456",
        type=PropertyType.SINGLE_FAMILY_HOME,
        # ... autres champs
    )
except ValidationError as e:
    print(f"Erreur de validation: {e}")
```

### **Sérialisation JSON**

```python
# Conversion en JSON
json_data = property_data.model_dump_json(indent=2)

# Conversion en dictionnaire
dict_data = property_data.model_dump()

# Conversion depuis JSON
property_from_json = Property.model_validate_json(json_data)
```

### **Validation des Données**

```python
# Validation des coordonnées GPS
if property_data.coordinates:
    assert -90 <= property_data.coordinates.latitude <= 90
    assert -180 <= property_data.coordinates.longitude <= 180

# Validation des prix
assert property_data.financial.price > 0
assert property_data.financial.price <= 10000000  # 10M$ max
```

## 🧪 Tests des Modèles

### **Tests de Validation**

```python
# Test de validation des types
def test_property_type_validation():
    with pytest.raises(ValidationError):
        Property(
            id="test",
            type="InvalidType",  # Type invalide
            # ... autres champs requis
        )

# Test de validation des prix
def test_price_validation():
    with pytest.raises(ValidationError):
        FinancialInfo(price=-1000)  # Prix négatif
```

### **Tests de Sérialisation**

```python
# Test de conversion JSON
def test_json_serialization():
    property_data = create_test_property()
    json_str = property_data.model_dump_json()
    assert isinstance(json_str, str)

    # Reconstruction depuis JSON
    reconstructed = Property.model_validate_json(json_str)
    assert reconstructed.id == property_data.id
```

## 🔧 Extensibilité des Modèles

### **Ajout de Nouveaux Champs**

```python
class Property(BaseModel):
    # ... champs existants ...

    # Nouveaux champs
    energy_rating: Optional[str]      # Cote énergétique
    accessibility_features: List[str]  # Fonctionnalités d'accessibilité
    smart_home_features: List[str]    # Fonctionnalités intelligentes
```

### **Ajout de Nouveaux Types**

```python
class PropertyType(str, Enum):
    # ... types existants ...

    # Nouveaux types
    TOWNHOUSE = "Townhouse"           # Maison de ville
    MOBILE_HOME = "MobileHome"        # Maison mobile
    FARM = "Farm"                     # Ferme
```

### **Validation Personnalisée**

```python
from pydantic import validator

class Property(BaseModel):
    # ... champs existants ...

    @validator('financial')
    def validate_financial_info(cls, v):
        if v.price <= 0:
            raise ValueError('Le prix doit être positif')
        if v.municipal_tax and v.municipal_tax < 0:
            raise ValueError('La taxe municipale ne peut pas être négative')
        return v
```

## 📈 Performance et Optimisation

### **Modèles Légers**

- **PropertySummary** : Pour les listes et recherches
- **Property** : Pour les détails complets
- **Validation différée** : Validation à la demande

### **Mise en Cache**

```python
# Cache des modèles validés
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_property(property_id: str) -> Property:
    # Récupération depuis la base de données
    pass
```

### **Validation en Streaming**

```python
# Validation progressive des données
async def validate_property_stream(property_data: dict):
    # Validation des champs critiques d'abord
    if not property_data.get('id'):
        raise ValidationError("ID requis")

    # Validation des autres champs progressivement
    # ...
```

---

## 🎉 Conclusion

Les modèles de données Pydantic offrent une base solide et extensible pour le pipeline. Ils garantissent la qualité des données, facilitent la validation et permettent une évolution future du système.

**📊 Modèles robustes et extensibles - Données validées et cohérentes !**
