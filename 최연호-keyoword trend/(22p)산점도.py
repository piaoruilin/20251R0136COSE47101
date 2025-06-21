import pandas as pd
import ast
from collections import defaultdict
import matplotlib.font_manager as fm
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# 1. 데이터 불러오기
df = pd.read_csv("top-10_with_genres_keywords.csv")  # 경로는 필요에 따라 수정

# 2. 키워드 리스트화
df = df.dropna(subset=["keywords"])
df["keywords"] = df["keywords"].apply(ast.literal_eval)

# 3. 키워드별 평균 생존력 및 시청 시간 집계
keyword_data = defaultdict(list)
for _, row in df.iterrows():
    for keyword in row["keywords"]:
        keyword_data[keyword].append({
            "weekly_hours_viewed": row["weekly_hours_viewed"],
            "cumulative_weeks_in_top_10": row["cumulative_weeks_in_top_10"]
        })

keyword_stats = []
for keyword, entries in keyword_data.items():
    avg_hours = sum(e["weekly_hours_viewed"] for e in entries) / len(entries)
    avg_weeks = sum(e["cumulative_weeks_in_top_10"] for e in entries) / len(entries)
    keyword_stats.append({
        "keyword": keyword,
        "avg_weekly_hours_viewed": avg_hours,
        "avg_cumulative_weeks": avg_weeks,
        "count": len(entries)
    })

# 4. 데이터프레임 정리
keyword_stats_df = pd.DataFrame(keyword_stats)
keyword_stats_df = keyword_stats_df.sort_values(by="count", ascending=False).head(30)

# 5. 폰트 설정 (Windows: 맑은 고딕)
matplotlib.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

# 6. 산점도 시각화
plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=keyword_stats_df,
    x="avg_cumulative_weeks",
    y="avg_weekly_hours_viewed",
    size="count",
    hue="keyword",
    palette="tab10",
    legend=False
)
plt.title("키워드별 평균 생존력 vs 평균 주간 시청시간")
plt.xlabel("평균 Top10 유지 주간 수")
plt.ylabel("평균 주간 시청시간 (시간)")
plt.tight_layout()

# 7. 이미지 저장
plt.savefig("키워드_생존력_시청시간_산점도.png", dpi=300)
plt.show()
