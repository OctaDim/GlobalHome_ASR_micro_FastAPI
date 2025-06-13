import asyncio
import os
from datetime import datetime
from functools import partial
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from configs.console_colors import CONSOLE_COLORS
from configs.settings import API_CONFIGS, BASE_DIR
from stt_WHISPER.funcs_whisper import (
    async_get_str_from_wav_whisper, get_str_from_wav_whisper)
from stt_WHISPER.init_whisper import whisper_model_instance
from utils_async_common.async_remove_file_by_path import async_remove_file
from utils_common.convert_save_mp3_to_wav import convert_and_save_mp3_to_wav
from utils_common.normalized_path import (
    get_full_dir_normal_path, get_full_file_normal_path)


whisper_base_url_name = API_CONFIGS.WHISPER_API_URL_BASE_NAME
router_whisper = APIRouter(prefix=f"/{whisper_base_url_name}", tags=["WHISPER"])


@router_whisper.post(path="/transcribe/")
async def vosk_transcribe_audio_to_text(
        file: Annotated[UploadFile, File(description="Audio file (.wav or .mp3)")],
        # TODO: username: Annotated[str, Depends(verify_auth_data)],
):
    print(f"{'#' * 95}")
    allowed_audio_types = API_CONFIGS.WHISPER_ALLOWED_AUDIO_TYPES
    if file.content_type not in allowed_audio_types:
        log_text = (f"Unsupported (audio file) media type [ERROR]: "
                    f"file.content_type: {file.content_type}, "
                    f"allowed audio types: {allowed_audio_types}")
        print(log_text)
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=log_text)

    allowed_extensions = API_CONFIGS.WHISPER_ALLOWED_AUDIO_EXTENSIONS
    if not file.filename.lower().endswith(allowed_extensions):
        log_text = (f"Media file (audio file) extension [ERROR]: "
                    f"file.filename: {file.filename}, "
                    f"allowed extensions: {allowed_audio_types}")
        print(log_text)
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=log_text)

    dir_full_path = get_full_dir_normal_path(
        all_dir_str_parts=[BASE_DIR, API_CONFIGS.API_IN_AUDIO_FILES_PATH])
    os.makedirs(dir_full_path, exist_ok=True)

    new_audio_full_path = get_full_file_normal_path(
        all_dir_str_parts=[BASE_DIR, API_CONFIGS.API_IN_AUDIO_FILES_PATH],
        file_name_with_ext=file.filename)

    with open(new_audio_full_path, "wb") as new_audio_file:
        upload_file_content = await file.read()
        new_audio_file.write(upload_file_content)

    # Create new .wav file if .mp3 (audio/mp3, audio/mpeg)
    if (file.content_type in ["audio/mpeg", "audio/mp3", ]
            and file.filename.lower().endswith(".mp3")):
        prepared_sync_func = partial(
            convert_and_save_mp3_to_wav,
            mp3_full_path=new_audio_full_path,
            wav_frame_rate=API_CONFIGS.WHISPER_AUDIO_FRAME_RATE,
            wav_channels=API_CONFIGS.WHISPER_AUDIO_CHANNELS_NUM)
        new_wav_full_path = await asyncio.to_thread(prepared_sync_func)
    else:  # Use existing .wav file
        new_wav_full_path = new_audio_full_path

    datetime_start = datetime.now()

    # # ########################## VAR A (start) #########################
    # # CONSISTENT MULTI WORKING with await async def async_get_str_from_wav_whisper()
    # # no server error, but only consistent execution one after another
    # phrase = await async_get_str_from_wav_whisper(
    #     model_obj=whisper_model_instance,
    #     full_file_path=new_wav_full_path,
    #     log_wav_path=True,
    #     log_wav_duration=True)
    # # ########################## VAR A (end) ###########################

    # ########################## VAR B (start) #######################
    # NOT MULTI WORKING with asyncio.to_thread(get_str_from_wav_whisper())
    # server error, one executes, others cause server error
    prepared_sync_func = partial(get_str_from_wav_whisper,
                                 model_obj=whisper_model_instance,
                                 full_file_path=new_wav_full_path,
                                 log_wav_path=True,
                                 log_wav_duration=True)
    phrase = await asyncio.to_thread(prepared_sync_func)  # Execute prepared func
    # ########################## VAR B (end) #########################

    recognition_time = (datetime.now() - datetime_start).total_seconds()
    recognition_time = round(recognition_time, 1)

    await async_remove_file(new_audio_full_path)
    if new_audio_full_path != new_wav_full_path:
        await async_remove_file(new_wav_full_path)

    blue_color, reset_color = CONSOLE_COLORS.BLUE, CONSOLE_COLORS.RESET
    print(f"Recognized Phrase: {blue_color}{phrase}{reset_color}\n")
    return JSONResponse(
        content={"message": "WHISPER: Audio file transcribed [OK]",
                 "filename": file.filename,
                 "content type": file.content_type,
                 "model init": API_CONFIGS.INIT_WHISPER_MODEL,
                 "model path": API_CONFIGS.WHISPER_MODEL_NAME,
                 "recognition time": recognition_time,
                 "phrase": phrase,
                 # TODO: "username": username,
                 },
        status_code=status.HTTP_200_OK,
    )
