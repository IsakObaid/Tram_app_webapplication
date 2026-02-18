import json
import sys

from django.conf import settings

from .graphs import WeightedGraph

sys.path.append(r'C:\Users\isako\Desktop\Advanced_python\lab1-group-135')
import tramdata as td

TRAM_FILE = r'C:\Users\isako\Desktop\Advanced_python\lab3-group-135\lab3\tram\utils\static\tramnetwork.json'


class TramNetwork(WeightedGraph):
    def __init__(self, *args, **kwargs):
        if len(args) >= 3:
            lines, stops, times = args[0], args[1], args[2]
        else:
            lines = kwargs.get('lines', {})
            stops = kwargs.get('stops', {})
            times = kwargs.get('times', {})
        
        super().__init__()
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times

        for stop in self._stopdict.keys():
            self.add_vertex(stop)

        for tram_line, stops in self._linedict.items():
            for j in range(len(stops) - 1):
                stop1 = stops[j]
                stop2 = stops[j + 1]
                self.add_edge(stop1, stop2)
        
        self.specialize_stops_to_lines()

    def stop_position(self, a):
        return self._stopdict[a]
    
    def get_transition_time(self, line, a, b):
        return td.time_between_stops(self._linedict, self._timedict, line, a, b)
    
    def get_distance(self, a, b):
        return td.distance_between_stops(self._stopdict, a, b)
    
    def get_lines_through_stop(self, a):
        return td.lines_via_stop(self._linedict, a)
    
    def all_stops(self):
        return self._stopdict.keys()
    
    def all_lines(self):
        return self._linedict.keys()
    
    def line_stops(self, line):
        return self._linedict.get(line, [])
    
    def extreme_positions(self):
        latitudes = [location['lat'] for location in self._stopdict.values()]
        longitudes = [location['lon'] for location in self._stopdict.values()]
        return min(latitudes), min(longitudes), max(latitudes), max(longitudes)

#--------------------------  new functions -----------------------------------

    def lines_between_stops(self, stop1, stop2):
        lines_btw_stops = []
        for key in self._linedict.keys():
            if stop1 in self._linedict[key] and stop2 in self._linedict[key]:
                lines_btw_stops.append(key)
        return sorted(lines_btw_stops, key=lambda x: int(x))

    def travel_time(self, a, b):
        common_lines = self.lines_between_stops(a, b)
        if not common_lines:
            return 0
        
        common_line = common_lines[0]
        
        stops_on_line = self.line_stops(common_line)
        start_index = stops_on_line.index(a)
        end_index = stops_on_line.index(b)
        
        if start_index == end_index:
            return 0
        elif start_index < end_index:
            stops_between = stops_on_line[start_index:end_index + 1]
        else:
            stops_between = stops_on_line[end_index:start_index + 1]
        
        time = 0
        for i in range(len(stops_between) - 1):
            stop_curr = stops_between[i]
            stop_next = stops_between[i + 1]
            time += self.get_transition_time(common_line, stop_curr, stop_next)
            
        return time
    
    def specialized_transition_time(self, a, b, changetime=10):
        time = self.travel_time(a, b)
        return changetime if time == 0 else time

    def specialized_geo_distance(self, a, b, changedistance=0.02):
        if a == b:
            return changedistance
        return self.get_distance(a, b)
    
    def specialize_stops_to_lines(self):
        for stop_name in self._stopdict.keys():
            for line in self._linedict.keys():
                if stop_name in self.line_stops(line):
                    self.add_vertex_pairs(stop_name, line)
                    stops = self._linedict[line]
                    for i in range(len(stops) - 1):
                        stop1 = stops[i]
                        stop2 = stops[i + 1]
                        vertex1 = (stop1, line)
                        vertex2 = (stop2, line)
                        self.add_edge_pairs(vertex1, vertex2)
        
        for tram_line, stops in self._linedict.items():
            for i in range(len(stops) - 1):
                stop1 = (stops[i], tram_line)
                stop2 = (stops[i + 1], tram_line)
                WeightedGraph.add_edge_pairs(self, stop1, stop2)
                if i == 0:
                    self.add_edge_pairs(stop1, stop1)

        for vertex_pair in self.vertices_pairs():
            for vertex in self.vertices():
                if vertex_pair[0] == vertex:
                    neighbors = self.neighbors(vertex)
                    for neighbor in neighbors:
                        for line in self._linedict.keys():
                            if vertex in self.line_stops(line) and neighbor in self.line_stops(line) and vertex_pair[1] == line:
                                neighbor_tuple = (neighbor, vertex_pair[1])
                                self.connect_edges(vertex_pair, neighbor_tuple)

        for stop_name in self._stopdict.keys():
            lines_at_stop = [
                line for line in self._linedict.keys()
                if stop_name in self.line_stops(line)
            ]
            for i in range(len(lines_at_stop)):
                for j in range(i + 1, len(lines_at_stop)):
                    line1 = lines_at_stop[i]
                    line2 = lines_at_stop[j]
                    vertex1 = (stop_name, line1)
                    vertex2 = (stop_name, line2)
                    self.add_edge_pairs(vertex1, vertex2)


def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    stops = data.get('stops', {})
    lines = data.get('lines', {})
    times = data.get('times', {})
    
    return TramNetwork(lines=lines, stops=stops, times=times)
