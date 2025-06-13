import json
import wave

from vosk import KaldiRecognizer, Model

from utils_common.exec_time_decorator import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          exec_time_logging=True,
                          note="VOSK recognition time")
def get_str_from_wav_vosk(model_obj: Model,
                          full_file_path: str,
                          log_wav_path: bool = False,
                          log_wav_duration: bool = False,
                          ) -> str | None:
    if not model_obj:
        print(f"VOSK model init not switched on in settings.py [ERROR]: "
              f"model: {model_obj}\n"
              f"full_file_path: {full_file_path}")
        return

    with wave.open(full_file_path, 'rb') as wav_file:
        frame_rate = wav_file.getframerate()
        frames_number = wav_file.getnframes()
        wav_duration = round(frames_number / frame_rate, 0)
        kaldi_recognizer = KaldiRecognizer(model_obj, frame_rate)

        if log_wav_path:
            print(f"Current wav file: {full_file_path}")
        if log_wav_duration:
            print(f"Total wav audio duration: {wav_duration} seconds")

        while True:
            # wave_byte_data = wave_file_obj.readframes(sample_rate*1)  # In seconds
            wave_byte_data = wav_file.readframes(frames_number)  # Full wav
            if not wave_byte_data:
                print(f"Empty wav file\n")
                break
            elif kaldi_recognizer.AcceptWaveform(wave_byte_data):
                pass
                # Intermediate result, but not final
                # result = recognizer_obj.Result()
                # print(result.get("text"))
            else:
                pass
                # Partially recognized result
                # result = recognizer_obj.PartialResult()
                # print(result.get("partial"))

            result = kaldi_recognizer.FinalResult()
            json_data = json.loads(result)
            final_result_text = json_data.get("text", "")
            return final_result_text
