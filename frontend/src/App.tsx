import {
  ChakraProvider,
  Box,
} from "@chakra-ui/react"
import Header from "./Header"
import AudioUpload from "./AudioUpload"
import theme from "./theme"

export const App = () => (
  <ChakraProvider theme={theme}>
    <Box alignContent="center">
      <Header />
      <AudioUpload />
    </Box>
  </ChakraProvider>
)
