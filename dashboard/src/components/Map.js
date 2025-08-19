import React, { useEffect, useRef } from "react";
import styled from "styled-components";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  CircleMarker,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { MapPin, TrendingUp, DollarSign, Home } from "lucide-react";

// Fix pour les icônes Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

const MapContainerStyled = styled.div`
  height: 600px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
`;

const MapHeader = styled.div`
  background: var(--bg-primary);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const MapTitle = styled.h3`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
`;

const MapLegend = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
`;

const LegendColor = styled.div`
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 1px var(--border-color);
`;

const PopupContent = styled.div`
  min-width: 250px;
  font-family: inherit;
`;

const PopupTitle = styled.h4`
  margin: 0 0 0.5rem 0;
  color: var(--primary-color);
  font-size: 1rem;
  font-weight: 600;
`;

const PopupRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
`;

const PopupLabel = styled.span`
  color: var(--text-secondary);
  font-weight: 500;
`;

const PopupValue = styled.span`
  color: var(--text-primary);
  font-weight: 600;
`;

const PopupMetrics = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color);
`;

const MetricCard = styled.div`
  text-align: center;
  padding: 0.5rem;
  background: var(--bg-secondary);
  border-radius: 6px;
`;

const MetricValue = styled.div`
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--primary-color);
`;

const MetricLabel = styled.div`
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const Map = ({ properties }) => {
  const mapRef = useRef();

  // Calculer le centre de la carte basé sur les propriétés
  const getMapCenter = () => {
    if (!properties || properties.length === 0) {
      return [46.8139, -71.208]; // Québec par défaut
    }

    const validCoords = properties.filter((p) => p.latitude && p.longitude);
    if (validCoords.length === 0) {
      return [46.8139, -71.208];
    }

    const avgLat =
      validCoords.reduce((sum, p) => sum + p.latitude, 0) / validCoords.length;
    const avgLng =
      validCoords.reduce((sum, p) => sum + p.longitude, 0) / validCoords.length;

    return [avgLat, avgLng];
  };

  // Obtenir la couleur du marqueur basée sur le rendement
  const getMarkerColor = (yieldValue) => {
    if (yieldValue >= 8) return "#10b981"; // Vert - Excellent
    if (yieldValue >= 6) return "#3b82f6"; // Bleu - Bon
    if (yieldValue >= 4) return "#f59e0b"; // Orange - Moyen
    return "#ef4444"; // Rouge - Faible
  };

  // Obtenir la taille du marqueur basée sur le prix
  const getMarkerSize = (price) => {
    if (price >= 500000) return 12;
    if (price >= 300000) return 10;
    if (price >= 150000) return 8;
    return 6;
  };

  useEffect(() => {
    if (mapRef.current && properties.length > 0) {
      // Ajuster la vue pour inclure tous les marqueurs
      const validCoords = properties.filter((p) => p.latitude && p.longitude);
      if (validCoords.length > 0) {
        const bounds = L.latLngBounds(
          validCoords.map((p) => [p.latitude, p.longitude])
        );
        mapRef.current.fitBounds(bounds, { padding: [20, 20] });
      }
    }
  }, [properties]);

  if (!properties || properties.length === 0) {
    return (
      <MapContainerStyled>
        <MapHeader>
          <MapTitle>
            <MapPin size={20} />
            Carte des Propriétés
          </MapTitle>
        </MapHeader>
        <div
          style={{
            height: "500px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "#1f2937",
            color: "#9ca3af",
          }}
        >
          Aucune propriété à afficher sur la carte
        </div>
      </MapContainerStyled>
    );
  }

  return (
    <MapContainerStyled>
      <MapHeader>
        <MapTitle>
          <MapPin size={20} />
          Carte des Propriétés ({properties.length})
        </MapTitle>
        <MapLegend>
          <LegendItem>
            <LegendColor style={{ background: "#10b981" }} />
            Rendement ≥ 8%
          </LegendItem>
          <LegendItem>
            <LegendColor style={{ background: "#3b82f6" }} />
            Rendement 6-8%
          </LegendItem>
          <LegendItem>
            <LegendColor style={{ background: "#f59e0b" }} />
            Rendement 4-6%
          </LegendItem>
          <LegendItem>
            <LegendColor style={{ background: "#ef4444" }} />
            Rendement &lt; 4%
          </LegendItem>
        </MapLegend>
      </MapHeader>

      <MapContainer
        ref={mapRef}
        center={getMapCenter()}
        zoom={10}
        style={{ height: "500px", width: "100%" }}
        zoomControl={true}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {properties.map((property, index) => {
          if (!property.latitude || !property.longitude) return null;

          const yieldValue = property.netYield || 0;
          const color = getMarkerColor(yieldValue);
          const size = getMarkerSize(property.price);

          return (
            <CircleMarker
              key={`${property.id || index}-${property.latitude}-${
                property.longitude
              }`}
              center={[property.latitude, property.longitude]}
              radius={size}
              fillColor={color}
              color={color}
              weight={2}
              opacity={0.8}
              fillOpacity={0.6}
            >
              <Popup>
                <PopupContent>
                  <PopupTitle>
                    {property.address || "Adresse non disponible"}
                  </PopupTitle>

                  <PopupRow>
                    <PopupLabel>Prix:</PopupLabel>
                    <PopupValue>
                      ${property.price?.toLocaleString() || "N/A"}
                    </PopupValue>
                  </PopupRow>

                  <PopupRow>
                    <PopupLabel>Type:</PopupLabel>
                    <PopupValue>{property.type || "N/A"}</PopupValue>
                  </PopupRow>

                  <PopupRow>
                    <PopupLabel>Ville:</PopupLabel>
                    <PopupValue>{property.city || "N/A"}</PopupValue>
                  </PopupRow>

                  <PopupRow>
                    <PopupLabel>Surface:</PopupLabel>
                    <PopupValue>{property.surface || "N/A"} pi²</PopupValue>
                  </PopupRow>

                  <PopupMetrics>
                    <MetricCard>
                      <MetricValue>{yieldValue.toFixed(2)}%</MetricValue>
                      <MetricLabel>Rendement</MetricLabel>
                    </MetricCard>
                    <MetricCard>
                      <MetricValue>
                        ${property.monthlyCashFlow?.toFixed(0) || "N/A"}
                      </MetricValue>
                      <MetricLabel>Cash-Flow</MetricLabel>
                    </MetricCard>
                  </PopupMetrics>

                  <div
                    style={{
                      marginTop: "0.75rem",
                      padding: "0.5rem",
                      background: color,
                      color: "white",
                      borderRadius: "6px",
                      textAlign: "center",
                      fontSize: "0.75rem",
                      fontWeight: "600",
                    }}
                  >
                    Score: {(property.opportunityScore || 0).toFixed(1)}/10
                  </div>
                </PopupContent>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </MapContainerStyled>
  );
};

export default Map;
