import React from "react";
import styled from "styled-components";
import {
  Building2,
  TrendingUp,
  DollarSign,
  Target,
  Home,
  MapPin,
  Calendar,
  Calculator,
} from "lucide-react";

const KPIContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const KPICard = styled.div`
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;

  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
`;

const KPIIcon = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  color: white;
  font-size: 1.5rem;
`;

const KPITitle = styled.h3`
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const KPIValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
`;

const KPISubtitle = styled.div`
  font-size: 0.875rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const KPITrend = styled.span`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  margin-left: auto;
`;

const KPICards = ({ properties }) => {
  if (!properties || properties.length === 0) {
    return (
      <KPIContainer>
        <KPICard>
          <KPITitle>Aucune donnée</KPITitle>
          <KPIValue>0</KPIValue>
        </KPICard>
      </KPIContainer>
    );
  }

  // Calculs des métriques
  const totalProperties = properties.length;
  const avgYield =
    properties.reduce((sum, p) => sum + (p.netYield || 0), 0) / totalProperties;
  const medianPrice =
    properties.sort((a, b) => a.price - b.price)[
      Math.floor(totalProperties / 2)
    ]?.price || 0;
  const bestOpportunity = properties.reduce(
    (best, current) =>
      (current.opportunityScore || 0) > (best.opportunityScore || 0)
        ? current
        : best,
    properties[0]
  );

  const totalRevenue = properties.reduce(
    (sum, p) => sum + (p.annualRevenue || 0),
    0
  );
  const avgCashFlow =
    properties.reduce((sum, p) => sum + (p.monthlyCashFlow || 0), 0) /
    totalProperties;
  const avgPricePerSqft =
    properties.reduce((sum, p) => sum + (p.pricePerSqft || 0), 0) /
    totalProperties;
  const avgBuildingAge =
    properties.reduce((sum, p) => sum + (p.buildingAge || 0), 0) /
    totalProperties;

  const kpis = [
    {
      title: "Total Propriétés",
      value: totalProperties.toLocaleString(),
      subtitle: "Propriétés analysées",
      icon: <Building2 size={24} />,
      color: "var(--primary-color)",
      trend: null,
    },
    {
      title: "Rendement Moyen",
      value: `${avgYield.toFixed(2)}%`,
      subtitle: "Rendement net moyen",
      icon: <TrendingUp size={24} />,
      color: "var(--success-color)",
      trend:
        avgYield > 6 ? "📈 Excellent" : avgYield > 4 ? "📊 Bon" : "⚠️ Faible",
    },
    {
      title: "Prix Médian",
      value: `$${medianPrice.toLocaleString()}`,
      subtitle: "Prix médian du marché",
      icon: <DollarSign size={24} />,
      color: "var(--info-color)",
      trend: null,
    },
    {
      title: "Meilleure Opportunité",
      value: `${(bestOpportunity?.opportunityScore || 0).toFixed(1)}/10`,
      subtitle: bestOpportunity?.address || "N/A",
      icon: <Target size={24} />,
      color: "var(--warning-color)",
      trend: "🏆 Top",
    },
    {
      title: "Revenus Totaux",
      value: `$${totalRevenue.toLocaleString()}`,
      subtitle: "Revenus annuels totaux",
      icon: <Home size={24} />,
      color: "var(--secondary-color)",
      trend: null,
    },
    {
      title: "Cash-Flow Moyen",
      value: `$${avgCashFlow.toFixed(0)}`,
      subtitle: "Cash-flow mensuel moyen",
      icon: <Calculator size={24} />,
      color: avgCashFlow > 0 ? "var(--success-color)" : "var(--danger-color)",
      trend: avgCashFlow > 0 ? "💰 Positif" : "💸 Négatif",
    },
    {
      title: "Prix au pi²",
      value: `$${avgPricePerSqft.toFixed(0)}`,
      subtitle: "Prix moyen au pied carré",
      icon: <MapPin size={24} />,
      color: "var(--info-color)",
      trend: null,
    },
    {
      title: "Âge Moyen",
      value: `${avgBuildingAge.toFixed(0)} ans`,
      subtitle: "Âge moyen des bâtiments",
      icon: <Calendar size={24} />,
      color: "var(--text-secondary)",
      trend:
        avgBuildingAge < 20
          ? "🆕 Récent"
          : avgBuildingAge < 50
          ? "📅 Moyen"
          : "🏚️ Ancien",
    },
  ];

  return (
    <KPIContainer>
      {kpis.map((kpi, index) => (
        <KPICard key={index}>
          <KPIIcon style={{ background: kpi.color }}>{kpi.icon}</KPIIcon>
          <KPITitle>{kpi.title}</KPITitle>
          <KPIValue>{kpi.value}</KPIValue>
          <KPISubtitle>
            {kpi.subtitle}
            {kpi.trend && (
              <KPITrend
                style={{
                  background:
                    kpi.trend.includes("Excellent") ||
                    kpi.trend.includes("Positif") ||
                    kpi.trend.includes("Top")
                      ? "var(--success-color)"
                      : kpi.trend.includes("Bon") ||
                        kpi.trend.includes("Récent")
                      ? "var(--info-color)"
                      : kpi.trend.includes("Faible") ||
                        kpi.trend.includes("Négatif")
                      ? "var(--danger-color)"
                      : "var(--warning-color)",
                  color: "white",
                }}
              >
                {kpi.trend}
              </KPITrend>
            )}
          </KPISubtitle>
        </KPICard>
      ))}
    </KPIContainer>
  );
};

export default KPICards;
