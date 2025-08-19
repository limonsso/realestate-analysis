import React from "react";
import styled from "styled-components";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
  ComposedChart,
  Area,
} from "recharts";
import {
  BarChart3,
  TrendingUp,
  PieChart as PieChartIcon,
  ScatterChart as ScatterIcon,
} from "lucide-react";

const ChartsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
`;

const ChartCard = styled.div`
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  min-height: 400px;
`;

const ChartHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
`;

const ChartTitle = styled.h3`
  margin: 0;
`;

const CustomTooltip = styled.div`
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
  box-shadow: var(--shadow-lg);
  font-size: 0.875rem;
`;

const TooltipLabel = styled.div`
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
`;

const TooltipRow = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.25rem;
`;

const TooltipValue = styled.span`
  font-weight: 500;
  color: var(--text-secondary);
`;

const Charts = ({ properties }) => {
  if (!properties || properties.length === 0) {
    return (
      <ChartsContainer>
        <ChartCard>
          <ChartHeader>
            <BarChart3 size={20} />
            <ChartTitle>Aucune donnée disponible</ChartTitle>
          </ChartHeader>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "300px",
              color: "var(--text-secondary)",
            }}
          >
            Aucune propriété à analyser
          </div>
        </ChartCard>
      </ChartsContainer>
    );
  }

  // Préparer les données pour les graphiques
  const scatterData = properties
    .filter((p) => p.price && p.netYield)
    .map((p) => ({
      price: p.price / 1000, // Convertir en milliers
      yield: p.netYield,
      surface: p.surface || 1000,
      city: p.city,
      type: p.type,
      address: p.address,
    }));

  const yieldDistribution = properties
    .filter((p) => p.netYield)
    .reduce((acc, p) => {
      const range = Math.floor(p.netYield / 2) * 2;
      const key = `${range}-${range + 2}%`;
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});

  const yieldData = Object.entries(yieldDistribution).map(([range, count]) => ({
    range,
    count,
  }));

  const pricePerSqftData = properties
    .filter((p) => p.pricePerSqft)
    .reduce((acc, p) => {
      const range = Math.floor(p.pricePerSqft / 50) * 50;
      const key = `$${range}-${range + 50}`;
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});

  const pricePerSqftChartData = Object.entries(pricePerSqftData).map(
    ([range, count]) => ({
      range,
      count,
    })
  );

  const buildingAgeData = properties
    .filter((p) => p.buildingAge)
    .reduce((acc, p) => {
      const range = Math.floor(p.buildingAge / 10) * 10;
      const key = `${range}-${range + 10} ans`;
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});

  const buildingAgeChartData = Object.entries(buildingAgeData).map(
    ([range, count]) => ({
      range,
      count,
    })
  );

  const topOpportunities = properties
    .filter((p) => p.opportunityScore)
    .sort((a, b) => (b.opportunityScore || 0) - (a.opportunityScore || 0))
    .slice(0, 10)
    .map((p, index) => ({
      rank: index + 1,
      address: p.address?.substring(0, 20) + "..." || "N/A",
      score: p.opportunityScore || 0,
      yield: p.netYield || 0,
      price: p.price || 0,
    }));

  const correlationData = properties
    .filter((p) => p.price && p.netYield && p.surface && p.buildingAge)
    .map((p) => ({
      price: p.price / 1000,
      yield: p.netYield,
      surface: p.surface,
      age: p.buildingAge,
    }));

  const CustomScatterTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <CustomTooltip>
          <TooltipLabel>{data.address}</TooltipLabel>
          <TooltipRow>
            <span>Prix:</span>
            <TooltipValue>${data.price.toFixed(0)}k</TooltipValue>
          </TooltipRow>
          <TooltipRow>
            <span>Rendement:</span>
            <TooltipValue>{data.yield.toFixed(2)}%</TooltipValue>
          </TooltipRow>
          <TooltipRow>
            <span>Surface:</span>
            <TooltipValue>{data.surface} pi²</TooltipValue>
          </TooltipRow>
          <TooltipRow>
            <span>Ville:</span>
            <TooltipValue>{data.city}</TooltipValue>
          </TooltipRow>
        </CustomTooltip>
      );
    }
    return null;
  };

  const COLORS = [
    "#3b82f6",
    "#10b981",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6",
    "#06b6d4",
    "#84cc16",
    "#f97316",
    "#ec4899",
    "#6366f1",
  ];

  return (
    <ChartsContainer>
      {/* Graphique Scatter: Prix vs Rendement */}
      <ChartCard>
        <ChartHeader>
          <ScatterIcon size={20} />
          <ChartTitle>Prix vs Rendement</ChartTitle>
        </ChartHeader>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart data={scatterData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="price"
              name="Prix (k$)"
              tickFormatter={(value) => `$${value}k`}
            />
            <YAxis
              dataKey="yield"
              name="Rendement (%)"
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip content={<CustomScatterTooltip />} />
            <Scatter
              dataKey="yield"
              fill="#3b82f6"
              shape="circle"
              data={scatterData}
            />
          </ScatterChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Distribution des rendements */}
      <ChartCard>
        <ChartHeader>
          <BarChart3 size={20} />
          <ChartTitle>Distribution des Rendements</ChartTitle>
        </ChartHeader>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={yieldData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" />
            <YAxis />
            <Tooltip
              formatter={(value, name) => [value, "Nombre de propriétés"]}
              labelFormatter={(label) => `Rendement: ${label}`}
            />
            <Bar dataKey="count" fill="#10b981" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Top 10 des meilleures opportunités */}
      <ChartCard>
        <ChartHeader>
          <TrendingUp size={20} />
          <ChartTitle>Top 10 des Opportunités</ChartTitle>
        </ChartHeader>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={topOpportunities} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={[0, 10]} />
            <YAxis dataKey="address" type="category" width={120} />
            <Tooltip
              formatter={(value, name) => [
                name === "score"
                  ? `${value}/10`
                  : name === "yield"
                  ? `${value}%`
                  : `$${value.toLocaleString()}`,
                name === "score"
                  ? "Score"
                  : name === "yield"
                  ? "Rendement"
                  : "Prix",
              ]}
            />
            <Bar dataKey="score" fill="#f59e0b" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Distribution des prix au pi² */}
      <ChartCard>
        <ChartHeader>
          <BarChart3 size={20} />
          <ChartTitle>Prix au Pied Carré</ChartTitle>
        </ChartHeader>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={pricePerSqftChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" />
            <YAxis />
            <Tooltip
              formatter={(value, name) => [value, "Nombre de propriétés"]}
              labelFormatter={(label) => `Prix: ${label}`}
            />
            <Bar dataKey="count" fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Distribution de l'âge des bâtiments */}
      <ChartCard>
        <ChartHeader>
          <BarChart3 size={20} />
          <ChartTitle>Âge des Bâtiments</ChartTitle>
        </ChartHeader>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={buildingAgeChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" />
            <YAxis />
            <Tooltip
              formatter={(value, name) => [value, "Nombre de propriétés"]}
              labelFormatter={(label) => `Âge: ${label}`}
            />
            <Bar dataKey="count" fill="#06b6d4" />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Évolution des prix selon l'année de construction */}
      <ChartCard>
        <ChartHeader>
          <TrendingUp size={20} />
          <ChartTitle>Prix vs Année de Construction</ChartTitle>
        </ChartHeader>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={correlationData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="age"
              name="Année de construction"
              tickFormatter={(value) => `${2025 - value}`}
            />
            <YAxis
              dataKey="price"
              name="Prix (k$)"
              tickFormatter={(value) => `$${value}k`}
            />
            <Tooltip
              formatter={(value, name) => [
                name === "price"
                  ? `$${value}k`
                  : name === "yield"
                  ? `${value}%`
                  : name === "surface"
                  ? `${value} pi²`
                  : value,
                name === "price"
                  ? "Prix"
                  : name === "yield"
                  ? "Rendement"
                  : name === "surface"
                  ? "Surface"
                  : "Âge",
              ]}
              labelFormatter={(label) => `Année: ${2025 - label}`}
            />
            <Area
              type="monotone"
              dataKey="price"
              fill="#3b82f6"
              fillOpacity={0.3}
              stroke="#3b82f6"
            />
            <Line
              type="monotone"
              dataKey="yield"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ fill: "#10b981", strokeWidth: 2, r: 4 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </ChartCard>
    </ChartsContainer>
  );
};

export default Charts;
