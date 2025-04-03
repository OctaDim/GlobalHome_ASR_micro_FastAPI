from configs.settings import BASE_DIR
from utilities_common.normalized_path import get_all_dirs_norm_path


wav_file_paths = [
    # Test wav file
    "wav_samples_MODEL/decoder-test.wav",
    # From Alena (HMAO)
    r"wav_samples_HMAO/hello.wav",
    r"wav_samples_HMAO/ask_want_appointment.wav",
    "wav_samples_HMAO/improper_answer_end_call.wav",
    "wav_samples_HMAO/1.wav",
    "wav_samples_HMAO/not_mfc_competency.wav",
    # From Fillip (OMSK)
    "wav_samples_OMSK/hello.wav",
    "wav_samples_OMSK/1.2.6.wav",
    # Empty
    "",
]
