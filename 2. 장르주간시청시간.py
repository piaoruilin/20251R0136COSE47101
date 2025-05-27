import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# ✅ 폰트 설정
matplotlib.rc('font', family='NanumGothic')  # 또는 찾은 한글 폰트 이름
plt.rcParams['axes.unicode_minus'] = False

# ✅ CSV 불러오기 (현재 디렉토리에 있다고 가정)
df = pd.read_csv("top-10_with_genres_keywords.csv")
df["week"] = pd.to_datetime(df["week"])
df["genres"] = df["genres"].str.split(", ")
df = df.explode("genres")

# ✅ 주차별 장르별 시청 시간 합계 계산
genre_week_hours = df.groupby(["week", "genres"])["weekly_hours_viewed"].sum().reset_index()
genre_pivot = genre_week_hours.pivot(index="week", columns="genres", values="weekly_hours_viewed").fillna(0)

# ✅ 가장 많이 시청된 상위 6개 장르 선택
top_genres = genre_pivot.sum().sort_values(ascending=False).head(6).index

# ✅ 시각화
genre_pivot[top_genres].plot(figsize=(14, 6), marker='o')

plt.title("Top10 내 장르별 주간 시청 시간 변화")
plt.xlabel("주차")
plt.ylabel("주간 시청 시간 (단위: 시간)")
plt.legend(title="장르")
plt.grid(True)
plt.tight_layout()

# 저장
plt.savefig("장르별_시청시간.png", dpi=300, bbox_inches='tight')
plt.show()
