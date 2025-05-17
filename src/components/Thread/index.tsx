import React from "react";

import * as S from "./styles";
import { IThread } from "./types";

const Thread = ({ post, ...rest }: IThread) => {
  const Post = () => {
    if (post) {
      return (
        <S.ContainerPost {...rest}>
          <S.Row>
            <S.Username>{post.username}</S.Username>
            <S.Verified source={require("../../assets/images/verified.png")} />
          </S.Row>
          <S.Post>{post.post}</S.Post>
          {post.postImage && <S.PostImage source={{ uri: post.postImage }} />}
        </S.ContainerPost>
      );
    }
  };

  const ActionButtons = () => (
    <S.ContainerActions>
      <S.Action>
        <S.Icon source={require("../../assets/images/actions/like.png")} />
      </S.Action>
      <S.Action>
        <S.Icon source={require("../../assets/images/actions/comment.png")} />
      </S.Action>
      <S.Action>
        <S.Icon source={require("../../assets/images/actions/reply.png")} />
      </S.Action>
      <S.Action>
        <S.Icon source={require("../../assets/images/actions/share.png")} />
      </S.Action>
    </S.ContainerActions>
  );

  const Interactions = () => (
    <S.ContainerInteractions>
      <S.AvatarGroupContent>
        <S.Row>
          <S.AvatarGroup
            h="16"
            w="16"
            source={{
              uri: "https://randomuser.me/api/portraits/men/84.jpg",
            }}
          />
          <S.AvatarGroup
            top="-8"
            source={{
              uri: "https://randomuser.me/api/portraits/men/85.jpg",
            }}
          />
        </S.Row>
        <S.AvatarGroup
          top="-4"
          h="12"
          w="12"
          source={{
            uri: "https://randomuser.me/api/portraits/men/86.jpg",
          }}
        />
      </S.AvatarGroupContent>
      <S.Likes>
        {post.answers.length} answers - {post.likes} likes
      </S.Likes>
    </S.ContainerInteractions>
  );

  return (
    <S.Container>
      <S.Row>
        <S.AlignCenter>
          <S.Avatar source={{ uri: post.avatar_uri }} />
          <S.Line />
        </S.AlignCenter>
        <S.Column>
          <Post />
          <ActionButtons />
        </S.Column>
      </S.Row>
      <Interactions />
    </S.Container>
  );
};

export default Thread;
