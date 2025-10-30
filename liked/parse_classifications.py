import json

from gpt_arbiter_human_in_loop.persistent import ItemAnnotations
JSON_PATH = './classifications.json'
OUT_PATH = './music_ids.txt'

def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        raw: dict = json.load(f)
    data = {id_: ItemAnnotations.model_validate(v) for id_, v in raw.items()}
    least_certain_verdict = 0.0
    least_certain_verdict_certainty = 0.5
    music_ids = []
    for id_, anno in data.items():
        assert anno.gpt_verdict is not None
        if judge(anno):
            music_ids.append(id_)
        if anno.human_label_no_or_yes is None:
            certainty = abs(anno.gpt_verdict - 0.5)
            if certainty < least_certain_verdict_certainty:
                least_certain_verdict_certainty = certainty
                least_certain_verdict = anno.gpt_verdict
    print(f'{least_certain_verdict = }')
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        for id_ in music_ids:
            f.write(id_ + '\n')

def judge(anno: ItemAnnotations) -> bool:
    if anno.human_label_no_or_yes is not None:
        return [False, True][anno.human_label_no_or_yes]
    assert anno.gpt_verdict is not None
    return anno.gpt_verdict > 0.5

if __name__ == '__main__':
    main()
