import sys
import json
from bs4 import BeautifulSoup


def kanji(bs):
    for head in bs.find_all("h2"):
        kanji = head.text
        kun = on = ""
        desc = head.find_next("ul")
        for line in [a.text for a in desc.find_all("li")]:
            if line.startswith("kun: "):
                kun = line.split(": ", 1)[-1]
            elif line.startswith("on: "):
                on = line.split(": ", 1)[-1]
        yield kanji, dict(kun=kun, on=on)


if __name__ == "__main__":
    data = dict()
    for filename in sys.argv[1:]:
        bs = BeautifulSoup(open(filename), "html.parser")
        data.update(kanji(bs))
    with open("dat/reading.js", "w") as fout:
        json.dump(data, fout, ensure_ascii=False)
