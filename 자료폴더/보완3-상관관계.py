import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib
matplotlib.rc("font", family="NanumGothic")  # 또는 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 📌 1. 데이터 불러오기 & 정제
df = pd.read_csv("top-10_with_genres_keywords.csv")
df = df.dropna(subset=["weekly_hours_viewed", "cumulative_weeks_in_top_10"])

# 📌 2. 상관계수 계산
corr, p_value = pearsonr(df["weekly_hours_viewed"], df["cumulative_weeks_in_top_10"])
print(f"📊 Pearson 상관계수: {corr:.3f}, p-value: {p_value:.5f}")

# 📌 3. 회귀 분석 (OLS)
X = sm.add_constant(df["weekly_hours_viewed"])
y = df["cumulative_weeks_in_top_10"]
model = sm.OLS(y, X).fit()
print(model.summary())

# 📌 4. 시각화
sns.regplot(
    x="weekly_hours_viewed",
    y="cumulative_weeks_in_top_10",
    data=df,
    scatter_kws={"alpha": 0.3}
)
plt.title("주간 시청시간과 Top10 유지 주차의 관계")
plt.xlabel("주간 시청 시간")
plt.ylabel("Top10 유지 주차")
plt.tight_layout()
plt.show()
