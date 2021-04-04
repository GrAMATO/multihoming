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


def build_liste_positions(nb_points, dict_pos):
    """Prend en entrée la liste des points. Renvoie une liste de position adaptée à chaque point."""
    liste_positions = []
    for i in nb_points:
        value = verif_value(i - int(i))
        liste_positions.append(dict_pos[value])
    return liste_positions

def verif_value(value):
    """Prend en entrée la position du consommateur indifférent."""
    all_values = [i/16 for i in range(17)]
    if value >= 0 :
        for min_val, max_val in [[all_values[i], all_values[i+1]] for i in range(16)]:
            if value >= min_val and value < max_val:
                return min_val
            elif value == 1:
                return min_val
    else:
        for min_val, max_val in [[-all_values[i], -all_values[i-1]] for i in range(16)]:
            if value >= min_val and value < max_val:
                return max_val
            elif value == -1:
                return max_val
            
dict_pos = {0:"top center", 1/16:"top right", 2/16:"top right", 3/16:"middle right", 4/16:"middle right", 5/16:"bottom right", 6/16:"bottom right", 
            7/16:"bottom center", 8/16:"bottom center", 9/16:"bottom left", 10/16:"bottom left", 11/16:"middle left", 12/16:"middle left", 13/16:"top left",
            14/16:"top left", 15/16:"top center", 1:"top center", -1/16:"top left", -2/16:"top left", -3/16:"middle left", -4/16:"middle left", -5/16:"bottom left", 
            -6/16:"bottom left", -7/16:"bottom center", -8/16:"bottom center", -9/16:"bottom right", -10/16:"bottom right", -11/16:"middle right", -12/16:"middle right", -13/16:"top right",
            -14/16:"top right", -15/16:"top center", -1:"top center"}            



    
    
def calc_loc_list(prix = 0.9, theta = 0.5, m = 1):
    loc_list = []
    utilite_multihomer = th*(v-t*(xi - xji))-pi
    pos_conso = calcul_pos_conso(utilite_multihomer, pi_val = prix, t_val = 1, th_val = theta, n_val = 3, m_val = m, v_val = 2)
    loc_list = add_to_list(loc_list, pos_conso)
    return loc_list



def contraintes_conso_indif(nb, nb2, pos_entr, pos_entr2, pos_entr3):
    """Prend en entrée nb et nb2, les listes des positions des consommateurs indifférents, pos_entr la position de l'entreprise préférée """
    x12, x13 = nb
    x21, x31 = nb2

    x12, x21 = [contraintes_conso(x12, x21, pos_entr, pos_entr2), contraintes_conso_sym(x21, x12, pos_entr2, pos_entr)]
    x13, x31 = [contraintes_conso(x13, x31, pos_entr, pos_entr3), contraintes_conso_sym(x31, x13, pos_entr3, pos_entr)]
    return [x12, x13], [x21, x31]

def contraintes_conso(pos_conso1, pos_conso2, pos_entr, pos_entr2):
    """Vérifie si les contraintes sont respectées"""
    if pos_conso1 < pos_entr:
        return pos_entr
    elif pos_conso1 > pos_conso2 and pos_conso2>pos_entr2:
        return pos_entr2
    elif pos_conso1 > pos_conso2 and pos_conso2<pos_entr2:
        return pos_conso2
    else:     
        return pos_conso1
    
def contraintes_conso_sym(pos_conso1, pos_conso2, pos_entr, pos_entr2):
    """Vérifie si les contraintes sont respectées (symétrique)"""
    if pos_conso1 > pos_entr:
        return pos_entr
    elif pos_conso1 < pos_conso2 and pos_conso2<pos_entr2:
        return pos_entr2
    elif pos_conso1 < pos_conso2 and pos_conso2>pos_entr2:
        return pos_conso2
    else:     
        return pos_conso1




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
    return "Valeur du paramètre d'hétérogénéité des consommateurs (𝜃) : {}".format(value)

@app.callback(
    dash.dependencies.Output('singleh', 'children'),
    [dash.dependencies.Input('theta', 'value'),
    dash.dependencies.Input('prix', 'value')])
def update_output_singlehomers(theta, prix):
    pos_xji, pos_xjn = calc_loc_list(prix, theta)
    nb = calc_loc_list(prix, theta)
    return "Singlehomers : {}".format(conso_exclu(pos_xji, pos_xjn)) #nb

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
    nb = calc_loc_list(prix, theta, 1)
    nb2 = calc_loc_list(prix, theta, 0)
    all_points = [m/nb_points for m in range(0, nb_points)]
    nb2, nb = contraintes_conso_indif(nb, nb2, 0, 2/3, 1/3)
    fig = go.Figure()
    # Add circles
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-1, y0=-1, x1=1, y1=1,
        line_color="LightSeaGreen",
    )
    # Create scatter trace of text labels
    fig.add_trace(go.Scatter(
        x = PointsInCircum_y(1, nb_points),
        y = PointsInCircum_x(1, nb_points),
        text = ["F1", "F2", "F3"],
        mode = 'markers+text',
        textposition=build_liste_positions(all_points, dict_pos)

    ))
    fig.add_trace(go.Scatter(
        x= PointsInCircum_y2(1, nb),
        y= PointsInCircum_x2(1, nb),
        mode = 'markers+text',
        text = ["x12", "x13"],
        textposition = build_liste_positions(nb, dict_pos),
        marker_color = "red"
        
    ))
    fig.add_trace(go.Scatter(
        x= PointsInCircum_y2(1, nb2),
        y= PointsInCircum_x2(1, nb2),
        mode = 'markers+text',
        text = ["x21", "x31"],
        textposition = build_liste_positions(nb2, dict_pos),
        marker_color = "red"
        
    ))
    fig.update_traces(textfont_size=18)
    # Set axes properties
    fig.update_xaxes(range=[-1.25, 1.25], zeroline=False, showgrid = False, visible = False)
    fig.update_yaxes(range=[-1.25, 1.25], zeroline=False, showgrid = False, visible = False)

    fig.update_layout(showlegend=False, margin=go.layout.Margin(
        l=70, #left margin
        r=0, #right margin
        b=35, #bottom margin
        t=35, #top margin
    ), 
    
                     width= 700, height=700)
    # Set figure size
    return fig






# Main
if __name__ == '__main__':
    app.run_server()
