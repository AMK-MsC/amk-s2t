import { Box, Center, Flex, HStack, Text } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";

const Header = (): JSX.Element => {
    return (
        <Box marginTop={0} w="100%">
            <Center borderColor="lightcyan" m="2rem auto">
                <HStack>
                    <Text fontSize="5xl" as="b" color="blue.100"> AMK SPEECH-TO-TEXT</Text>
                </HStack>
            </Center>
        </Box>
    );
};

export default Header;