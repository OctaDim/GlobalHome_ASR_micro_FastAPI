import asyncio
from pathlib import Path

import aiohttp


audio_file_full_paths = [
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ask_want_appointment_0.wav",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ask_want_appointment_0.wav",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ask_want_appointment_0.wav",
]

API_URLS = [f"http://192.168.0.117:8000/vosk/transcribe/",
            f"http://192.168.0.117:8000/whisper/transcribe/"]

async def main():
    for cur_api_url in API_URLS:
        print("#"*100)
        for cur_file in audio_file_full_paths:
            with open(cur_file, "rb") as audio_file:
                try:
                    form_data = aiohttp.FormData()
                    file_ext = Path(cur_file).suffix[1:]
                    file_name = Path(cur_file).name
                    form_data.add_field(name="file", value=audio_file,
                                        content_type=f"audio/{file_ext}",
                                        filename=file_name,
                                        content_transfer_encoding=None)
                except Exception as error:
                    print(f"Creating form_data [ERROR]: {error}")

                try:
                    async with aiohttp.request(method="POST", url=cur_api_url, data=form_data) as response:
                        print(f"Request status: {response.status}")
                        try:
                            print(await response.json())
                        except Exception as error:
                            print(f"Request .json() [ERROR]: {error}")
                            try:
                                print(await response.text())
                            except Exception as error:
                                print(f"Request .text() [ERROR]: {error}")
                except Exception as error:
                    print(f"API request [ERROR]: {error}")

if __name__ == "__main__":
    asyncio.run(main())
