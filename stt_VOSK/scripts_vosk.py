import os

from configs.settings import API_CONFIGS, BASE_DIR
from configs.console_colors import CONSOLE_COLORS
from stt_VOSK.funcs_vosk import get_str_from_wav_vosk
from stt_VOSK.init_vosk import vosk_model_instance
from stt_VOSK.init_vosk_punctuator import vosk_punctuator_model_instance
from utils_common.convert_save_mp3_to_wav import convert_save_mp3_to_wav
from utils_common.get_dir_file_names import get_directory_file_names
from utils_common.normalized_path import (
    get_all_dirs_norm_path, get_full_file_normal_path)


vosk_model_inst = vosk_model_instance
vosk_punctuator_inst = vosk_punctuator_model_instance

full_dir_path = get_all_dirs_norm_path(
    all_dirs_paths=[BASE_DIR, API_CONFIGS.INCOMING_AUDIO_FILES_PATH])

wav_file_names = get_directory_file_names(full_dir_path=full_dir_path)

audio_files_paths = []
for file_name in wav_file_names:
    full_file_path = get_full_file_normal_path(
        all_dirs_paths=[BASE_DIR, API_CONFIGS.INCOMING_AUDIO_FILES_PATH],
        file_name=file_name)
    audio_files_paths.append(full_file_path)

if not audio_files_paths:
    print(f"No files in directory defined in settings [ERROR]: "
          f"full_dir_path: {full_dir_path}\n")

for cur_audio_path in audio_files_paths:
    print(f"{'#' * 95}")
    if not cur_audio_path:
        print(f"Full file path not found [ERROR]: {cur_audio_path}\n")
        continue

    new_wav_full_path = None
    if cur_audio_path.endswith(".mp3"):
        new_wav_full_path = convert_save_mp3_to_wav(
            mp3_full_path=cur_audio_path,
            wav_frame_rate=API_CONFIGS.VOSK_AUDIO_FRAME_RATE,
            wav_channels=API_CONFIGS.VOSK_AUDIO_CHANNELS_NUM)
        cur_audio_path = new_wav_full_path

    if not cur_audio_path.endswith(".wav"):
        print(f"File format not 'wav' [ERROR]: {cur_audio_path}\n")

    phrase = get_str_from_wav_vosk(model_obj=vosk_model_inst,
                                   full_file_path=cur_audio_path,
                                   log_wav_path=True,
                                   log_wav_duration=True)

    if new_wav_full_path and os.path.exists(new_wav_full_path):
        os.remove(new_wav_full_path)

    if API_CONFIGS.INIT_VOSK_PUNCTUATOR_MODEL and vosk_punctuator_inst:
        try:
            new_phrase = vosk_punctuator_inst.recase(phrase)
            print(f"Punctuation [OK]: "
                  f"new_phrase: {new_phrase}, phrase: {phrase}\n")
        except Exception as error:
            print(f"Punctuation [ERROR]: "
                  f"error: {error}, phrase: {phrase}\n")

    green_color, reset_color = CONSOLE_COLORS.GREEN, CONSOLE_COLORS.RESET
    print(f"Recognized Phrase: {green_color}{phrase}{reset_color}\n")
