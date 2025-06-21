import pandas as pd
import ast
from collections import Counter, defaultdict
from pytrends.request import TrendReq
import time

# 1. 데이터 불러오기
df = pd.read_csv("merged_file.csv")
df["keywords"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
all_keywords = [kw for kws in df["keywords"] for kw in kws]
top_keywords = [kw for kw, _ in Counter(all_keywords).most_common(30)]

# 2. PyTrends 객체 (User-Agent 지정)
pytrends = TrendReq(hl='en-US', tz=0, requests_args={'headers': {'User-Agent': 'Mozilla/5.0'}})

# 3. 키워드 5개씩 나누어 요청
chunks = [top_keywords[i:i+5] for i in range(0, len(top_keywords), 5)]
all_trend_dfs = []

for chunk in chunks:
    try:
        pytrends.build_payload(chunk, timeframe='2022-01-01 2024-12-31', geo='')
        df_trend = pytrends.interest_over_time().drop(columns="isPartial", errors="ignore")
        all_trend_dfs.append(df_trend)
        time.sleep(10)  # Google 요청 제한 회피용
    except Exception as e:
        print(f"Error for keywords {chunk}: {e}")

# 4. 검색량 시계열 통합
trend_all = pd.concat(all_trend_dfs, axis=1)
trend_all = trend_all.loc[:, ~trend_all.columns.duplicated()]  # 중복 키워드 제거
trend_all["year"] = trend_all.index.year
yearly_avg = trend_all.groupby("year").mean().T
yearly_avg["growth(%)"] = (yearly_avg[2024] - yearly_avg[2021]) / yearly_avg[2021] * 100

# 5. 넷플릭스 키워드별 시청시간 평균 계산
kw_perf = defaultdict(list)
for _, row in df.iterrows():
    for kw in row["keywords"]:
        kw_perf[kw].append(row["weekly_hours_viewed"])

kw_avg_perf = pd.DataFrame(
    [{"keyword": k, "avg_hours": sum(v)/len(v)} for k, v in kw_perf.items()]
)

# 6. 병합 및 정렬
trend_growth = yearly_avg[["growth(%)"]].reset_index().rename(columns={"index": "keyword"})
merged_result = trend_growth.merge(kw_avg_perf, on="keyword", how="inner")
merged_result = merged_result.sort_values("growth(%)", ascending=False)

# 7. 결과 저장
merged_result.to_csv("전략키워드_트렌드+성과분석(통합).csv", index=False, encoding="utf-8-sig")
