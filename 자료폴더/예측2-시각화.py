import os
import pandas as pd

# ✅ 경로 설정: 압축 해제된 trend_predictions 폴더
prediction_dir = r"C:\Users\saiyo\Documents\25-1Yoon\trend_predictions" 
# ✅ 병합 시작
merged_df = pd.DataFrame()

for file_name in sorted(os.listdir(prediction_dir)):
    if file_name.endswith(".csv"):
        file_path = os.path.join(prediction_dir, file_name)
        df = pd.read_csv(file_path)
        
        # 파일명에서 키워드 추출
        keyword = file_name.replace("_prediction.csv", "").replace("_", " ")
        df["keyword"] = keyword
        
        merged_df = pd.concat([merged_df, df], ignore_index=True)

# ✅ 저장 경로 설정 (원하는 경로로 수정 가능)
save_path = r"C:\Users\saiyo\Documents\25-1Yoon\merged_prediction_results.csv"

# ✅ CSV 저장
merged_df.to_csv(save_path, index=False, encoding="utf-8-sig")
print(f"✅ 저장 완료: {save_path}")
