import asyncio
from pathlib import Path

import aiohttp

from configs.console_colors import CONSOLE_COLORS
from configs.settings import API_CONFIGS, API_ENV_HOST, API_ENV_PORT, BASE_DIR
from utils_common.dir_files_names_paths import get_dir_files_full_paths
from utils_common.normalized_path import get_full_dir_normal_path


async def req_api_stt_audio(session: aiohttp.ClientSession,
                            audio_file_full_path):
    with open(audio_file_full_path, "rb") as audio_file:
        try:
            form_data = aiohttp.FormData()
            file_ext = Path(audio_file_full_path).suffix[1:]
            file_name = Path(audio_file_full_path).name
            form_data.add_field(name="file", value=audio_file,
                                content_type=f"audio/{file_ext}",
                                filename=file_name,
                                content_transfer_encoding=None)
        except Exception as error:
            error_info = f"Creating form_data [ERROR]: error: {error}"
            print(error_info)
            return error_info

        try:
            base_url = API_CONFIGS.WHISPER_API_URL_BASE_NAME
            API_URL = f"http://{API_ENV_HOST}:{API_ENV_PORT}/{base_url}/transcribe/"
            async with aiohttp.request(method="POST", url=API_URL, data=form_data) as response:
                # async with session.post(API_URL, data=form_data) as response:
                if response.status not in ["200", "201", "202"]:
                    result = await response.json()
                    print(f"API response [OK]: "
                          f"response.status: {response.status}")
                    return result
                else:
                    response_text = await response.text()
                    error_info = (f"API response status not 200, 201 or 202 [ERROR]: "
                                  f"response_status: {response.status}, "
                                  f"response_text: {response_text}")
                    print(error_info)
                    return {"error": error_info}
        except Exception as error:
            error_info = f"API response [ERROR]: error: {error}"
            print(error_info)
            return {"error": error_info}


async def main_test_process(all_audio_files_paths):
    async with aiohttp.ClientSession() as session:
        coro_tasks = []
        for cur_audio_path in all_audio_files_paths:
            coro_tasks.append(req_api_stt_audio(session, cur_audio_path))

        green_color, reset_color = CONSOLE_COLORS.BRIGHT_GREEN, CONSOLE_COLORS.RESET
        for cur_async_coro_task in asyncio.as_completed(coro_tasks):
            result = await cur_async_coro_task
            print(f"{green_color}{result}{reset_color}\n")


if __name__ == '__main__':
    full_dir_path = get_full_dir_normal_path(
        all_dir_str_parts=[BASE_DIR, API_CONFIGS.SCRIPT_IN_AUDIO_FILES_PATH])

    all_files_paths = get_dir_files_full_paths(full_dir_path)

    all_audio_files_paths = []
    for cur_file_path in all_files_paths:
        if cur_file_path.endswith(API_CONFIGS.WHISPER_ALLOWED_AUDIO_EXTENSIONS):
            all_audio_files_paths.append(cur_file_path)

    if not all_audio_files_paths:
        print(f"No files in settings defined directory "
              f"API_CONFIGS.SCRIPT_IN_AUDIO_FILES_PATH [ERROR]: "
              f"{API_CONFIGS.SCRIPT_IN_AUDIO_FILES_PATH}\n")
    else:
        asyncio.run(main_test_process(all_audio_files_paths))
