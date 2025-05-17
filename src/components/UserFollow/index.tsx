import React from "react";

import * as S from "./styles";
import Button from "../Button";
import { IUserFollow } from "./types";

const UserFollow = ({ user }: IUserFollow) => {
  return (
    <S.Container>
      <S.Row>
        <S.Row>
          <S.Avatar source={{ uri: user.avatar_uri }} />
          {user.message && (
            <S.UserContainerIcon>
              <S.UserIcon
                source={require("../../assets/images/tab/profile_focused.png")}
              />
            </S.UserContainerIcon>
          )}
        </S.Row>
        <S.Column>
          <S.Row>
            <S.Username>{user.username}</S.Username>
            <S.Verified source={require("../../assets/images/verified.png")} />
          </S.Row>
          {user.message ? (
            <S.Message>{user.message}</S.Message>
          ) : (
            <S.Name>{user.name}</S.Name>
          )}

          {!user.message && (
            <S.Followers>{user.followers} followers</S.Followers>
          )}
        </S.Column>
      </S.Row>
      <S.ContainerButton>
        <Button inverted text="Follow" />
      </S.ContainerButton>
    </S.Container>
  );
};

export default UserFollow;
