import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# ✅ 한글 폰트 설정 (Windows용: 맑은 고딕)
matplotlib.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 1. CSV 파일 불러오기
df = pd.read_csv("C:/Users/saiyo/Documents/25-1Yoon/top-10_with_genres_keywords.csv")

# 2. 날짜 형식으로 변환
df["week"] = pd.to_datetime(df["week"])

# 3. 장르 컬럼 분리 및 전개
df["genres"] = df["genres"].str.split(", ")
df = df.explode("genres")

# 4. 주차별 장르 등장 횟수 집계
genre_week_counts = df.groupby(["week", "genres"]).size().reset_index(name="count")

# 5. 피벗 테이블 (행: 주차, 열: 장르)
genre_trend = genre_week_counts.pivot(index="week", columns="genres", values="count").fillna(0)

# 6. 가장 많이 등장한 상위 6개 장르만 추출
top_genres = genre_trend.sum().sort_values(ascending=False).head(6).index
genre_trend[top_genres].plot(figsize=(14, 6), marker='o')

# 7. 그래프 꾸미기 및 저장
plt.title("Top10 내 장르별 등장 수 변화 (주차 기준)")
plt.xlabel("주차 (Week)")
plt.ylabel("Top10 등장 횟수")
plt.legend(title="장르")
plt.grid(True)
plt.tight_layout()

# ✅ 이미지 저장
plt.savefig("장르트렌드_그래프.png", dpi=300, bbox_inches='tight')
