import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div(children=[html.Iframe(id = 'map', src = "https://raw.githubusercontent.com/alexchunet/bcac_pixart/main/assets/index.html", width='100%', height='900')])

if __name__ == '__main__':
    app.run_server()
