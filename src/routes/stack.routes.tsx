import { createStackNavigator } from "@react-navigation/stack";
import Detail from "../screens/Detail";
import TabRoutes from "./tab.routes";

const Stack = createStackNavigator<RootStackParamList>();

const StackRoutes = () => {
  return (
    <Stack.Navigator
      initialRouteName="Tabs"
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name="Detail" component={Detail} />
      <Stack.Screen name="Tabs" component={TabRoutes} />
    </Stack.Navigator>
  );
};

export default StackRoutes;
