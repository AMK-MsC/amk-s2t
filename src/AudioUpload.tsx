import { Box, Center, Text } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { HuggingFaceAPI } from "./api";



const AudioUpload = (): JSX.Element => {

    const [countDown, setCountDown] = useState<number>(20);

    useEffect(() => {
        const initializeModel = async () => {
            const response = await HuggingFaceAPI.initializeModel();
            setCountDown(response.estimated_time)
            console.log(countDown)
        }

        void initializeModel();
    }, [])

    //Count down timer based on countDown state and stop when countDown is 0
    useEffect(() => {
        const timer = setTimeout(() => {
            if (countDown > 0) {
                setCountDown(countDown - 1);
            }
        }, 1000);
        return () => clearTimeout(timer);
    }, [countDown]);


    return (
        <Center>
            <Box>
                <Text>Hei du har {countDown} sekund igjen å leva :p</Text>
            </Box>
        </Center>
    );
};

export default AudioUpload;