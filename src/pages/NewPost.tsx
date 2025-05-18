import React, { useState } from 'react';
import styled from 'styled-components';
import Header from '../components/common/Header';
import Avatar from '../components/common/Avatar';
import Button from '../components/common/Button';

const PageContainer = styled.div`
  background-color: ${props => props.theme.colors.background};
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const HeaderContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
`;

const CancelButton = styled.button`
  background: transparent;
  border: none;
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
  cursor: pointer;
`;

const HeaderTitle = styled.h1`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.large};
  font-weight: 600;
  margin: 0;
`;

const PublishButton = styled(Button)`
  background-color: ${props => props.theme.colors.purple};
  color: ${props => props.theme.colors.white};
  padding: 8px 16px;
  border-radius: 16px;
`;

const PostContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: 16px;
  flex: 1;
`;

const UserSection = styled.div`
  display: flex;
  margin-bottom: 16px;
`;

const UserInfo = styled.div`
  margin-left: 12px;
`;

const TextareaContainer = styled.div`
  flex: 1;
  margin-left: 12px;
`;

const PostTextarea = styled.textarea`
  width: 100%;
  min-height: 120px;
  background-color: transparent;
  border: none;
  color: ${props => props.theme.colors.white};
  font-family: ${props => props.theme.fonts.primary};
  font-size: ${props => props.theme.fontSizes.medium};
  resize: none;
  outline: none;
  
  &::placeholder {
    color: ${props => props.theme.colors.gray};
  }
`;

const AttachmentButton = styled.button`
  background: transparent;
  border: none;
  color: ${props => props.theme.colors.gray};
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
`;

const BottomSection = styled.div`
  margin-top: auto;
  padding: 16px;
  border-top: 1px solid ${props => props.theme.colors.gray_dark};
`;

const PrivacyText = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
  margin: 0;
`;

const ToolbarContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background-color: ${props => props.theme.colors.gray_dark};
  border-radius: 8px;
`;

const ToolbarButton = styled.button`
  background: transparent;
  border: none;
  color: ${props => props.theme.colors.gray};
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
`;

const NewPost: React.FC = () => {
  const [postContent, setPostContent] = useState('');
  
  // Mock user data
  const user = {
    username: 'Metimol',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
  };

  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPostContent(e.target.value);
  };

  const handlePublish = () => {
    console.log('Publishing post:', postContent);
    // In a real app, you would send this to your backend
  };

  return (
    <PageContainer>
      <HeaderContainer>
        <CancelButton>Cancel</CancelButton>
        <HeaderTitle>New Post</HeaderTitle>
        <PublishButton onClick={handlePublish}>Publish</PublishButton>
      </HeaderContainer>
      
      <PostContainer>
        <UserSection>
          <Avatar src={user.avatar} size="medium" />
          <TextareaContainer>
            <PostTextarea 
              placeholder="Write a new post..." 
              value={postContent}
              onChange={handleContentChange}
              autoFocus
            />
          </TextareaContainer>
        </UserSection>
        
        <AttachmentButton>
          📎
        </AttachmentButton>
      </PostContainer>
      
      <BottomSection>
        <PrivacyText>Anyone can answer</PrivacyText>
      </BottomSection>
      
      <ToolbarContainer>
        <ToolbarButton>GIF</ToolbarButton>
        <ToolbarButton>⚙️</ToolbarButton>
        <ToolbarButton>🖼️</ToolbarButton>
        <ToolbarButton>😊</ToolbarButton>
        <ToolbarButton>•••</ToolbarButton>
        <ToolbarButton>🎤</ToolbarButton>
      </ToolbarContainer>
    </PageContainer>
  );
};

export default NewPost;
