# IMPORTANT: pip install openai-whisper (try first, if not working,
# execute pip install whisper also in addition to the first step)
# pip uninstall numpy
# pip install numpy==2.1.0
# (newer version is not acceptable)

# import os
# import wave
# from datetime import datetime
#
# import numpy
# import whisper
#
# from configs.settings import WHISPER_configs
# from data_incoming.incoming_wav_file_paths.incoming_wav_paths import (
#     wav_file_paths)
#
#
# def load_wav_file(file_path):
#     with wave.open(file_path, 'rb') as wav_file_obj:
#         total_frames_num = wav_file_obj.getnframes()
#         audio_data = wav_file_obj.readframes(total_frames_num)
#         audio_array = numpy.frombuffer(audio_data, dtype=numpy.int16)
#         sample_rate = wav_file_obj.getframerate()
#     return audio_array, sample_rate
#
#
# def get_text_from_wav(full_wav_file_path):
#     audio_array, sample_rate = load_wav_file(full_wav_file_path)
#     transcribed_text = model.transcribe(audio_array.astype(numpy.float32))
#     print(f"Recognized TEXT PHRASE: {transcribed_text}\n")
#     return transcribed_text
#
#
# model_name = WHISPER_configs.tiny_model
#
# prev_time = datetime.now()
# model = whisper.load_model(model_name)
# cur_time = datetime.now()
# print(f"Model obj initialization time: "
#       f"{(cur_time - prev_time).total_seconds()}\n")
#
# for cur_path in wav_file_paths:
#     if not cur_path:
#         continue
#     wav_normal_path = os.path.normpath(cur_path)
#     phrase = get_text_from_wav(full_wav_file_path=wav_normal_path)
