import torch
from transformers import pipeline
import librosa
from lib import generate_srt_file

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="oyvindgrutle/amk-whisper",
  chunk_length_s=30,
  device=device,
)

audio_file = "Lydlogg-2-test-113.wav"

audio, _ = librosa.load(audio_file, sr=16000)

# we can also return timestamps for the predictions
prediction = pipe(audio, return_timestamps=True)["chunks"]
generate_srt_file(prediction, "output.srt")
print(prediction)
