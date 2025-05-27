import pandas as pd
import ast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Step 0. 데이터 불러오기
df = pd.read_csv("top-10_with_genres_keywords.csv")

# Step 1. 키워드 전처리
df = df.dropna(subset=["keywords"])  # 키워드 결측치 제거
df["keywords_list"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["keywords_joined"] = df["keywords_list"].apply(lambda x: " ".join(x))

# Step 2. TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["keywords_joined"])

# Step 3. KMeans 클러스터링
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X)

# Step 4. 클러스터별 대표 키워드 10개 추출
terms = vectorizer.get_feature_names_out()
top_keywords_per_cluster = {}

for cluster_num in range(5):
    cluster_indices = df[df["cluster"] == cluster_num].index
    cluster_tfidf_matrix = X[cluster_indices]
    mean_tfidf = np.asarray(cluster_tfidf_matrix.mean(axis=0)).flatten()
    top_indices = mean_tfidf.argsort()[-10:][::-1]
    top_keywords = [terms[i] for i in top_indices]
    top_keywords_per_cluster[cluster_num] = top_keywords

# Step 5. 결과 정리
top_keywords_df = pd.DataFrame.from_dict(top_keywords_per_cluster, orient="index")
top_keywords_df.columns = [f"Top{i+1}" for i in range(10)]
top_keywords_df.index.name = "클러스터"

# Step 6. 출력
print(top_keywords_df)
