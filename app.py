import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import sympy as sp
import plotly.graph_objects as go
import math

########### Define your variables
n, th, v, t, xi, xji, pi, pj, pk = sp.symbols("n theta v t x_i x_{ji} p_i p_j p_k")
def position_indif(utilite_multihomer, m):
    equation = sp.Eq(utilite_multihomer, 0)
    pos_xji, = sp.solve(equation, xji)
    return pos_xji.subs(xi, m/n)

def PointsInCircum_x(r, n):
    return [math.cos(2*math.pi/n*x)*r for x in range(0,n+1)] 

def PointsInCircum_y(r, n):
    return [math.sin(2*math.pi/n*x)*r for x in range(0,n+1)] 

def PointsInCircum_x2(r, list_pos):
    return [math.cos(pos*360*math.pi/180)*r for pos in list_pos]

def PointsInCircum_y2(r, list_pos):
    return [math.sin(pos*360*math.pi/180)*r for pos in list_pos]


def position_indif_sym(pos_xji):
    return 1-pos_xji

def conso_exclu(pos_xji, pos_xjn):
    x_exclu_i = pos_xji + (1 - pos_xjn)
    return x_exclu_i.subs(2*pi, pj + pk)

def pos_conso(utilite_multihomer, nb):
    pos_xji = position_indif(utilite_multihomer, nb)
    return [pos_xji, position_indif_sym(pos_xji)]

def calcul_pos_conso(utilite_multihomer, pi_val, t_val, th_val, n_val, m_val, v_val):
    pos_xji, pos_xjn = pos_conso(utilite_multihomer, m_val)
    pos_xji_value = pos_xji.subs([(pi, pi_val), (t, t_val), (th, th_val), (n, n_val), (v, v_val)])
    pos_xjn_value = pos_xjn.subs([(pi, pi_val), (t, t_val), (th, th_val), (n, n_val), (v, v_val)])
    return [pos_xji_value, pos_xjn_value]

def calc_dmd(pi_val, t_val, th_val, v_val):
    demande = 2/t *((th*v-pi)/th)
    return demande.subs([(pi, pi_val), (t, t_val), (th, th_val), (v, v_val)])

def add_to_list(loc_list, pos_conso):
    for i in pos_conso:
        loc_list.append(i) 
    return loc_list

def build_circle(nb_points, nb):

    fig = go.Figure()

    # Create scatter trace of text labels
    fig.add_trace(go.Scatter(
        x= PointsInCircum_y(1, nb_points),
        y= PointsInCircum_x(1, nb_points),
        text = [r"$F_1$", r"$F_2$", r"$F_3$"],
        mode = 'markers+text',

    ))

    fig.add_trace(go.Scatter(
        x= PointsInCircum_y2(1, nb),
        y= PointsInCircum_x2(1, nb),
        mode = 'markers+text',
        text = [r"$x_{12}$"+r'<br>'+"-", r"$x_{13}$"],
        marker_color = "red"
        
    ))
    print(nb)
    fig.update_traces(textposition="top left", textfont_size=18)

    # Set axes properties
    fig.update_xaxes(range=[-1.5, 1.5], zeroline=False, showgrid = False, visible = False)
    fig.update_yaxes(range=[-1.5, 1.5], zeroline=False, showgrid = False, visible = False)

    # Add circles
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-1, y0=-1, x1=1, y1=1,
        line_color="LightSeaGreen",
    )

    # Set figure size
    fig.update_layout(width=800, height=800)
    return fig


    
    
def calc_loc_list(prix = 0.9, theta = 0.5):
    loc_list = []
    utilite_multihomer = th*(v-t*(xi - xji))-pi
    pos_conso = calcul_pos_conso(utilite_multihomer, pi_val = prix, t_val = 1, th_val = theta, n_val = 3, m_val = 1, v_val = 2)
    loc_list = add_to_list(loc_list, pos_conso)
    return loc_list


########### Initiate the app
app = dash.Dash(__name__)

server = app.server


layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h")
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Sélection des paramètres pour l'entreprise 1 :", className="control_label"),
                        html.P(id = "value_theta", className="control_label"),
                        dcc.Slider(
                        id='theta',
                        min=0,
                        max=1,
                        step=0.01,
                        value=0.5
                            ),
                        
                        html.P(id = "value_prix", className="control_label"),
                        dcc.Slider(
                        id='prix',
                        min=0.1,
                        max=2,
                        step=0.01,
                        value=0.9
                            ),
                    ],
                    className="pretty_container five columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="oilText"), html.P("")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="well_text")],
                                    id="multih",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText")],
                                    id="singleh",
                                    className="mini_container",
                                ),

                                html.Div(
                                    [html.H6(id="waterText"), html.P("")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="salop_circle")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"}
        )

@app.callback(
    dash.dependencies.Output('value_prix', 'children'),
    [dash.dependencies.Input('prix', 'value')])
def update_output_prix(value):
    return "Prix de tous les biens : {}".format(value)

@app.callback(
    dash.dependencies.Output('value_theta', 'children'),
    [dash.dependencies.Input('theta', 'value')])
def update_output_theta(value):
    return "Valeur de theta : {}".format(value)

@app.callback(
    dash.dependencies.Output('singleh', 'children'),
    [dash.dependencies.Input('theta', 'value'),
    dash.dependencies.Input('prix', 'value')])
def update_output_singlehomers(theta, prix):
    pos_xji, pos_xjn = calc_loc_list(prix, theta)
    return "Singlehomers : {}".format(conso_exclu(pos_xji, pos_xjn))

@app.callback(
    dash.dependencies.Output('multih', 'children'),
    [dash.dependencies.Input('theta', 'value'),
    dash.dependencies.Input('prix', 'value')])
def update_output_multihomers(theta, prix):
    pos_xji, pos_xjn = calc_loc_list(prix, theta)
    singleh = conso_exclu(pos_xji, pos_xjn)
    demande_val = calc_dmd(prix, 1, theta, 2)
    return "Multihomers : {}".format(demande_val - singleh)



@app.callback(
    dash.dependencies.Output('salop_circle', 'figure'),
    [dash.dependencies.Input('theta', 'value'),
    dash.dependencies.Input('prix', 'value')])

def build_circle(prix, theta):
    nb_points = 3
    nb = calc_loc_list(prix, theta)
    fig = go.Figure()
    # Add circles
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-1, y0=-1, x1=1, y1=1,
        line_color="LightSeaGreen",
    )
    # Create scatter trace of text labels
    fig.add_trace(go.Scatter(
        x= PointsInCircum_y(1, nb_points),
        y= PointsInCircum_x(1, nb_points),
        text = ["F1", "F2", "F3"],
        mode = 'markers+text',

    ))

    fig.add_trace(go.Scatter(
        x= PointsInCircum_y2(1, nb),
        y= PointsInCircum_x2(1, nb),
        mode = 'markers+text',
        text = ["x12", "x13"],
        marker_color = "red"
        
    ))

    fig.update_traces(textposition="top left", textfont_size=18)

    # Set axes properties
    fig.update_xaxes(range=[-1.25, 1.25], zeroline=False, showgrid = False, visible = False)
    fig.update_yaxes(range=[-1.25, 1.25], zeroline=False, showgrid = False, visible = False)

    fig.update_layout(showlegend=False, margin=go.layout.Margin(
        l=70, #left margin
        r=0, #right margin
        b=35, #bottom margin
        t=35, #top margin
    ), 
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                     width= 700, height=700)
    # Set figure size
    return fig





# Main
if __name__ == '__main__':
    app.run_server()
