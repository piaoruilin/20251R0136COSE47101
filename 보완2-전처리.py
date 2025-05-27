import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib


matplotlib.rc("font", family="NanumGothic")  # 또는 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지


# 📌 Step 0: 데이터 불러오기
df = pd.read_csv("top-10_with_genres_keywords.csv")  # 경로 수정 가능

# 📌 Step 1: 키워드 전처리
df = df.dropna(subset=["keywords"])  # 키워드 없는 행 제거
df["keywords_list"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["keywords_joined"] = df["keywords_list"].apply(lambda x: " ".join(x))

# 📌 Step 2: TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["keywords_joined"])

# 📌 Step 3: 클러스터링 (5개 그룹)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

# 📌 Step 4: 클러스터별 평균 시청 지표
cluster_summary = df.groupby("cluster")[["weekly_hours_viewed", "cumulative_weeks_in_top_10"]].mean()
cluster_summary = cluster_summary.rename(columns={
    "weekly_hours_viewed": "평균_주간_시청시간",
    "cumulative_weeks_in_top_10": "평균_Top10_유지_주차"
})
print(cluster_summary)

# 📌 Step 5 (선택): 클러스터별 시청 지표 시각화
cluster_summary.plot(kind='bar', figsize=(10,6))
plt.title("키워드 클러스터별 시청 지표")
plt.ylabel("평균 수치")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
