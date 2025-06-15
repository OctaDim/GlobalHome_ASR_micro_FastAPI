import os
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

full_path = os.path.join(BASE_DIR, ".env")
normal_env_path = os.path.normpath(full_path)

env = load_dotenv(normal_env_path)  # just to stay import
# API_ENV_HOST: str = os.getenv("API_HOST")
# API_ENV_PORT: int = int(os.getenv("API_PORT"))
# API_ENV_USERNAME = os.getenv("API_USERNAME")
# API_ENV_PASSWORD = os.getenv("API_PASSWORD")

@dataclass
class API_CONFIG_NAMES:
    API_PRODUCT_SERVER_IP = "API_prod_server_ip_8000"
    API_TEST_ANY_PORT_IP = "API_test_0_0_0_0_8000"
    API_TEST_LOCALHOST = "API_test_127_0_0_1_8000"


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
    INIT_VOSK_MODEL: bool = True
    # INIT_VOSK_MODEL: bool = False
    VOSK_MODEL_PATH: str = VOSK_MODEL_PATHS.SMALL_87MB_RU_022
    VOSK_AUDIO_FRAME_RATE: int = 16000
    VOSK_AUDIO_CHANNELS_NUM: int = 1
    VOSK_ALLOWED_AUDIO_TYPES: tuple = ("audio/wav", "audio/mpeg", "audio/mp3",)
    VOSK_ALLOWED_AUDIO_EXTENSIONS: tuple = (".wav", ".mp3",)
    VOSK_API_URL_BASE_NAME = "vosk"

    # INIT_VOSK_PUNCTUATOR_MODEL = True
    INIT_VOSK_PUNCTUATOR_MODEL = False
    VOSK_PUNCTUATOR_MODEL_PATH: str = VOSK_MODEL_PATHS.RECASEPUNC_2GB_RU_022

    INIT_WHISPER_MODEL: bool = True
    # INIT_WHISPER_MODEL: bool = False
    WHISPER_MODEL_NAME: str = WHISPER_MODEL_NAMES.SMALL
    WHISPER_AUDIO_FRAME_RATE: int = 16000
    WHISPER_AUDIO_CHANNELS_NUM: int = 1
    WHISPER_ALLOWED_AUDIO_TYPES: tuple = ("audio/wav", "audio/mpeg", "audio/mp3",)
    WHISPER_ALLOWED_AUDIO_EXTENSIONS: tuple = (".wav", ".mp3",)
    WHISPER_API_URL_BASE_NAME = "whisper"

    API_ENV_CONFIGS_NAME = API_CONFIG_NAMES.API_TEST_LOCALHOST
    SCRIPT_IN_AUDIO_FILES_PATH: str = "data_incoming/mp3_samples_KIROV"
    API_IN_AUDIO_FILES_PATH: str = "data_incoming/temporary_files_API"


full_path = os.path.join(BASE_DIR, ".configs.ini")
normal_env_path = os.path.normpath(full_path)

api_configs = ConfigParser()
api_configs.read(filenames=normal_env_path)
API_ENV_HOST: str = api_configs.get(
    section=API_CONFIGS.API_ENV_CONFIGS_NAME, option="API_HOST")

API_ENV_PORT: int = int(api_configs.get(
    section=API_CONFIGS.API_ENV_CONFIGS_NAME, option="API_PORT"))

API_ENV_USERNAME: str = api_configs.get(
    section=API_CONFIGS.API_ENV_CONFIGS_NAME, option="API_USERNAME")

API_ENV_PASSWORD: str = api_configs.get(
    section=API_CONFIGS.API_ENV_CONFIGS_NAME, option="API_PASSWORD")
