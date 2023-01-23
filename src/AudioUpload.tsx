import { Box, Button, Center, Text, VStack } from "@chakra-ui/react";
import { useEffect, useRef, useState } from "react";
import HuggingFaceAPI from "./api";



const AudioUpload = (): JSX.Element => {

    const [countDown, setCountDown] = useState<number>(0);
    const [audio, setAudio] = useState<Blob>();
    const [loading, setLoading] = useState<boolean>(false);
    const [transcript, setTranscript] = useState<string>();

    useEffect(() => {
        const initializeModel = async () => {
            try {
                const response = await HuggingFaceAPI.initializeModel();
                setCountDown(parseInt(response.estimated_time))
                console.log(countDown)
            } catch (error) {
                console.log(error);
            }
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
            setAudio(file);
            const objectUrl = URL.createObjectURL(file);
            console.log(objectUrl);
            if (audioRef.current) {
                audioRef.current.src = objectUrl;
                audioRef.current.play();
            }
        }
    };

    const transcribeAudio = async (file: Blob) => {
        setLoading(true);
        if (!file) {
            return;
        }
        const response = await HuggingFaceAPI.transcribeAudio(file);
        console.log(response);
        setLoading(false);
        setTranscript(response.text)
    };



    return (
        <Center>
            {countDown === 0 ? (
                <VStack>
                    <Box>
                        <Text>Model initialized. Please upload an audio file.</Text>
                        <input type="file" onChange={uploadAudio} />
                        <audio ref={audioRef} controls />
                    </Box>
                    <Box>
                        {loading ? <Text>Transcribing audio. Please wait.</Text> : <Button onClick={() => transcribeAudio(audio!)}>Transcribe</Button>}
                    </Box>
                    <Box>
                        <Text>{transcript}</Text>
                    </Box>
                </VStack>
            ) : (
                <Box>
                    <Text>Initializing model. Please wait {countDown} seconds.</Text>
                </Box>
            )}
        </Center>
    );

};

export default AudioUpload;