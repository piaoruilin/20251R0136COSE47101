import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 1. 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'

# 2. 데이터 불러오기
df = pd.read_csv("merged_file.csv")
df["keywords"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["keyword_count"] = df["keywords"].apply(len)

# 3. 키워드 수별 평균 시청시간 계산
grouped = df.groupby("keyword_count")["weekly_hours_viewed"].mean().reset_index()

# 4. 상관관계 계산
correlation = df[["keyword_count", "weekly_hours_viewed"]].corr().iloc[0, 1]

# 5. 시각화 저장
plt.figure(figsize=(8, 5))
sns.barplot(x="keyword_count", y="weekly_hours_viewed", data=grouped, palette="Blues_d")
plt.xlabel("키워드 수")
plt.ylabel("평균 시청시간 (주간)")
plt.title(f"키워드 수 vs 평균 시청시간 (상관관계: {correlation:.2f})")
plt.tight_layout()
plt.savefig("키워드수_vs_시청시간.png", dpi=300)
plt.show()

# 6. 결과 CSV 저장
grouped["상관관계"] = correlation
grouped.to_csv("키워드수_시청시간분석.csv", index=False, encoding="utf-8-sig")
