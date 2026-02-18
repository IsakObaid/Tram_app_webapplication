import re
import json
import trams as tm
import os

# Define paths
TRAM_FILE = r'C:\Users\isako\Desktop\Advanced_python\lab3-group-135\lab3\tram\utils\static\tramnetwork.json'
OUTPUT_PATH = r'C:\Users\isako\Desktop\Advanced_python\lab3-group-135\lab3\tram\utils\static\tramstop_url.json'
HTML_PATH = r'C:\Users\isako\Desktop\Advanced_python\lab3-group-135\hållplatslista.html'
url_base = "https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid="

# Load tram network
network = tm.readTramNetwork(tramfile=TRAM_FILE)
stops = list(network._stopdict.keys())

# Read the HTML file
with open(HTML_PATH, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Dictionary to store results
stop_area_Gid = {}

# Regex pattern to find the links with stop IDs
# Captures stop names and IDs - matches stops in any municipality
pattern = r'<a href="/reseplanering/hallplatser/(\d+)">([^,<]+),[^<]*</a>'

# Find all matches
matches = re.findall(pattern, html_content)

# Create a set of stop names for faster lookup and case-insensitive comparison
stops_lower = {stop.lower(): stop for stop in stops}


for match in matches:
    stop_Gid = match[0]
    stop_name = match[1].strip()
    
    # Check if stop exists in our tram network (case-insensitive)
    if stop_name in stops:
        stop_area_Gid[stop_name] = url_base + stop_Gid
    elif stop_name.lower() in stops_lower:
        # If not exact match, try case-insensitive
        stop_area_Gid[stop_name.lower()] = url_base + stop_Gid
    else:
        pass


# Save to JSON file at the specified path
with open(OUTPUT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stop_area_Gid, json_file, ensure_ascii=False, indent=4)

