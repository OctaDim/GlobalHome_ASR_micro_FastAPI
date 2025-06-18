import os

import torch
import whisper
from whisper import Whisper

from configs.console_colors import CONSOLE_COLORS
from configs.settings import BASE_DIR, WHISPER_OPTIONS
from utils_common.exec_time_decorator import execution_time_decorator
from utils_common.normalized_path import get_full_dir_normal_path


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          new_line_after=True,
                          note="WHISPER Model initialization time")
def initialise_whisper_model(model_name: str,
                             model_download_path: str) -> Whisper:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    green_color = CONSOLE_COLORS.BRIGHT_GREEN
    reset_color = CONSOLE_COLORS.RESET
    print(f"Device: {green_color}{device.upper()}{reset_color}\n"
          f"Model: {green_color}{model_name.upper()}{reset_color}\n"
          f"Path: {green_color}{model_download_path}{reset_color}")

    model = whisper.load_model(name=model_name,
                               device=device,
                               download_root=model_download_path,  # download to cur dir
                               in_memory=True)
    # model = whisper.load_model(name=model_name, device=device)  # download to .cached by default
    return model


whisper_model_instance = None

if WHISPER_OPTIONS.WHISPER_MODEL_INIT:
    whisper_model_path = get_full_dir_normal_path(
        [BASE_DIR, WHISPER_OPTIONS.WHISPER_MODELS_DOWNLOAD_PATH])

    os.makedirs(name=whisper_model_path, exist_ok=True)

    whisper_model_instance = initialise_whisper_model(
        model_name=WHISPER_OPTIONS.WHISPER_MODEL_NAME,
        model_download_path=whisper_model_path)
