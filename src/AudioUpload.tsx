import { Box, Button, Center, HStack, Input, SimpleGrid, Text, Textarea, VStack } from "@chakra-ui/react";
import { SetStateAction, useEffect, useRef, useState } from "react";
import API from "./api";



const AudioUpload = (): JSX.Element => {

    const [audio, setAudio] = useState<File>();
    const [audioFile, setAudioFile] = useState<File>();
    const [loading, setLoading] = useState<boolean>(false);
    const [transcript, setTranscript] = useState<string>();
    const [audioUrl, setAudioUrl] = useState<string>();



    // Upload audio from local file system
    const audioRef = useRef<HTMLAudioElement>(null);


    const uploadAudio = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setAudio(file);
            setAudioFile(file);
            const objectUrl = URL.createObjectURL(file);
            console.log(objectUrl);
            if (audioRef.current) {
                audioRef.current.src = objectUrl;
                //audioRef.current.play();
            }
        }
    };

    const transcribeAudio = async (file: Blob) => {
        setLoading(true);
        if (!file) {
            setLoading(false);
            return;
        }
        const response = await API.transcribeAudio(file);
        console.log(response);
        setLoading(false);
        setTranscript(response);
    };

    // download transcript as a doc file
    const downloadTranscript = async () => {
        const element = document.createElement("a");
        // file as .docx
        const file = new Blob([transcript!], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
        element.href = URL.createObjectURL(file);
        element.download = `${audioFile!.name.slice(0, -4)}.doc`;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
    }

    const handleTranscriptChange = (event: { target: { value: SetStateAction<string | undefined>; }; }) => {
        setTranscript(event.target.value);
    }

    // download transcript as a srt file

    const downloadTranscriptSrt = async () => {
        const element = document.createElement("a");


        const file = new Blob([transcript!], { type: 'application/octet-stream' });
        element.href = URL.createObjectURL(file);
        element.download = `${audioFile!.name.slice(0, -4)}.srt`;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
    }




    return (
        <Center>
            <SimpleGrid columns={1} alignContent="center" gap={5}>
                <Box>
                    <input type="file" onChange={uploadAudio} />
                    <audio ref={audioRef} controls />
                </Box>
                <Box>
                    <Button
                        isLoading={loading}
                        loadingText='Submitting'
                        //colorScheme='teal'
                        variant='outline'
                        onClick={() => transcribeAudio(audio!)}>Transcribe
                    </Button>
                </Box>
                {transcript && (
                    <>
                        <Box padding="10px" borderRadius="2xl">
                            <Textarea
                                size="lg"
                                minWidth="600px"
                                minHeight="300px"
                                value={transcript}
                                onChange={handleTranscriptChange}
                            />
                        </Box>
                        {/* whenClicked is a property not an event, per se. */}
                        <HStack>
                            <Button onClick={downloadTranscript}>Download Transcript as .doc</Button>
                            <Button onClick={downloadTranscriptSrt}>Download Transcript as .srt</Button>
                        </HStack>
                    </>
                )}
            </SimpleGrid>
        </Center>
    );

};

export default AudioUpload;