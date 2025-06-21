import pandas as pd
import ast
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 데이터 불러오기
df = pd.read_csv("top-10_with_genres_keywords.csv")

# 키워드 전처리
df["keywords_list"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["keywords_joined"] = df["keywords_list"].apply(lambda x: " ".join(x))

# 벡터화
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["keywords_joined"])

# 클러스터링 (3개 클러스터)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

# 라벨링
cluster_labels = {
    0: "로맨스 중심",
    1: "범죄/서스펜스",
    2: "정치/사회"
}
df["cluster_label"] = df["cluster"].map(cluster_labels)

# 저장
df.to_csv("clustered_with_labels.csv", index=False, encoding="utf-8-sig")
