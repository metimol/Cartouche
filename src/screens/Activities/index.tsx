import React from "react";

import * as S from "./styles";

import users from "../../assets/json/users_request.json";
import UserFollow from "../../components/UserFollow";
import { ListRenderItemInfo } from "react-native";

const Activities = () => {
  const [selectedItem, setSelectedItem] = React.useState();

  const CATEGORIES = [
    {
      name: "All",
    },
    {
      name: "Answers",
    },
    {
      name: "Mentions",
    },
    {
      name: "Verified",
    },
  ];

  return (
    <S.Container>
      <S.SafeArea />
      <S.Header>
        <S.Title>Activity</S.Title>
      </S.Header> 
      <S.ContainerList>
        <S.CategoriesList
          horizontal
          data={CATEGORIES}
          renderItem={({ item, index }) => (
            <S.ButtonCategories
              focused={selectedItem === index}
              onPress={() => setSelectedItem(index)}
            >
              <S.ButtonText focused={selectedItem === index}>
                {item.name}
              </S.ButtonText>
            </S.ButtonCategories>
          )}
        />
      </S.ContainerList>
      <S.List
        data={users}
        keyExtractor={(item: IUser) => `${item.id}`}
        ItemSeparatorComponent={S.Divider}
        renderItem={({ item }: ListRenderItemInfo<IUserRequest>) => (
          <UserFollow user={item} />
        )}
      />
    </S.Container>
  );
};

export default Activities;
