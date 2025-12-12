import requests
import os
from tqdm import tqdm

def download_file(url, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Browsers often send User-Agent, CivitAI might require it or checking cookies. 
    # But often direct download links work. Let's try following redirects explicitly.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://civitai.com/'
    }
    response = requests.get(url, stream=True, allow_redirects=True, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to download. Status code: {response.status_code}")
        print(f"Content: {response.text[:200]}")
        return

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024 * 1024 # 1MB
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
    else:
        print(f"Downloaded to {filename}. Size: {progress_bar.n} bytes")

if __name__ == "__main__":
    # URL provided by user ("baked" version)
    # URL provided by user ("baked" version)
    url = "https://civitai.com/api/download/models/1969455?type=Model&format=SafeTensor&size=full&fp=fp16"
    filename = "data/models/cheyenne_v24.safetensors"
    print(f"Downloading model from {url}...")
    download_file(url, filename)
