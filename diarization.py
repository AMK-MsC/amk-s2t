import librosa
from pyannote.audio import Pipeline
import torch
import datetime

starttime = datetime.datetime.now()
pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="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")
print("pyanote:",  datetime.datetime.now() - starttime)


audio_file = "audio/113-samtale test.wav"


audio, sr = librosa.load(audio_file, sr=16000)

dz = pipeline(audio_file, min_speakers=2, max_speakers=5)
print("diarization:", datetime.datetime.now() - starttime)


from transformers import pipeline
from lib import generate_srt_file

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipe = pipeline(
  "automatic-speech-recognition",
  #model="oyvindgrutle/amk-whisper",
  model="amk-whisper",  # Gets model from local instead of HuggingFace
  chunk_length_s=30,
  device=device,
)
print("pipeline whisper:", datetime.datetime.now() - starttime)

predictions = pipe(audio_file, return_timestamps=True)["chunks"]

print("predictions:", datetime.datetime.now() - starttime)


def get_speaker_list(diarization):
    speaker_list = []
    speaker_mo = ""
    speaker_i = ""
    for track in diarization.itertracks(yield_label=True):
        if track[0].start < 2:
            continue

        # Find the speaker labels
        if not speaker_mo:
            if track[2] == "SPEAKER_00":
                speaker_mo = "SPEAKER_00"
                speaker_i = "SPEAKER_01"
            else:
                speaker_mo = "SPEAKER_01"
                speaker_i = "SPEAKER_00"
        
        if track[2] == speaker_mo:
            speaker_id = "MO"
        elif track[2] == speaker_i:
            speaker_id = "I"
            
        speaker_list.append([track[0].start, track[0].end, speaker_id])
    return speaker_list

def label_transcriptions(transcriptions, speakers):
    labeled_transcriptions = []

    for transcription in transcriptions:
        # If the median of transcription is inside of timerange of speaker, then label it with that speaker
        transcription_median = (transcription["timestamp"][0] + transcription["timestamp"][1]) / 2
        closest_speaker_index = find_bucket(speakers, transcription_median)
        if closest_speaker_index == 0:
            # Do the same but round down the median to closest integer
            transcription_median = int(transcription_median)
            closest_speaker_index = find_bucket(speakers, transcription_median)


        labeled_transcriptions.append({
            "timestamp": [transcription["timestamp"][0],transcription["timestamp"][1]],
            "text": speakers[closest_speaker_index][2] + ": " + transcription["text"],
            "speaker_label": speakers[closest_speaker_index][2]
        })

    return labeled_transcriptions

def find_bucket(speakers, transcription_median):
    closest_speaker_index = 0
    for i, speaker in enumerate(speakers):
        if transcription_median >= speaker[0] and transcription_median <= speaker[1]:
            closest_speaker_index = i
            break
    return closest_speaker_index



speaker_list = get_speaker_list(dz)

labeled_predictions = label_transcriptions(predictions, speaker_list)

generate_srt_file(labeled_predictions, "output_lydlogg-1.srt")