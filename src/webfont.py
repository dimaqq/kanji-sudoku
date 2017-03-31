import sys
import json
import subprocess
from os.path import relpath, exists

top = relpath(f"{__file__}/../../")

def split_webfont(font_file_name):
    done = set()
    css = []
    sets = json.loads(open(f"{top}/kanji.js").read().split(" = ", 1)[-1])
    for i, data in enumerate(sets.values()):
        data = "".join(set(data) - done)
        urange = ", ".join("U+%X" % s for s in sorted(map(ord, data)))
        subprocess.call(f"pyftsubset {font_file_name} --output-file={top}/fnt/stroke{i}.woff --flavor=woff --text={data}", shell=True)
        css.append(f"""
@font-face {{
    font-family: 'Kanji Stroke Order';
    font-weight: normal;
    font-style: normal;
    src: url('./stroke{i}.woff') format('woff');
    unicode-range: {urange};
    }}
        """)
        done = done.union(data)

    with open(f"{top}/fnt/font.css", "w") as fout:
        fout.write("".join(css))

if __name__ == "__main__":
    if len(sys.argv) < 2 or not exists(sys.argv[1]):
        exit(f"Usage: {sys.argv[0]} path/to/KanjiStrokeOrders_vN.NNN.ttf")
    split_webfont(sys.argv[1])

