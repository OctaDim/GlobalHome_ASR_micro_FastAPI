from configs.settings import API_CONFIGS, BASE_DIR
from data_incoming.incoming_wav_file_paths.incoming_wav_paths import (
    wav_file_paths)
from stt_WHISPER.utils_whisper.funcs_whisper import (
    get_str_from_wav_whisper, whisper_model_initializing)
from stt_WHISPER.utils_whisper.init_model_whisper import (
    whisper_model_obj)
from utilities_common.normalized_path import get_all_dirs_norm_path


model_name = API_CONFIGS.CUR_WHISPER_MODEL
model_obj = whisper_model_initializing(model_name=model_name)

for cur_wav_path in wav_file_paths:
    wav_path = get_all_dirs_norm_path(
        [BASE_DIR, "data_incoming/", cur_wav_path])

    if not cur_wav_path:
        continue

    phrase = get_str_from_wav_whisper(model=whisper_model_obj,
                                      full_file_path=wav_path,
                                      log_wav_path=True,
                                      log_wav_duration=True)
    print(f"Recognized Phrase: {phrase}\n")
