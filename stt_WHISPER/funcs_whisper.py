import wave

import whisper
from fastapi import HTTPException, status
from whisper import Whisper

from utils_common.exec_time_decorator import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          note="WHISPER recognition time")
def get_str_from_wav_whisper(model_obj: Whisper,
                             full_file_path: str,
                             log_wav_path: bool = False,
                             log_wav_duration: bool = False,
                             ) -> str | None:
    if not model_obj:
        log_text = (f"WHISPER model init not switched on in settings.py [ERROR]: "
                    f"model: {model_obj}\n"
                    f"full_file_path: {full_file_path}")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": log_text},
            headers=None)

    try:
        with wave.open(full_file_path, 'rb') as wav_file:
            frame_rate = wav_file.getframerate()
            frames_number = wav_file.getnframes()
            wav_duration = round(frames_number / frame_rate, 0)

            if log_wav_path:
                print(f"Current wav file: {full_file_path}")
            if log_wav_duration:
                if wav_duration:
                    print(f"Total wav audio duration: {wav_duration} secs")
                else:
                    log_text = (f"Zero wav audio duration [ERROR]: "
                                f"{wav_duration} secs, "
                                f"full_file_path: {full_file_path}")
                    print(log_text)
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail={"error": log_text},
                        headers=None)

            audio_numpy_arr_float32 = whisper.load_audio(full_file_path)
            result_dict = model_obj.transcribe(
                # audio=full_file_path,  # as full audio file path
                audio=audio_numpy_arr_float32,  # as numpy float 32 array
                verbose=True,
            )

            result_text = result_dict.get("text", "")
            return result_text
    except Exception as error:
        log_text = f"WHISPER transcribing [ERROR]: error: {error}"
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": log_text},
            headers=None)


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          note="WHISPER recognition time")
async def async_get_str_from_wav_whisper(model_obj: Whisper,
                                         full_file_path: str,
                                         log_wav_path: bool = False,
                                         log_wav_duration: bool = False,
                                         ) -> str | tuple[str, str]:
    if not model_obj:
        log_text = (f"WHISPER model init not switched on in settings.py [ERROR]: "
                    f"model: {model_obj}\n"
                    f"full_file_path: {full_file_path}")
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)

    try:
        with wave.open(full_file_path, 'rb') as wav_file:
            frame_rate = wav_file.getframerate()
            frames_number = wav_file.getnframes()
            wav_duration = round(frames_number / frame_rate, 0)

            if log_wav_path:
                print(f"Current wav file: {full_file_path}")

            if wav_duration <= 0:
                log_text = (f"Zero wav audio duration [ERROR]: "
                            f"{wav_duration} secs, "
                            f"full_file_path: {full_file_path}")
                print(log_text)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=log_text)

            if log_wav_duration:
                print(f"Total wav audio duration: {wav_duration} secs")

            audio_numpy_arr_float32 = whisper.load_audio(full_file_path)
            result_dict = model_obj.transcribe(
                # audio=full_file_path,  # as full audio file path
                audio=audio_numpy_arr_float32,  # as numpy float 32 array
                verbose=True,
            )

            result_text = result_dict.get("text", "")
            return result_text
    except Exception as error:
        log_text = f"WHISPER transcribe [ERROR]: error: {error}"
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
