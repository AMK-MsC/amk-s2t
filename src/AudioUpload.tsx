import { Box, Button, Center, HStack, Input, SimpleGrid, Text, Textarea, VStack } from "@chakra-ui/react";
import { SetStateAction, useEffect, useRef, useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import API from "./api";



const AudioUpload = (): JSX.Element => {

    const [audio, setAudio] = useState<File>();
    const [audioFile, setAudioFile] = useState<File>();
    const [loading, setLoading] = useState<boolean>(false);
    const [srtTranscript, setSrt] = useState<string>();
    const [docTranscript, setDocTranscript] = useState<string>();



    // Upload audio from local file system
    const audioRef = useRef<HTMLAudioElement>(null);

    // useEffect when audio is uploaded. Use uploadAudio function to set audio file
    useEffect(() => {
        if (audio) {
            uploadAudio(audio);
        }
    }, [audio]);




    const uploadAudio = async (audio: File) => {
        if (audio) {
            setAudioFile(audio);
            const objectUrl = URL.createObjectURL(audio);
            console.log(objectUrl);
            if (audioRef.current) {
                audioRef.current.src = objectUrl;
            }
        }
    };

    //handle change function while file is uploaded. setFile to uploaded file

    const handleChange = (file: File) => {
        setAudio(file);
    };

    const transcribeAudio = async (file: Blob) => {
        setLoading(true);
        setDocTranscript("");
        if (!file) {
            setLoading(false);
            return;
        }
        try {
            const response = await API.transcribeAudio(file, audioFile!.name);
            setLoading(false);
            setDocTranscript(response.doc_text);
            setSrt(response.srt_text);
        } catch (error) {
            setDocTranscript("An error occurred while transcribing the audio. Please try again.");
            console.log(error);
            setLoading(false);
        }

    };

    // download transcript as a doc file
    const downloadTranscript = async () => {
        const element = document.createElement("a");
        // file as .docx
        const file = new Blob([docTranscript!], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
        element.href = URL.createObjectURL(file);
        element.download = `${audioFile!.name.slice(0, -4)}.doc`;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
    }

    const handleTranscriptChange = (event: { target: { value: SetStateAction<string | undefined>; }; }) => {
        setDocTranscript(event.target.value);
    }

    // download transcript as a srt file

    const downloadTranscriptSrt = async () => {
        const element = document.createElement("a");


        const file = new Blob([srtTranscript!], { type: 'application/octet-stream' });
        element.href = URL.createObjectURL(file);
        element.download = `${audioFile!.name.slice(0, -4)}.srt`;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
    }




    return (
        <Center>
            <SimpleGrid columns={1} alignContent="center" gap={5}>
                <VStack spacing={5}>
                    <FileUploader
                        multiple={false}
                        handleChange={handleChange}
                        types={['WAV']}
                    />
                    <Text>{audio ? `${audio.name}` : ""}</Text>
                    <audio ref={audioRef} controls />
                </VStack>
                <Button
                    isLoading={loading}
                    loadingText='Transcribing'
                    spinnerPlacement="end"
                    variant='outline'
                    onClick={() => transcribeAudio(audio!)}>Transcribe
                </Button>
                {docTranscript && (
                    <>
                        <Box padding="10px" borderRadius="2xl">
                            <Textarea
                                size="lg"
                                minWidth="600px"
                                minHeight="300px"
                                value={docTranscript}
                                onChange={handleTranscriptChange}
                            />
                        </Box>
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