# -*- coding: utf-8 -*-
"""
vulovix/body-muscles (Apache-2.0) 의 근육 path 데이터를 받아
bodydata.json 으로 추출한다. 한 번만 실행하면 된다.

  python extract_body.py

출처: https://github.com/vulovix/body-muscles  (Apache License 2.0)
"""
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://raw.githubusercontent.com/vulovix/body-muscles/main/src/data/"
OUT = os.path.join(HERE, "bodydata.json")

# 렌더러 BodyChart.ts 기준 viewBox
VIEWBOX = {"front": "0 0 35 93", "back": "37 0 35 93"}

# 근육이 아닌(항상 중립 흰색으로 둘) 부위
NEUTRAL = re.compile(r"^(head|face|neck|nape|hand|foot|knee|elbow|head-back)")


def fetch(name):
    with urllib.request.urlopen(BASE + name, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(ts):
    """{ id: "...", name: "...", view: ..., path: "..." } 블록에서 id/path 추출."""
    out = []
    for m in re.finditer(r'id:\s*"([^"]+)".*?path:\s*"([^"]+)"', ts, re.S):
        out.append([m.group(1), m.group(2)])
    return out


def main():
    front = parse(fetch("muscles.front.ts"))
    back = parse(fetch("muscles.back.ts"))
    if not front or not back:
        raise SystemExit("path 추출 실패 — 업스트림 형식이 바뀌었을 수 있습니다.")

    data = {
        "_license": "Muscle path data from https://github.com/vulovix/body-muscles - Apache License 2.0",
        "viewBox": VIEWBOX,
        "front": front,
        "back": back,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    ids = [i for i, _ in front + back]
    neutral = [i for i in ids if NEUTRAL.match(i)]
    print("front {} / back {} = 총 {}개 부위".format(len(front), len(back), len(ids)))
    print("중립(근육 아님) {}개: {}".format(len(neutral), ", ".join(neutral[:8]) + " ..."))
    print("저장: {}  ({:,} bytes)".format(OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
