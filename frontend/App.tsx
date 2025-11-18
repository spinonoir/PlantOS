import "react-native-gesture-handler";

import { NavigationContainer } from "@react-navigation/native";
import { StatusBar } from "expo-status-bar";
import { useColorScheme } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";

import { useNotificationBootstrap } from "@/hooks/useNotifications";
import { AppNavigator } from "@/navigation/AppNavigator";
import { darkTheme, lightTheme } from "@/theme";

export default function App() {
  const scheme = useColorScheme();
  useNotificationBootstrap();

  return (
    <SafeAreaProvider>
      <NavigationContainer theme={scheme === "dark" ? darkTheme : lightTheme}>
        <StatusBar style={scheme === "dark" ? "light" : "dark"} />
        <AppNavigator />
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
