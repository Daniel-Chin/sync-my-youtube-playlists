# Drafted by GPT-5

import yt_dlp
import json
import random
import time
from pathlib import Path
import typing as tp

input_file  = Path('liked_ids.txt')
output_file = Path('meta-enriched.jsonl')

FIELDS = [
    'id',
    'title',
    'channel',
    'uploader',
    'description',
    'categories',
    'chapters',
    'duration',
    '_filename',
    'filename',
    '_type',
    '_version',
    'acodec',
    'abr',
    'asr',
    'audio_channels',
]

def fetchMetadata(video_id: str) -> tp.Optional[dict]:
    url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            print(f'Error fetching {video_id}: {e}')
            return None
    return {k: info.get(k) for k in FIELDS}

def main():
    results = []
    with input_file.open() as f:
        ids = [line.strip() for line in f if line.strip()]

    for video_id in ids:
        jitter = random.uniform(1.0, 3.0)
        print(f'Fetching {video_id} (delay {jitter:.2f}s)...')
        data = fetchMetadata(video_id)
        if data:
            results.append(data)
            with output_file.open('a') as out:
                out.write(json.dumps(data, ensure_ascii=False) + '\n')
        time.sleep(jitter)

    print(f'Done. {len(results)} entries saved to {output_file}')

if __name__ == '__main__':
    main()
