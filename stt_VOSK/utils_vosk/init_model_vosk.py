from vosk import Model

from configs.settings import API_CONFIGS, BASE_DIR
from utilities_common.exec_time_decorator import execution_time_decorator
from utilities_common.normalized_path import get_all_dirs_norm_path


class SingletonVOSK(Model):
    _vosk_singleton = None

    def __new__(cls):
        if not cls._vosk_singleton:
            cls._vosk_singleton = super().__new__(cls)
        return cls._vosk_singleton


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          new_line_after=True,
                          note="VOSK Model initialization time")
def vosk_model_initializing(model_path: str) -> Model:
    vosk_model = SingletonVOSK(model_path=model_path)
    # vosk_model = Model(model_path=model_path)
    return vosk_model


vosk_model_obj = None

if API_CONFIGS.INIT_VOSK_MODEL:
    vosk_model_path = get_all_dirs_norm_path(
        [BASE_DIR, API_CONFIGS.CUR_VOSK_MODEL])

    vosk_model_obj = vosk_model_initializing(
        model_path=vosk_model_path)
