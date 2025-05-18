import React from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import TabBar from '../components/common/TabBar';
import Avatar from '../components/common/Avatar';
import Button from '../components/common/Button';

const PageContainer = styled.div`
  background-color: ${props => props.theme.colors.background};
  min-height: 100vh;
  padding-bottom: 60px;
`;

const ActivityHeader = styled.div`
  padding: 16px;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.xlarge};
  font-weight: 600;
  margin: 0;
`;

const TabsContainer = styled.div`
  display: flex;
  margin-top: 16px;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const Tab = styled.button<{ active: boolean }>`
  background: transparent;
  border: none;
  color: ${props => props.active ? props.theme.colors.white : props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
  padding: 12px 16px;
  cursor: pointer;
  position: relative;
  
  &:after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background-color: ${props => props.active ? props.theme.colors.white : 'transparent'};
  }
`;

const ActivityList = styled.div`
  display: flex;
  flex-direction: column;
`;

const ActivityItem = styled.div`
  display: flex;
  padding: 16px;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const ActivityContent = styled.div`
  flex: 1;
  margin-left: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const Username = styled.span`
  color: ${props => props.theme.colors.white};
  font-weight: 600;
  font-size: ${props => props.theme.fontSizes.medium};
`;

const ActivityText = styled.span`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const VerifiedBadge = styled.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  background-color: ${props => props.theme.colors.purple};
  border-radius: 50%;
  margin-left: 4px;
  color: ${props => props.theme.colors.white};
  font-size: 10px;
`;

const Activities: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('home');
  const [activeFilter, setActiveFilter] = React.useState('all');
  
  // Mock data for activities
  const activities = [
    {
      id: 1,
      username: 'thomas',
      userAvatar: 'https://randomuser.me/api/portraits/men/1.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 2,
      username: 'mike',
      userAvatar: 'https://randomuser.me/api/portraits/men/2.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 3,
      username: 'michael',
      userAvatar: 'https://randomuser.me/api/portraits/men/3.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 4,
      username: 'willie',
      userAvatar: 'https://randomuser.me/api/portraits/men/4.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 5,
      username: 'peter',
      userAvatar: 'https://randomuser.me/api/portraits/men/5.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 6,
      username: 'angela',
      userAvatar: 'https://randomuser.me/api/portraits/women/1.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 7,
      username: 'devon',
      userAvatar: 'https://randomuser.me/api/portraits/men/6.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 8,
      username: 'col',
      userAvatar: 'https://randomuser.me/api/portraits/men/7.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 9,
      username: 'templeton',
      userAvatar: 'https://randomuser.me/api/portraits/men/8.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 10,
      username: 'willie',
      userAvatar: 'https://randomuser.me/api/portraits/men/9.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 11,
      username: 'dori',
      userAvatar: 'https://randomuser.me/api/portraits/women/2.jpg',
      verified: true,
      action: 'Started following you'
    },
    {
      id: 12,
      username: 'rick',
      userAvatar: 'https://randomuser.me/api/portraits/men/10.jpg',
      verified: true,
      action: 'Started following you'
    }
  ];

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    // In a real app, you would navigate to the corresponding page
  };

  return (
    <PageContainer>
      <ActivityHeader>
        <Title>Activity</Title>
        <TabsContainer>
          <Tab 
            active={activeFilter === 'all'} 
            onClick={() => setActiveFilter('all')}
          >
            All
          </Tab>
          <Tab 
            active={activeFilter === 'answers'} 
            onClick={() => setActiveFilter('answers')}
          >
            Answers
          </Tab>
          <Tab 
            active={activeFilter === 'mentions'} 
            onClick={() => setActiveFilter('mentions')}
          >
            Mentions
          </Tab>
          <Tab 
            active={activeFilter === 'verified'} 
            onClick={() => setActiveFilter('verified')}
          >
            Verified
          </Tab>
        </TabsContainer>
      </ActivityHeader>
      
      <ActivityList>
        {activities.map(activity => (
          <ActivityItem key={activity.id}>
            <Avatar src={activity.userAvatar} size="small" verified={activity.verified} />
            <ActivityContent>
              <UserInfo>
                <Username>
                  {activity.username}
                  {activity.verified && <VerifiedBadge>✓</VerifiedBadge>}
                </Username>
                <ActivityText>{activity.action}</ActivityText>
              </UserInfo>
              <Button outline>Follow</Button>
            </ActivityContent>
          </ActivityItem>
        ))}
      </ActivityList>
      
      <TabBar activeTab={activeTab} onTabChange={handleTabChange} />
    </PageContainer>
  );
};

export default Activities;
