import { Box, Center, Flex, HStack, Spacer, Text } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";

const Header = (): JSX.Element => {
    return (
        <Center>
            <Flex alignContent="center" padding={5}>
                <Box>
                    <Text fontSize="5xl" as="b" color="blue.100">AMK SPEECH-TO-TEXT</Text>
                </Box>
            </Flex>
            <ColorModeSwitcher />
        </Center>

    );
};

export default Header;