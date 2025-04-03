import wave

import torch
import whisper
from whisper import Whisper

from utilities_common.exec_time_decorator import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          new_line_after=True,
                          note="WHISPER Model initialization time")
def whisper_model_initializing(model_name: str) -> Whisper:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model(name=model_name, device=device)
    return model


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          note="WHISPER recognition time")
def get_str_from_wav_whisper(model: Whisper,
                             full_file_path: str,
                             log_wav_path: bool = False,
                             log_wav_duration: bool = False,
                             ) -> str:
    with wave.open(full_file_path, 'rb') as wav_file:
        frame_rate = wav_file.getframerate()
        frames_number = wav_file.getnframes()
        wav_duration = round(frames_number / frame_rate, 0)

        if log_wav_path:
            print(f"Current wav file: {full_file_path}")
        if log_wav_duration:
            print(f"Total wav audio duration: {wav_duration} seconds")

        audio_float = whisper.load_audio(full_file_path)
        result_dict = model.transcribe(audio_float)

        result_text = result_dict.get("text", "")
        return result_text
