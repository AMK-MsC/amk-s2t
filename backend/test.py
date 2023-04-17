from transformers import WhisperForConditionalGeneration, WhisperProcessor, GenerationConfig
import librosa
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = WhisperForConditionalGeneration.from_pretrained("oyvindgrutle/amk-whisper").to(device)
processor = WhisperProcessor.from_pretrained("oyvindgrutle/amk-whisper")
forced_decoder_ids = processor.get_decoder_prompt_ids(language="no", task="transcribe")

generation_config = GenerationConfig.from_pretrained("openai/whisper-base")
model.generation_config = generation_config

audio_file = "Lydlogg-2-test-113.wav"

audio, _ = librosa.load(audio_file, sr=16000)
input_features = processor.feature_extractor(audio, sampling_rate=16_000, return_tensors="pt").input_features.to(device)
predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids, return_timestamps=True)
result = processor.tokenizer.decode(predicted_ids.cpu()[0], decode_with_timestamps=True, output_offsets=True)
print(result)