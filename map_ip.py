""" map_ip """
import plotly.graph_objects as go
from ipdata import ipdata as IPD
import log_parser

def get_coord_from_ip(client):
    """ get_coord_from_ip """
    latitude = []
    longitude = []
    nompoints = []
    log_total,_=log_parser.recup_log(client)
    _, tab_ip = log_parser.number_of_diff_ip(log_total)
    ipdata = IPD.IPData('12e19ee015c10bbb393c33cebbc11655bab60336034ee6217d0538c3')
    for i in range(10):
        response = ipdata.lookup(tab_ip[i], fields=['ip','latitude','longitude'])
        latitude.append(response.get('latitude'))
        longitude.append(response.get('longitude'))
        nompoints.append(response.get('ip'))
    return latitude, longitude, nompoints

def localise(client):
    """ localise """
    latitude, longitude, nompoints=get_coord_from_ip(client)
    fig = go.Figure(go.Scattermapbox(
            lat=latitude,
            lon=longitude,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=nompoints,
        ))

    fig.update_layout(
        autosize=False,
        height=1000,
        width=1800,
        hovermode='closest',
        mapbox=dict(
            accesstoken="pk.eyJ1IjoibGUtY2FpZ25lYy1yb2JpbiIsImEiOiJja2s1bG9neG4xdnlqMnVwY3c1Z2s0bDhtIn0.kIzVnWaRgUr31B-xzy5aGQ",
            bearing=0,
            center=dict(
                lat=18,
                lon=-15
            ),
            pitch=0,
            zoom=1.8
        ),
    )

    return fig
