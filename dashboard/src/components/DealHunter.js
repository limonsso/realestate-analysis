import React, { useState } from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Target,
  Zap,
  Crown,
  Star,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";

const DealHunterContainer = styled(motion.div)`
  background: var(--bg-secondary);
  border-radius: 20px;
  padding: 2rem;
  border: 2px solid var(--border-gold);
  box-shadow: var(--shadow-lg), var(--shadow-gold);
  position: relative;
  overflow: hidden;
`;

const ContainerHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
`;

const Title = styled.h3`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-gold);
  margin: 0;
`;

const SearchContainer = styled.div`
  position: relative;
  width: 100%;
  max-width: 400px;
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all var(--transition-normal);

  &:focus {
    outline: none;
    border-color: var(--border-gold);
    box-shadow: var(--shadow-gold);
  }

  &::placeholder {
    color: var(--text-muted);
  }
`;

const SearchIcon = styled.div`
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
`;

const DealsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
`;

const DealCard = styled(motion.div)`
  background: var(--bg-tertiary);
  border-radius: 16px;
  padding: 1.5rem;
  border: 2px solid
    ${(props) => {
      switch (props.dealType) {
        case "DEAL DU SIÈCLE":
          return "var(--gold-primary)";
        case "OPPORTUNITÉ HOT":
          return "var(--danger-color)";
        case "DIAMANT BRUT":
          return "var(--emerald-primary)";
        case "CASH MACHINE":
          return "var(--warning-color)";
        default:
          return "var(--border-color)";
      }
    }};
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: ${(props) => {
      switch (props.dealType) {
        case "DEAL DU SIÈCLE":
          return "var(--gradient-gold)";
        case "OPPORTUNITÉ HOT":
          return "var(--danger-color)";
        case "DIAMANT BRUT":
          return "var(--gradient-emerald)";
        case "CASH MACHINE":
          return "var(--warning-color)";
        default:
          return "var(--border-color)";
      }
    }};
  }
`;

const DealHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const DealType = styled.span`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: ${(props) => {
    switch (props.dealType) {
      case "DEAL DU SIÈCLE":
        return "rgba(251, 191, 36, 0.2)";
      case "OPPORTUNITÉ HOT":
        return "rgba(239, 68, 68, 0.2)";
      case "DIAMANT BRUT":
        return "rgba(16, 185, 129, 0.2)";
      case "CASH MACHINE":
        return "rgba(245, 158, 11, 0.2)";
      default:
        return "rgba(100, 116, 139, 0.2)";
    }
  }};
  color: ${(props) => {
    switch (props.dealType) {
      case "DEAL DU SIÈCLE":
        return "var(--gold-primary)";
      case "OPPORTUNITÉ HOT":
        return "var(--danger-color)";
      case "DIAMANT BRUT":
        return "var(--emerald-primary)";
      case "CASH MACHINE":
        return "var(--warning-color)";
      default:
        return "var(--text-muted)";
    }
  }};
  border: 1px solid
    ${(props) => {
      switch (props.dealType) {
        case "DEAL DU SIÈCLE":
          return "var(--gold-primary)";
        case "OPPORTUNITÉ HOT":
          return "var(--danger-color)";
        case "DIAMANT BRUT":
          return "var(--emerald-primary)";
        case "CASH MACHINE":
          return "var(--warning-color)";
        default:
          return "var(--border-color)";
      }
    }};
`;

const DealScore = styled.div`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-gold);
`;

const DealAddress = styled.h4`
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
`;

const DealMetrics = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1rem 0;
`;

const Metric = styled.div`
  text-align: center;
  padding: 0.75rem;
  background: var(--bg-elevated);
  border-radius: 8px;
`;

const MetricValue = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-gold);
  margin-bottom: 0.25rem;
`;

const MetricLabel = styled.div`
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const DealActions = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const ActionButton = styled.button`
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: var(--gradient-gold);
  color: var(--bg-primary);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-gold);
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 3rem 2rem;
  color: var(--text-muted);
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const DealHunter = ({ properties, onPropertySelect }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDealType, setSelectedDealType] = useState("all");

  // Filtrer les propriétés selon les critères
  const filteredDeals = properties.filter((property) => {
    const matchesSearch =
      property.address?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      property.city?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesType =
      selectedDealType === "all" || property.dealType === selectedDealType;

    return matchesSearch && matchesType;
  });

  // Trier par score d'opportunité
  const sortedDeals = filteredDeals.sort(
    (a, b) => (b.opportunityScore || 0) - (a.opportunityScore || 0)
  );

  // Prendre les top 6
  const topDeals = sortedDeals.slice(0, 6);

  const getDealIcon = (dealType) => {
    switch (dealType) {
      case "DEAL DU SIÈCLE":
        return <Crown size={16} />;
      case "OPPORTUNITÉ HOT":
        return <Zap size={16} />;
      case "DIAMANT BRUT":
        return <Star size={16} />;
      case "CASH MACHINE":
        return <TrendingUp size={16} />;
      default:
        return <Target size={16} />;
    }
  };

  const handleDealSelect = (property) => {
    onPropertySelect(property);
  };

  return (
    <DealHunterContainer
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <ContainerHeader>
        <Title>
          <Target size={24} />
          Deal Hunter Intelligent
        </Title>
      </ContainerHeader>

      <SearchContainer>
        <SearchIcon>
          <Search size={20} />
        </SearchIcon>
        <SearchInput
          type="text"
          placeholder="Rechercher une propriété ou une ville..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </SearchContainer>

      {topDeals.length > 0 ? (
        <DealsGrid>
          <AnimatePresence>
            {topDeals.map((property, index) => (
              <DealCard
                key={property.id}
                dealType={property.dealType}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                onClick={() => handleDealSelect(property)}
              >
                <DealHeader>
                  <DealType dealType={property.dealType}>
                    {getDealIcon(property.dealType)}
                    {property.dealType}
                  </DealType>
                  <DealScore>
                    <Star size={20} />
                    {property.opportunityScore?.toFixed(1)}
                  </DealScore>
                </DealHeader>

                <DealAddress>{property.address}</DealAddress>
                <div
                  style={{
                    color: "var(--text-secondary)",
                    marginBottom: "1rem",
                  }}
                >
                  {property.city} • {property.type}
                </div>

                <DealMetrics>
                  <Metric>
                    <MetricValue>
                      ${property.price?.toLocaleString()}
                    </MetricValue>
                    <MetricLabel>Prix</MetricLabel>
                  </Metric>
                  <Metric>
                    <MetricValue>{property.netYield?.toFixed(2)}%</MetricValue>
                    <MetricLabel>ROI Net</MetricLabel>
                  </Metric>
                  <Metric>
                    <MetricValue>
                      ${property.monthlyCashFlow?.toFixed(0)}
                    </MetricValue>
                    <MetricLabel>Cash-Flow</MetricLabel>
                  </Metric>
                  <Metric>
                    <MetricValue>{property.buildingAge} ans</MetricValue>
                    <MetricLabel>Âge</MetricLabel>
                  </Metric>
                </DealMetrics>

                <DealActions>
                  <ActionButton
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDealSelect(property);
                    }}
                  >
                    Analyser
                  </ActionButton>
                </DealActions>
              </DealCard>
            ))}
          </AnimatePresence>
        </DealsGrid>
      ) : (
        <EmptyState>
          <EmptyIcon>
            <Target size={64} />
          </EmptyIcon>
          <h4>Aucune opportunité trouvée</h4>
          <p>Essayez de modifier vos critères de recherche</p>
        </EmptyState>
      )}
    </DealHunterContainer>
  );
};

export default DealHunter;

