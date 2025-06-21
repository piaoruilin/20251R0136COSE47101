# ✅ 필요한 라이브러리 불러오기
import pandas as pd
import matplotlib.pyplot as plt
import platform

# ✅ 한글 폰트 설정 (운영체제별)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'

# ✅ CSV 파일 불러오기
df = pd.read_csv("전략키워드_트렌드+성과분석(통합).csv")  # 파일 경로 확인 필요

# ✅ 성장률 기준 상위 10개 키워드 추출
top10 = df.sort_values("growth(%)", ascending=False).head(15)

# ✅ 수평 막대 그래프 생성
plt.figure(figsize=(10, 6))
plt.barh(top10["keyword"], top10["growth(%)"], color='tomato')
plt.xlabel("검색량 증가율 (%)")
plt.title("Google Trends 기준 키워드 성장률 (2021 → 2024)")
plt.gca().invert_yaxis()
plt.tight_layout()

# ✅ 저장 (파일명 변경 가능)
plt.savefig("전략키워드_GoogleTrends성장률_TOP10.png", dpi=300)
plt.show()
