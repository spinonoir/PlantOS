import { DarkTheme, DefaultTheme, Theme } from "@react-navigation/native";

const palette = {
  forest: "#1B4332",
  mint: "#74C69D",
  sand: "#F0EAD2",
  charcoal: "#1F1F1F",
};

export const lightTheme: Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: palette.forest,
    background: "#FFFFFF",
    card: "#FFFFFF",
    text: palette.charcoal,
    border: "#E5E5E5",
    notification: palette.mint,
  },
};

export const darkTheme: Theme = {
  ...DarkTheme,
  colors: {
    ...DarkTheme.colors,
    primary: palette.mint,
    background: "#0B1D16",
    card: "#13291F",
    text: "#F5F7F2",
    border: "#1F4333",
    notification: palette.mint,
  },
};
