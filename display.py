import dash  # type: ignore
from dash import dcc, html, Output, Input, dash_table  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import plotly.express as px  # type: ignore

# import pandas as pd  # type: ignore


from manipulations import BarChartBuilder, TableBuilder

bar_chart_builder = BarChartBuilder()
table_builder = TableBuilder()


# Define functions that do not require callback
def display_provision_type_table():
    df = table_builder.calculate_provision_types_breakdown().to_frame().reset_index()
    df.columns = ["Provision Type", "Count"]
    data = df.to_dict("records")

    return data


def display_facilities_count():

    return f"Total Number of Facilities: {table_builder.calculate_total_number_of_facilities()}"


def display_provision_places_count():

    return f"Total Number of Places: {table_builder.calculate_total_number_of_places()}"


def display_places_by_provision_type_table():
    df = table_builder.calculate_places_by_provision_type().to_frame().reset_index()
    df.columns = ["Provision Type", "Places"]
    data = df.to_dict("records")

    return data


# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
        html.Div(style={"height": "20px"}),
        # Row 2: h2 level header
        dbc.Row(
            [
                dbc.Col(html.H2("The United Kingdom at a Glance", className="text-center"), width=6),
                dbc.Col(html.H2("Social Care Effectiveness", className="text-center"), width=6),
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
                                        id="effectiveness",
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
                        display_facilities_count(),
                        id="facilities-count",
                    ),
                    width=1,
                ),
                dbc.Col(
                    dash_table.DataTable(
                        data=display_provision_type_table(),
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
                        display_provision_places_count(),
                        id="places-count",
                    ),
                    width=1,
                ),
                dbc.Col(
                    dash_table.DataTable(
                        data=display_places_by_provision_type_table(),
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
        # Row 5: Another h2 level header
        dbc.Row([dbc.Col(html.H2("Subheading 2"), width=12)]),
        # Row 6: Two columns containing markdown text
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown("## Markdown Text 1\n\nSome example markdown text here."),
                    width=6,
                ),
                dbc.Col(
                    dcc.Markdown("## Markdown Text 2\n\nSome more example markdown text here."),
                    width=6,
                ),
            ]
        ),
        # Row 7: Two columns containing tables
        dbc.Row(
            [
                dbc.Col(html.Table(id="table-3"), width=6),
                dbc.Col(html.Table(id="table-4"), width=6),
            ]
        ),
        # Row 8: Five columns containing markdown text
        dbc.Row(
            [
                dbc.Col(dcc.Markdown("### Markdown 1\n\nText 1"), width=2),
                dbc.Col(dcc.Markdown("### Markdown 2\n\nText 2"), width=2),
                dbc.Col(dcc.Markdown("### Markdown 3\n\nText 3"), width=2),
                dbc.Col(dcc.Markdown("### Markdown 4\n\nText 4"), width=2),
                dbc.Col(dcc.Markdown("### Markdown 5\n\nText 5"), width=2),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("outcome", "figure"),
    Input("effectiveness", "value"),
)
def display_bar_chart(drop_down_option: str):
    series = bar_chart_builder.supply_bar_chart_info(column=drop_down_option)
    fig = px.bar(
        series,
        color=series.index,
        title=drop_down_option,
    )

    fig.update_layout(
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
