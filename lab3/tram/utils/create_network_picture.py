"""
Baseline tram visualization for Lab 3

Creates an SVG image usable on the home page.
This image is then coloured by tramviz.py depending on the route.
You only need to run this file once, to change the URLs of the vertices.
"""

from trams import readTramNetwork
import graphviz
import json

MY_GBG_SVG = 'my_gbg_tramnet.svg'  # the output SVG file
MY_TRAMNETWORK_JSON = r'C:\Users\isako\Desktop\Python\lab3-group-135\lab3\tram\utils\static\tramnetwork.json'  # JSON file from lab1
TRAM_URL_FILE = r'C:\Users\isako\Desktop\Python\lab3-group-135\lab3\tram\utils\static\tramstop_url.json'  # given in lab3/files, replace with your own stop URL file

# assign colors to lines, indexed by line number; not quite accurate
gbg_linecolors = {
    1: 'gray',
    2: 'yellow',
    3: 'blue',
    4: 'green',
    5: 'red',
    6: 'orange',
    7: 'brown',
    8: 'purple',
    9: 'cyan',
    10: 'lightgreen',
    11: 'black',
    13: 'pink'
}


# Return a function which scales positions, based on scale of entire network.
# You may want to test different heuristics to make map look better
def position_scaler(network):
    minlat, minlon, maxlat, maxlon = network.extreme_positions()
    minlat = float(minlat)
    minlon = float(minlon)
    maxlat = float(maxlat)
    maxlon = float(maxlon)
    size_x = maxlon - minlon
    size_y = maxlat - minlat
    scalefactor = len(network)/4  # heuristic
    x_factor = scalefactor/size_x
    y_factor = scalefactor/size_y
    return lambda x,y: (x_factor*(float(x)-minlon), y_factor*(float(y)-minlat))


# You don't probably need to change this, if your TramNetwork class uses the same
# method names and types and represents positions as ordered pairs.
# If not, you will need to change the method call to correspond to your class.
def network_graphviz(network, outfile=MY_GBG_SVG):
    with open(TRAM_URL_FILE) as file:
        stop_urls = json.loads(file.read())

    dot = graphviz.Graph(
        engine='fdp', 
        graph_attr={
            'size': '12,12' # max image size (in inches!)
        }
    )
    scaler = position_scaler(network)

    for stop in network.all_stops():
        pos_dict = network.stop_position(stop)
        lat = float(pos_dict['lat'])
        lon = float(pos_dict['lon'])
        pos_x, pos_y = scaler(lon, lat)
        dot.node(
            stop,
            label=stop,
            shape='rectangle',
            pos=f'{pos_x},{pos_y}!',
            fontsize='8pt',
            width='0.4',
            height='0.05',
            URL=stop_urls.get(stop, '.'),
            fillcolor='white',
            style='filled'
        )
        
    for line in network.all_lines():
        stops = network.line_stops(line)
        for i in range(len(stops)-1):
            dot.edge(
                stops[i],
                stops[i+1],
                color=gbg_linecolors[int(line)],
                penwidth=str(2)
            )

    # Save as DOT file first (no graphviz executables needed)
    dot_file = outfile.replace('.svg', '.dot')
    dot.save(dot_file)
    print(f"Saved graph to {dot_file}")
    
    # Try to render to SVG if graphviz is available, otherwise just save DOT
    try:
        dot.format = 'svg'
        s = dot.pipe().decode('utf-8')
        with open(outfile, 'w', encoding='utf-8') as file:
            file.write(s)
        print(f"Saved SVG to {outfile}")
    except Exception as e:
        print(f"Note: Graphviz executables not found. Saved DOT file instead.")
        print(f"To generate SVG, install Graphviz from https://graphviz.org/download/")
        print(f"Then run: dot -Tsvg {dot_file} -o {outfile}")


if __name__ == '__main__':
    network = readTramNetwork(tramfile=MY_TRAMNETWORK_JSON)
    network_graphviz(network)

"""
# This is how the url json file was created
import urllib.parse
dict = {}
url = 'https://www.vasttrafik.se/sok/'
for stop in network.all_stops():
    attrs = urllib.parse.urlencode({'q': stop})
    dict[stop] = url + '?' + attrs
with open(TRAM_URL_FILE, 'w') as file:
    json.dump(dict, file, indent=2, ensure_ascii=False)
"""

