from configs.settings import API_CONFIGS
from stt_WHISPER.utils_whisper.funcs_whisper import (
    whisper_model_initializing)


whisper_model_obj = None

if API_CONFIGS.INIT_WHISPER_MODEL:
    # whisper_model_path = get_all_dirs_norm_path(
    #     [BASE_DIR, API_CONFIGS.CUR_WHISPER_MODEL])

    whisper_model_name = API_CONFIGS.CUR_WHISPER_MODEL
    whisper_model_obj = whisper_model_initializing(
        model_name=whisper_model_name)
