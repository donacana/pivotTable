import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

engine = create_engine(
    "postgresql://GGM:1111@localhost:5433/mydb"
)

sql = """
    SELECT *
    FROM vw_sales;
"""

sales = pd.read_sql(sql, engine)

sales["date"] = pd.to_datetime(sales["date"])
sales["년도"] = sales["date"].dt.year
sales["분기"] = sales["date"].dt.quarter
sales["월"] = sales["date"].dt.month

years = sorted(sales["년도"].unique())

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "매출 분석 대시보드",
            style={
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Label("조회 기준"),
                        dcc.RadioItems(
                            id="group-type",
                            options=[
                                {"label": "년도별", "value": "year"},
                                {"label": "분기별", "value": "quarter"},
                                {"label": "월별", "value": "month"},
                            ],
                            value="month",
                            inline=True,
                            inputStyle={"marginLeft": "12px", "marginRight": "5px"}
                        )
                    ],
                    style={"marginBottom": "15px"}
                ),

                html.Div(
                    [
                        html.Label("그래프 종류"),
                        dcc.RadioItems(
                            id="chart-type",
                            options=[
                                {"label": "선 그래프", "value": "line"},
                                {"label": "막대 그래프", "value": "bar"},
                            ],
                            value="line",
                            inline=True,
                            inputStyle={"marginLeft": "12px", "marginRight": "5px"}
                        )
                    ],
                    style={"marginBottom": "15px"}
                ),

                html.Div(
                    [
                        html.Label("연도 선택"),
                        dcc.Dropdown(
                            id="year-select",
                            options=[
                                {"label": f"{year}년", "value": year}
                                for year in years
                            ],
                            value=years[-1],
                            clearable=False,
                            style={"width": "180px", "marginTop": "5px"}
                        )
                    ],
                    id="year-select-area"
                )
            ],
            style={
                "width": "700px",
                "margin": "0 auto 20px auto",
                "padding": "20px",
                "border": "1px solid #dddddd",
                "borderRadius": "10px"
            }
        ),

        dcc.Graph(
            id="sales-chart",
            style={
                "width": "90%",
                "margin": "0 auto"
            },
            config={
                "displaylogo": False
            }
        )
    ],
    style={
        "padding": "20px"
    }
)


@app.callback(
    Output("year-select-area", "style"),
    Input("group-type", "value")
)
def show_year_select(group_type):
    if group_type == "month":
        return {
            "display": "block"
        }

    return {
        "display": "none"
    }


@app.callback(
    Output("sales-chart", "figure"),
    Input("group-type", "value"),
    Input("chart-type", "value"),
    Input("year-select", "value")
)
def update_chart(group_type, chart_type, selected_year):

    if group_type == "year":
        chart_data = (
            sales.groupby("년도", as_index=False)["sales_amount"]
            .sum()
        )

        chart_data["구분"] = chart_data["년도"].astype(str) + "년"
        title = "년도별 전체 매출"
        x_title = "년도"

    elif group_type == "quarter":
        chart_data = (
            sales.groupby(["년도", "분기"], as_index=False)["sales_amount"]
            .sum()
        )

        chart_data["구분"] = (
            chart_data["년도"].astype(str)
            + "년 "
            + chart_data["분기"].astype(str)
            + "분기"
        )

        title = "분기별 전체 매출"
        x_title = "분기"

    else:
        year_sales = sales[sales["년도"] == selected_year]

        chart_data = (
            year_sales.groupby("월", as_index=False)["sales_amount"]
            .sum()
        )

        all_months = pd.DataFrame({"월": range(1, 13)})

        chart_data = (
            all_months
            .merge(chart_data, on="월", how="left")
            .fillna(0)
        )

        chart_data["구분"] = chart_data["월"].astype(str) + "월"
        title = f"{selected_year}년 월별 전체 매출"
        x_title = "월"

    if chart_type == "line":
        figure = px.line(
            chart_data,
            x="구분",
            y="sales_amount",
            markers=True,
            title=title
        )
    else:
        figure = px.bar(
            chart_data,
            x="구분",
            y="sales_amount",
            title=title
        )

    figure.update_layout(
        template="plotly_white",
        title={
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title=x_title,
        yaxis_title="매출액",
        hovermode="x unified",
        margin={
            "l": 70,
            "r": 40,
            "t": 80,
            "b": 70
        }
    )

    figure.update_yaxes(
        tickformat=","
    )

    figure.update_xaxes(
        tickangle=0
    )

    return figure


if __name__ == "__main__":
    app.run(debug=True)