# -*- coding: utf-8 -*-
"""
gymlog.src.html 의 자리표시자를 채워 두 가지 결과물을 만든다.

  gymlog.html       아티팩트용 — 단일 파일, 서비스워커 없음
  pages/index.html  GitHub Pages용 — manifest + 서비스워커로 오프라인 동작

자리표시자
  __DOHYEON_B64__  <- 도현 woff2 (base64)
  __BODY_DATA__    <- bodydata.json (근육 도해 path)
  __PWA_HEAD__     <- manifest/아이콘/서비스워커 등록 (pages 판만)

  python build.py

fonts/DoHyeon.woff2 가 없으면 fonts/DoHyeon.ttf 에서 자동 변환한다 (brotli 필요).
bodydata.json 은 extract_body.py 로 만든다.
"""
import base64
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
SRC = os.path.join(HERE, "gymlog.src.html")
OUT = os.path.join(HERE, "gymlog.html")
W2 = os.path.join(FONTS, "DoHyeon.woff2")
TTF = os.path.join(FONTS, "DoHyeon.ttf")
BODY = os.path.join(HERE, "bodydata.json")
PAGES = os.path.join(HERE, "docs")
PAGES_OUT = os.path.join(PAGES, "index.html")
SW_SRC = os.path.join(PAGES, "sw.js")
PLACEHOLDER = "__DOHYEON_B64__"
BODY_PH = "__BODY_DATA__"
PWA_PH = "__PWA_HEAD__"

PWA_HEAD = """<link rel="manifest" href="./manifest.json" />
<link rel="apple-touch-icon" href="./apple-touch-icon.png" />
<script>
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("./sw.js").catch(function () {});
    });
  }
</script>"""


def ensure_woff2():
    if os.path.exists(W2):
        return
    if not os.path.exists(TTF):
        sys.exit("DoHyeon.ttf 를 찾을 수 없습니다: " + TTF)
    from fontTools.ttLib import TTFont
    f = TTFont(TTF)
    f.flavor = "woff2"
    f.save(W2)
    print("변환: DoHyeon.ttf -> DoHyeon.woff2")


def main():
    ensure_woff2()
    with open(SRC, "r", encoding="utf-8") as f:
        html = f.read()
    for ph in (PLACEHOLDER, BODY_PH, PWA_PH):
        if ph not in html:
            sys.exit("소스에 " + ph + " 자리표시자가 없습니다.")

    with open(W2, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    html = html.replace(PLACEHOLDER, b64)

    if not os.path.exists(BODY):
        sys.exit("bodydata.json 이 없습니다. 먼저 extract_body.py 를 실행하세요.")
    with open(BODY, "r", encoding="utf-8") as f:
        body = f.read()
    html = html.replace(BODY_PH, body)

    # 1) 아티팩트용 — 단일 파일
    art = html.replace(PWA_PH, "")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(art)

    # 2) GitHub Pages용 — manifest + 서비스워커
    os.makedirs(PAGES, exist_ok=True)
    page = html.replace(PWA_PH, PWA_HEAD)
    with open(PAGES_OUT, "w", encoding="utf-8") as f:
        f.write(page)

    # 내용이 바뀌면 캐시 버전을 갱신해야 폰에서 새 버전을 받는다
    build_id = hashlib.sha1(page.encode("utf-8")).hexdigest()[:8]
    if os.path.exists(SW_SRC):
        with open(SW_SRC, "r", encoding="utf-8") as f:
            sw = f.read()
        sw = re.sub(r'const CACHE = "gymlog-[^"]*"',
                    'const CACHE = "gymlog-{}"'.format(build_id), sw)
        with open(SW_SRC, "w", encoding="utf-8") as f:
            f.write(sw)

    print("빌드 완료 (폰트 {:.0f} KB / 도해 {:.0f} KB)".format(
        os.path.getsize(W2) / 1024, os.path.getsize(BODY) / 1024))
    print("  아티팩트: {}  ({:.2f} MB)".format(OUT, os.path.getsize(OUT) / 1024 / 1024))
    print("  Pages   : {}  ({:.2f} MB)".format(PAGES_OUT, os.path.getsize(PAGES_OUT) / 1024 / 1024))
    print("  캐시 버전: gymlog-{}".format(build_id))


if __name__ == "__main__":
    main()
