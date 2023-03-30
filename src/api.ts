const API = {
    
    transcribeAudio: async (audio: Blob, name: string) => {
        const data = new FormData();
        data.append("file", audio, name);
        console.log(data)
        try {
            const response = await fetch("http://localhost:5000/transcribe",
                {
                    method: "POST",
                    body: data,
                }
            )
            if (response.ok) {
                const result = await response.json();
                return result;
            } else {
                throw new Error(`${response.status}`);
            }
        } catch (error) {
            console.log(`${error}`);
            return null;
        }
    },
}

export default API;