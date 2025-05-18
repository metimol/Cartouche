import React from 'react';
import styled from 'styled-components';
import { FlexContainer, ResponsivePadding } from '../layout/Responsive';

interface TabBarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const TabBarContainer = styled.div`
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  background-color: ${props => props.theme.colors.background};
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-top: 1px solid ${props => props.theme.colors.gray_dark};
  z-index: 10;
  
  @media (min-width: 768px) {
    position: sticky;
    bottom: auto;
    border-radius: 0 0 16px 16px;
  }
  
  @media (min-width: 992px) {
    width: 80px;
    height: auto;
    flex-direction: column;
    position: fixed;
    top: 100px;
    left: 20px;
    bottom: 100px;
    border-top: none;
    border-right: 1px solid ${props => props.theme.colors.gray_dark};
    border-radius: 16px;
    padding: 20px 0;
  }
`;

const TabItem = styled.div<{ active: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
  cursor: pointer;
  opacity: ${props => props.active ? 1 : 0.6};
  transition: opacity 0.2s ease;
  
  @media (min-width: 992px) {
    margin: 16px 0;
  }
`;

const TabIcon = styled.img`
  width: 24px;
  height: 24px;
`;

const TabBar: React.FC<TabBarProps> = ({ activeTab, onTabChange }) => {
  return (
    <TabBarContainer>
      <TabItem 
        active={activeTab === 'home'} 
        onClick={() => onTabChange('home')}
      >
        <TabIcon 
          src={activeTab === 'home' 
            ? '/src/assets/images/tab/home_focused.png' 
            : '/src/assets/images/tab/home.png'} 
          alt="Home" 
        />
      </TabItem>
      <TabItem 
        active={activeTab === 'activity'} 
        onClick={() => onTabChange('activity')}
      >
        <TabIcon 
          src={activeTab === 'activity' 
            ? '/src/assets/images/tab/activity_focused.png' 
            : '/src/assets/images/tab/activity.png'} 
          alt="Activity" 
        />
      </TabItem>
      <TabItem 
        active={activeTab === 'post'} 
        onClick={() => onTabChange('post')}
      >
        <TabIcon 
          src={activeTab === 'post' 
            ? '/src/assets/images/tab/post_focused.png' 
            : '/src/assets/images/tab/post.png'} 
          alt="New Post" 
        />
      </TabItem>
      <TabItem 
        active={activeTab === 'profile'} 
        onClick={() => onTabChange('profile')}
      >
        <TabIcon 
          src={activeTab === 'profile' 
            ? '/src/assets/images/tab/profile_focused.png' 
            : '/src/assets/images/tab/profile.png'} 
          alt="Profile" 
        />
      </TabItem>
    </TabBarContainer>
  );
};

export default TabBar;
