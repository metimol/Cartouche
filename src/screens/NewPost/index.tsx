import React from "react";

import * as S from "./styles";

import { BottomSheetModal } from "@gorhom/bottom-sheet";

import Feather from "@expo/vector-icons/Feather";

import { dark } from "../../themes/dark";

const NewPost = () => {

  // ref
  const bottomSheetModalRef = React.useRef<BottomSheetModal>(null);

  // variables
  const snapPoints = React.useMemo(() => ["92%"], []);

  // callbacks
  const handlePresentModalPress = React.useCallback(() => {
    bottomSheetModalRef.current?.present();
  }, []);

  const handleCloseModalPress = React.useCallback(() => {
    bottomSheetModalRef.current?.close();
  }, []);

  return (
    <S.Container>
      <S.Button onPress={handlePresentModalPress}>
        <S.Icon source={require("../../assets/images/tab/post.png")} />
      </S.Button>
      <S.BottomModal
        enablePanDownToClose={false}
        ref={bottomSheetModalRef}
        index={0}
        snapPoints={snapPoints}
      >
        <S.CancelButton onPress={handleCloseModalPress}>
          <S.Cancel>Cancel</S.Cancel>
        </S.CancelButton>
        <S.Heading>New chirp</S.Heading>

        <S.Divider />
        <S.Content>
          <S.Row>
            <S.AlignCenter>
              <S.Avatar
                source={{
                  uri: "https://randomuser.me/api/portraits/men/86.jpg",
                }}
              />
              <S.Line />
              <S.AvatarSmall
                source={{
                  uri: "https://randomuser.me/api/portraits/men/86.jpg",
                }}
              />
            </S.AlignCenter>
            <S.Column>
              <S.Username>melieskubrick</S.Username>
              <S.Input
                placeholder="Start a new chirp..."
                placeholderTextColor={dark.colors.gray}
              />
              <S.ButtonAttach>
                <Feather name="paperclip" size={24} color={dark.colors.gray} />
              </S.ButtonAttach>
            </S.Column>
          </S.Row>
        </S.Content>
      </S.BottomModal>
    </S.Container>
  );
};

export default NewPost;
