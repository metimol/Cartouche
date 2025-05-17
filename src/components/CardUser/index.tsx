import React from "react";

import * as S from "./styles";
import { IUser } from "./types";

const CardUser = ({ user }: IUser) => {
  return (
    <S.Container>
      <S.Row>
        <S.Column>
          <S.Name>{user ? user.name : "Melies Kubrick"}</S.Name>
          <S.ContainerUsername>
            <S.Username>{user ? user.username : "melieskubrick"}</S.Username>
            <S.TagContainer>
              <S.Tag>chirp</S.Tag>
            </S.TagContainer>
          </S.ContainerUsername>
        </S.Column>

        <S.Column>
          <S.Avatar
            source={{
              uri: user
                ? user.avatar_uri
                : "https://randomuser.me/api/portraits/men/86.jpg",
            }}
          />
          <S.Verified source={require("../../assets/images/verified.png")} />
        </S.Column>
      </S.Row>
      <S.Bio>{user ? user.bio : "Programmer"}</S.Bio>
      <S.AvatarGroupContainer>
        <S.AvatarGroup
          source={{ uri: "https://randomuser.me/api/portraits/men/86.jpg" }}
        />
        <S.AvatarGroup
          ml="-8"
          source={{ uri: "https://randomuser.me/api/portraits/women/3.jpg" }}
        />
        <S.AvatarGroup
          ml="-8"
          source={{ uri: "https://randomuser.me/api/portraits/men/31.jpg" }}
        />
        <S.Followers>{user ? user.followers : "200"} followers</S.Followers>
      </S.AvatarGroupContainer>
    </S.Container>
  );
};

export default CardUser;
