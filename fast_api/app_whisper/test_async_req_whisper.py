import asyncio
from pathlib import Path

import aiohttp

from configs.console_colors import CONSOLE_COLORS
from configs.settings import API_HOST, API_PORT, BASE_DIR, WHISPER_OPTIONS
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
            base_url = WHISPER_OPTIONS.WHISPER_API_URL_BASE_NAME
            API_URL = f"http://{API_HOST}:{API_PORT}/{base_url}/transcribe/"
            async with aiohttp.request(method="POST", url=API_URL, data=form_data) as response:
                # async with session.post(API_URL, data=form_data) as response:
                if response.status in ["200", "201", "202"]:
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
        # Works consistently with many files in dir
        for cur_audio_path in all_audio_files_paths:
            result = await req_api_stt_audio(
                session=session, audio_file_full_path=cur_audio_path)
            green_color = CONSOLE_COLORS.BRIGHT_GREEN
            reset_color = CONSOLE_COLORS.RESET
            print(f"{green_color}{result}{reset_color}\n")

        # # Works with the only file in dir, else server error 500
        # coro_tasks = []
        # for cur_audio_path in all_audio_files_paths:
        #     cur_task = req_api_stt_audio(
        #         session=session, audio_file_full_path=cur_audio_path)
        #     coro_tasks.append(asyncio.create_task(cur_task))
        # result = await asyncio.gather(*coro_tasks)
        # green_color, reset_color = CONSOLE_COLORS.BRIGHT_GREEN, CONSOLE_COLORS.RESET
        # print(f"{green_color}{result}{reset_color}\n")

        # # Works with the only file in dir, else server error 500
        # coro_tasks = []
        # for cur_audio_path in all_audio_files_paths:
        #     cur_task = req_api_stt_audio(
        #         session=session, audio_file_full_path=cur_audio_path)
        #     coro_tasks.append(cur_task)
        # green_color, reset_color = CONSOLE_COLORS.BRIGHT_GREEN, CONSOLE_COLORS.RESET
        # for cur_async_coro_task in asyncio.as_completed(coro_tasks):
        #     result = await cur_async_coro_task
        #     print(f"{green_color}{result}{reset_color}\n")


if __name__ == '__main__':
    full_dir_path = get_full_dir_normal_path(
        all_dir_str_parts=[BASE_DIR, WHISPER_OPTIONS.WHISPER_SCRIPT_IN_AUDIO_PATH])

    all_files_paths = get_dir_files_full_paths(full_dir_path)

    all_audio_files_paths = []
    for cur_file_path in all_files_paths:
        if cur_file_path.endswith(WHISPER_OPTIONS.WHISPER_ALLOWED_AUDIO_EXTENSIONS):
            all_audio_files_paths.append(cur_file_path)

    if not all_audio_files_paths:
        print(f"No files in settings defined directory "
              f"WHISPER_OPTIONS.SCRIPT_IN_AUDIO_FILES_PATH [ERROR]: "
              f"{WHISPER_OPTIONS.WHISPER_SCRIPT_IN_AUDIO_PATH}\n")
    else:
        asyncio.run(main_test_process(all_audio_files_paths))
