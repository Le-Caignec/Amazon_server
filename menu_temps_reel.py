""" menu_temps_reel """
import threading
import time as TimeS
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly
from dash.dependencies import Input, Output
import paramiko
import script
import log_parser
import map_ip

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

CLIENT =script.ssh_conn()
SERVEUR_ACTUEL = 'monitorme1.ddns.net'

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div([
        html.H2("MENU", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/Accueil", active="exact"),
                dbc.NavLink("Graphs", href="/Graphs", active="exact"),
                dbc.NavLink("Serveur info", href="/Serveur_info", active="exact"),
                dbc.NavLink("Paramètres", href="/Parametres", active="exact"),
                dbc.NavLink("Logs", href="/Logs", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(id="page-content", children=[], style=CONTENT_STYLE),
    dcc.Interval(
            id='interval-component',
            interval=4*1000, # in milliseconds
            n_intervals=0
        )
])

DATA = {
        'time': [],
        'number_process': [],
        'get_memory_free': [],
        'get_memory_used': [],
        'get_processor_used': [],
        'nb_connection': [],
        'nb_404': [],
        'ping_moyen': []
    }

STATIC_CPU_MODEL = str(script.get_cpu_model_name(CLIENT))
STATIC_CACHE_SIZE = str(script.get_cache_size(CLIENT))
STATIC_CPU_FREQ = str(script.get_cpu_frequency(CLIENT))
STATIC_NB_CORES = str(script.get_number_of_cores(CLIENT))
STATIC_MEM_TOTAL = str(script.get_memory_total(CLIENT))
FIGURE_MAP = map_ip.localise(CLIENT)

def collect_data():
    """ collect_data """
    while RUN_THREAD:
        try :
            # Collect some DATA
            global LOG_TOTAL
            global LOG_TOTAL_RESPONSE
            LOG_TOTAL,LOG_TOTAL_RESPONSE=log_parser.recup_log(CLIENT)
            time = datetime.datetime.now()
            number_process=script.get_ps(CLIENT)
            get_memory_free=script.get_memory_free(CLIENT)
            get_memory_used=script.get_memory_used(CLIENT)
            get_processor_used=script.get_processor_used(CLIENT)
            nb_connection,dummy=log_parser.number_of_diff_ip(LOG_TOTAL)
            nb_404=log_parser.nb_of_errors(LOG_TOTAL)
            ping_moyen=log_parser.get_average_ping(LOG_TOTAL_RESPONSE)

            if len(DATA['time'])>=55:

                del DATA['time'][0]
                del DATA['number_process'][0]
                del DATA['get_memory_free'][0]
                del DATA['get_memory_used'][0]
                del DATA['get_processor_used'][0]
                del DATA['nb_connection'][0]
                del DATA['nb_404'][0]
                del DATA['ping_moyen'][0]

            DATA['time'].append(time)
            DATA['number_process'].append(number_process)
            DATA['get_memory_free'].append(get_memory_free)
            DATA['get_memory_used'].append(get_memory_used)
            DATA['get_processor_used'].append(get_processor_used)
            DATA['nb_connection'].append(nb_connection)
            DATA['nb_404'].append(nb_404)
            DATA['ping_moyen'].append(ping_moyen)
        except paramiko.ssh_exception.SSHException:
            print('pb dans le thread')
        finally:
            TimeS.sleep(2)

def draw_graph(information):
    """ draw_graph """
    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': DATA['time'],
        'y': DATA[information],
        'name': information,
        'mode': 'lines+markers',
        'type': 'scatter'
    },1,1)
    return fig

def draw_graph_bar(information1,information2):
    """ draw_graph_bar """
    fig={
            'data': [
                {'x': DATA['time'], 'y': DATA[information1], 'type': 'bar', 'name': information1},
                {'x': DATA['time'], 'y': DATA[information2], 'type': 'bar', 'name': information2},
            ],
        }
    return fig

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"),
    Input('interval-component', 'n_intervals')]
)

def render_page_content(pathname, n):
    """ render_page_content """
    if pathname == "/Accueil":
        return [
                html.H1('Accueil',
                        style={'textAlign':'center'}),
                html.H4('Localisation des différentes ip connectées au serveur :'+SERVEUR_ACTUEL,
                style={'textAlign':'left'}),

                dcc.Graph(figure=FIGURE_MAP),

                ]
    if pathname == "/Graphs":
        figure1 = draw_graph('number_process')
        figure2 = draw_graph_bar('get_memory_free','get_memory_used')
        figure3 = draw_graph('get_processor_used')
        figure4 = draw_graph('nb_connection')
        figure5 = draw_graph('nb_404')
        figure6 = draw_graph('ping_moyen')
        return [
                html.H1('Graphs',
                        style={'textAlign':'center'}),
                html.H4('Nombre de processus en cours',
                        style={'textAlign':'left'}),
                dcc.Graph(figure=figure1),
                html.H4('Evolution de la mémoire du serveur',
                        style={'textAlign':'left'}),
                dcc.Graph(figure=figure2),
                html.H4('Pourcentage du processeur utilisé',
                        style={'textAlign':'left'}),
                dcc.Graph(figure=figure3),
                html.H4('Nombre de connection active sur le serveur',
                        style={'textAlign':'left'}),
                dcc.Graph(figure=figure4),
                html.H4("Nombre d'erreur 404 sur le serveur",
                        style={'textAlign':'left'}),
                dcc.Graph(figure=figure5),
                html.H4('Ping moyen sur le serveur',
                        style={'textAlign':'left'}),
                dcc.Graph(figure=figure6)
                ]
    if pathname == "/Serveur_info":
        return [
                html.H1('Serveur info',
                        style={'textAlign':'center'}),
                dbc.Navbar([
                html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(dbc.NavbarBrand("Information Serveur", className="ml-1",)),
                            ],
                            align="center",
                            no_gutters=True,
                        ),
                        href="https://plot.ly",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler"),
                ],
                color="dark",
                dark=True,
                ),
                html.Div([
                    html.H5('Model : ' + STATIC_CPU_MODEL),
                    html.H5('Cache size : ' + STATIC_CACHE_SIZE),
                    html.H5('Cpu frequency : ' + STATIC_CPU_FREQ),
                    html.H5('Number of cores : ' + STATIC_NB_CORES),
                    html.H5('Memory Total : ' + STATIC_MEM_TOTAL),
                ]),
                ]
    if pathname == "/Parametres":
        return [
                html.H1('Parametres',
                        style={'textAlign':'center'}),
                html.Div([
                    dcc.Dropdown(
                        id='server-dropdown',
                        options=[
                            {'label': 'monitorme1.ddns.net', 'value': 'monitorme1.ddns.net'},
                            {'label': 'monitorme2.ddns.net', 'value': 'monitorme2.ddns.net'},
                            {'label': 'monitorme3.ddns.net', 'value': 'monitorme3.ddns.net'},
                            {'label': 'defense1.hopto.org', 'value': 'defense1.hopto.org'}
                        ],
                        value=SERVEUR_ACTUEL
                    ),
                    html.Div(id='dd-output-container')
                ]),
        ]
    if pathname == "/Logs":
        return [
                html.H1('Logs',
                        style={'textAlign':'center'}),
                 html.Div([
                    html.H5("Access Log : ", style={'textAlign':'left', 'padding':15}),
                    dcc.Textarea(
                        id='textarea-for-logs',
                        value=LOG_TOTAL,
                        style={'width': '100%', 'height': 900},
                        readOnly=True,
                    ),
                    html.H5("Response Time Log : ", style={'textAlign':'left', 'padding':15}),
                    dcc.Textarea(
                        id='textarea-for-Response-logs',
                        value=LOG_TOTAL_RESPONSE,
                        style={'width': '100%', 'height': 900},
                        readOnly=True,
                    ),
                 ]),
        ]

@app.callback(
    Output('dd-output-container', 'children'),
    [Input('server-dropdown', 'value')])
def update_output(value):
    """ update_output """
    global SERVEUR_ACTUEL
    if value != SERVEUR_ACTUEL:
        global CLIENT
        global DATA
        global STATIC_CPU_MODEL
        global STATIC_CACHE_SIZE
        global STATIC_CPU_FREQ
        global STATIC_NB_CORES
        global STATIC_MEM_TOTAL
        global FIGURE_MAP

        print("changement de serveur")
        SERVEUR_ACTUEL = value
        DATA = {
            'time': [],
            'number_process': [],
            'get_memory_free': [],
            'get_memory_used': [],
            'get_processor_used': [],
            'nb_connection': [],
            'nb_404': [],
            'ping_moyen': []
        }
        script.ChangeMachine(value)
        CLIENT.close()
        CLIENT =script.ssh_conn()
        STATIC_CPU_MODEL = str(script.get_cpu_model_name(CLIENT))
        STATIC_CACHE_SIZE = str(script.get_cache_size(CLIENT))
        STATIC_CPU_FREQ = str(script.get_cpu_frequency(CLIENT))
        STATIC_NB_CORES = str(script.get_number_of_cores(CLIENT))
        STATIC_MEM_TOTAL = str(script.get_memory_total(CLIENT))
        FIGURE_MAP = map_ip.localise(CLIENT)
    return 'Vous etes connecte a :"{}"'.format(value)

RUN_THREAD = True
threading.Thread(target=collect_data).start()

if __name__=='__main__':
    app.run_server(debug=True,host="0.0.0.0", port=8050,dev_tools_ui=False,dev_tools_props_check=False)
    RUN_THREAD=False
