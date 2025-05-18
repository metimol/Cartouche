import React from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import TabBar from '../components/common/TabBar';
import PostCard from '../components/common/PostCard';
import { ResponsiveContainer, FlexContainer } from '../components/layout/Responsive';

const PageContainer = styled.div`
  background-color: ${props => props.theme.colors.background};
  min-height: 100vh;
  padding-bottom: 60px;
  
  @media (min-width: 768px) {
    padding-bottom: 0;
  }
  
  @media (min-width: 992px) {
    padding-left: 100px;
  }
`;

const PostsContainer = styled.div`
  display: flex;
  flex-direction: column;
  
  @media (min-width: 768px) {
    border-radius: 8px;
    overflow: hidden;
  }
`;

const SidebarContainer = styled.div`
  display: none;
  
  @media (min-width: 992px) {
    display: block;
    width: 280px;
    padding: 16px;
  }
`;

const SidebarCard = styled.div`
  background-color: ${props => props.theme.colors.gray_dark};
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
`;

const SidebarTitle = styled.h3`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: 12px;
`;

const SidebarContent = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const Home: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('home');
  
  // Mock data for posts
  const posts = [
    {
      id: 1,
      username: 'Metimol',
      userAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      verified: true,
      timeAgo: '2 min',
      content: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.',
      image: 'https://i.imgur.com/ybt3P5P.jpg', // Cat bread image
      likes: 27,
      answers: 3
    },
    {
      id: 2,
      username: 'Liza',
      userAvatar: 'https://randomuser.me/api/portraits/women/44.jpg',
      verified: false,
      timeAgo: '10 min',
      content: 'There are many variations of passages of Lorem Ipsum available.',
      likes: 12,
      answers: 2
    },
    {
      id: 3,
      username: 'Metimol',
      userAvatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      verified: true,
      timeAgo: '15 min',
      content: 'The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested.',
      likes: 59,
      answers: 7
    }
  ];

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    // In a real app, you would navigate to the corresponding page
  };

  return (
    <PageContainer>
      <Header />
      
      <ResponsiveContainer>
        <FlexContainer gap="24px">
          <PostsContainer>
            {posts.map(post => (
              <PostCard
                key={post.id}
                username={post.username}
                userAvatar={post.userAvatar}
                verified={post.verified}
                timeAgo={post.timeAgo}
                content={post.content}
                image={post.image}
                likes={post.likes}
                answers={post.answers}
                onLike={() => console.log('Like')}
                onComment={() => console.log('Comment')}
                onShare={() => console.log('Share')}
                onRepost={() => console.log('Repost')}
              />
            ))}
          </PostsContainer>
          
          <SidebarContainer>
            <SidebarCard>
              <SidebarTitle>Trending Topics</SidebarTitle>
              <SidebarContent>
                #AI #MachineLearning #WebDevelopment
              </SidebarContent>
            </SidebarCard>
            
            <SidebarCard>
              <SidebarTitle>Suggested Users</SidebarTitle>
              <SidebarContent>
                Find more interesting people to follow
              </SidebarContent>
            </SidebarCard>
          </SidebarContainer>
        </FlexContainer>
      </ResponsiveContainer>
      
      <TabBar activeTab={activeTab} onTabChange={handleTabChange} />
    </PageContainer>
  );
};

export default Home;
