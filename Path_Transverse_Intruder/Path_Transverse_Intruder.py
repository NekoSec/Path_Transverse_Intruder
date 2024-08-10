import requests
import os
from datetime import datetime

os.system('title xiangnile')

current_time = datetime.now().strftime('%Y.%m.%d.%H.%M')
result_folder = f'result/{current_time}'

if not os.path.exists(result_folder):
    os.makedirs(result_folder)

with open('url.txt', 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file.readlines()]

with open('path.txt', 'r', encoding='utf-8') as file:
    paths = [line.strip() for line in file.readlines()]

result_files = {
    200: open(f'{result_folder}/200.txt', 'w', encoding='utf-8'),
    404: open(f'{result_folder}/404.txt', 'w', encoding='utf-8'),
    'timeout': open(f'{result_folder}/outtime.txt', 'w', encoding='utf-8'),
}

total_urls = len(urls) * len(paths)
processed_urls = 0

for url in urls:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
        
    for path in paths:
        full_url = f"{url}{path}"
        try:
            response = requests.get(full_url, timeout=5)
            status_code = response.status_code
            
            if status_code in result_files:
                result_files[status_code].write(full_url + '\n')
            else:
                with open(f'{result_folder}/{status_code}.txt', 'a', encoding='utf-8') as f:
                    f.write(full_url + '\n')
        except requests.exceptions.Timeout:
            result_files['timeout'].write(full_url + '\n')
        except requests.exceptions.RequestException:
            pass

        processed_urls += 1
        progress = (processed_urls / total_urls) * 100
        print(f"处理进度: {progress:.2f}%", end='\r')

for file in result_files.values():
    file.close()

print("\n任务完成!")
