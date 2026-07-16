# 헬스로그

아이폰 홈 화면에 추가해서 쓰는 헬스 기록 웹앱(PWA). 운동일지 · 식단 · 인바디 · 통계 · 이론.
데이터는 폰 안(localStorage)에만 저장되고 서버로 전송되지 않는다.

## 기능

- **운동일지** — 부위/종목 선택 후 무게·횟수를 스테퍼로 기록. 종목별 볼륨 자동 계산
- **근육 지도** — 종목마다 타겟 근육을 정면·후면 도해에 표시 (주동근/협응근 구분)
- **휴식 타이머** — 세트 추가 시 자동 시작, 탭을 옮겨도 하단에 고정
- **식단** — 끼니별 칼로리·탄단지
- **인바디** — 체중·골격근량·체지방률·체지방량을 한 그래프에서 비교, 점을 누르면 그날 수치 표시
- **통계** — 종목별 볼륨 추이, 최고 무게 / 추정 1RM(Epley) / 최고 볼륨, 최근 7일 부위별 세트
- **이론** — 트레이닝 원리 노트(수정·추가 가능)
- **백업** — JSON 내보내기/불러오기, CSV 내보내기
- 오프라인 동작(서비스워커), 다크모드 지원

## 구조

```
gymlog.src.html   소스 (자리표시자 포함) — 여기를 수정한다
build.py          빌드: 자리표시자를 채워 결과물 2개 생성
extract_body.py   근육 도해 path 데이터 추출 (최초 1회)
bodydata.json     추출된 도해 데이터
docs/             GitHub Pages 배포 대상 (빌드 결과물)
gymlog.html       단일 파일 버전 (서비스워커 없음)
```

## 빌드

```bash
python build.py
```

`gymlog.src.html` 의 자리표시자를 채운다.

| 자리표시자 | 내용 |
|---|---|
| `__DOHYEON_B64__` | 도현 폰트(woff2)를 base64로 인라인 |
| `__BODY_DATA__` | 근육 도해 path 데이터 |
| `__PWA_HEAD__` | manifest·아이콘·서비스워커 등록 (docs 판에만) |

내용이 바뀌면 `sw.js` 의 캐시 버전이 자동으로 갱신돼 폰에서 새 버전을 받는다.

## 배포

`docs/` 폴더를 GitHub Pages 소스로 지정하면 끝. 수정 후에는 `python build.py` → commit → push.

## 라이선스 / 출처

- 근육 도해 path: [vulovix/body-muscles](https://github.com/vulovix/body-muscles) — Apache License 2.0
- 폰트: [도현(Do Hyeon)](https://fonts.google.com/specimen/Do+Hyeon) — SIL Open Font License 1.1

## 참고

이론 노트의 트레이닝 내용은 일반적인 가이드라인이다. 개인 상황에 따라 다르므로 통증이나 질환이 있으면 전문가와 상담할 것.
