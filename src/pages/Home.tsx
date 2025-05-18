import React from 'react';
import styled from 'styled-components';

const MainContainer = styled.div`
  position: relative;
  width: 100vw;
  min-height: 100vh;
  background: #101010;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 0;
  overflow-x: hidden;
`;

const ContentWrapper = styled.div`
  width: 100%;
  max-width: 390px;
  min-height: 100vh;
  background: #101010;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  @media (min-width: 500px) {
    border-radius: 16px;
    box-shadow: 0 0 24px 0 rgba(0,0,0,0.12);
    margin: 0 auto;
  }
`;

// Header
const Header = styled.div`
  position: sticky;
  top: 0;
  left: 0;
  width: 100%;
  height: 40px;
  background: #101010;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
`;
const Logo = styled.img`
  width: 40px;
  height: 40px;
`;

// Feed container
const Feed = styled.div`
  width: 100%;
  min-height: calc(100vh - 90px);
  background: #101010;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0;
  margin-bottom: 50px;
`;

// Thread (Post + replies)
const Thread = styled.div`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  padding: 8px 16px;
  gap: 8px;
  width: 390px;
`;

// Thread left (avatars + line)
const ThreadLeft = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
  gap: 16px;
  width: 36px;
  min-height: 100px;
  position: relative;
`;
const Avatar = styled.img<{size?: number}>`
  width: ${p => p.size || 36}px;
  height: ${p => p.size || 36}px;
  border-radius: 1000px;
  object-fit: cover;
  background: #232323;
`;
const VerticalLine = styled.div<{height?: number}>`
  width: 0px;
  height: ${p => p.height || 45}px;
  border-left: 1.5px solid #616161;
`;

// Thread right (infos + actions)
const ThreadRight = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
  width: 314px;
`;

// Post info
const PostInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  width: 314px;
`;
const PostHeaderRow = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 314px;
`;
const Username = styled.span`
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  color: #fff;
`;
const PostHeaderRight = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
`;
const TimeAgo = styled.span`
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 12px;
  color: #616161;
`;
const Dots = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 2px;
  width: 13px;
  height: 3px;
`;
const Dot = styled.div`
  width: 3px;
  height: 3px;
  background: #fff;
  border-radius: 1000px;
`;

const PostText = styled.div`
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 13px;
  color: #fff;
  line-height: 19px;
  width: 314px;
`;
const PostImage = styled.img`
  width: 314px;
  height: 230px;
  border-radius: 8px;
  object-fit: cover;
`;

// Actions
const Actions = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  width: 132px;
  height: 24px;
`;
const ActionBtn = styled.button`
  width: 24px;
  height: 24px;
  background: none;
  border: none;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
`;
const ActionIcon = styled.img`
  width: 24px;
  height: 24px;
`;

// Stats (answers, likes)
const Stats = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 4px;
  width: 117px;
  height: 19px;
`;
const StatText = styled.span`
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 13px;
  color: #616161;
  letter-spacing: -0.2px;
`;
const StatDot = styled.div`
  width: 2px;
  height: 2px;
  background: #616161;
  border-radius: 1000px;
`;

// Navigation (TabBar)
const NavBtn = styled.button<{active?: boolean}>`
  width: 30px;
  height: 30px;
  background: none;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
`;
const NavIcon = styled.img`
  width: 24px;
  height: 24px;
`;
const Navigation = styled.div`
  position: sticky;
  left: 0;
  bottom: 0;
  width: 100%;
  max-width: 390px;
  height: 50px;
  background: #101010;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 10px 40px;
  gap: 51px;
  z-index: 100;
  margin: 0 auto;
`;

// MOCK DATA
const posts = [
  {
    id: 1,
    username: 'Metimol',
    avatar: '/assets/images/user0.png',
    time: '2 min',
    text: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.',
    image: '/assets/images/test_image.png',
    likes: 27,
    answers: 3,
    replies: [
      {
        id: 2,
        username: 'Liza',
        avatar: '/assets/images/user1.png',
        time: '10 min',
        text: 'There are many variations of passages of Lorem Ipsum available.',
        likes: 12,
        answers: 2,
      }
    ]
  },
  {
    id: 3,
    username: 'Metimol',
    avatar: '/assets/images/user0.png',
    time: '15 min',
    text: 'The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested.',
    likes: 59,
    answers: 0,
  }
];

const Home: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('home');

  return (
    <MainContainer>
      <ContentWrapper>
        <Header>
          <Logo src="/assets/images/logo.svg" alt="logo" />
        </Header>
        <Feed>
          {posts.map(post => (
            <Thread key={post.id}>
              <ThreadLeft>
                <Avatar src={post.avatar} />
                <VerticalLine height={post.replies ? (post.replies.length ? 100 : 45) : 45} />
                {post.replies && post.replies.map((reply, idx) => (
                  <Avatar key={reply.id} src={reply.avatar} size={20} style={{ marginTop: idx === 0 ? 0 : 8 }} />
                ))}
              </ThreadLeft>
              <ThreadRight>
                <PostInfo>
                  <PostHeaderRow>
                    <Username>{post.username}</Username>
                    <PostHeaderRight>
                      <TimeAgo>{post.time}</TimeAgo>
                      <Dots>
                        <Dot /><Dot /><Dot />
                      </Dots>
                    </PostHeaderRight>
                  </PostHeaderRow>
                  <PostText>{post.text}</PostText>
                  {post.image && <PostImage src={post.image} alt="post" />}
                </PostInfo>
                <Actions>
                  <ActionBtn><ActionIcon src="/assets/images/like.svg" alt="like" /></ActionBtn>
                  <ActionBtn><ActionIcon src="/assets/images/comment.svg" alt="comment" /></ActionBtn>
                  <ActionBtn><ActionIcon src="/assets/images/repost.svg" alt="repost" /></ActionBtn>
                  <ActionBtn><ActionIcon src="/assets/images/share.svg" alt="share" /></ActionBtn>
                </Actions>
                <Stats>
                  <StatText>{post.answers} answers</StatText>
                  <StatDot />
                  <StatText>{post.likes} likes</StatText>
                </Stats>
                {/* Replies */}
                {post.replies && post.replies.map(reply => (
                  <Thread key={reply.id} style={{ padding: '8px 0 0 0', background: 'none', width: '100%' }}>
                    <ThreadLeft>
                      <Avatar src={reply.avatar} size={36} />
                    </ThreadLeft>
                    <ThreadRight>
                      <PostInfo>
                        <PostHeaderRow>
                          <Username>{reply.username}</Username>
                          <PostHeaderRight>
                            <TimeAgo>{reply.time}</TimeAgo>
                            <Dots>
                              <Dot /><Dot /><Dot />
                            </Dots>
                          </PostHeaderRight>
                        </PostHeaderRow>
                        <PostText>{reply.text}</PostText>
                      </PostInfo>
                      <Actions>
                        <ActionBtn><ActionIcon src="/assets/images/like.svg" alt="like" /></ActionBtn>
                        <ActionBtn><ActionIcon src="/assets/images/comment.svg" alt="comment" /></ActionBtn>
                        <ActionBtn><ActionIcon src="/assets/images/repost.svg" alt="repost" /></ActionBtn>
                        <ActionBtn><ActionIcon src="/assets/images/share.svg" alt="share" /></ActionBtn>
                      </Actions>
                      <Stats>
                        <StatText>{reply.answers} answers</StatText>
                        <StatDot />
                        <StatText>{reply.likes} likes</StatText>
                      </Stats>
                    </ThreadRight>
                  </Thread>
                ))}
              </ThreadRight>
            </Thread>
          ))}
        </Feed>
        <Navigation>
          <NavBtn active={activeTab === 'home'} onClick={() => setActiveTab('home')}>
            <NavIcon src="/assets/images/home_filled.svg" alt="home" />
          </NavBtn>
          <NavBtn active={activeTab === 'activity'} onClick={() => setActiveTab('activity')}>
            <NavIcon src="/assets/images/activity.svg" alt="activity" />
          </NavBtn>
          <NavBtn active={activeTab === 'post'} onClick={() => setActiveTab('post')}>
            <NavIcon src="/assets/images/post.svg" alt="post" />
          </NavBtn>
          <NavBtn active={activeTab === 'profile'} onClick={() => setActiveTab('profile')}>
            <NavIcon src="/assets/images/profile.svg" alt="profile" />
          </NavBtn>
        </Navigation>
      </ContentWrapper>
    </MainContainer>
  );
};

export default Home;
