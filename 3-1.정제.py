import pandas as pd
import ast

# 1. 데이터 불러오기
df_max_weeks = pd.read_csv("top-10_max_weeks.csv")
df_genres_keywords = pd.read_csv("top-10_with_genres_keywords.csv")

# 2. 장르 정보 정제: show_title과 genres만 가져와 중복 제거
title_genres = df_genres_keywords[["show_title", "genres"]].drop_duplicates()

# 3. 문자열 형태의 리스트 처리: "['Drama']" → ['Drama']
title_genres["genres"] = title_genres["genres"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [x])

# 4. 장르 분해: 리스트 형태를 explode해서 개별 장르로
title_genres = title_genres.explode("genres")

# 5. 두 데이터 병합: show_title 기준으로 누적 주차 정보와 장르 결합
df_merged = pd.merge(df_max_weeks, title_genres, on="show_title", how="inner")

# 6. 장르별 Top10 유지기간 분석 (합계, 평균, 작품 수)
genre_lifetime = df_merged.groupby("genres")["cumulative_weeks_in_top_10"].agg(["sum", "mean", "count"])
genre_lifetime = genre_lifetime.sort_values(by="mean", ascending=False)

# 7. 결과 확인
print(genre_lifetime.head(10))

