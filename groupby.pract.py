from unittest import result

import pandas as pd

if __name__ == '__main__':
    merged_sales = pd.read_pickle('data/merged_sales.pkl')
    merged_sales['판매가격']=(
        merged_sales["수량"]*
        (merged_sales['단가']*(1-merged_sales['할인율']))
    )
    #print(merged_sales.keys())
    #exit()

    result = pd.pivot_table(
        merged_sales,
        index=["분류명","제품분류명","제품명"],
        columns=["년도","분기","월(영문)"],
        values="순이익",
        aggfunc=sum,
        fill_value=0
    )
    sns.heatmap(
        result,
        annot=True,
        fmt="0",
        cmap="ylGnBu",

    )
    plt.show()



    import matplotlib.pyplot as plt

    # 총매출액 상위 10개 제품
    top10 = result.sort_values("총매출액", ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    plt.bar(top10["제품명"], top10["총매출액"])

    plt.title("제품별 총매출액 TOP 10")
    plt.xlabel("제품명")
    plt.ylabel("총매출액")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    print(result)


