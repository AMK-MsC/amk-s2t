import { Box, Center, Flex, HStack, Spacer, Text, useColorModeValue } from "@chakra-ui/react";
import { ColorModeSwitcher} from "./ColorModeSwitcher";

const Header = (): JSX.Element => {

    //use font color based on color mode
    const fontColor = useColorModeValue("mode.header.light", "mode.header.dark");

    return (
        <Center>
            <Flex alignContent="center" padding={5}>
                <Box>

                    <Text fontSize="5xl" as="b" color={fontColor}>AMK SPEECH-TO-TEXT</Text>
                </Box>
            </Flex>
            <ColorModeSwitcher />
        </Center>

    );
};

export default Header;