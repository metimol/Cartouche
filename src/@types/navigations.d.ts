declare type RootStackParamList = {
  Detail: undefined;
  Tabs: undefined;
};

declare type StackParamList = {
  Detail: undefined;
};

declare type HomeScreenNavigationProp = CompositeNavigationProp<
  StackNavigationProp<StackParamList, "Home">
>;
