import React from "react";

import * as S from "./styles";
import CardUser from "../../components/CardUser";
import { useNavigation, useRoute } from "@react-navigation/native";
import Thread from "../../components/Thread";

const Detail = () => {
  const navigation = useNavigation();
  const route = useRoute<HomeScreenNavigationProp>();

  const { user, post } = route.params;

  return (
    <S.Container>
      <S.SafeArea />
      <S.Header>
        <S.BackButton onPress={() => navigation.goBack()}>
          <S.Back>Voltar</S.Back>
        </S.BackButton>
        <S.Heading>Thread</S.Heading>
      </S.Header>
      <S.List>
        <CardUser user={user} />
        <Thread post={post} />
      </S.List>
    </S.Container>
  );
};

export default Detail;
