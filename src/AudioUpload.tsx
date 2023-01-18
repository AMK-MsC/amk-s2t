import { Box, Center, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { HuggingFaceAPI } from "./api";



const AudioUpload = (): JSX.Element => {

    const [countDown, setCountDown] = useState();

    useEffect(() => {
        const response = HuggingFaceAPI.initializeModel();
        console.log(response);
    })
    return (
        <Center>
            <Box>
                <Text>Hei</Text>
            </Box>
        </Center>
    );
};

export default AudioUpload;