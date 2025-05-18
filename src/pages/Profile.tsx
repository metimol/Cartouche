import React, { useState } from 'react';
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

const ProfileHeader = styled.div`
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const ProfileInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin-top: 16px;
`;

const Username = styled.h1`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.xlarge};
  font-weight: 600;
  margin: 8px 0 0;
  display: flex;
  align-items: center;
`;

const DisplayName = styled.h2`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
  font-weight: 400;
  margin: 4px 0;
`;

const Bio = styled.p`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.medium};
  text-align: center;
  margin: 8px 0;
`;

const ProfileLink = styled.a`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
  text-decoration: none;
  margin-bottom: 16px;
  
  &:hover {
    text-decoration: underline;
  }
`;

const SubscribersInfo = styled.div`
  display: flex;
  align-items: center;
  margin: 8px 0 16px;
`;

const SubscriberAvatars = styled.div`
  display: flex;
  margin-right: 8px;
`;

const SubscriberAvatar = styled.img`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: -8px;
  border: 2px solid ${props => props.theme.colors.background};
`;

const SubscribersCount = styled.span`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.small};
`;

const EditButton = styled(Button)`
  width: 100%;
  margin-top: 16px;
`;

const TabsContainer = styled.div`
  display: flex;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const Tab = styled.button<{ active: boolean }>`
  flex: 1;
  background: transparent;
  border: none;
  color: ${props => props.active ? props.theme.colors.white : props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
  padding: 16px;
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

const PostsContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const PostItem = styled.div`
  padding: 16px;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const PostHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
`;

const PostUser = styled.div`
  display: flex;
  align-items: center;
`;

const PostUsername = styled.span`
  color: ${props => props.theme.colors.white};
  font-weight: 600;
  font-size: ${props => props.theme.fontSizes.medium};
  margin-right: 8px;
`;

const PostTime = styled.span`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const PostOptions = styled.span`
  color: ${props => props.theme.colors.gray};
`;

const PostContent = styled.p`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.medium};
  margin: 8px 0;
  line-height: 1.5;
`;

const PostImage = styled.img`
  width: 100%;
  border-radius: 8px;
  margin: 8px 0;
`;

const PostActions = styled.div`
  display: flex;
  margin-top: 8px;
`;

const ActionButton = styled.button`
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  margin-right: 16px;
  padding: 0;
  cursor: pointer;
`;

const ActionIcon = styled.img`
  width: 20px;
  height: 20px;
`;

const PostStats = styled.div`
  display: flex;
  align-items: center;
  margin-top: 8px;
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const StatItem = styled.span`
  margin-right: 8px;
`;

const VerifiedBadge = styled.img`
  width: 16px;
  height: 16px;
  margin-left: 4px;
`;

const Profile: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('profile');
  const [activeProfileTab, setActiveProfileTab] = useState('posts');
  
  // Mock data
  const profile = {
    username: 'Metimol',
    displayName: 'Vladyslav',
    bio: 'Backend Developer | My portfolio',
    website: 'https://metimol.github.io/portfolio/',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    verified: true,
    subscribers: 3257,
    subscriberAvatars: [
      'https://randomuser.me/api/portraits/women/33.jpg',
      'https://randomuser.me/api/portraits/men/44.jpg',
    ]
  };
  
  const posts = [
    {
      id: 1,
      content: 'The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested.',
      time: '15 min',
      likes: 59,
      answers: 7
    },
    {
      id: 2,
      content: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.',
      time: '20 min',
      image: 'https://i.imgur.com/ybt3P5P.jpg', // Cat bread image
      likes: 27,
      answers: 3
    }
  ];

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    // In a real app, you would navigate to the corresponding page
  };

  return (
    <PageContainer>
      <Header />
      
      <ProfileHeader>
        <Avatar src={profile.avatar} size="large" verified={profile.verified} />
        <ProfileInfo>
          <Username>
            {profile.username}
            {profile.verified && <VerifiedBadge src="/src/assets/images/verified.png" alt="Verified" />}
          </Username>
          <DisplayName>{profile.displayName}</DisplayName>
          <Bio>{profile.bio}</Bio>
          <ProfileLink href={profile.website} target="_blank" rel="noopener noreferrer">
            {profile.website}
          </ProfileLink>
          
          <SubscribersInfo>
            <SubscriberAvatars>
              {profile.subscriberAvatars.map((avatar, index) => (
                <SubscriberAvatar key={index} src={avatar} alt="Subscriber" />
              ))}
            </SubscriberAvatars>
            <SubscribersCount>{profile.subscribers} Subscribers</SubscribersCount>
          </SubscribersInfo>
          
          <EditButton outline fullWidth>Edit profile</EditButton>
        </ProfileInfo>
      </ProfileHeader>
      
      <TabsContainer>
        <Tab 
          active={activeProfileTab === 'posts'} 
          onClick={() => setActiveProfileTab('posts')}
        >
          Posts
        </Tab>
        <Tab 
          active={activeProfileTab === 'answers'} 
          onClick={() => setActiveProfileTab('answers')}
        >
          Answers
        </Tab>
      </TabsContainer>
      
      <PostsContainer>
        {posts.map(post => (
          <PostItem key={post.id}>
            <PostHeader>
              <PostUser>
                <PostUsername>{profile.username}</PostUsername>
                <PostTime>{post.time}</PostTime>
              </PostUser>
              <PostOptions>•••</PostOptions>
            </PostHeader>
            
            <PostContent>{post.content}</PostContent>
            
            {post.image && <PostImage src={post.image} alt="Post" />}
            
            <PostStats>
              <StatItem>{post.answers} answers</StatItem>
              <StatItem>•</StatItem>
              <StatItem>{post.likes} likes</StatItem>
            </PostStats>
            
            <PostActions>
              <ActionButton>
                <ActionIcon src="/src/assets/images/actions/like.png" alt="Like" />
              </ActionButton>
              <ActionButton>
                <ActionIcon src="/src/assets/images/actions/comment.png" alt="Comment" />
              </ActionButton>
              <ActionButton>
                <ActionIcon src="/src/assets/images/actions/repost.png" alt="Repost" />
              </ActionButton>
              <ActionButton>
                <ActionIcon src="/src/assets/images/actions/share.png" alt="Share" />
              </ActionButton>
            </PostActions>
          </PostItem>
        ))}
      </PostsContainer>
      
      <TabBar activeTab={activeTab} onTabChange={handleTabChange} />
    </PageContainer>
  );
};

export default Profile;
