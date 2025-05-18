import React from 'react';
import styled from 'styled-components';

interface PostCardProps {
  username: string;
  userAvatar: string;
  verified?: boolean;
  timeAgo: string;
  content: string;
  image?: string;
  likes: number;
  answers: number;
  onLike?: () => void;
  onComment?: () => void;
  onShare?: () => void;
  onRepost?: () => void;
}

const PostCardContainer = styled.div`
  background-color: ${props => props.theme.colors.background};
  border-bottom: 1px solid ${props => props.theme.colors.gray_dark};
  padding: 16px;
`;

const PostHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
`;

const UserAvatar = styled.img`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
`;

const UserDetails = styled.div`
  display: flex;
  flex-direction: column;
`;

const Username = styled.span`
  color: ${props => props.theme.colors.white};
  font-weight: 600;
  font-size: ${props => props.theme.fontSizes.medium};
  display: flex;
  align-items: center;
`;

const VerifiedIcon = styled.img`
  width: 16px;
  height: 16px;
  margin-left: 4px;
`;

const TimeAgo = styled.span`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const MoreOptions = styled.span`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.medium};
`;

const PostContent = styled.p`
  color: ${props => props.theme.colors.white};
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: 12px;
  line-height: 1.5;
`;

const PostImage = styled.img`
  width: 100%;
  border-radius: 8px;
  margin-bottom: 12px;
`;

const PostActions = styled.div`
  display: flex;
  align-items: center;
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

const ActionCount = styled.span`
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
  margin-left: 8px;
`;

const PostStats = styled.div`
  display: flex;
  align-items: center;
  margin-top: 8px;
`;

const StatItem = styled.div`
  display: flex;
  align-items: center;
  margin-right: 16px;
  color: ${props => props.theme.colors.gray};
  font-size: ${props => props.theme.fontSizes.small};
`;

const PostCard: React.FC<PostCardProps> = ({
  username,
  userAvatar,
  verified = false,
  timeAgo,
  content,
  image,
  likes,
  answers,
  onLike,
  onComment,
  onShare,
  onRepost
}) => {
  return (
    <PostCardContainer>
      <PostHeader>
        <UserInfo>
          <UserAvatar src={userAvatar} alt={username} />
          <UserDetails>
            <Username>
              {username}
              {verified && <VerifiedIcon src="/src/assets/images/verified.png" alt="Verified" />}
            </Username>
            <TimeAgo>{timeAgo}</TimeAgo>
          </UserDetails>
        </UserInfo>
        <MoreOptions>•••</MoreOptions>
      </PostHeader>
      
      <PostContent>{content}</PostContent>
      
      {image && <PostImage src={image} alt="Post image" />}
      
      <PostStats>
        <StatItem>{answers} answers</StatItem>
        <StatItem>•</StatItem>
        <StatItem>{likes} likes</StatItem>
      </PostStats>
      
      <PostActions>
        <ActionButton onClick={onLike}>
          <ActionIcon src="/src/assets/images/actions/like.png" alt="Like" />
        </ActionButton>
        <ActionButton onClick={onComment}>
          <ActionIcon src="/src/assets/images/actions/comment.png" alt="Comment" />
        </ActionButton>
        <ActionButton onClick={onRepost}>
          <ActionIcon src="/src/assets/images/actions/repost.png" alt="Repost" />
        </ActionButton>
        <ActionButton onClick={onShare}>
          <ActionIcon src="/src/assets/images/actions/share.png" alt="Share" />
        </ActionButton>
      </PostActions>
    </PostCardContainer>
  );
};

export default PostCard;
