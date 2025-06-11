import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
full_path = os.path.join(BASE_DIR, ".env")
normal_env_path = os.path.normpath(full_path)

env = load_dotenv(normal_env_path)
API_ENV_HOST: str = os.getenv("API_HOST")
API_ENV_PORT: int = int(os.getenv("API_PORT"))
API_DEFAULT_USERNAME = os.getenv("API_USERNAME")
API_DEFAULT_PASSWORD = os.getenv("API_PASSWORD")


@dataclass
class VOSK_MODEL_PATHS:
    BIG_3_5GB_RU_010: str = "stt_VOSK/models_vosk/vosk-model-ru-0.10"
    BIG_2_5GB_RU_022: str = "stt_VOSK/models_vosk/vosk-model-ru-0.22"
    BIG_3_5GB_RU_042: str = "stt_VOSK/models_vosk/vosk-model-ru-0.42"
    SMALL_87MB_RU_022: str = "stt_VOSK/models_vosk/vosk-model-small-ru-0.22"
    RECASEPUNC_2GB_RU_022: str = "stt_VOSK/models_vosk/vosk-recasepunc-ru-0.22"


@dataclass
class WHISPER_MODEL_NAMES:
    """Whisper models available:
    - tiny - the smallest and fastest model_obj, but with low accuracy.
    - base - a balance between speed and accuracy.
    - small - more accurate but slower.
    - medium - high accuracy but requires more resources.
    - large - the most accurate, the slowest and most demanding on resources."""
    TINY: str = "tiny"
    BASE: str = "base"
    SMALL: str = "small"
    MEDIUM: str = "medium"
    LARGE: str = "large"


@dataclass
class API_CONFIGS:
    BASE_HOST: str = API_ENV_HOST
    BASE_PORT: int = API_ENV_PORT

    INIT_VOSK_MODEL: bool = True
    # INIT_VOSK_MODEL: bool = False
    VOSK_MODEL_PATH: str = VOSK_MODEL_PATHS.SMALL_87MB_RU_022
    VOSK_AUDIO_FRAME_RATE: int = 16000
    VOSK_AUDIO_CHANNELS_NUM: int = 1
    VOSK_ALLOWED_AUDIO_TYPES: tuple = ("audio/wav", "audio/mpeg", "audio/mp3",)
    VOSK_ALLOWED_AUDIO_EXTENSIONS: tuple = (".wav", ".mp3",)

    # INIT_VOSK_PUNCTUATOR_MODEL = True
    INIT_VOSK_PUNCTUATOR_MODEL = False
    VOSK_PUNCTUATOR_MODEL_PATH: str = VOSK_MODEL_PATHS.RECASEPUNC_2GB_RU_022

    INIT_WHISPER_MODEL: bool = True
    # INIT_WHISPER_MODEL: bool = False
    WHISPER_MODEL_NAME: str = WHISPER_MODEL_NAMES.LARGE
    WHISPER_AUDIO_FRAME_RATE: int = 16000
    WHISPER_AUDIO_CHANNELS_NUM: int = 1
    WHISPER_ALLOWED_AUDIO_TYPES: tuple = ("audio/wav", "audio/mpeg", "audio/mp3",)
    WHISPER_ALLOWED_AUDIO_EXTENSIONS: tuple = (".wav", ".mp3",)

    INCOMING_AUDIO_FILES_PATH: str = "data_incoming/mp3_samples_KIROV"
