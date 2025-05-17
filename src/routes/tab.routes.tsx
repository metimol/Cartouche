import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Home from "../screens/Home";
import { dark } from "../themes/dark";
import { Image } from "react-native";
import { ITabIcon } from "./tab.types";
import Profile from "../screens/Profile";
import Search from "../screens/Search";
import Activities from "../screens/Activities";
import NewPost from "../screens/NewPost";
import NewThreadModal from "../components/NewThreadModal";

const AppTab = createBottomTabNavigator();

const TabRoutes = ({ navigation }) => {
  const TabIcon = ({ focused, imageName, imageFocusedName }: ITabIcon) => (
    <Image source={focused ? imageFocusedName : imageName} />
  );

  return (
    <AppTab.Navigator
      screenOptions={{
        tabBarStyle: {
          backgroundColor: dark.colors.background,
          borderTopWidth: 0,
          paddingTop: 16,
        },
        headerShown: false,
        title: "",
      }}
      id="TabRoutes"
    >
      <AppTab.Screen
        options={{
          tabBarIcon: ({ focused }) => (
            <TabIcon
              focused={focused}
              imageName={require("../assets/images/tab/home.png")}
              imageFocusedName={require("../assets/images/tab/home_focused.png")}
            />
          ),
        }}
        name="Home"
        component={Home}
      />
      <AppTab.Screen
        options={{
          tabBarIcon: ({ focused }) => (
            <TabIcon
              focused={focused}
              imageName={require("../assets/images/tab/search.png")}
              imageFocusedName={require("../assets/images/tab/search_focused.png")}
            />
          ),
        }}
        name="Search"
        component={Search}
      />
      <AppTab.Screen
        options={{
          tabBarButton: () => <NewPost />,
        }}
        name="NewThread"
        component={NewPost}
      />
      <AppTab.Screen
        options={{
          tabBarIcon: ({ focused }) => (
            <TabIcon
              focused={focused}
              imageName={require("../assets/images/tab/activity.png")}
              imageFocusedName={require("../assets/images/tab/activity_focused.png")}
            />
          ),
        }}
        name="Activities"
        component={Activities}
      />
      <AppTab.Screen
        options={{
          tabBarIcon: ({ focused }) => (
            <TabIcon
              focused={focused}
              imageName={require("../assets/images/tab/profile.png")}
              imageFocusedName={require("../assets/images/tab/profile_focused.png")}
            />
          ),
        }}
        name="Profile"
        component={Profile}
      />
    </AppTab.Navigator>
  );
};

export default TabRoutes;
