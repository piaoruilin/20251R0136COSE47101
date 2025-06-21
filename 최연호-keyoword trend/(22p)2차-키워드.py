import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from collections import Counter
import ast

# ✅ 한글 폰트 설정 (Windows 기준: 맑은 고딕)
font_path = "C:/Windows/Fonts/malgun.ttf"
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 로드 및 전처리
df = pd.read_csv("top-10_with_genres_keywords.csv")  # 경로 수정 가능

# 문자열을 리스트로 변환
df['keywords'] = df['keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# 모든 키워드 수집
all_keywords = [kw for kws in df['keywords'] for kw in kws]

# 키워드 등장 횟수 계산
keyword_counts = Counter(all_keywords)

# Top 30 키워드 추출
top_keywords_df = pd.DataFrame(keyword_counts.most_common(30), columns=["keyword", "count"])

# ✅ 시각화
plt.figure(figsize=(12, 10))
sns.barplot(data=top_keywords_df, y="keyword", x="count", palette="viridis")
plt.title("Top 30 키워드 등장 빈도", fontsize=16)
plt.xlabel("빈도수", fontsize=12)
plt.ylabel("키워드", fontsize=12)
plt.tight_layout()

# ✅ 이미지 저장
plt.savefig("top30_keywords.png", dpi=300)  # 현재 작업 폴더에 저장
plt.show()

# ✅ Top 30 키워드 출력 (선택 사항)
print("🔎 Top 30 Keywords:\n")
print(top_keywords_df.to_string(index=False))
