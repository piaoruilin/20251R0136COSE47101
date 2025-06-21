import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# ✅ 한글 폰트 설정
matplotlib.rc('font', family='NanumGothic')  # 또는 'AppleGothic' for Mac
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 불러오기
df = pd.read_csv("장르별_Top10_유지기간_분석.csv")  # 필요 시 경로 수정

# ✅ 평균 생존력 기준 상위 30개 장르 추출
top_30_genres = df.sort_values(by="mean", ascending=False).head(30)

# ✅ 시각화
plt.figure(figsize=(10, 12))
sns.barplot(data=top_30_genres, x="mean", y="genres", palette="Blues_d")
plt.title("장르별 평균 Top10 유지 주간 수 (Top 30)", fontsize=16)
plt.xlabel("평균 유지 주간 수", fontsize=12)
plt.ylabel("장르", fontsize=12)
plt.tight_layout()

# ✅ 이미지 저장
plt.savefig("장르별_생존력_Top30.png", dpi=300)
plt.show()
    