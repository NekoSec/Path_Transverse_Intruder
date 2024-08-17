import requests
import os
import concurrent.futures
from datetime import datetime
from threading import Lock

# Set console title
os.system('title xiangnile')

# Create result folder with timestamp
current_time = datetime.now().strftime('%Y.%m.%d.%H.%M')
result_folder = f'result/{current_time}'
os.makedirs(result_folder, exist_ok=True)

# Read URLs and paths from files
with open('url.txt', 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

with open('path.txt', 'r', encoding='utf-8') as file:
    paths = [line.strip() for line in file if line.strip()]

# Prepare result files
result_files = {
    200: open(f'{result_folder}/200.txt', 'w', encoding='utf-8'),
    404: open(f'{result_folder}/404.txt', 'w', encoding='utf-8'),
    'timeout': open(f'{result_folder}/outtime.txt', 'w', encoding='utf-8'),
}

total_urls = len(urls) * len(paths)
processed_urls = 0
lock = Lock()  # Lock to manage concurrent access to the progress counter

def check_url(url, path):
    global processed_urls
    full_url = f"{url.rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.get(full_url, timeout=5)
        status_code = response.status_code
        
        with lock:
            if status_code in result_files:
                result_files[status_code].write(full_url + '\n')
            else:
                with open(f'{result_folder}/{status_code}.txt', 'a', encoding='utf-8') as f:
                    f.write(full_url + '\n')
    except requests.exceptions.Timeout:
        with lock:
            result_files['timeout'].write(full_url + '\n')
    except requests.exceptions.RequestException:
        # No action required for other request exceptions
        pass

    with lock:
        processed_urls += 1
        progress = (processed_urls / total_urls) * 100
        print(f"处理进度: {progress:.2f}%", end='\r')

# Thread pool executor for concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for url in urls:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        for path in paths:
            futures.append(executor.submit(check_url, url, path))

    # Ensure all futures are completed
    concurrent.futures.wait(futures)

# Close result files
for file in result_files.values():
    file.close()

print("\n任务完成!")
