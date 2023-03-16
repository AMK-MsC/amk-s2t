const API = {
    
    transcribeAudio: async (audio: Blob) => {
        const data = new FormData();
        data.append("file", audio, "file");
        try {
            const response = await fetch("http://localhost:5000/pipeline/audio",
                {
                    method: "POST",
                    body: data,
                }
            )
            console.log(`Response status code: ${response.status}`)
            if (response.status == 200) {
                const result = await response.json();
                console.log(`Result: ${result}`);
                return result;
            }
        } catch (error) {
            console.log(`Error: ${error}`);
            return error;
        }
    },
}

export default API;