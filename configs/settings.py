from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from configs.creds_from_env import API_ENV_HOST, API_ENV_PORT
from stt_VOSK.configs_vosk.models_paths_vosk import VOSK_MODELS
from stt_WHISPER.configs_whisper.models_names_whisper import WHISPER_MODELS


BASE_DIR = Path(__file__).resolve().parent.parent



@dataclass
class API_CONFIGS:
    BASE_HOST: str = API_ENV_HOST
    BASE_PORT: int = API_ENV_PORT

    INIT_VOSK_MODEL: bool = True
    # INIT_WHISPER_MODEL: bool = True
    # INIT_VOSK_MODEL: bool = False
    INIT_WHISPER_MODEL: bool = False

    CUR_VOSK_MODEL: str = VOSK_MODELS.path_big_model_3_5GB
    CUR_WHISPER_MODEL: str = WHISPER_MODELS.base_model
