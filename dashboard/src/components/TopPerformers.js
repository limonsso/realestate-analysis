import React from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import {
  Trophy,
  Medal,
  Crown,
  Star,
  TrendingUp,
  MapPin,
  DollarSign,
  Target,
} from "lucide-react";

const TopPerformersContainer = styled(motion.div)`
  background: var(--bg-secondary);
  border-radius: 20px;
  padding: 2rem;
  border: 2px solid var(--border-emerald);
  box-shadow: var(--shadow-lg), var(--shadow-emerald);
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
  color: var(--emerald-primary);
  margin: 0;
`;

const Leaderboard = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const LeaderboardItem = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--bg-tertiary);
  border-radius: 16px;
  border: 2px solid transparent;
  transition: all var(--transition-normal);
  cursor: pointer;
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateX(8px);
    border-color: var(--border-gold);
    box-shadow: var(--shadow-md);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 4px;
    background: ${(props) => {
      switch (props.rank) {
        case 1:
          return "var(--gradient-gold)";
        case 2:
          return "var(--gradient-emerald)";
        case 3:
          return "var(--warning-color)";
        default:
          return "var(--border-color)";
      }
    }};
  }
`;

const RankBadge = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-weight: 800;
  font-size: 1.25rem;
  color: white;
  background: ${(props) => {
    switch (props.rank) {
      case 1:
        return "var(--gradient-gold)";
      case 2:
        return "var(--gradient-emerald)";
      case 3:
        return "var(--warning-color)";
      default:
        return "var(--bg-elevated)";
    }
  }};
  border: 2px solid
    ${(props) => {
      switch (props.rank) {
        case 1:
          return "var(--gold-primary)";
        case 2:
          return "var(--emerald-primary)";
        case 3:
          return "var(--warning-color)";
        default:
          return "var(--border-color)";
      }
    }};
  box-shadow: ${(props) => {
    switch (props.rank) {
      case 1:
        return "var(--shadow-gold)";
      case 2:
        return "var(--shadow-emerald)";
      default:
        "none";
    }
  }};
`;

const RankIcon = styled.div`
  font-size: 1.5rem;
  color: white;
`;

const PropertyInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const PropertyName = styled.h4`
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const PropertyLocation = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
`;

const PropertyType = styled.span`
  background: var(--bg-elevated);
  color: var(--text-muted);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
`;

const PerformanceMetrics = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  min-width: 120px;
`;

const Score = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-gold);
`;

const ROI = styled.div`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--emerald-primary);
`;

const Price = styled.div`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
`;

const DealTypeBadge = styled.span`
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
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

const TopPerformers = ({ properties }) => {
  // Trier par score d'opportunité et prendre les top 10
  const topProperties = properties
    .filter((p) => p.opportunityScore > 0)
    .sort((a, b) => (b.opportunityScore || 0) - (a.opportunityScore || 0))
    .slice(0, 10);

  const getRankIcon = (rank) => {
    switch (rank) {
      case 1:
        return <Crown size={24} />;
      case 2:
        return <Medal size={24} />;
      case 3:
        return <Trophy size={24} />;
      default:
        return null;
    }
  };

  const getRankDisplay = (rank) => {
    switch (rank) {
      case 1:
        return "🥇";
      case 2:
        return "🥈";
      case 3:
        return "🥉";
      default:
        return rank;
    }
  };

  if (topProperties.length === 0) {
    return (
      <TopPerformersContainer
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <ContainerHeader>
          <Title>
            <Trophy size={24} />
            Top Performers
          </Title>
        </ContainerHeader>
        <EmptyState>
          <EmptyIcon>
            <Trophy size={64} />
          </EmptyIcon>
          <h4>Aucune performance à afficher</h4>
          <p>Les propriétés apparaîtront ici une fois analysées</p>
        </EmptyState>
      </TopPerformersContainer>
    );
  }

  return (
    <TopPerformersContainer
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <ContainerHeader>
        <Title>
          <Trophy size={24} />
          Top Performers
        </Title>
      </ContainerHeader>

      <Leaderboard>
        <AnimatePresence>
          {topProperties.map((property, index) => (
            <LeaderboardItem
              key={property.id}
              rank={index + 1}
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 30 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
            >
              <RankBadge rank={index + 1}>
                {getRankIcon(index + 1) || getRankDisplay(index + 1)}
              </RankBadge>

              <PropertyInfo>
                <PropertyName>{property.address}</PropertyName>
                <PropertyLocation>
                  <MapPin size={16} />
                  {property.city}
                </PropertyLocation>
                <PropertyType>{property.type}</PropertyType>
              </PropertyInfo>

              <PerformanceMetrics>
                <Score>
                  <Star size={20} />
                  {property.opportunityScore?.toFixed(1)}
                </Score>
                <ROI>
                  <TrendingUp size={16} />
                  {property.netYield?.toFixed(2)}%
                </ROI>
                <Price>
                  <DollarSign size={14} />
                  {property.price?.toLocaleString()}
                </Price>
              </PerformanceMetrics>

              <DealTypeBadge dealType={property.dealType}>
                {property.dealType}
              </DealTypeBadge>
            </LeaderboardItem>
          ))}
        </AnimatePresence>
      </Leaderboard>
    </TopPerformersContainer>
  );
};

export default TopPerformers;

