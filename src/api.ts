
const HuggingFaceAPI = {
    initializeModel: async () => {
        console.log("start model")
        try {
            const response = await fetch("https://api-inference.huggingface.co/models/openai/whisper-large-v2",
                {
                    headers: { Authorization: `Bearer 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` },
                    method: "POST",
                    body: "start",
                }
            )
            if (response.status == 503){
                const result = await response.json();
                return result;
            }
        }
        catch (error) {
            console.log(error);
        }
    }
}

export { HuggingFaceAPI };