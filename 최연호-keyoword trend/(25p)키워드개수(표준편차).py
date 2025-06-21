import pandas as pd
import ast
import matplotlib.pyplot as plt
import platform
import seaborn as sns
import numpy as np

# 1. 시스템별 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (예: Colab)
    # Colab의 경우에는 아래 주석 해제 후 설치 필요
    # !apt-get -qq install fonts-nanum
    # !fc-cache -fv
    # !rm ~/.cache/matplotlib -rf
    plt.rcParams['font.family'] = 'DejaVu Sans'  # Colab에선 기본 sans로 대체
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
df = pd.read_csv("merged_file.csv")
df["keywords"] = df["keywords"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["keyword_count"] = df["keywords"].apply(len)

# 3. 키워드 수별 통계값 계산
grouped = df.groupby("keyword_count")["weekly_hours_viewed"].agg(["mean", "std", "count"]).reset_index()
grouped.columns = ["키워드 수", "평균 시청시간", "표준편차", "콘텐츠 수"]

# 4. 에러바 그래프 시각화
plt.figure(figsize=(10, 6))
plt.errorbar(
    grouped["키워드 수"],
    grouped["평균 시청시간"],
    yerr=grouped["표준편차"],
    fmt='o', capsize=5, ecolor='gray', color='navy'
)
plt.xlabel("키워드 수")
plt.ylabel("평균 시청시간 ± 표준편차")
plt.title("키워드 수별 시청시간 평균 및 안정성")


plt.xticks(np.arange(0, grouped["키워드 수"].max() + 1, 5))

plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()

# 5. 이미지와 CSV 저장
plt.savefig("키워드수_시청시간_표준편차.png", dpi=300)
grouped.to_csv("키워드수_시청시간_표준편차.csv", index=False, encoding="utf-8-sig")
plt.show()
