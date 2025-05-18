import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const MainContainer = styled.div`
  position: relative;
  width: 100%;
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
  min-height: 100vh;
  background: #101010;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  margin-left: auto;
  margin-right: auto;
  max-width: 100vw;
  @media (min-width: 500px) {
    border-radius: 16px;
    max-width: 500px;
  }
  @media (min-width: 900px) {
    max-width: 700px;
    padding-bottom: 0;
  }
  @media (min-width: 1200px) {
    max-width: 900px;
    padding-bottom: 0;
  }
`;

const Header = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  max-width: 100vw;
  height: 48px;
  background: #101010;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  margin-left: auto;
  margin-right: auto;
  @media (min-width: 500px) {
    height: 56px;
  }
  @media (min-width: 900px) {
    height: 64px;
    max-width: 700px;
  }
  @media (min-width: 1200px) {
    max-width: 900px;
  }
`;
const Logo = styled.img`
  width: 44px;
  height: 44px;
  @media (min-width: 500px) {
    width: 52px;
    height: 52px;
  }
  @media (min-width: 900px) {
    width: 60px;
    height: 60px;
  }
`;

const Feed = styled.div`
  width: 100%;
  min-height: calc(100vh - 90px);
  background: #101010;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
  margin-bottom: 70px;
  margin-top: 56px;
  margin-left: auto;
  margin-right: auto;
  max-width: 100vw;
  @media (min-width: 900px) {
    margin-bottom: 0;
    align-items: center;
    padding-bottom: 32px;
    margin-top: 64px;
    max-width: 700px;
  }
  @media (min-width: 1200px) {
    max-width: 900px;
  }
`;

// Thread (Post + replies)
const Thread = styled.div`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  padding: 8px 8px;
  gap: 8px;
  width: 100%;
  max-width: 600px;
  @media (min-width: 900px) {
    padding: 12px 0;
    max-width: 700px;
  }
`;

// Thread left (avatars + line)
const ThreadLeft = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0;
  gap: 0;
  width: 36px;
  min-height: 100px;
  position: relative;
`;

const VerticalLine = styled.div<{height?: number}>`
  width: 0px;
  border-left: 1.5px solid #616161;
  position: absolute;
  left: 50%;
  z-index: 0;
  top: 36px;
  transform: translateX(-50%);
  height: ${p => p.height ? `${p.height}px` : '45px'};
`;

const Avatar = styled.img<{size?: number}>`
  width: ${p => p.size || 36}px;
  height: ${p => p.size || 36}px;
  border-radius: 1000px;
  object-fit: cover;
  background: #232323;
  position: relative;
  z-index: 1;
`;

// Thread right (infos + actions)
const ThreadRight = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0;
  width: 100%;
  max-width: 514px;
  margin-left: 24px;
`;

// Post info
const PostInfo = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  width: 100%;
  margin-bottom: 8px;
`;
const PostHeaderRow = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
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
  width: 100%;
`;

const PostImage = styled.img`
  width: 100%;
  max-width: 514px;
  height: auto;
  max-height: 350px;
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
  margin-bottom: 4px;
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
  margin-bottom: 0;
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
  @media (min-width: 900px) {
    width: 40px;
    height: 40px;
    margin-bottom: 16px;
  }
`;
const NavIcon = styled.img`
  width: 24px;
  height: 24px;
  @media (min-width: 900px) {
    width: 32px;
    height: 32px;
  }
`;
const Navigation = styled.div`
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 60px;
  background: #101010;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 10px 40px;
  gap: 51px;
  z-index: 100;
  margin: 0 auto;
  overflow-x: hidden;
  @media (min-width: 900px) {
    position: fixed;
    flex-direction: column;
    width: 70px;
    min-width: 70px;
    max-width: 70px;
    height: 320px;
    left: 0;
    right: auto;
    top: 50%;
    bottom: auto;
    border-radius: 24px;
    padding: 32px 0;
    gap: 32px;
    justify-content: center;
    align-items: center;
    transform: translateY(-50%);
    overflow: visible;
  }
  @media (min-width: 1200px) {
    left: 32px;
  }
`;

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('home');
  const [likedPosts, setLikedPosts] = useState<{[key: string]: boolean}>({});
  const [likedReplies, setLikedReplies] = useState<{[key: string]: boolean}>({});
  const [posts, setPosts] = useState<any[]>([]);
  // refs for dynamic positioning
  const statsRefs = useRef<{[key: number]: HTMLDivElement | null}>({});
  const threadLeftRefs = useRef<{[key: number]: HTMLDivElement | null}>({});
  const [lineHeights, setLineHeights] = useState<{[key: number]: number}>({});
  const [repliesTops, setRepliesTops] = useState<{[key: number]: number}>({});

  useEffect(() => {
    fetch('/assets/json/posts.json')
      .then(res => res.json())
      .then(data => setPosts(data));
  }, []);

  // calculate the height of the line and top for replies after render
  useEffect(() => {
    const newLineHeights: {[key: number]: number} = {};
    const newRepliesTops: {[key: number]: number} = {};
    posts.forEach(post => {
      const statsEl = statsRefs.current[post.id];
      const leftEl = threadLeftRefs.current[post.id];
      if (statsEl && leftEl) {
        const statsRect = statsEl.getBoundingClientRect();
        const leftRect = leftEl.getBoundingClientRect();
        // Line height: from avatar to the center of the stats block
        newLineHeights[post.id] = (statsRect.top + statsRect.height / 2) - leftRect.top;
        // Top for replies: center of the stats block relative to ThreadLeft
        newRepliesTops[post.id] = (statsRect.top + statsRect.height / 2) - leftRect.top - 14; // 14 — half the height of the replies block
      }
    });
    setLineHeights(newLineHeights);
    setRepliesTops(newRepliesTops);
  }, [posts]);

  const handleLikePost = (id: number) => {
    setLikedPosts(prev => ({ ...prev, [id]: !prev[id] }));
  };
  const handleLikeReply = (id: number) => {
    setLikedReplies(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // Tab navigation
  const handleTabClick = (tab: string) => {
    setActiveTab(tab);
    if (tab === 'home') navigate('/home');
    if (tab === 'activity') navigate('/activities');
    if (tab === 'post') navigate('/new');
    if (tab === 'profile') navigate('/profile');
  };

  // Component for replies and the line
  const RepliesAndLine = ({ post }: { post: any }) => {
    const AVATAR_SIZE = 36;
    const REPLIES_BLOCK_HEIGHT = post.replies && post.replies.length === 3 ? 32 : 28;
    const GAP = 0;
    const uniqueUsers: {avatar: string; username: string}[] = [];
    const seen = new Set<string>();
    post.replies.forEach((r: any) => {
      if (!seen.has(r.username)) {
        uniqueUsers.push({ avatar: r.avatar, username: r.username });
        seen.add(r.username);
      }
    });
    const avatars = uniqueUsers.slice(0, 3);
    if (!post.replies || post.replies.length === 0) return null;
    const startY = AVATAR_SIZE / 2 + GAP;
    const endY = (repliesTops[post.id] || 60) - REPLIES_BLOCK_HEIGHT / 2 - GAP;
    const lineHeight = endY - startY;
    return (
      <>
        <VerticalLine height={lineHeight > 0 ? lineHeight : 10} style={{ top: startY }} />
        {avatars.length > 0 && (
          <div style={{
            position: 'absolute',
            top: repliesTops[post.id] || 60,
            left: '50%',
            transform: 'translateX(-50%)',
            width: avatars.length === 1 ? 28 : 48,
            height: REPLIES_BLOCK_HEIGHT,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            {avatars.length === 1 && (
              <Avatar src={avatars[0].avatar} size={28} style={{ border: '2px solid #232323', background: '#c9b6f7' }} />
            )}
            {avatars.length === 2 && (
              <>
                <Avatar src={avatars[0].avatar} size={22} style={{ position: 'absolute', left: 0, top: 3, border: '2px solid #232323', background: '#c9b6f7', zIndex: 2 }} />
                <Avatar src={avatars[1].avatar} size={22} style={{ position: 'absolute', left: 26, top: 3, border: '2px solid #232323', background: '#f7b6e0', zIndex: 1 }} />
              </>
            )}
            {avatars.length === 3 && (
              <>
                <Avatar src={avatars[0].avatar} size={20} style={{ position: 'absolute', left: 0, top: 0, border: '2px solid #232323', background: '#c9b6f7', zIndex: 2 }} />
                <Avatar src={avatars[1].avatar} size={20} style={{ position: 'absolute', left: 28, top: 0, border: '2px solid #232323', background: '#f7b6e0', zIndex: 2 }} />
                <Avatar src={avatars[2].avatar} size={20} style={{ position: 'absolute', left: 14, top: 16, border: '2px solid #232323', background: '#b6e0f7', zIndex: 1 }} />
              </>
            )}
          </div>
        )}
      </>
    );
  };

  return (
    <MainContainer>
      <ContentWrapper>
        <Header>
          <Logo src="/assets/images/logo.svg" alt="logo" />
        </Header>
        <Feed style={{ marginTop: '48px' }}>
          {posts.map(post => (
            <Thread key={post.id}>
              <ThreadLeft style={{ position: 'relative' }} ref={el => { threadLeftRefs.current[post.id] = el; }}>
                <Avatar src={post.avatar} />
                {post.replies && post.replies.length > 0 && (
                  <RepliesAndLine post={post} />
                )}
              </ThreadLeft>
              <ThreadRight>
                <PostInfo style={{ marginLeft: 0 }}>
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
                <Actions style={{ marginTop: 8, marginLeft: 0 }}>
                  <ActionBtn onClick={() => handleLikePost(post.id)}>
                    <ActionIcon src={likedPosts[post.id] ? "/assets/images/like_filled.svg" : "/assets/images/like.svg"} alt="like" />
                  </ActionBtn>
                  <ActionBtn><ActionIcon src="/assets/images/comment.svg" alt="comment" /></ActionBtn>
                  <ActionBtn><ActionIcon src="/assets/images/repost.svg" alt="repost" /></ActionBtn>
                  <ActionBtn><ActionIcon src="/assets/images/share.svg" alt="share" /></ActionBtn>
                </Actions>
                <Stats style={{ marginLeft: 0 }} ref={el => { statsRefs.current[post.id] = el; }}>
                  <StatText>{post.answers} answers</StatText>
                  <StatDot />
                  <StatText>{post.likes + (likedPosts[post.id] ? 1 : 0)} likes</StatText>
                </Stats>
                {/* Replies */}
                {post.replies && (post.replies as Array<any>).map((reply: any) => (
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
                        {'image' in reply && reply.image && <PostImage src={reply.image} alt="reply-img" />}
                      </PostInfo>
                      <Actions>
                        <ActionBtn onClick={() => handleLikeReply(reply.id)}>
                          <ActionIcon src={likedReplies[reply.id] ? "/assets/images/like_filled.svg" : "/assets/images/like.svg"} alt="like" />
                        </ActionBtn>
                        <ActionBtn><ActionIcon src="/assets/images/comment.svg" alt="comment" /></ActionBtn>
                        <ActionBtn><ActionIcon src="/assets/images/repost.svg" alt="repost" /></ActionBtn>
                        <ActionBtn><ActionIcon src="/assets/images/share.svg" alt="share" /></ActionBtn>
                      </Actions>
                      <Stats>
                        <StatText>{reply.answers} answers</StatText>
                        <StatDot />
                        <StatText>{reply.likes + (likedReplies[reply.id] ? 1 : 0)} likes</StatText>
                      </Stats>
                    </ThreadRight>
                  </Thread>
                ))}
              </ThreadRight>
            </Thread>
          ))}
        </Feed>
        <Navigation>
          <NavBtn active={activeTab === 'home'} onClick={() => handleTabClick('home')}>
            <NavIcon src="/assets/images/home_filled.svg" alt="home" />
          </NavBtn>
          <NavBtn active={activeTab === 'activity'} onClick={() => handleTabClick('activity')}>
            <NavIcon src="/assets/images/activity.svg" alt="activity" />
          </NavBtn>
          <NavBtn active={activeTab === 'post'} onClick={() => handleTabClick('post')}>
            <NavIcon src="/assets/images/post.svg" alt="post" />
          </NavBtn>
          <NavBtn active={activeTab === 'profile'} onClick={() => handleTabClick('profile')}>
            <NavIcon src="/assets/images/profile.svg" alt="profile" />
          </NavBtn>
        </Navigation>
      </ContentWrapper>
    </MainContainer>
  );
};

export default Home;

if (typeof window !== 'undefined') {
  document.documentElement.style.overflowX = 'hidden';
  document.body.style.overflowX = 'hidden';
}
