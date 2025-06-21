import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ 한글 폰트 설정 (NanumGothic 기준, 시스템에 따라 다른 폰트로 변경 가능)
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

# ✅ 병합된 데이터 불러오기
df = pd.read_csv("merged_file.csv")

# ✅ 클러스터별 평균 시청 시간 계산
watch_avg = df.groupby("cluster_label")["weekly_hours_viewed"].mean().sort_values(ascending=False)

# ✅ 클러스터별 평균 Top10 유지 주간 수 계산
week_avg = df.groupby("cluster_label")["cumulative_weeks_in_top_10_y"].mean().sort_values(ascending=False)

# ✅ 시각화 1: 클러스터별 평균 시청 시간
plt.figure(figsize=(10, 6))
watch_avg.plot(kind="bar", color="skyblue")
plt.title("클러스터별 평균 시청 시간", fontsize=16)
plt.ylabel("평균 시청 시간")
plt.xlabel("클러스터")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("클러스터별_평균_시청시간.png")
plt.close()

# ✅ 시각화 2: 클러스터별 평균 Top10 유지 주간 수
plt.figure(figsize=(10, 6))
week_avg.plot(kind="bar"    , color="salmon")
plt.title("클러스터별 평균 Top10 유지 주간 수", fontsize=16)
plt.ylabel("평균 유지 주간 수")
plt.xlabel("클러스터")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("클러스터별_평균_유지주간수.png")
plt.close()


