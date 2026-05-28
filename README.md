# THEME ETF MONITOR

터미널 스타일 테마 ETF 대시보드. 야후 파이낸스 데이터를 GitHub Actions로 매일 끌어와 정적 JSON으로 떨구고, GitHub Pages가 그걸 읽어서 렌더한다. 서버 없음.

## 구조

```
theme-etf-dashboard/
├── index.html                  # 대시보드 (data/etf_data.json 을 fetch)
├── data/etf_data.json          # 데이터 (Action 이 덮어씀, 지금은 샘플)
├── scripts/fetch_data.py       # yfinance → JSON 빌더
└── .github/workflows/update.yml# 스케줄 + 수동 실행
```

## 띄우기

1. 위 4개를 레포 루트에 그대로 넣고 push.
2. **Settings → Pages → Source: `main` / root** 로 배포.
3. **Settings → Actions → General → Workflow permissions: Read and write** 체크. 안 하면 봇이 JSON 커밋을 못 함.
4. **Actions 탭 → Update ETF data → Run workflow** 로 첫 데이터 강제 생성. 이후 평일 자동.

샘플 JSON이 들어있어서 Action 돌기 전에도 화면은 바로 뜬다. 우상단에 `SAMPLE DATA` 뱃지가 떠 있으면 아직 더미. 실데이터가 커밋되면 `LIVE` 로 바뀐다.

## 종목 / 그룹 손보기

`scripts/fetch_data.py` 상단 `GROUPS` 한 곳만 고치면 끝. 프론트는 JSON 구조만 보고 그린다. 행 추가/삭제해도 레이아웃이 알아서 채워진다.

## 지표

- **CLOSE** 종가
- **±%** 전일 대비 일간 변동
- **52W PEAK** 최근 2년 종가 고점 대비 하락률 (이미지2의 "최고점대비 하락률")

## 로컬 테스트

```bash
pip install yfinance
python scripts/fetch_data.py
python -m http.server 8000   # http://localhost:8000
```

## 알아둘 것

- 야후가 가끔 레이트리밋을 건다. 한 종목 실패해도 그 타일만 빈칸으로 두고 나머지는 정상 렌더.
- 샘플의 종가는 데모용 더미값이다. 실수치는 Action 이 처음 돌면서 덮어쓴다.
- 하락률 막대 폭은 "절대값 % = 막대 길이" (100% 에서 캡). 디자인 기준이지 정밀 스케일 아님.
