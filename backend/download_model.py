import torch
from transformers import pipeline
import librosa
from lib import generate_srt_file

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  model="Jethuestad/amk-whisper-v5.5",  # Gets model from HuggingFace
  chunk_length_s=30,
  device=device,
)

audio_file = "backend/data/113-samtale_part0.wav"

audio, _ = librosa.load(audio_file, sr=16000)

# we can also return timestamps for the predictions
prediction = pipe(audio, return_timestamps=True)["chunks"]
generate_srt_file(prediction, "backend/data/outputs/" + audio_file.split("/")[-1].split(".")[0] + ".srt")
print(prediction)

pipe.save_pretrained("amk-whisper-local")  # Saves model to local once in order to use it later