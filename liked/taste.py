import json
import os
from os import path
from pprint import pprint

from tqdm import tqdm

IN_PATH = './music_ids.txt'
OUT_PATH = './good_music_ids.txt'
META_PATH = './meta-enriched.jsonl'

def main():
    with open(IN_PATH, 'r', encoding='utf-8') as f:
        ids = [line.strip() for line in f if line.strip()]
    meta = {}
    with open(META_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            meta[d['id']] = d
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        for id_ in tqdm(ids):
            print('https://youtu.be/' + id_)
            m = meta[id_]
            print('title', end=': ')
            print(m['title'      ])
            print('channel', end=': ')
            print(m['channel'    ])
            print('----')
            print('description', end=': ')
            print(m['description'][:200].replace('\n', ' '))
            print('categories', end=': ')
            print(m['categories' ])
            print('chapters', end=': ')
            print(m['chapters'   ])
            print('duration', end=': ')
            print(m['duration'   ])
            print()
            if input('Take? y/n > ').lower() == 'y':
                print('taken.')
                f.write(id_ + '\n')
            else:
                print('skipped.')
                list_dir = os.listdir('./songs')
                matches = [x for x in list_dir if id_ in x]
                for fn in matches:
                    print('found local file:', fn)
                    if input('Delete local file? y/n > ').lower() == 'y':
                        os.remove(path.join('./songs', fn))
                        print('deleted.')
            print('========')

if __name__ == '__main__':
    main()
