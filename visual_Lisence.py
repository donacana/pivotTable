import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_ag_grid as dag

engine = create_engine(
    "postgresql://tndka:qwert12345@localhost:5433/mydb"
)

sql = """
    SELECT *
    FROM vw_sales;
"""

sales = pd.read_sql(sql, engine)

# 날짜 처리
sales["date"] = pd.to_datetime(sales["date"])
sales["년도"] = sales["date"].dt.year
sales["월"] = sales["date"].dt.month

# 데이터에 있는 연도 목록
years = sorted(sales["년도"].unique())
first_year = years[0]

app = Dash(__name__)

app.layout = html.Div([
    html.H2("연도별 월 매출 히트맵"),

    dcc.Store(
        id="current-year",
        data=first_year
    ),

    html.Div([
        html.Button("◀ 이전 년도", id="prev-year", n_clicks=0),

        html.H3(
            id="year-title",
            style={
                "display": "inline-block",
                "margin": "0 30px"
            }
        ),

        html.Button("다음 년도 ▶", id="next-year", n_clicks=0),
    ], style={
        "textAlign": "center",
        "marginBottom": "20px"
    }),

    dag.AgGrid(
        id="sales-grid",

        columnDefs=[],
        rowData=[],

        defaultColDef={
            "sortable": True,
            "filter": True,
            "resizable": True,
            "minWidth": 100
        },

        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 15
        },

        style={
            "height": "600px",
            "width": "100%"
        },

        className="ag-theme-alpine"
    )
])


# 이전 / 다음 버튼 클릭 시 연도 변경
@app.callback(
    Output("current-year", "data"),
    Input("prev-year", "n_clicks"),
    Input("next-year", "n_clicks"),
    State("current-year", "data")
)
def change_year(prev_clicks, next_clicks, current_year):

    if ctx.triggered_id == "prev-year":
        current_index = years.index(current_year)

        if current_index > 0:
            return years[current_index - 1]

    elif ctx.triggered_id == "next-year":
        current_index = years.index(current_year)

        if current_index < len(years) - 1:
            return years[current_index + 1]

    return current_year


# 선택된 연도의 월별 매출 테이블 생성
@app.callback(
    Output("sales-grid", "rowData"),
    Output("sales-grid", "columnDefs"),
    Output("year-title", "children"),
    Input("current-year", "data")
)
def update_grid(selected_year):

    year_sales = sales[sales["년도"] == selected_year]

    pivot_sales = pd.pivot_table(
        year_sales,
        index="product_name",
        columns="월",
        values="sales_amount",
        aggfunc="sum",
        fill_value=0
    )

    # 1월 ~ 12월 항상 표시
    pivot_sales = pivot_sales.reindex(
        columns=range(1, 13),
        fill_value=0
    )

    # 컬럼 이름 변경
    pivot_sales.columns = [f"{month}월" for month in pivot_sales.columns]

    pivot_sales = pivot_sales.reset_index()

    column_defs = [
        {
            "headerName": "제품명",
            "field": "product_name",
            "pinned": "left",
            "minWidth": 180
        }
    ]

    # 월별 히트맵 컬럼
    for month in range(1, 13):
        column_defs.append({
            "headerName": f"{month}월",
            "field": f"{month}월",
            "type": "numericColumn",

            "valueFormatter": {
                "function": "d3.format(',')(params.value)"
            },

            "cellStyle": {
                "styleConditions": [
                    {
                        "condition": "params.value === 0",
                        "style": {
                            "backgroundColor": "#f3f4f6",
                            "color": "#9ca3af"
                        }
                    },
                    {
                        "condition": "params.value > 0 && params.value < 100000",
                        "style": {
                            "backgroundColor": "#dbeafe"
                        }
                    },
                    {
                        "condition": "params.value >= 100000 && params.value < 300000",
                        "style": {
                            "backgroundColor": "#93c5fd"
                        }
                    },
                    {
                        "condition": "params.value >= 300000 && params.value < 500000",
                        "style": {
                            "backgroundColor": "#3b82f6",
                            "color": "white"
                        }
                    },
                    {
                        "condition": "params.value >= 500000",
                        "style": {
                            "backgroundColor": "#1e3a8a",
                            "color": "white",
                            "fontWeight": "bold"
                        }
                    }
                ],
                "defaultStyle": {
                    "textAlign": "right"
                }
            }
        })

    return (
        pivot_sales.to_dict("records"),
        column_defs,
        f"{selected_year}년 월별 매출 히트맵"
    )


if __name__ == "__main__":
    app.run(debug=True)
exit()
app = Dash(__name__)
app.layout = dash_table.DataTable(
    data=sales.to_dict("records"),
    columns=[{"name": col, "id": col} for col in sales.columns],
)

#
# app.layout = html.Div([
#     html.H1("Dash 시작", style={"width": "200px", "height": "200px"}),
#     html.P("첫번째 Dash 프로그램입니다."),
#     html.Button("클릭", id="btn1", style={"width": "50px", "height": "50px"}),
#     dcc.Input(id="k", type="text"),
#     dcc.Input(id="e", type="text"),
#     html.Div(id="result_k"),
#     html.Div(id="result_e"),
# ])
#
# @app.callback(
#     Output('result_k', 'children'),
#     Output('result_e', 'children'),
#     Input('k', 'value'),
#     Input('e', 'value'),
# )
# def update_output(k, e):
#     return F"입력값은 {k}", F"입력값은 {e}"

if __name__ == "__main__":
    app.run(debug=True)
    exit()
    sql ='''
        select * from vw_sales;
    '''

    sales = pd.read_sql(sql, engine)
    print(sales)