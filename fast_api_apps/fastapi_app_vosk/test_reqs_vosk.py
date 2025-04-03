import requests

from configs.settings import API_CONFIGS, BASE_DIR
from data_incoming.incoming_wav_file_paths.incoming_wav_paths import wav_file_paths
from utilities_common.normalized_path import get_all_dirs_norm_path

wav_file_path = get_all_dirs_norm_path(
    [BASE_DIR, "data_incoming/", wav_file_paths[1]])
files = {"file": open(wav_file_path, "rb")}

auth_data = {"login": "zxc", "password": "123"}


response = requests.post(
    url=f"http://{API_CONFIGS.BASE_HOST}:{API_CONFIGS.BASE_PORT}/vosk",
    json=auth_data
)

print(f"response.content: {response.content}")
print(f"response.status_code: {response.status_code}")
print(f"response.json(): {response.json()}")
print(f"response.json().get('login'): {response.json().get('login')}")
print(f"response.json().get('password'): {response.json().get('password')}")
