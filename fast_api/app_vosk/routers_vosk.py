import asyncio
import os
from functools import partial
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from configs.console_colors import CONSOLE_COLORS
from configs.settings import API_CONFIGS, BASE_DIR
from fast_api.app_vosk.funcs_vosk import async_remove_file
from stt_VOSK.funcs_vosk import get_str_from_wav_vosk
from stt_VOSK.init_vosk import vosk_model_instance
from utils_common.convert_save_mp3_to_wav import convert_and_save_mp3_to_wav
from utils_common.normalized_path import (
    get_all_dirs_norm_path, get_full_file_normal_path)


router_vosk = APIRouter(prefix="/vosk", tags=["VOSK"])


@router_vosk.post(path="/transcribe/")
async def vosk_transcribe_audio_to_text(
        file: Annotated[UploadFile, File(description="Audio file (.wav or .mp3)")],
        # TODO: username: Annotated[str, Depends(verify_auth_data)],
):
    print(f"{'#' * 95}")
    allowed_audio_types = API_CONFIGS.VOSK_ALLOWED_AUDIO_TYPES
    if file.content_type not in allowed_audio_types:
        log_text = (f"Unsupported (audio file) media type [ERROR]: "
                    f"file.content_type: {file.content_type}, "
                    f"allowed audio types: {allowed_audio_types}")
        print(log_text)
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=log_text)

    allowed_extensions = API_CONFIGS.VOSK_ALLOWED_AUDIO_EXTENSIONS
    if not file.filename.lower().endswith(allowed_extensions):
        log_text = (f"Media file (audio file) extension [ERROR]: "
                    f"file.filename: {file.filename}, "
                    f"allowed extensions: {allowed_audio_types}")
        print(log_text)
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=log_text)

    dir_full_path = get_all_dirs_norm_path(
        all_dirs_paths=[BASE_DIR, API_CONFIGS.INCOMING_AUDIO_FILES_PATH])
    os.makedirs(dir_full_path, exist_ok=True)

    new_audio_full_path = get_full_file_normal_path(
        all_dirs_paths=[BASE_DIR, API_CONFIGS.INCOMING_AUDIO_FILES_PATH],
        file_name=file.filename)

    with open(new_audio_full_path, "wb") as new_audio_file:
        upload_file_content = await file.read()
        new_audio_file.write(upload_file_content)

    if (file.content_type in ["audio/mpeg", "audio/mp3"]
            and file.filename.lower().endswith(".mp3")):
        prepared_sync_func = partial(
            convert_and_save_mp3_to_wav,
            mp3_full_path=new_audio_full_path,
            wav_frame_rate=API_CONFIGS.VOSK_AUDIO_FRAME_RATE,
            wav_channels=API_CONFIGS.VOSK_AUDIO_CHANNELS_NUM)
        new_wav_full_path = await asyncio.to_thread(prepared_sync_func)
    else:
        new_wav_full_path = new_audio_full_path

    prepared_sync_func = partial(get_str_from_wav_vosk,
                                 model_obj=vosk_model_instance,
                                 full_file_path=new_wav_full_path,
                                 log_wav_path=True,
                                 log_wav_duration=True)
    phrase = await asyncio.to_thread(prepared_sync_func)

    await async_remove_file(new_audio_full_path)
    if new_audio_full_path != new_wav_full_path:
        await async_remove_file(new_wav_full_path)

    green_color, reset_color = CONSOLE_COLORS.GREEN, CONSOLE_COLORS.RESET
    print(f"Recognized Phrase: {green_color}{phrase}{reset_color}\n")
    return JSONResponse(
        content={"message": "Audio file transcribed [OK]",
                 "filename": file.filename,
                 "content_type": file.content_type,
                 "model_init": API_CONFIGS.INIT_VOSK_MODEL,
                 "model_path": API_CONFIGS.VOSK_MODEL_PATH,
                 "phrase": phrase,
                 # TODO: "username": username,
                 },
        status_code=status.HTTP_202_ACCEPTED,
    )
