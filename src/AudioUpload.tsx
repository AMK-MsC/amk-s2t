import { Box, Button, Center, Input, SimpleGrid, Text, Textarea, VStack } from "@chakra-ui/react";
import { SetStateAction, useEffect, useRef, useState } from "react";
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

    // check if model is initialized when countDown is divisible by 20
    useEffect(() => {
        const checkModel = async () => {
            try {
                const response = await HuggingFaceAPI.checkModel();
                if (response) {
                    setCountDown(0);
                }
            } catch (error) {
                console.log(error);
            }
        }
        void checkModel();
    }, [countDown % 20 == 0 && countDown > 0])

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
                //audioRef.current.play();
            }
        }
    };

    const transcribeAudio = async (file: Blob) => {
        setTranscript("");
        setLoading(true);
        if (!file) {
            return;
        }
        const response = await HuggingFaceAPI.transcribeAudio(file);
        console.log(response);
        setLoading(false);
        if (response.text === "") {
            setTranscript("No speech detected");
            return;
        }
        setTranscript(response.text)
    };

    // download transcript as a doc file
    const downloadTranscript = async () => {
        const element = document.createElement("a");
        // file as .docx
        const file = new Blob([transcript!], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
        element.href = URL.createObjectURL(file);
        element.download = `transcription.docx`;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
    }

    const handleTranscriptChange = (event: { target: { value: SetStateAction<string | undefined>; }; }) => {
        setTranscript(event.target.value);
    }




    return (
        <Center>
            {countDown === 0 ? (
                <SimpleGrid columns={1} alignContent="center" gap={5}>
                    <Box>
                        <input type="file" onChange={uploadAudio} />
                        <audio ref={audioRef} controls />
                    </Box>
                    <Box>
                        {loading ? <Text>Transcribing audio. Please wait.</Text> : <Button onClick={() => transcribeAudio(audio!)}>Transcribe</Button>}
                    </Box>
                    {transcript && (
                        <>
                            <Box padding="10px" borderRadius="2xl" bgColor="blue.800">
                                <Textarea
                                    size="lg"
                                    minWidth="600px"
                                    minHeight="300px"
                                    value={transcript}
                                    onChange={handleTranscriptChange}
                                />
                            </Box>
                            <Button onClick={downloadTranscript}>Download Transcript</Button>
                        </>
                    )}
                </SimpleGrid>
            ) : (
                <Box>
                    <Text>Initializing model. Estimated time remaining: {countDown}s</Text>
                </Box>
            )}
        </Center>
    );

};

export default AudioUpload;