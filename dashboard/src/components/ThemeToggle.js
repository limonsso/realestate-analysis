import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { Sun, Moon, Monitor } from "lucide-react";

const ToggleContainer = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 12px;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;

  &:hover {
    border-color: var(--border-gold);
    box-shadow: var(--shadow-md);
  }

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-gold);
    opacity: 0;
    transition: opacity var(--transition-normal);
  }

  &:hover::before {
    opacity: 0.1;
  }
`;

const ToggleButton = styled(motion.button)`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: ${(props) =>
    props.active ? "var(--gradient-gold)" : "transparent"};
  border: none;
  color: ${(props) => (props.active ? "white" : "var(--text-secondary)")};
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  z-index: 1;

  &:hover {
    transform: scale(1.1);
    color: ${(props) => (props.active ? "white" : "var(--text-gold)")};
  }

  &:active {
    transform: scale(0.95);
  }
`;

const ToggleLabel = styled.span`
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  position: relative;
  z-index: 1;
`;

const ThemeToggle = ({ currentTheme, onThemeChange }) => {
  const themes = [
    { id: "light", icon: <Sun size={16} />, label: "Clair" },
    { id: "dark", icon: <Moon size={16} />, label: "Sombre" },
    { id: "auto", icon: <Monitor size={16} />, label: "Auto" },
  ];

  const handleThemeChange = (themeId) => {
    onThemeChange(themeId);
  };

  return (
    <ToggleContainer
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
    >
      {themes.map((theme) => (
        <ToggleButton
          key={theme.id}
          active={currentTheme === theme.id}
          onClick={() => handleThemeChange(theme.id)}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          {theme.icon}
        </ToggleButton>
      ))}
      <ToggleLabel>Thème</ToggleLabel>
    </ToggleContainer>
  );
};

export default ThemeToggle;

