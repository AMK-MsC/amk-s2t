from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from transformers import WhisperForConditionalGeneration, WhisperProcessor, GenerationConfig, pipeline
import librosa
import torch
import torchaudio
from lib import generate_srt_file, generate_srt_text, generate_doc_text
from pyannote.audio import Pipeline
import json
from diarization import get_speaker_list, label_transcriptions

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

whisper_pipeline = pipeline(
  "automatic-speech-recognition",
  model="oyvindgrutle/amk-whisper",
  chunk_length_s=30,
  device=device,
)

dz_pipeline = Pipeline.from_pretrained(
    'pyannote/speaker-diarization', 
    use_auth_token="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"
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
    audio_file = request.files['file']

    # save audio file as  wav file
    audio_file.save('audio.wav')

    
    #print(f"file: {audio_file.filename.split('.')[0]}")
    #audio, sr = librosa.load(audio_file, sr=16000)
    #data_waveform, sr = torchaudio.load(audio_file)
    #Convert audio numpy array to tensor
    #tensor = torch.from_numpy(audio)

   # print(f"Tensor info: {torchaudio.info}")
    #audio_dict = {"waveform": tensor, "sample_rate": sr}

    #print("Audio dict: ", audio_dict)
    #print(type(audio_dict['waveform']))
    #print(f"Audio; {audio}\nAudio type: {type(audio)}")
    #print(f"Audio file: {audio_file}\nAudio file type: {type(audio_file)}")

    # we can also return timestamps for the predictions
    transcription = whisper_pipeline("audio.wav", return_timestamps=True)["chunks"]
    dz = dz_pipeline("audio.wav", min_speakers=2, max_speakers=5)

    print(f"Transcription: {transcription}")
    print(f"Diarization: {dz}")

    speaker_list = get_speaker_list(dz)

    print(speaker_list)

    labeled_transcriptions = label_transcriptions(transcription, speaker_list)

    # generate_srt_file(prediction, "{audio_file.filename.split('.')[0]}.srt")
    srt_text = generate_srt_text(labeled_transcriptions)
    doc_text = generate_doc_text(labeled_transcriptions)

    print(srt_text)
    print(doc_text)

    data = {}
    data['doc_text'] = doc_text
    data['srt_text'] = srt_text


    return jsonify(data)

        
if __name__ == '__main__':
    app.run()