import * as React from "react"
import {
  ChakraProvider,
  Box,
  Text,
  Link,
  VStack,
  Code,
  Grid,
  theme,
} from "@chakra-ui/react"
import { ColorModeSwitcher } from "./ColorModeSwitcher"
import Header from "./Header"

export const App = () => (
  <ChakraProvider theme={theme}>
    <Box alignContent="center">
      <Header />
    </Box>
  </ChakraProvider>
)
