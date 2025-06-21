import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm

# ✅ 시스템에서 사용 가능한 한글 폰트 설정
import platform
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (Google Colab 포함)
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 불러오기
content_df = pd.read_csv("top-10_with_genres_keywords.csv")
content_df = content_df.dropna(subset=["keywords"])

import ast
content_df["keywords"] = content_df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# ✅ 클러스터 불러오기
cluster_df = pd.read_csv("클러스터별_대표_키워드.csv")
cluster_keywords = {}
for i, row in cluster_df.iterrows():
    keywords = [str(k).strip() for k in row[1:] if pd.notna(k)]
    cluster_keywords[i] = keywords

# ✅ 클러스터 할당
def assign_cluster(keywords):
    for cluster_id, cluster_kw in cluster_keywords.items():
        if any(kw in cluster_kw for kw in keywords):
            return cluster_id
    return -1

content_df["cluster"] = content_df["keywords"].apply(assign_cluster)

# ✅ 클러스터별 콘텐츠 수 시각화
cluster_counts = content_df["cluster"].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=cluster_counts.index.astype(str), y=cluster_counts.values, palette="Set3")
plt.title("클러스터별 콘텐츠 개수", fontsize=14)
plt.xlabel("클러스터 번호", fontsize=12)
plt.ylabel("콘텐츠 수", fontsize=12)
plt.tight_layout()
plt.savefig("클러스터별_콘텐츠_개수.png", dpi=300)
plt.show()
