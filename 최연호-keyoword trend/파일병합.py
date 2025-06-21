import pandas as pd

# ✅ 파일 경로 (현재 작업 폴더 기준)
df_keywords = pd.read_csv("top-10_with_genres_keywords.csv")
df_performance = pd.read_csv("top-10_max_weeks.csv")

# ✅ 컬럼명 확인
print("Keywords 파일 컬럼:", df_keywords.columns)
print("Performance 파일 컬럼:", df_performance.columns)

df = pd.merge(df_keywords, df_performance, on="show_title")
df.to_csv("merged_keywords_performance.csv", index=False, encoding="utf-8-sig")
