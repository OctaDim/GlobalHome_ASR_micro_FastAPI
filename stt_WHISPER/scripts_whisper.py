from configs.settings import API_CONFIGS, BASE_DIR
from stt_WHISPER.funcs_whisper import get_str_from_wav_whisper
from stt_WHISPER.init_whisper import whisper_model_instance
from utils_common.convert_save_mp3_to_wav import convert_save_mp3_to_wav
from utils_common.get_dir_file_names import get_directory_file_names
from utils_common.normalized_path import (
    get_all_dirs_norm_path, get_full_file_normal_path)


whisper_model_obj = whisper_model_instance

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
    print(f"{'#' * 120}")
    if not cur_audio_path:
        print(f"Full file path not found [ERROR]: {cur_audio_path}\n")
        continue

    if cur_audio_path.endswith(".mp3"):
        new_wav_full_path = convert_save_mp3_to_wav(
            mp3_full_path=cur_audio_path,
            wav_frame_rate=API_CONFIGS.WHISPER_AUDIO_FRAME_RATE,
            wav_channels=API_CONFIGS.WHISPER_AUDIO_CHANNELS_NUM)
        cur_audio_path = new_wav_full_path

    if not cur_audio_path.endswith(".wav"):
        print(f"File format not 'wav' [ERROR]: {cur_audio_path}\n")

    phrase = get_str_from_wav_whisper(model_obj=whisper_model_instance,
                                      full_file_path=cur_audio_path,
                                      log_wav_path=True,
                                      log_wav_duration=True)
    print(f"Recognized Phrase: {phrase}\n")
