from fastapi import (
    APIRouter, HTTPException, Request, status)
from fastapi.params import Body
from starlette.responses import JSONResponse

from configs.settings import BASE_DIR
from data_incoming.incoming_wav_file_paths.incoming_wav_paths import (
    wav_file_paths)
from fast_api_apps.fastapi_app_auth.pydantic_auth import (
    LogPassPydantic)
from stt_VOSK.utils_vosk.funcs_vosk import get_str_from_wav_path_vosk
from stt_VOSK.utils_vosk.init_model_vosk import vosk_model_obj
from stt_WHISPER.utils_whisper.init_model_whisper import (
    whisper_model_obj)
from utilities_common.normalized_path import get_all_dirs_norm_path


router_vosk = APIRouter(prefix="/vosk", tags=["vosk"])


# RESPONSES = {
#     200: {"model": LogPassPydantic, "detail": "Success"},
#     400: {"model": LogPassErrorPydantic, "detail": "Bad Request"},
#     405: {"model": LogPassErrorPydantic, "detail": "Only POST method allowed"},
#     406: {"model": ErrorVoskPydantic, "detail": "Only .wav (audio/wav) allowed"}
# }


@router_vosk.post(path="",
                  # responses=RESPONSES
                  )
async def get_text_from_wav_vosk(
        request: Request,
        log_path: LogPassPydantic = Body(
            description="{'login': '<any>', 'password': '<any>'}")
        # wav_file: UploadFile = File(description="Audio file in wav format")
):
    if not vosk_model_obj:
        err_msg = f"Model VOSK not initialized, ask admin to change settings"
        response = JSONResponse(
            content={"detail": err_msg},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    # TODO: Transfer exceptions bodies to the common separate file
    if request.method != "POST":
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"POST method awaited, got {request.method} instead")

    # content_type = request.headers.get("Content-Type")
    # if content_type != "multipart/form-data":
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Headers key 'Content-Type' must be 'multipart/form-data',"
    #                f"got {content_type} instead")

    # # TODO: DM: Transfer to common pydantic scheme validation
    # file_name = wav_file.filename
    # if not file_name.endswith(".wav"):
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #         detail=f"Accepting 'file.wav', got '{file_name}' instead")
    #
    # # # TODO: DM: Transfer to common pydantic scheme validation
    # file_type = wav_file.content_type
    # if not file_type == "audio/wav":
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #         detail=f"Accepting file type 'audio/wav', got '{file_type}' instead")

    if vosk_model_obj:
        print(f"VOSK [OK]: {type(vosk_model_obj)}")

    if whisper_model_obj:
        print(f"WHISPER [OK]: {type(whisper_model_obj)}")

    for cur_wav_path in wav_file_paths[0:3]:
        wav_path = get_all_dirs_norm_path(
            [BASE_DIR, "data_incoming/", cur_wav_path])

        if not cur_wav_path:
            continue
        phrase = get_str_from_wav_path_vosk(model=vosk_model_obj,
                                            full_file_path=wav_path,
                                            log_wav_path=True,
                                            log_wav_duration=True)
        print(f"Recognized Phrase: {phrase}\n")

    return {"message": "URL [OK]",
            "login": log_path.login,
            "password": log_path.password,
            "status": status.HTTP_200_OK}
