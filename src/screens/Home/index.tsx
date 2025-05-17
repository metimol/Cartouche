import React from "react";

import posts from "../../assets/json/posts.json";

import * as S from "./styles";
import { IPost } from "../../components/Thread/types";
import { ListRenderItemInfo } from "react-native";
import Thread from "../../components/Thread";
import { useNavigation } from "@react-navigation/native";

const Home = () => {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  return (
    <S.Container>
      <S.SafeArea />
      <S.List
        data={posts}
        keyExtractor={(item: IPost) => `${item.id}`}
        renderItem={({ item }: ListRenderItemInfo<IPost>) => (
          <Thread
            post={item}
            onPress={() =>
              navigation.navigate("Detail", {
                user: {
                  name: item.name,
                  username: item.username,
                  bio: "Biografia do usuário",
                  followers: "130 followers",
                  avatar_uri: item.avatar_uri,
                },
                post: item,
              })
            }
          />
        )}
        ItemSeparatorComponent={S.Divider}
      />
    </S.Container>
  );
};

export default Home;
