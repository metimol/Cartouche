import "react-native-gesture-handler";

import { StatusBar } from "expo-status-bar";

import Routes from "./src/routes";
import { dark } from "./src/themes/dark";

import React from "react";
import { BottomSheetModalProvider } from "@gorhom/bottom-sheet";

export default function App() {
  return (
    <>
      <StatusBar backgroundColor={dark.colors.background} style="light" />
      <BottomSheetModalProvider>
        <Routes />
      </BottomSheetModalProvider>
    </>
  );
}
