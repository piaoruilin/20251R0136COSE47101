# 📌 필요한 라이브러리
from pytrends.request import TrendReq
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib

# 📌 한글 폰트 설정 (윈도우: 맑은 고딕)
matplotlib.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# ✅ pytrends 초기화
pytrends = TrendReq(hl='en-US', tz=540)

# ✅ 분석할 국가 코드 목록
countries = ['KR', 'JP', 'US', 'GB', 'IN']  # 한국, 일본, 미국, 영국, 인도
genres = ['drama', 'action', 'animation', 'romance', 'thriller']

# ✅ 결과 저장 딕셔너리
all_data = {}

# ✅ 각 국가별로 요청 및 평균값 계산
for country in countries:
    try:
        print(f"[INFO] {country} 데이터 요청 중...")
        pytrends.build_payload(genres, geo=country, timeframe='today 12-m')
        df = pytrends.interest_over_time()

        if not df.empty:
            all_data[country] = df[genres].mean()
        else:
            print(f"[WARN] {country} 데이터 없음")

        time.sleep(10)  # 요청 간 딜레이 (429 방지)
    except Exception as e:
        print(f"[ERROR] {country} 처리 중 오류 발생:", e)

# ✅ 데이터프레임 통합
region_df = pd.DataFrame(all_data).T  # 국가가 행, 장르가 열
region_df.index.name = "국가"

# ✅ 저장
region_df.to_csv("google_trends_by_country.csv", encoding="utf-8-sig")
print("[OK] CSV 저장 완료")

# ✅ 시각화
region_df.plot(kind='bar', figsize=(12, 6))
plt.title("국가별 장르 관심도 비교 (Google Trends 기준)")
plt.ylabel("관심도 지수 (0~100)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
