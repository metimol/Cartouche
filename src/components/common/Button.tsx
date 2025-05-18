import React from 'react';
import styled from 'styled-components';

interface ButtonProps {
  primary?: boolean;
  outline?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
}

const StyledButton = styled.button<ButtonProps>`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 14px 20px;
  border-radius: 8px;
  font-family: ${props => props.theme.fonts.primary};
  font-size: ${props => props.theme.fontSizes.medium};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  color-scheme: only dark;

  ${props => props.primary && `
    background-color: #fff !important;
    color: #000 !important;
    border: 1px solid #fff !important;
    box-shadow: 0 1px 8px 0 rgba(0,0,0,0.04);
  `}
  
  ${props => props.outline && `
    background-color: transparent !important;
    border: 1px solid #fff !important;
    color: #fff !important;
  `}
  
  ${props => !props.primary && !props.outline && `
    background-color: ${props.theme.colors.gray_mid};
    color: #fff;
  `}
  
  ${props => props.fullWidth && `
    width: 100%;
  `}
  
  &:hover {
    opacity: 0.9;
  }
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const Button: React.FC<ButtonProps> = ({ 
  primary = false, 
  outline = false,
  fullWidth = false,
  children, 
  onClick,
  type = 'button',
  disabled = false
}) => {
  return (
    <StyledButton 
      primary={primary} 
      outline={outline}
      fullWidth={fullWidth}
      onClick={onClick}
      type={type}
      disabled={disabled}
    >
      {children}
    </StyledButton>
  );
};

export default Button;
