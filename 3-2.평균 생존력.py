import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

# ✅ 한글 폰트 설정
matplotlib.rc('font', family='NanumGothic')  # or Malgun Gothic
plt.rcParams['axes.unicode_minus'] = False

# ✅ CSV 파일 읽기
df = pd.read_csv("장르별_Top10_유지기간_분석.csv")

# ✅ 평균 기준 상위 6개 장르 선택
top_lifetime_genres = df.sort_values(by="mean", ascending=False).head(6)
top_lifetime_genres.set_index("genres", inplace=True)  # 장르를 x축 레이블로

# ✅ 시각화
plt.figure(figsize=(10, 6))
plt.bar(top_lifetime_genres.index, top_lifetime_genres["mean"], color='skyblue')

plt.title("Top10 평균 생존력이 높은 장르 (평균 유지 주간 수)")
plt.ylabel("평균 Top10 유지 주간 수")
plt.xlabel("장르")
plt.xticks(rotation=45)
plt.tight_layout()

# ✅ 저장
plt.savefig("평균_생존력_상위_장르.png", dpi=300)
plt.show()
