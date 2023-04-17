from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import torch
from lib import generate_srt_text, generate_doc_text
from pyannote.audio import Pipeline
from diarization import get_speaker_list, label_transcriptions

app = Flask(__name__)
CORS(app)


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
    
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['file']
    # print entire file name'
    print(audio_file.filename)
    file_name = audio_file.filename

    audio_file.save(file_name)

    transcription = whisper_pipeline(file_name, return_timestamps=True)["chunks"]
    dz = dz_pipeline(file_name, min_speakers=2, max_speakers=5)

    speaker_list = get_speaker_list(dz)

    labeled_transcriptions = label_transcriptions(transcription, speaker_list)

    srt_text = generate_srt_text(labeled_transcriptions)
    doc_text = generate_doc_text(labeled_transcriptions)

    data = {}
    data['doc_text'] = doc_text
    data['srt_text'] = srt_text


    return jsonify(data)

        
if __name__ == '__main__':
    app.run()