from unittest import result
import pandas as pd
# [수정] 하단 시각화 함수들이 정상 호출되도록 상단에 라이브러리 import 선언 배치
import seaborn as sns
import matplotlib.pyplot as plt

# 맷플롯립 한글 폰트 깨짐 방지 설정 (대시보드 가독성 확보)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

if __name__ == '__main__':
    merged_sales = pd.read_pickle('data/merged_sales.pkl')
    merged_sales['판매가격'] = (
            merged_sales["수량"] *
            (merged_sales['단가'] * (1 - merged_sales['할인율']))
    )
    merged_sales['순이익'] = merged_sales['판매가격'] - (merged_sales['원가'] * merged_sales['수량'])

    # print(merged_sales.keys())
    # exit()

    result = pd.pivot_table(
        merged_sales,
        index=["분류명", "제품분류명", "제품명"],
        columns=["년도", "분기", "월(영문)"],
        values="순이익",
        aggfunc=sum,
        fill_value=0
    )

    # 1. 히트맵 시각화 (sns가 정상 임포트되어 이제 에러 없이 작동합니다)
    plt.figure(figsize=(14, 8))  # 히트맵이 겹치지 않도록 캔버스 크기 확보
    sns.heatmap(
        result,
        annot=True,
        fmt=".0f",  # 안전한 데이터 표현을 위해 포맷 코드 ".0f"로 보완
        cmap="YlGnBu",  # 대소문자 명확히 지정
    )
    plt.show()

    # 2. 바 차트 시각화 데이터 정렬 (피벗 테이블 구조에 맞게 수정)
    # [수정] 피벗 테이블의 전체 기간 순이익 합계를 구하여 '총순이익' 기준으로 상위 10개를 뽑도록 보완합니다.
    result['총순이익'] = result.sum(axis=1)
    top10 = result.sort_values("총순이익", ascending=False).head(10).reset_index()

    plt.figure(figsize=(12, 6))
    # [수정] 정렬 지표 컬럼 이름 매칭 변경
    plt.bar(top10["제품명"], top10["총순이익"])

    plt.title("제품별 총순이익 TOP 10")  # values 대상인 순이익에 맞춰 타이틀 변경
    plt.xlabel("제품명")
    plt.ylabel("총순이익")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # 원본 피벗 테이블 출력을 위해 임시로 만든 '총순이익' 컬럼을 제거하고 출력
    print(result.drop(columns=['총순이익']))