from datetime import timedelta
import os

def generate_srt_file(input_data, output_file_path):
    with open(output_file_path, 'w') as output_file:
        segment_index = 1
        for segment_data in input_data:
            start_time = segment_data['timestamp'][0]
            end_time = segment_data['timestamp'][1]
            text = segment_data['text']
            output_file.write(f"{segment_index}\n")
            output_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            output_file.write(f"{text.strip()}\n\n")
            segment_index += 1

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def generate_srt_text(input_data):
    output_text = ""
    count = 0
    segment_index = 1
    for segment_data in input_data:
        start_time = segment_data['timestamp'][0]
        end_time = segment_data['timestamp'][1]
        text = segment_data['text']
        output_text += f"{segment_index}\n"
        output_text += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        output_text += f"{text.strip()}\n\n"

        segment_index += 1
    return output_text

def generate_doc_text(input_data):
    count = 0
    output_text = ""
    for segment_data in list(input_data):
        text = segment_data['text']
        output_text += f"{text.strip()}\n"


    return output_text
