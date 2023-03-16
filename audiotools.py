from pydub import AudioSegment
import csv
import math

def split_audio_file(audio:AudioSegment, save_path, start, stop, filename):
    newAudio = audio[start:stop]
    newAudio = newAudio.set_frame_rate(16000)
    newAudio.export(f"{save_path}/audio/{filename}.wav", format="wav") #Exports to a wav file in the current path.

def fullsplit_audio_file(path, save_path, sec_per_split=30):
    
    oldAudio = AudioSegment.from_wav(path)
    total_sec = math.ceil(oldAudio.duration_seconds) # Using ceiling to get max num of splits
    
    metadata_header = "file_name"
    write_metadata_csv(metadata_header, save_path, True)
    
    for i in range(0, math.ceil(total_sec/sec_per_split)): 
        start = i * sec_per_split * 1000       # Works in milliseconds
        stop = (i+1) * sec_per_split * 1000
        newName = "113-samtale_part" + str(i)
        split_audio_file(oldAudio, save_path, start, stop, newName)
        write_metadata_csv(f"audio/{newName}.wav", save_path)


def custom_audio_split(path, save_path, time_list):
    
    oldAudio = AudioSegment.from_wav(path)
    
    metadata_header = "file_name"
    write_metadata_csv(metadata_header, save_path, True)
    
    
    for i, (start, stop) in enumerate(time_list):
        newName = "113-samtale_part" + str(i)
        split_audio_file(oldAudio, save_path, start*1000, stop*1000, newName)
        write_metadata_csv(f"audio/{newName}.wav", save_path)


def write_metadata_csv(data, save_path, overwrite=False):
    if overwrite:
        task = "w"
    else:
        task = "a"
        
    with open(f"{save_path}/metadata.csv", task, encoding="UTF8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data])


