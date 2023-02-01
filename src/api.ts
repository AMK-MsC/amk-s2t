const HuggingFaceAPI = {
    initializeModel: async () => {

        try {
            const response = await fetch("https://api-inference.huggingface.co/models/oyvindgrutle/amk-whisper",
                {
                    headers: { Authorization: `Bearer ${process.env.REACT_APP_HUGGINGFACE_TOKEN}` },
                    method: "POST",
                    body: "start",
                }
            )
            console.log(`Response status code: ${response.status}`)
            if (response.status == 503) {
                const result = await response.json();
                console.log(`Result: ${result.estimated_time}`);
                return result;
            }
        }
        catch (error) {
            console.log(`Error: ${error}`);
        }
    },

    checkModel: async () => {
        try {
            const response = await fetch("https://api-inference.huggingface.co/models/oyvindgrutle/amk-whisper",
                {
                    headers: { Authorization: `Bearer ${process.env.REACT_APP_HUGGINGFACE_TOKEN}` },
                    method: "POST",
                    body: "start",
                }
            )
            console.log("check model")
            if (response.status != 503) {
                return true;
            }
        }
        catch (error) {
            console.log(`Error: ${error}`);
        }
    },

    transcribeAudio: async (audio: Blob) => {
        console.log("audio inference")
        try {
            const response = await fetch("https://api-inference.huggingface.co/models/oyvindgrutle/amk-whisper",
                {
                    headers: { Authorization: `Bearer ${process.env.REACT_APP_HUGGINGFACE_TOKEN}`},
                    method: "POST",
                    body: audio,

                }
            )
            console.log(`Response status code: ${response.status}`)
            if (response.status == 200) {
                const result = await response.json();
                console.log(`Result: ${result.transcript}`);
                return result;
            }
        } catch (error) {
            console.log(`Error: ${error}`);
            return error;
        }
    }
}

export default HuggingFaceAPI;