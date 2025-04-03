from configs.settings import API_CONFIGS, BASE_DIR
from data_incoming.incoming_wav_file_paths.incoming_wav_paths import (
    wav_file_paths)

from stt_VOSK.utils_vosk.funcs_vosk import (
    get_str_from_wav_path_vosk)
from stt_VOSK.utils_vosk.init_model_vosk import vosk_model_initializing, vosk_model_obj
from utilities_common.normalized_path import get_all_dirs_norm_path


path_to_model = get_all_dirs_norm_path(
    [BASE_DIR, API_CONFIGS.CUR_VOSK_MODEL])

model_obj = vosk_model_initializing(model_path=path_to_model)

for cur_wav_path in wav_file_paths:
    wav_path = get_all_dirs_norm_path(
        [BASE_DIR, "data_incoming/", cur_wav_path])

    if not cur_wav_path:
        continue
    phrase = get_str_from_wav_path_vosk(model=vosk_model_obj,
                                        full_file_path=wav_path,
                                        log_wav_path=True,
                                        log_wav_duration=True)
    print(f"Recognized Phrase: {phrase}\n")
