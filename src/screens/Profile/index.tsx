import Button from "../../components/Button";

import { Tabs } from "react-native-collapsible-tab-view";

import * as S from "./styles";
import React from "react";
import { ListRenderItemInfo, StyleSheet } from "react-native";
import { dark } from "../../themes/dark";
import Thread from "../../components/Thread";

import posts from "../../assets/json/posts.json";
import { IPost } from "../../components/Thread/types";
import CardUser from "../../components/CardUser";

const Profile = () => {
  const Header = () => {
    return (
      <>
        <S.Header>
          <S.ButtonIcon> 
            <S.Icon source={require("../../assets/images/privacy.png")} />
          </S.ButtonIcon>
          <S.Header>
            <S.ButtonIcon mr="24">   
              <S.Icon source={require("../../assets/images/instagram.png")} />
            </S.ButtonIcon>
            <S.ButtonIcon>
              <S.Icon
                source={require("../../assets/images/configuration.png")}
              />
            </S.ButtonIcon>
          </S.Header>
        </S.Header>
        <CardUser />
        <S.ContainerButtons>
          <Button text="Edit profile" inverted />
          <S.Spacing />
          <Button text="Share profile" inverted />
        </S.ContainerButtons>
      </>
    );
  };

  return (
    <S.Container>
      <S.SafeArea
        style={{ backgroundColor: dark.colors.background, zIndex: 99 }}
      />

      <Tabs.Container
        allowHeaderOverscroll
        renderHeader={Header}
        renderTabBar={(props) => <S.CustomTabBar {...props} />}
        headerContainerStyle={{ backgroundColor: dark.colors.background }}
      >
        <Tabs.Tab name="chirps" label={() => <S.TabLabel>Chirps</S.TabLabel>}>
          <Tabs.FlatList
            data={posts}
            ItemSeparatorComponent={S.Divider}
            keyExtractor={(item: IPost) => `${item.id}`}
            renderItem={({ item }: ListRenderItemInfo<IPost>) => (
              <Thread post={item} />
            )}
            onRefresh={null}
          />
        </Tabs.Tab>
        <Tabs.Tab name="B" label={() => <S.TabLabel>Answers</S.TabLabel>}>
          {/* <Tabs.ScrollView>
            <Thread />
            <Thread />
            <Thread />
          </Tabs.ScrollView> */}
        </Tabs.Tab>
      </Tabs.Container>
    </S.Container>
  );
};

const styles = StyleSheet.create({
  box: {
    flex: 1,
    width: "100%",
  },
  boxA: {
    backgroundColor: "white",
  },
  boxB: {
    backgroundColor: "red",
  },
  header: {
    width: "100%",
    backgroundColor: "red",
  },
});

export default Profile;
