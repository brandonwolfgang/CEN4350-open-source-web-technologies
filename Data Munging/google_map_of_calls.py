#!/usr/local/bin/python3

import numpy as np
import pandas as pd


class Map(object):

    def __init__(self):
        self._points = []

    def add_point(self, coordinates):
        self._points.append(coordinates)

    def __str__(self):
        center_lat = sum((x[0] for x in self._points)) / len(self._points)
        center_lon = sum((x[1] for x in self._points)) / len(self._points)
        markers_code = '\n'.join([
            """new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map,
                icon: '{icon}'
            }})
            """.format(lat=x[0], lon=x[1], icon=x[2]) for x in self._points
        ])

        return """<html>
        <head>
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
        </head>
        <body>
            <div id="map-canvas" style="height:100%;width:100%;"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 11,
                        center: new google.maps.LatLng({center_lat}, {center_lon})
                    }});
                    {markers_code}
                }}
                google.maps.event.addDomListener(window, 'load', show_map)
            </script>
        </body>
        </html>""".format(center_lat=center_lat, center_lon=center_lon, markers_code=markers_code)


# Create Pandas DataFrame and isolate relevant columns
df = pd.read_csv('fire_clean.csv')
df = df[['type', 'latitude', 'longitude']]

# Remove outliers
df = df[np.abs(df.latitude - df.latitude.mean()) <= (0.3 * df.latitude.std())]
df = df[np.abs(df.longitude - df.longitude.mean()) <= (2 * df.longitude.std())]


def get_icon(event_type):
    """
    This function returns an icon path based on event_type
    :param event_type: the event type used to specify an icon
    """
    if event_type == 'AUTOMATIC ALARM':
        return 'Google Maps Markers/blue_MarkerA.png'
    elif event_type == 'EMS':
        return 'Google Maps Markers/red_MarkerE.png'
    elif event_type == 'FIRE':
        return 'Google Maps Markers/orange_MarkerF.png'
    elif event_type == 'HAZMAT':
        return 'Google Maps Markers/purple_MarkerH.png'
    elif event_type == 'MUTUAL AID':
        return 'Google Maps Markers/green_MarkerM.png'
    elif event_type == 'PUBLIC SERVICE':
        return 'Google Maps Markers/pink_MarkerP.png'
    elif event_type == 'TRAFFIC':
        return 'Google Maps Markers/darkgreen_MarkerT.png'
    else:
        return 'Google Maps Markers/brown_MarkerU.png'

# Create Map object
event_map = Map()

# Loop through data, get icon, and add data to Map object
for i in df.index:
    icon = get_icon(df['type'][i])
    event_map.add_point((df['latitude'][i], df['longitude'][i], icon))

# Write map object to HTML file
with open('output.html', 'w') as outfile:
    print(event_map, file=outfile)
