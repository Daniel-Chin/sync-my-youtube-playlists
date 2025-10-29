import json
import random

from gpt_arbiter_human_in_loop import ArbiterHiLUI, ArbiterDummy

META = './liked/meta-enriched.jsonl'
PROMPT_AND_EXAMPLES_FILENAME = './liked/prompt_and_examples.json'
RW_JSON_PATH = './liked/classifications.json'
LAMBDA = 20
MODEL = 'gpt-5-nano'

def MetaLoader():
    with open(META, 'r', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)

def main():
    d = { x['id']: x for x in MetaLoader() }
    all_ids = [*d.keys()]
    random.shuffle(all_ids) # i.i.d. is important
    def idToClassifiee(id_: str) -> str:
        entry = d[id_]
        title = entry['title']
        channel = entry['channel']
        description = entry['description']
        categories = entry['categories']
        chapters = entry['chapters']
        duration = entry['duration']

        categories = '; '.join(categories)
        chapters = [x['title'] for x in chapters]
        h = duration // 3600
        m = duration // 60 - h * 60
        s = duration - h * 3600 - m * 60
        duration = f'{h} h {m} m {s} s'
        duration = duration.removeprefix('0 h ')
        duration = duration.removeprefix('0 m ')

        return json.dumps(dict(
            title=title            [:60],
            channel=channel        [:60],
            categories=categories  [:60],
            description=description[:60],
            chapters=chapters      [:60],
            duration=duration      [:60],
        ), indent=2, ensure_ascii=False)

    ui = ArbiterHiLUI(
        arbiter=ArbiterDummy(),
        prompt_and_examples_filename=PROMPT_AND_EXAMPLES_FILENAME,
        all_ids=all_ids,
        idToClassifiee=idToClassifiee,
        rw_json_path=RW_JSON_PATH,
        Lambda=LAMBDA,
        model_name=MODEL,
    )
    ui.run()

if __name__ == "__main__":
    main()
