import pandas as pd
import ast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# 데이터 불러오기
df = pd.read_csv("top-10_with_genres_keywords.csv")

# 키워드 리스트로 변환
df["keywords_list"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["keywords_joined"] = df["keywords_list"].apply(lambda x: " ".join(x))

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["keywords_joined"])

# Silhouette Score 계산
sil_scores_sampled = []
sample_size = 500
range_n_clusters = range(2, 11)

for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    preds = kmeans.fit_predict(X)

    if X.shape[0] > sample_size:
        idx = np.random.choice(X.shape[0], sample_size, replace=False)
        score = silhouette_score(X[idx], preds[idx])
    else:
        score = silhouette_score(X, preds)

    sil_scores_sampled.append(score)

# 그래프 시각화 및 저장
plt.figure(figsize=(8, 5))
plt.plot(range_n_clusters, sil_scores_sampled, marker='o', color='green')
plt.title("Silhouette Score by Number of Clusters")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.grid(True)
plt.savefig("silhouette_score_final.png")
plt.close()
