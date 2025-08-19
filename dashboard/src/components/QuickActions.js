import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import {
  Zap,
  TrendingUp,
  Target,
  BarChart3,
  Download,
  Share2,
  Settings,
  RefreshCw,
  AlertTriangle,
  Star,
  Filter,
  Search,
} from "lucide-react";

const QuickActionsContainer = styled(motion.div)`
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

const ActionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const ActionCard = styled(motion.div)`
  background: var(--bg-tertiary);
  border-radius: 16px;
  padding: 1.5rem;
  border: 2px solid transparent;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-4px);
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
    transform: scaleX(0);
    transition: transform var(--transition-normal);
  }

  &:hover::before {
    transform: scaleX(1);
  }
`;

const ActionIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: var(--gradient-gold);
  margin-bottom: 1rem;
  color: white;
  font-size: 1.5rem;
`;

const ActionTitle = styled.h4`
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
`;

const ActionDescription = styled.p`
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
`;

const ActionBadge = styled.span`
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--emerald-primary);
  color: white;
`;

const QuickActions = ({
  onExport,
  onRefresh,
  onSettings,
  onAdvancedSearch,
  onMarketAnalysis,
  onPortfolioOptimization,
  onRiskAssessment,
  onPerformanceTracking,
}) => {
  const actions = [
    {
      id: "export",
      icon: <Download size={24} />,
      title: "Exporter Données",
      description: "Télécharger le rapport complet en PDF/Excel",
      action: onExport,
      badge: "Nouveau",
    },
    {
      id: "refresh",
      icon: <RefreshCw size={24} />,
      title: "Actualiser",
      description: "Mettre à jour les données en temps réel",
      action: onRefresh,
    },
    {
      id: "search",
      icon: <Search size={24} />,
      title: "Recherche Avancée",
      description: "Filtres intelligents et recherche sémantique",
      action: onAdvancedSearch,
      badge: "Premium",
    },
    {
      id: "market",
      icon: <TrendingUp size={24} />,
      title: "Analyse Marché",
      description: "Tendances et prévisions du marché immobilier",
      action: onMarketAnalysis,
    },
    {
      id: "portfolio",
      icon: <Target size={24} />,
      title: "Optimisation Portefeuille",
      description: "Algorithme IA pour maximiser les rendements",
      action: onPortfolioOptimization,
      badge: "IA",
    },
    {
      id: "risk",
      icon: <AlertTriangle size={24} />,
      title: "Évaluation Risques",
      description: "Analyse complète des risques d'investissement",
      action: onRiskAssessment,
    },
    {
      id: "performance",
      icon: <BarChart3 size={24} />,
      title: "Suivi Performance",
      description: "Métriques avancées et tableaux de bord",
      action: onPerformanceTracking,
    },
    {
      id: "settings",
      icon: <Settings size={24} />,
      title: "Paramètres",
      description: "Personnaliser l'interface et les préférences",
      action: onSettings,
    },
  ];

  const handleAction = (actionId) => {
    const action = actions.find((a) => a.id === actionId);
    if (action && action.action) {
      action.action();
    } else {
      // Actions par défaut
      switch (actionId) {
        case "export":
          console.log("Export des données...");
          break;
        case "refresh":
          window.location.reload();
          break;
        case "settings":
          console.log("Ouverture des paramètres...");
          break;
        default:
          console.log(`Action ${actionId} non implémentée`);
      }
    }
  };

  return (
    <QuickActionsContainer
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <ContainerHeader>
        <Title>
          <Zap size={24} />
          Actions Rapides
        </Title>
      </ContainerHeader>

      <ActionsGrid>
        {actions.map((action, index) => (
          <ActionCard
            key={action.id}
            onClick={() => handleAction(action.id)}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {action.badge && <ActionBadge>{action.badge}</ActionBadge>}

            <ActionIcon>{action.icon}</ActionIcon>

            <ActionTitle>{action.title}</ActionTitle>
            <ActionDescription>{action.description}</ActionDescription>
          </ActionCard>
        ))}
      </ActionsGrid>
    </QuickActionsContainer>
  );
};

export default QuickActions;

