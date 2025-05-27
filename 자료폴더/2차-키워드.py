import pandas as pd
from collections import Counter
import ast

# 데이터 로드
df = pd.read_csv("top-10_with_genres_keywords.csv")

# 키워드 파싱: 문자열을 리스트로 변환
df['keywords'] = df['keywords'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# 전체 키워드 빈도 세기
all_keywords = [kw for kws in df['keywords'] for kw in kws]
keyword_counts = Counter(all_keywords)

# 상위 키워드 출력
print(keyword_counts.most_common(30))
