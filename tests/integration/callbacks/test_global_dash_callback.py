import pytest

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


def test_dash_callback_001(dash_duo):
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            dcc.Input(id="input"),
            html.Div(id="div-1"),
            html.Div(id="div-2"),
            html.Div(id="div-3"),
            html.Div(id="div-4"),
            html.Div(id="div-5"),
        ]
    )

    @dash.callback(Output("div-1", "children"), Input("input", "value"))
    def update_1(value):
        return f"Input 1 - {value}"

    @dash.callback(Output("div-2", "children"), Input("input", "value"))
    def update_2(value):
        return f"Input 2 - {value}"

    @app.callback(Output("div-3", "children"), Input("input", "value"))
    def update_3(value):
        return f"Input 3 - {value}"

    app.clientside_callback(
        """
        function (args) {return ('Input 4 - ' + args);}
        """,
        Output("div-4", "children"),
        Input("input", "value"),
    )

    dash.clientside_callback(
        """
        function (args) {return ('Input 5 - ' + args);}
        """,
        Output("div-5", "children"),
        Input("input", "value"),
    )

    dash_duo.start_server(app)
    input = dash_duo.find_element("#input")
    input.send_keys("dash.callback")
    dash_duo.wait_for_text_to_equal("#div-1", "Input 1 - dash.callback")
    dash_duo.wait_for_text_to_equal("#div-2", "Input 2 - dash.callback")
    dash_duo.wait_for_text_to_equal("#div-3", "Input 3 - dash.callback")
    dash_duo.wait_for_text_to_equal("#div-4", "Input 4 - dash.callback")
    dash_duo.wait_for_text_to_equal("#div-5", "Input 5 - dash.callback")