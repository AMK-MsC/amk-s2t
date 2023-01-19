import { Box, Center, Text } from "@chakra-ui/react";
import { useEffect, useRef, useState } from "react";
import { HuggingFaceAPI } from "./api";



const AudioUpload = (): JSX.Element => {

    const [countDown, setCountDown] = useState<number>(10);

    useEffect(() => {
        const initializeModel = async () => {
            const response = await HuggingFaceAPI.initializeModel();
            setCountDown(response.estimated_time)
            console.log(countDown)
        }

        void initializeModel();
    }, [])

    // Timer that counts down from countDown to 0 and updates the state every second
    useEffect(() => {
        const timer = setTimeout(() => {
            if (countDown > 0) {
                setCountDown(countDown - 1);
            }
        }, 1000);
        return () => clearTimeout(timer);
    }, [countDown]);


    // Upload audio from local file system
    const audioRef = useRef<HTMLAudioElement>(null);


    const uploadAudio = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const objectUrl = URL.createObjectURL(file);
            if (audioRef.current) {
                audioRef.current.src = objectUrl;
                audioRef.current.play();
            }
        }
    };
    
    

    return (
        <Center>
            {countDown === 0 ? (
                <Box>
                    <Text>Model initialized. Please upload an audio file.</Text>
                    <input type="file" onChange={uploadAudio} />
                    <audio ref={audioRef} controls />
                </Box>
            ) : (
                <Box>
                    <Text>Initializing model. Please wait {countDown} seconds.</Text>
                </Box>
            )}
        </Center>
    );

};

export default AudioUpload;