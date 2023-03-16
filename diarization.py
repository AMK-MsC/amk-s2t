import librosa
from pyannote.audio import Pipeline
import torch

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="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")

audio_file = "audio/113-samtale test.wav"

audio, sr = librosa.load(audio_file, sr=16000)

dz = pipeline(audio_file, min_speakers=2, max_speakers=5)


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

predictions = pipe(audio_file, return_timestamps=True)["chunks"]



# Make a list of list where each elemnt is a list of the form [start, stop, speaker]
# where start and stop are the start and stop time of the speaker in seconds
# and speaker is the speaker label where SPEAKER_00 == MO and SPEAKER_01 == I
# This is the format that is needed for the generate_srt_file function
# in the pipeline.py file
# If start time is < 2, then ignore that segment from the resulting speaker_list
def get_speaker_list(diarization):
    speaker_list = []
    for track in diarization.itertracks(yield_label=True):
        if track[2] == "SPEAKER_00":
            speaker_id = "I"
        elif track[2] == "SPEAKER_01":
            speaker_id = "MO"
        if track[0].start > 2:
            speaker_list.append([track[0].start, track[0].end, speaker_id])
    return speaker_list

speaker_list = get_speaker_list(dz)

print(speaker_list, len(speaker_list))
print(predictions, len(predictions))


# Takes a list of transcriptions that includes dictionaries with keys "timestamp" and "text".
# The values of "timestamp" is a list with start time then end time.
# Also takes a list of speakers with start and end times
# and returns a list of transcriptions with start and end times and speaker labels.
# All transcriptions have a speaker label, so label the transcriptions with the closest
# matching speaker label.
# If a transcription has a start time that is before the first speaker label, then
# label the transcription with the first speaker label.
def label_transcriptions(transcriptions, speakers):
    # If the first transcription starts before the first speaker label, then label
    # the transcription with the first speaker label
    if transcriptions[0]['timestamp'][0] < speakers[0][0]:
        transcriptions[0]['speaker'] = speakers[0][2]
        transcriptions[0]['text'] = speakers[0][2] + ": " + transcriptions[0]['text']
    else:
        # Find the first speaker label that is after the first transcription
        for speaker in speakers:
            if speaker[0] > transcriptions[0]['timestamp'][0]:
                transcriptions[0]['speaker'] = speaker[2]
                transcriptions[0]['text'] = speaker[2] + ": " + transcriptions[0]['text']
                break
    # Label the rest of the transcriptions
    for i in range(1, len(transcriptions)):
        for speaker in speakers:
            if speaker[0] > transcriptions[i]['timestamp'][0]:
                transcriptions[i]['speaker'] = speaker[2]
                transcriptions[i]['text'] = speaker[2] + ": " + transcriptions[i]['text']
                break
    return transcriptions

labeled_predictions = label_transcriptions(predictions, speaker_list)

generate_srt_file(labeled_predictions, "output.srt")
print(labeled_predictions)