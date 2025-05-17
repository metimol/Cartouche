import React from "react";
import { View } from "react-native";

import * as S from "./styles";

const NewThreadModal = (focused: boolean) => {
  return (
    <S.Btn>
      <S.Icon source={require("../../assets/images/tab/post.png")} />
    </S.Btn>
  );
};

export default NewThreadModal;
