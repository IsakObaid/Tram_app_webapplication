import os

from django.conf import settings
from django.core.files.storage import default_storage

from .trams import readTramNetwork
from .graphs import dijkstra
from .color_tram_svg import color_svg_network


def show_shortest(dep, dest):
    network = readTramNetwork()

    distance, shortpath = dijkstra(network, dep, cost=network.specialized_geo_distance)
    
    min_distance = float('inf')
    shortest = None
    
    for vertex in shortpath:
        if vertex[0] == dest and distance[vertex] < min_distance:
            min_distance = distance[vertex]
            shortest = shortpath[vertex]
    
    if shortest is None:
        return "No path found", "No path found", None
    
    distance_traveled = min_distance

    time, quickpath = dijkstra(network, dep, cost=network.specialized_transition_time)

    min_time = float('inf')
    quickest = None
    for vertex in quickpath:
        if vertex[0] == dest and time[vertex] < min_time:
            min_time = time[vertex]
            quickest = quickpath[vertex]

    if quickest is None:
        return "No path found", "No path found", None
    
    travel_time = min_time
    
    def format_path_with_lines(path):
        if not path:
            return ""
        
        result = []
        current_line = None
        #print(path)
        for item in path:
            stop = item[0]
            line = item[1]
            
            if line != current_line:
                result.append(f"via line {line}")
                current_line = line
            
            result.append(stop)
        
        return ' '.join(result)
    
    timepath = f"Quickest: {dep} {format_path_with_lines(quickest)}. Time: {travel_time} min."
    geopath = f"Shortest: {dep} {format_path_with_lines(shortest)}. Distance: {distance_traveled:.3f} km."
    
    shortest_stops = [dep] + [item[0] for item in shortest]
    quickest_stops = [dep] + [item[0] for item in quickest]

    def colors(v):
        if v in shortest_stops and v in quickest_stops:
            return 'cyan'
        elif v in shortest_stops:
            return 'limegreen'
        elif v in quickest_stops:
            return 'orange'
        else:
            return 'white'

    dep_safe = default_storage.get_valid_name(dep)
    dest_safe = default_storage.get_valid_name(dest)
    outfile_unique_name = f"shortest_path_{dep_safe}_{dest_safe}.svg"

    infile = os.path.join(settings.BASE_DIR, 'tram/templates/tram/images/gbg_tramnet.svg')
    outfile = os.path.join(settings.BASE_DIR, f'tram/templates/tram/images/generated/{outfile_unique_name}')
    color_svg_network(infile, outfile, colormap=colors)
    
    with open(outfile, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    return timepath, geopath, svg_content