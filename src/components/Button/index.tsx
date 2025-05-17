import React from "react";

import * as S from "./styles";
import { IButton } from "./types";

const Button = ({ inverted, text }: IButton) => {
  return (
    <S.Btn inverted={inverted}>
      <S.BtnText inverted={inverted}>{text}</S.BtnText>
    </S.Btn>
  );
};

export default Button;
