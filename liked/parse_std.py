import json

ERR = './err.txt'
META = './meta.json'
OUT = './liked_ids.txt'

TEMPLATES = (
    'ERROR: [youtube] xxxxxxxxxxx: ',
    'WARNING: [youtube] xxxxxxxxxxx: ',
)

def main():
    ids = []
    last_id = None
    def addId(id_: str):
        nonlocal last_id
        if id_ in ids:
            assert id_ == last_id, id_
        else:
            ids.append(id_)
            last_id = id_
    
    with open(ERR, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            for template in TEMPLATES:
                L, R = template.split('xxxxxxxxxxx')
                l0 = line[:len(template)]
                if (
                    l0.startswith(L)
                    and l0.endswith(R)
                ):
                    video_id = l0[len(L):-len(R)]
                    addId(video_id)
                    break
            else:
                print('unmatched line:')
                print(line)
    with open(OUT, 'w', encoding='utf-8') as out_f:
        for id_ in ids:
            out_f.write(id_ + '\n')

if __name__ == "__main__":
    main()
