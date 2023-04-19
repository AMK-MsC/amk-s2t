import { extendTheme, ThemeConfig } from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "dark",
  useSystemColorMode: false, // Add this if you don't want to use the system color mode
};

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: {
        bg: "mode.background",
        color: "mode.text",
      },
    },
  },
  colors: {
    mode: {
      background: {
        light: "red.100",
        dark: "gray.800",
      },
      text: {
        light: "#bee3f8",
        dark: "#2a4365",
      },
      heading: {
        light: "#1A365D",
        dark: "#bee3f8",
      },
    },
  },
});

export default theme;
