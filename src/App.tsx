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
import AudioUpload from "./AudioUpload"

export const App = () => (
  <ChakraProvider theme={theme}>
    <Box alignContent="center">
      <Header />
      <AudioUpload />
    </Box>
  </ChakraProvider>
)
