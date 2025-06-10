import torch
import whisper
from whisper import Whisper

from configs.settings import API_CONFIGS
from utils_common.exec_time_decorator import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          new_line_after=True,
                          note="WHISPER Model initialization time")
def initialise_whisper_model(model_name: str) -> Whisper:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"device: {device}")
    model = whisper.load_model(name=model_name, device=device)
    return model


whisper_model_instance = None

if API_CONFIGS.INIT_WHISPER_MODEL:
    whisper_model_instance = initialise_whisper_model(
        model_name=API_CONFIGS.WHISPER_MODEL_NAME)
