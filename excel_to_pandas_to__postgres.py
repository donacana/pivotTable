from calendar import prmonth

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://tndka:qwert12345@localhost:5432/postgres"
)

if __name__ == "__main__":
    sales = pd.read_excel('./data/Sales.xlsx')
    details = pd.read_excel('./data/Details.xlsx', sheet_name=None)
    regions = details['지역']
    promotions = details['프로모션']
    channels = details["채널"]
    customers = details["2018년도~2022년도 주문고객"]
    products = details["제품"]
    product_categories = details["제품분류"]
    categories = details["분류"]
    date = details["날짜"]

    sales.rename(
        columns={
            "날짜": "date",
            "제품코드": "product_code",
            "고객코드": "customer_code",
            "프로모션코드": "promotion_code",
            "채널코드": "channel_code",
            "Quantity": "quantity",
        },
        inplace=True

    )
    sales.insert(0, "id", range(1, len(sales) + 1))

    sales.to_sql(
        "sales",
        engine,
        index=False,
        if_exists="replace",
    )
    sql = text('''
            ALTER TABLE sales ADD PRIMARY KEY (id);

            ALTER TABLE sales ADD FOREIGN KEY (product_code) REFERENCES products (id);
            ALTER TABLE sales ADD FOREIGN KEY (customer_code) REFERENCES customers (id);
            ALTER TABLE sales ADD FOREIGN KEY (promotion_code) REFERENCES promotions (id);
            ALTER TABLE sales ADD FOREIGN KEY (channel_code) REFERENCES channels (id);

            ALTER TABLE sales DROP COLUMN IF EXISTS "지역";
            ALTER TABLE sales DROP COLUMN IF EXISTS "UnitPrice";
        ''')

    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()

    exit()

    customers.rename(
        columns={
            '고객코드': "id",
            "지역코드": "region_code",
            "고객명": "customer_name",
            "성별": "gender",
            "생년월일": "birth_date",
        },
        inplace=True
    )
    customers.to_sql(
        "customers",
        engine,
        index=False,
        if_exists="replace",
    )
    sql = text('''
                                  alter table customers
                                      add primary key (id),
                                      add foreign key (region_code) references regions (id);
                                  ''')

    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()

    exit()
    channels.rename(
        columns={
        "채널코드": "id",
        "채널명": "channel_name",

        },
        inplace=True
    )
    channels.to_sql(
        "channels",
        engine,
        index=False,
        if_exists="replace",
    )
    sql = text('''
                               alter table channels
                                   add primary key (id)
                               ''')
    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()

    exit()

    regions.rename(
        columns={

        '지역코드': "id",
        '시도': "province",
        '구군시': 'city_district',
        '지역': 'region_name',
    },
        inplace=True

    )

    regions.to_sql(
        "regions",
        engine,
        index=False,
        if_exists="replace",
    )
    sql = text('''
                           alter table regions
                               add primary key (id)
                           ''')


    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()
    exit()

    promotions.rename(
        columns={
        "프로모션코드": "id",
        "프로모션": "promotion_name",
        "할인율": "discount_rate"
        },
    inplace=True
    )
    promotions.to_sql(
        "promotions",
        engine,
        index=False,
        if_exists="replace",
    )
    sql = text('''
                alter table promotions
                    add primary key (id)
            ''')
    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()

    exit()

    products.rename(
        columns={
            "제품코드": "id",
            "제품명": "product_name",
            "색상": "color",
            "원가": "price",
            "단가": "sale_price",
            "제품분류코드": "product_category_code"
        },
        inplace=True
    )
    products.to_sql(
        "products",
        engine,
        index=False,
        if_exists="replace",
    )
    sql = text('''
                   alter table products
                       add primary key (id)
                   ''')

    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()

    sql = text('''
            alter table products
                add foreign key (product_category_code) references products_categories (id);
                   ''')

    with engine.begin() as conn:
        conn.execute(sql)
        conn.commit()

    sales.rename(
        columns={
            "주문번호": "id",
            "주문일자": "order_date",
            "고객번호": "customer_id",
            "제품코드": "product_id",
            "수량": "quantity"
        },
        inplace=True
    )


    sales.to_sql(
        "sales",
        engine,
        index=False,
        if_exists="replace",
    )

    sql_sales_pk = text('''
            alter table sales
                add primary key (id);
        ''')
    with engine.begin() as conn:
        conn.execute(sql_sales_pk)
        conn.commit()

    exit()

