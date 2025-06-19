import asyncio
from pathlib import Path

import aiohttp


audio_file_full_paths = [
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ffa2bea1_80f1_4bd1_a78a_78975fc0716c_2024_12_26_12_17_49_3_89235953249.mp3",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ffa2bea1_80f1_4bd1_a78a_78975fc0716c_2024_12_26_12_17_49_3_89235953249.mp3",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ffa2bea1_80f1_4bd1_a78a_78975fc0716c_2024_12_26_12_17_49_3_89235953249.mp3",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ask_want_appointment_0.wav",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ask_want_appointment_0.wav",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\3b136563-a94a-4953-9456-9547783ecb78_2025-05-19-15-43-40_79968971905_1000004.mp3",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\ask_want_appointment_1.wav",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\15209673-6e15-40b0-be75-c24d4bbb9bfc_2025-05-19-15-43-36_79091447010_1000004.mp3",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\KIROV_1_f61cbd53_89bd_4d5f_92e5_595ec3a5c882_2025_06_13_13_18_06_79165937387.mp3",
    r"C:\Users\dexp\Projects\GlobalHome_ASR_micro_FastAPI\data_incoming\mp3_samples_KIROV\KIROV_2_0ad4aa59_d022_476e_8b58_549beccb96be_2025_06_13_12_37_03_79823813009.mp3",

]

API_URLS = [
    f"http://176.124.136.4:8000/vosk/transcribe/",  # Server 176.124.136.4 API VOSK-WHISPER
    f"http://176.124.136.4:8000/whisper/transcribe/",  # Server 176.124.136.4 API VOSK-WHISPER
    # f"http://192.168.0.117:8000/vosk/transcribe/",  # Local Dexp API VOSK-WHISPER
    # f"http://192.168.0.117:8000/whisper/transcribe/",  # Local Dexp API VOSK-WHISPER
]


async def main():
    for cur_api_url in API_URLS:
        print("#" * 100)
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
                    async with aiohttp.request(method="POST",
                                               url=cur_api_url,
                                               data=form_data) as response:
                        print(f"Request status: {response.status}")
                        try:
                            json_response = await response.json()
                            print(f"Request response: {json_response}\n")
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
