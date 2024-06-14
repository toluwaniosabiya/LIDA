import dash  # type: ignore
from dash import dcc, html, Output, Input, dash_table  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import plotly.express as px  # type: ignore

# import pandas as pd  # type: ignore


from manipulations import BarChartBuilder, TableBuilder, LAFilter

bar_chart_builder = BarChartBuilder()
table_builder = TableBuilder()
la_filter = LAFilter()


# Define functions that do not require callback
def display_provision_type_table(data):
    df = table_builder.calculate_provision_types_breakdown(data).to_frame().reset_index()
    df.columns = ["Provision Type", "Count"]
    data = df.to_dict("records")

    return data


def display_facilities_count(data):

    return f"Total Number of Facilities: {table_builder.calculate_total_number_of_facilities(data)}"


def display_provision_places_count(data):

    return f"Total Number of Places: {table_builder.calculate_total_number_of_places(data)}"


def display_places_by_provision_type_table(data):
    df = table_builder.calculate_places_by_provision_type(data).to_frame().reset_index()
    df.columns = ["Provision Type", "Places"]
    data = df.to_dict("records")

    return data


# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

app.layout = dbc.Container(
    [
        # Row 1: General title for the app
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Overview Statistics from the 2022 OFSTED Data", className="text-center"),
                    width=12,
                )
            ]
        ),
        html.Hr(),
        dbc.Row([dbc.Col(html.H2("National Statistics", className="text-center"), width=12)]),
        html.Div(style={"height": "20px"}),
        # Row 2: h2 level header
        dbc.Row(
            [
                dbc.Col(html.H3("The United Kingdom at a Glance", className="text-center"), width=6),
                dbc.Col(html.H3("Social Care Effectiveness", className="text-center"), width=6),
            ]
        ),
        # Row 3: Two columns, each containing a drop-down menu and a graph/figure
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="dropdown-1",
                                        options=[
                                            {"label": "Option 1", "value": "1"},
                                            {"label": "Option 2", "value": "2"},
                                        ],
                                    ),
                                    width=12,
                                )
                            ]
                        ),
                        dbc.Row([dbc.Col(dcc.Graph(id="graph-1"), width=12)]),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="effectiveness-dropdown",
                                        options=bar_chart_builder.get_dropdown_options(),
                                        value=bar_chart_builder.get_dropdown_options()[0]["value"],
                                    ),
                                    width=12,
                                )
                            ]
                        ),
                        dbc.Row([dbc.Col(dcc.Graph(id="outcome"), width=12)]),
                    ],
                    width=6,
                ),
            ]
        ),
        # Row 4: Four columns containing tables and markdown
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(
                        display_facilities_count(table_builder.dataset),
                        id="facilities-count",
                        style={"fontSize": "24px"},
                    ),
                    width=1,
                ),
                dbc.Col(
                    dash_table.DataTable(
                        data=display_provision_type_table(table_builder.dataset),
                        id="provision-types",
                        style_cell={
                            "textAlign": "left",
                            "maxWidth": "150px",
                            "whiteSpace": "normal",
                        },
                    ),
                    width=5,
                ),
                dbc.Col(
                    dcc.Markdown(
                        display_provision_places_count(table_builder.dataset),
                        id="places-count",
                        style={"fontSize": "24px"},
                    ),
                    width=1,
                ),
                dbc.Col(
                    dash_table.DataTable(
                        data=display_places_by_provision_type_table(table_builder.dataset),
                        id="places-by-provision-type",
                        style_cell={
                            "textAlign": "left",
                            "maxWidth": "150px",
                            "whiteSpace": "normal",
                        },
                    ),
                    width=5,
                ),
            ]
        ),
        html.Div(style={"height": "20px"}),
        html.Hr(),
        html.Div(style={"height": "50px"}),
        # Row 5: Another h2 level header
        dbc.Row([dbc.Col(html.H2("LA-level Statistics", className="text-center"), width=12)]),
        html.Div(style={"height": "20px"}),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="local-authority",
                        options=la_filter.get_la_dropdown_options(),
                        value=la_filter.get_la_dropdown_options()[0]["value"],
                    ),
                    width=3,
                )
            ]
        ),
        html.Div(style={"height": "10px"}),
        # Row 6: Four columns containing tables and markdown
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(id="la-facilities-count", style={"fontSize": "24px"}),
                    width=1,
                ),
                dbc.Col(
                    dash_table.DataTable(
                        id="la-provision-types",
                        style_cell={
                            "textAlign": "left",
                            "maxWidth": "150px",
                            "whiteSpace": "normal",
                        },
                    ),
                    width=5,
                ),
                dbc.Col(
                    dcc.Markdown(id="la-places-count", style={"fontSize": "24px"}),
                    width=1,
                ),
                dbc.Col(
                    dash_table.DataTable(
                        id="la-places-by-provision-type",
                        style_cell={
                            "textAlign": "left",
                            "maxWidth": "150px",
                            "whiteSpace": "normal",
                        },
                    ),
                    width=5,
                ),
            ]
        ),
        html.Div(style={"height": "50px"}),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="la-level-effectiveness-dropdown",
                        options=la_filter.get_la_effectiveness_dropdown_options(),
                        value=la_filter.get_la_effectiveness_dropdown_options()[0]["value"],
                    ),
                    width=6,
                )
            ]
        ),
        # Row 6: la-level bar charts
        dbc.Row([dbc.Col(dcc.Graph(id="la-level-effectiveness"), width=12)]),
    ],
    fluid=True,
)


@app.callback(
    Output("outcome", "figure"),
    Input("effectiveness-dropdown", "value"),
)
def display_bar_chart(drop_down_option: str):
    series = bar_chart_builder.supply_bar_chart_info(column=drop_down_option)
    fig = px.bar(
        series,
        color=series.index,
        title="",
    )

    fig.update_layout(
        yaxis_title="Percentage (%)",
        xaxis=dict(
            tickvals=[],  # Empty list to hide x-axis tick values
            ticktext=[],  # Empty list to hide x-axis tick labels
        ),
        legend=dict(
            title="Categories",
        ),
    )

    return fig


@app.callback(
    Output("la-facilities-count", "children"),
    Output("la-provision-types", "data"),
    Output("la-places-count", "children"),
    Output("la-places-by-provision-type", "data"),
    Input("local-authority", "value"),
)
def display_la_level_provision_type_and_places_statistics(local_authority: str):
    df = la_filter.filter_dataset_by_LA(local_authority=local_authority)
    facilities_count = display_facilities_count(df)
    provision_type_table = display_provision_type_table(df)
    places_count = display_provision_places_count(df)
    places_by_provision_type = display_places_by_provision_type_table(df)

    return facilities_count, provision_type_table, places_count, places_by_provision_type


@app.callback(
    Output("la-level-effectiveness", "figure"),
    Input("local-authority", "value"),
    Input("la-level-effectiveness-dropdown", "value"),
)
def display_la_level_effectiveness_barchart(local_authority: str, drop_down_option: str):
    df = la_filter.filter_dataset_by_LA(local_authority=local_authority)
    series = la_filter.supply_la_level_bar_chart_info(data=df, column=drop_down_option)
    fig = px.bar(
        series,
        color=series.index,
        title="",
    )

    fig.update_layout(
        yaxis_title="Percentage (%)",
        xaxis=dict(
            tickvals=[],  # Empty list to hide x-axis tick values
            ticktext=[],  # Empty list to hide x-axis tick labels
        ),
        legend=dict(
            title="Categories",
        ),
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
