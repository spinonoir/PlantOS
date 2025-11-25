import { DarkTheme, DefaultTheme, Theme } from "@react-navigation/native";

const palette = {
  forest: "#1B4332",
  mint: "#74C69D",
  sand: "#F0EAD2",
  charcoal: "#1F1F1F",
  white: "#FFFFFF",
  lightGray: "#F3F4F6",
  gray: "#6B7280",
  red: "#EF4444",
};

export const lightTheme: Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: palette.forest,
    background: palette.white,
    card: palette.white,
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

// Extended theme object for direct usage
export const theme = {
  colors: {
    primary: palette.forest,
    secondary: palette.mint,
    background: palette.white,
    surface: palette.lightGray,
    text: palette.charcoal,
    textSecondary: palette.gray,
    border: "#E5E5E5",
    error: palette.red,
  }
};
