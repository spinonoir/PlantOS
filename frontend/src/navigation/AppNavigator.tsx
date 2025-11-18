import { Feather } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { useNavigation } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { Pressable } from "react-native";

import { DiagnosticsScreen } from "@/screens/DiagnosticsScreen";
import { ExperimentsScreen } from "@/screens/ExperimentsScreen";
import { HomeScreen } from "@/screens/HomeScreen";
import { MarketplaceScreen } from "@/screens/MarketplaceScreen";
import { NewPlantScreen } from "@/screens/NewPlantScreen";
import { PlantDetailScreen } from "@/screens/PlantDetailScreen";
import type { RootStackParamList } from "@/types/navigation";

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();

function HomeTabScreens() {
  const navigation =
    useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerRight: () =>
          route.name === "Home" ? (
            <Pressable
              onPress={() => navigation.navigate("NewPlant")}
              style={{ marginRight: 12 }}
            >
              <Feather name="plus" size={20} color="#1B4332" />
            </Pressable>
          ) : null,
        tabBarIcon: ({ color, size }) => {
          const icons: Record<string, keyof typeof Feather.glyphMap> = {
            Home: "leaf",
            Diagnostics: "activity",
            Experiments: "sliders",
            Marketplace: "shopping-bag",
          };
          return (
            <Feather
              name={icons[route.name] ?? "circle"}
              size={size}
              color={color}
            />
          );
        },
      })}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: "Plants" }}
      />
      <Tab.Screen name="Diagnostics" component={DiagnosticsScreen} />
      <Tab.Screen name="Experiments" component={ExperimentsScreen} />
      <Tab.Screen name="Marketplace" component={MarketplaceScreen} />
    </Tab.Navigator>
  );
}

export function AppNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="Tabs"
        component={HomeTabScreens}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="PlantDetail"
        component={PlantDetailScreen}
        options={{ title: "Plant Detail" }}
      />
      <Stack.Screen
        name="NewPlant"
        component={NewPlantScreen}
        options={{ presentation: "modal", title: "New Plant" }}
      />
    </Stack.Navigator>
  );
}
