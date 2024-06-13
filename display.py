import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


from manipulations import BarChartBuilder

bar_chart_builder = BarChartBuilder()

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        # Row 1: General title for the app
        dbc.Row([dbc.Col(html.H1("General Title for the App"), width=12)]),
        # Row 2: h2 level header
        dbc.Row(
            [
                dbc.Col(html.H2("Subheading 1"), width=6),
                dbc.Col(html.H2("Subheading 2"), width=6),
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
        # Row 4: Two columns containing tables
        dbc.Row(
            [
                dbc.Col(html.Table(id="table-1"), width=6),
                dbc.Col(html.Table(id="table-2"), width=6),
            ]
        ),
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
