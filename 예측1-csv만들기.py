import time
import os
import pandas as pd
import numpy as np
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression

# ✅ 예측에 사용할 키워드 목록 (조정 가능)
keywords = ['war']

# ✅ pytrends 초기화 및 결과 폴더 준비
pytrends = TrendReq(hl='en-US', tz=540)
os.makedirs("trend_predictions", exist_ok=True)

# ✅ 키워드 반복 처리 (429 에러 대비 재시도 포함)
for kw in keywords:
    for attempt in range(5):  # 최대 5회 재시도
        try:    
            pytrends.build_payload([kw], timeframe='today 5-y', geo='')
            df = pytrends.interest_over_time()

            if df.empty or 'isPartial' not in df.columns:
                print(f"[SKIP] {kw}: 데이터 없음")
                break

            df = df[~df['isPartial']].reset_index()
            df["timestamp"] = df["date"].map(pd.Timestamp.toordinal)

            X = df[["timestamp"]]
            y = df[kw]
            model = LinearRegression().fit(X, y)

            future_dates = pd.date_range(start=df["date"].iloc[-1], periods=27, freq="W")
            future_ordinals = future_dates.map(pd.Timestamp.toordinal).to_numpy().reshape(-1, 1)
            future_preds = model.predict(future_ordinals)

            result_df = pd.DataFrame({
                "date": future_dates,
                "keyword": kw,
                "predicted_interest": future_preds
            })

            filename = f"trend_predictions/{kw.replace(' ', '_')}_prediction.csv"
            result_df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"[OK] 저장 완료: {kw}")

            time.sleep(60)  # 성공 후 60초 대기
            break

        except Exception as e:
            print(f"[RETRY {attempt+1}] {kw} 실패: {e}")
            time.sleep(60)
