import json
from datetime import datetime
from pathlib import Path

with open("food_kind.json", 'r', encoding='utf-8') as f:
    temp = f.read()
fk = json.loads(temp)

fileTime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
for k, vs in fk.items():
    file_path = Path(f'./{k}_{fileTime}')
    if not(file_path.exists()):
        file_path.mkdir()  # 建立目錄， parents 參數若是 True, 形同 mkdirs
    for v in vs:
        for i in Path('./').iterdir():
            if i.is_dir() and str(i).startswith(v):
                oriPath = Path(f'./{i}')
                tarPath = Path(f'{file_path}/{i}')
                oriPath.replace(tarPath)
