
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
            console.log(`Response status code: ${response.status}`)
            if (response.status == 503){
                const result = await response.json();
                console.log(`Result: ${result.estimated_time}`);
                return result;
            }
        }
        catch (error) {
            console.log(`Error: ${error}`);
        }
    }
}

export { HuggingFaceAPI };