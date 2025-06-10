import os


def get_full_file_normal_path(all_dirs_paths: list[str],
                              file_name: str) -> str:
    results_wav_path = os.path.join(*all_dirs_paths, file_name)
    normalized_file_path = os.path.normpath(results_wav_path)
    return normalized_file_path


def get_all_dirs_norm_path(all_dirs_paths: list[str]) -> str:
    results_wav_path = os.path.join(*all_dirs_paths)
    normalized_dirs_path = os.path.normpath(results_wav_path)
    return normalized_dirs_path
