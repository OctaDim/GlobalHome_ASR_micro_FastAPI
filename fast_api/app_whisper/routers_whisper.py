import asyncio
import os
from datetime import datetime
from functools import partial
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from configs.console_colors import CONSOLE_COLORS
from configs.settings import BASE_DIR, WHISPER_OPTIONS
from stt_WHISPER.funcs_whisper import get_str_from_wav_whisper, async_get_str_from_wav_whisper
from stt_WHISPER.init_whisper import whisper_model_instance
from utils_async_common.async_remove_file_by_path import async_remove_file
from utils_common.convert_save_mp3_to_wav import convert_and_save_mp3_to_wav, async_convert_and_save_mp3_to_wav
from utils_common.normalized_path import (
    get_full_dir_normal_path, get_full_file_normal_path)

whisper_base_url_name = WHISPER_OPTIONS.WHISPER_API_URL_BASE_NAME
router_whisper = APIRouter(prefix=f"/{whisper_base_url_name}", tags=["WHISPER"])


@router_whisper.post(path="/transcribe/")
async def whisper_transcribe_audio_to_text(
        file: Annotated[UploadFile, File(description="Audio file (.wav or .mp3)")],
        # TODO: username: Annotated[str, Depends(verify_auth_data)],
):
    print(f"\n{'#' * 95}")
    allowed_audio_types = WHISPER_OPTIONS.WHISPER_ALLOWED_AUDIO_TYPES
    if file.content_type not in allowed_audio_types:
        log_text = (f"Unsupported (audio file) media type [ERROR]: "
                    f"file.content_type: {file.content_type}, "
                    f"allowed audio types: {allowed_audio_types}")
        print(log_text)
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=log_text)

    allowed_extensions = WHISPER_OPTIONS.WHISPER_ALLOWED_AUDIO_EXTENSIONS
    if not file.filename.lower().endswith(allowed_extensions):
        log_text = (f"Media file (audio file) extension [ERROR]: "
                    f"file.filename: {file.filename}, "
                    f"allowed extensions: {allowed_audio_types}")
        print(log_text)
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=log_text)

    try:
        dir_full_path = get_full_dir_normal_path(
            all_dir_str_parts=[BASE_DIR, WHISPER_OPTIONS.WHISPER_API_IN_AUDIO_PATH])
        os.makedirs(dir_full_path, exist_ok=True)

        new_audio_full_path = get_full_file_normal_path(
            all_dir_str_parts=[BASE_DIR, WHISPER_OPTIONS.WHISPER_API_IN_AUDIO_PATH],
            file_name_with_ext=file.filename)

        with open(new_audio_full_path, "wb") as new_audio_file:
            upload_file_content = await file.read()
            new_audio_file.write(upload_file_content)

        # Create new .wav file if .mp3 (audio/mp3, audio/mpeg)
        if (file.content_type in ["audio/mpeg", "audio/mp3", ]
                and file.filename.lower().endswith(".mp3")):
            new_wav_full_path = await async_convert_and_save_mp3_to_wav(
                mp3_full_path=new_audio_full_path,
                wav_frame_rate=WHISPER_OPTIONS.WHISPER_AUDIO_FRAME_RATE,
                wav_channels=WHISPER_OPTIONS.WHISPER_AUDIO_CHANNELS_NUM)
        else:  # Use existing .wav file
            new_wav_full_path = new_audio_full_path

        verbose_flag = WHISPER_OPTIONS.WHISPER_TRANSCRIBE_VERBOSE
        use_language = WHISPER_OPTIONS.WHISPER_TRANSCRIBE_LANGUAGE

        datetime_start = datetime.now()

        # ########################## VAR A (start) #######################
        # CONSISTENT MULTI WORKING with await async def async_get_str_from_wav_whisper()
        # no server error, but only consistent execution one after another
        phrase = await async_get_str_from_wav_whisper(
            model_obj=whisper_model_instance,
            full_file_path=new_wav_full_path,
            language=use_language,
            log_wav_path=True,
            log_wav_duration=True,
            transcribe_verbose=verbose_flag)
        # ########################## VAR A (end) #########################

        # ########################## VAR B (start) #######################
        # # NOT MULTI WORKING with asyncio.to_thread(get_str_from_wav_whisper())
        # # server error, one executes, others cause server error
        # prepared_sync_func = partial(get_str_from_wav_whisper,
        #                              model_obj=whisper_model_instance,
        #                              full_file_path=new_wav_full_path,
        #                              language=use_language,
        #                              log_wav_path=True,
        #                              log_wav_duration=True,
        #                              transcribe_verbose=verbose_flag)
        # phrase = await asyncio.to_thread(prepared_sync_func)  # Execute prepared func
        # ########################## VAR B (end) #########################

        recognition_time = (datetime.now() - datetime_start).total_seconds()
        recognition_time = round(recognition_time, 1)

        await async_remove_file(new_audio_full_path)
        if new_audio_full_path != new_wav_full_path:
            await async_remove_file(new_wav_full_path)

        json_response = JSONResponse(
            content={"message": "WHISPER: Audio file transcribed [OK]",
                     # TODO: "username": username,
                     "filename": file.filename,
                     "content type": file.content_type,
                     "model init": WHISPER_OPTIONS.WHISPER_MODEL_INIT,
                     "model path": WHISPER_OPTIONS.WHISPER_MODEL_NAME,
                     "recognition time": recognition_time,
                     "phrase": phrase, },
            status_code=status.HTTP_200_OK,
        )

        blue_color = CONSOLE_COLORS.BRIGHT_BLUE
        reset_color = CONSOLE_COLORS.RESET
        print(f"WHISPER response.body: {json_response.body}\n"
              f"WHISPER response.status_code: {json_response.status_code}\n"
              f"WHISPER Recognized Phrase: {blue_color}{phrase}{reset_color}\n")
        return json_response
    except Exception as error:
        log_text = f"WHISPER router [ERROR]: error: {error}"
        print(log_text)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_text)
