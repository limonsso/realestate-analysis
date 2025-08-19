import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import {
  Crown,
  TrendingUp,
  Target,
  Zap,
  Star,
  Trophy,
  Award,
} from "lucide-react";

const HeroContainer = styled(motion.div)`
  background: linear-gradient(
    135deg,
    rgba(15, 23, 42, 0.95) 0%,
    rgba(30, 41, 59, 0.95) 100%
  );
  border-radius: 24px;
  padding: 3rem 2rem;
  margin: 2rem 0;
  border: 2px solid var(--border-gold);
  box-shadow: var(--shadow-xl), var(--shadow-gold);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
`;

const HeroContent = styled.div`
  position: relative;
  z-index: 2;
  text-align: center;
`;

const HeroTitle = styled(motion.h1)`
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: var(--gradient-gold);
  -webkit-background-clip: text;
  -webkit-background-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(251, 191, 36, 0.3);
`;

const HeroSubtitle = styled(motion.p)`
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const PortfolioStats = styled(motion.div)`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
`;

const StatCard = styled(motion.div)`
  background: rgba(30, 41, 59, 0.8);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-8px);
    border-color: var(--border-gold);
    box-shadow: var(--shadow-lg), var(--shadow-gold);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-gold);
  }
`;

const StatIcon = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 2rem;
  background: var(--gradient-gold);
  color: var(--bg-primary);
  box-shadow: var(--shadow-gold);
`;

const StatValue = styled.div`
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--text-gold);
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const StatTrend = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: rgba(16, 185, 129, 0.2);
  color: var(--emerald-primary);
  border: 1px solid var(--emerald-primary);
`;

const UserLevelBadge = styled(motion.div)`
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--gradient-gold);
  color: var(--bg-primary);
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: var(--shadow-gold);
  margin-top: 2rem;
`;

const LevelIcon = styled.div`
  font-size: 1.5rem;
`;

const HotDealsAlert = styled(motion.div)`
  background: linear-gradient(
    135deg,
    rgba(239, 68, 68, 0.2) 0%,
    rgba(220, 38, 38, 0.2) 100%
  );
  border: 2px solid var(--danger-color);
  border-radius: 16px;
  padding: 1.5rem;
  margin-top: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: var(--danger-color);
  font-weight: 600;
  font-size: 1.125rem;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
`;

const HeroSection = ({ properties, userLevel }) => {
  if (!properties || properties.length === 0) {
    return null;
  }

  // Calculs des statistiques premium
  const totalProperties = properties.length;
  const avgYield =
    properties.reduce((sum, p) => sum + (p.netYield || 0), 0) / totalProperties;
  const hotDeals = properties.filter(
    (p) => p.dealType === "OPPORTUNITÉ HOT" || p.dealType === "DEAL DU SIÈCLE"
  ).length;
  const avgScore =
    properties.reduce((sum, p) => sum + (p.opportunityScore || 0), 0) /
    totalProperties;

  const getLevelIcon = (level) => {
    switch (level) {
      case "Légende":
        return <Crown size={24} />;
      case "Maître":
        return <Trophy size={24} />;
      case "Expert":
        return <Award size={24} />;
      default:
        return <Star size={24} />;
    }
  };

  return (
    <HeroContainer
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.2 }}
    >
      <HeroContent>
        <HeroTitle
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          PORTFOLIO PERFORMANCE
        </HeroTitle>

        <HeroSubtitle
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          Analyse intelligente des opportunités d'investissement immobilier
          premium
        </HeroSubtitle>

        <PortfolioStats
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <StatCard whileHover={{ scale: 1.05 }}>
            <StatIcon>
              <TrendingUp size={32} />
            </StatIcon>
            <StatValue>{avgYield.toFixed(1)}%</StatValue>
            <StatLabel>ROI Moyen</StatLabel>
            <StatTrend>
              <TrendingUp size={16} />
              +2.3% ce mois
            </StatTrend>
          </StatCard>

          <StatCard whileHover={{ scale: 1.05 }}>
            <StatIcon>
              <Target size={32} />
            </StatIcon>
            <StatValue>{totalProperties}</StatValue>
            <StatLabel>Deals Analysés</StatLabel>
            <StatTrend>
              <TrendingUp size={16} />
              +15 cette semaine
            </StatTrend>
          </StatCard>

          <StatCard whileHover={{ scale: 1.05 }}>
            <StatIcon>
              <Crown size={32} />
            </StatIcon>
            <StatValue>{avgScore.toFixed(1)}</StatValue>
            <StatLabel>Score Max</StatLabel>
            <StatTrend>
              <Star size={16} />
              Excellence
            </StatTrend>
          </StatCard>

          <StatCard whileHover={{ scale: 1.05 }}>
            <StatIcon>
              <Zap size={32} />
            </StatIcon>
            <StatValue>{hotDeals}</StatValue>
            <StatLabel>Hot Deals</StatLabel>
            <StatTrend>
              <Zap size={16} />
              🔥 Opportunités
            </StatTrend>
          </StatCard>
        </PortfolioStats>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.0 }}
        >
          <UserLevelBadge whileHover={{ scale: 1.05 }}>
            <LevelIcon>{getLevelIcon(userLevel)}</LevelIcon>
            Niveau {userLevel}
          </UserLevelBadge>
        </motion.div>

        {hotDeals > 0 && (
          <HotDealsAlert
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 1.2 }}
            whileHover={{ scale: 1.02 }}
          >
            <Zap size={24} />
            🚨 {hotDeals} OPPORTUNITÉS HOT DÉTECTÉES !
          </HotDealsAlert>
        )}
      </HeroContent>
    </HeroContainer>
  );
};

export default HeroSection;
