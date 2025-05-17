import React from "react";
import { ListRenderItemInfo } from "react-native";

import * as S from "./styles";
import { dark } from "../../themes/dark";

import Feather from "@expo/vector-icons/Feather";
import UserFollow from "../../components/UserFollow";

import users from "../../assets/json/users.json";

const Search = () => {
  return (
    <S.Container>
      <S.SafeArea />
      <S.Header>
        <S.Title>Search</S.Title>
        <S.ContainerInput>
          <Feather name="search" color={dark.colors.gray} size={20} />
          <S.Input
            placeholder="Search"
            placeholderTextColor={dark.colors.gray}
          />
        </S.ContainerInput>
      </S.Header>
      <S.List
        data={users}
        keyExtractor={(item: IUser) => `${item.id}`}
        ItemSeparatorComponent={S.Divider}
        renderItem={({ item }: ListRenderItemInfo<IUser>) => (
          <UserFollow user={item} />
        )}
      />
    </S.Container>
  );
};

export default Search;
