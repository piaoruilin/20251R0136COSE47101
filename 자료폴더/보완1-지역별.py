import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError

# ✅ 한글 폰트 설정
matplotlib.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# ✅ Pytrends 연결
pytrends = TrendReq(hl='ko', tz=540)

# ✅ 분석 대상 키워드 (장르)
all_keywords = [
    "drama", "action", "animation", "romance", "thriller",
    "comedy", "crime", "documentary", "sci-fi", "horror"
]

# ✅ 키워드를 5개씩 나누기
keyword_groups = [all_keywords[i:i + 5] for i in range(0, len(all_keywords), 5)]

# ✅ 결과 저장용
merged_region_df = pd.DataFrame()

# ✅ 각 키워드 그룹마다 요청 (예외 처리 포함)
for group in keyword_groups:
    success = False
    for attempt in range(5):  # 최대 5번 재시도
        try:
            print(f"[INFO] 요청 중: {group} ...")
            pytrends.build_payload(group, geo='KR', timeframe='today 12-m')
            region_df = pytrends.interest_by_region()
            merged_region_df = pd.concat([merged_region_df, region_df[group]], axis=1)
            success = True
            print("[OK] 성공! 60초 대기 후 다음 요청 진행...")
            time.sleep(60)
            break
        except TooManyRequestsError:
            print(f"[WARN] 429 오류 발생, {group} 재시도 중... (1분 대기)")
            time.sleep(60)
    if not success:
        print(f"[FAIL] {group} 요청 실패, 건너뜀")

# ✅ 누락 열 제거 및 상위 국가만 보기
merged_region_df = merged_region_df.dropna(how='all')
top_regions = merged_region_df.sort_values(by='drama', ascending=False).head(10)

# ✅ 저장
top_regions.to_csv("google_trends_by_region_KR.csv", encoding='utf-8-sig')

# ✅ 시각화
top_regions.plot(kind='bar', figsize=(14, 6))
plt.title("한국 내 장르별 관심도 (Google Trends)")
plt.ylabel("관심도 지수 (0~100)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
