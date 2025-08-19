import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { Crown, Star, Zap, Target, TrendingUp, Award } from "lucide-react";

const BadgeContainer = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: ${(props) => {
    switch (props.level) {
      case "ELITE":
        return "var(--gradient-gold)";
      case "PREMIUM":
        return "var(--gradient-emerald)";
      case "PRO":
        return "var(--gradient-royal)";
      case "STANDARD":
        return "var(--bg-elevated)";
      default:
        return "var(--bg-elevated)";
    }
  }};
  border: 2px solid
    ${(props) => {
      switch (props.level) {
        case "ELITE":
          return "var(--gold-primary)";
        case "PREMIUM":
          return "var(--emerald-primary)";
        case "PRO":
          return "var(--royal-primary)";
        case "STANDARD":
          return "var(--border-color)";
        default:
          return "var(--border-color)";
      }
    }};
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  box-shadow: ${(props) => {
    switch (props.level) {
      case "ELITE":
        return "var(--shadow-gold)";
      case "PREMIUM":
        return "var(--shadow-emerald)";
      case "PRO":
        return "var(--shadow-royal)";
      default:
        return "var(--shadow-sm)";
    }
  }};
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    transition: left 0.5s;
  }

  &:hover::before {
    left: 100%;
  }
`;

const LevelIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
`;

const LevelText = styled.span`
  font-weight: 700;
`;

const UserLevelBadge = ({ level = "STANDARD" }) => {
  const getLevelIcon = (level) => {
    switch (level) {
      case "ELITE":
        return <Crown size={16} />;
      case "PREMIUM":
        return <Star size={16} />;
      case "PRO":
        return <Zap size={16} />;
      case "STANDARD":
        return <Target size={16} />;
      default:
        return <Target size={16} />;
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case "ELITE":
        return "var(--gold-primary)";
      case "PREMIUM":
        return "var(--emerald-primary)";
      case "PRO":
        return "var(--royal-primary)";
      case "STANDARD":
        return "var(--text-muted)";
      default:
        return "var(--text-muted)";
    }
  };

  return (
    <BadgeContainer
      level={level}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <LevelIcon>{getLevelIcon(level)}</LevelIcon>
      <LevelText>{level}</LevelText>
    </BadgeContainer>
  );
};

export default UserLevelBadge;

