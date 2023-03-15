from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from transformers import WhisperForConditionalGeneration, WhisperProcessor, GenerationConfig, pipeline
import librosa
import torch
from lib import generate_srt_file

app = Flask(__name__)
CORS(app)

# device = "cuda" if torch.cuda.is_available() else "cpu"

#model = WhisperForConditionalGeneration.from_pretrained("oyvindgrutle/amk-whisper").to(device)
#processor = WhisperProcessor.from_pretrained("oyvindgrutle/amk-whisper")
#forced_decoder_ids = processor.get_decoder_prompt_ids(language="no", task="transcribe")

#generation_config = GenerationConfig.from_pretrained("openai/whisper-base")
#model.generation_config = generation_config

if torch.cuda.is_available():
    device = torch.cuda.current_device()
else:
    device = "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="oyvindgrutle/amk-whisper",
  chunk_length_s=30,
  device=device,
)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# endpoint to receive audio file and return text
@app.route('/audio', methods=['POST'])
def audio():
    if request.method == 'POST':
        # get audio file
        audio_file = request.files['audio']
        print(audio_file)
        # save audio file
        #audio_file.save('audio.wav')
        # return text

        audio, _ = librosa.load(audio_file, sr=16000)
        input_features = processor.feature_extractor(audio, sampling_rate=16_000, return_tensors="pt").input_features.to(device)
        predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids, return_timestamps=True, max_new_tokens=100000)
        result = processor.tokenizer.decode(predicted_ids.cpu()[0], decode_with_timestamps=True, output_offsets=True)

        return jsonify(result["offsets"])
    
@app.route('/pipeline/audio', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    print(f"file: {audio_file.filename.split('.')[0]}")
    audio, _ = librosa.load(audio_file, sr=16000)

    # we can also return timestamps for the predictions
    prediction = pipe(audio, return_timestamps=True)["chunks"]

    generate_srt_file(prediction, f"{audio_file.filename.split('.')[0]}.srt")

    return jsonify(prediction)

        
if __name__ == '__main__':
    app.run()