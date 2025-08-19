import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { TrendingUp } from "lucide-react";
import UserLevelBadge from "./UserLevelBadge";
import ThemeToggle from "./ThemeToggle";

const HeaderContainer = styled(motion.header)`
  background: var(--bg-secondary);
  border-bottom: 2px solid var(--border-emerald);
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-lg);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
`;

const Logo = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
`;

const LogoIcon = styled.div`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--gradient-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  box-shadow: var(--shadow-gold);
`;

const LogoText = styled.h1`
  font-size: 1.75rem;
  font-weight: 800;
  background: var(--gradient-gold);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
`;

const HeaderRight = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const Header = ({
  userLevel = "PREMIUM",
  darkMode = true,
  onToggleDarkMode,
}) => {
  return (
    <HeaderContainer
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Logo whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
        <LogoIcon>
          <TrendingUp size={24} />
        </LogoIcon>
        <LogoText>REAL ESTATE INTELLIGENCE</LogoText>
      </Logo>

      <HeaderRight>
        <UserLevelBadge level={userLevel} />
        <ThemeToggle
          currentTheme={darkMode ? "dark" : "light"}
          onThemeChange={onToggleDarkMode}
        />
      </HeaderRight>
    </HeaderContainer>
  );
};

export default Header;
