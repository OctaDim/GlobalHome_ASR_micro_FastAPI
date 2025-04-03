from dataclasses import dataclass


@dataclass
class VOSK_MODELS:
    path_big_model_3_5GB: str = "stt_VOSK/models_vosk/vosk-model-ru-0.10"
    path_big_model_2_5GB: str = "stt_VOSK/models_vosk/vosk-model-ru-0.22"
    path_small_model_45_MB: str = "stt_VOSK/models_vosk/vosk-model-small-ru-0.22"
