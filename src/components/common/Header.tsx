import React from 'react';
import styled from 'styled-components';

interface HeaderProps {
  title?: string;
  showBackButton?: boolean;
  onBack?: () => void;
  rightAction?: React.ReactNode;
}

const HeaderContainer = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: ${props => props.theme.colors.background};
  position: sticky;
  top: 0;
  z-index: 10;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.xlarge};
  font-weight: 600;
  margin: 0;
  flex: 1;
  text-align: center;
`;

const BackButton = styled.button`
  background: transparent;
  border: none;
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.large};
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
`;

const BackIcon = styled.img`
  width: 20px;
  height: 20px;
  margin-right: 8px;
`;

const BackText = styled.span`
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 16px;
  line-height: 16px;
  color: #FFFFFF;
`;

const RightActionContainer = styled.div`
  min-width: 40px;
  display: flex;
  justify-content: flex-end;
`;

const Header: React.FC<HeaderProps> = ({
  title,
  showBackButton = false,
  onBack,
  rightAction
}) => {
  return (
    <HeaderContainer>
      {showBackButton ? (
        <BackButton onClick={onBack}>
          <BackIcon src="/assets/images/arrow_back.svg" alt="Back" />
          <BackText>Back</BackText>
        </BackButton>
      ) : (
        <div style={{ width: 40 }} />
      )}
      {title && <Title>{title}</Title>}
      <RightActionContainer>
        {rightAction}
      </RightActionContainer>
    </HeaderContainer>
  );
};

export default Header;
