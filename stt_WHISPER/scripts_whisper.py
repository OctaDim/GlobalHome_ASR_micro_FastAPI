import os

from configs.console_colors import CONSOLE_COLORS
from configs.settings import API_CONFIGS, BASE_DIR
from stt_WHISPER.funcs_whisper import get_str_from_wav_whisper
from utils_common.convert_save_mp3_to_wav import convert_and_save_mp3_to_wav
from utils_common.dir_files_names_paths import get_dir_files_only_names
from utils_common.normalized_path import (
    get_full_dir_normal_path, get_full_file_normal_path)


def execute_scripts_whisper():
    from stt_WHISPER.init_whisper import whisper_model_instance
    full_dir_path = get_full_dir_normal_path(
        all_dir_str_parts=[BASE_DIR, API_CONFIGS.SCRIPT_IN_AUDIO_FILES_PATH])

    audio_file_names = get_dir_files_only_names(full_dir_path=full_dir_path)

    audio_files_paths = []
    for audio_file_name in audio_file_names:
        full_file_path = get_full_file_normal_path(
            all_dir_str_parts=[BASE_DIR, API_CONFIGS.SCRIPT_IN_AUDIO_FILES_PATH],
            file_name_with_ext=audio_file_name)
        audio_files_paths.append(full_file_path)

    if not audio_files_paths:
        print(f"No files in directory defined in settings [ERROR]: "
              f"full_dir_path: {full_dir_path}\n")

    counter = 0
    total_files = len(audio_files_paths)
    for cur_audio_path in audio_files_paths:
        print(f"{'#' * 95}")
        counter += 1
        if not cur_audio_path:
            print(f"Full file path not found [ERROR]: {cur_audio_path}\n")
            continue

        new_wav_full_path = None
        if cur_audio_path.endswith(".mp3"):
            new_wav_full_path = convert_and_save_mp3_to_wav(
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

        if new_wav_full_path and os.path.exists(new_wav_full_path):
            os.remove(new_wav_full_path)

        green_color, reset_color = CONSOLE_COLORS.BRIGHT_GREEN, CONSOLE_COLORS.RESET
        print(f"{counter}/{total_files} Recognized Phrase: "
              f"{green_color}{phrase}{reset_color}\n")


if __name__ == "__main__":
    execute_scripts_whisper()
