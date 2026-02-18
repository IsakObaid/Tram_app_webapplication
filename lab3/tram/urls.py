from django.urls import path
from . import views

urlpatterns = [
    path('', views.tram_net),
    path('route/', views.find_route),
]

if __name__ == "__main__":
    # generate URLs for tram app
    import trams as tn
    import re
    stops, lines, times, = tn.read_tram_data(tn.TRAM_FILE)

    # Read the HTML file
    with open('hållplatslista.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Dictionary to store results
    stops_in_goteborg = {}

    # Regex pattern to find the links with Göteborg
    pattern = r'<a href="/reseplanering/hallplatser/(\d+)">([^<]+), Göteborg[^<]*</a>'

    # Find all matches
    matches = re.findall(pattern, html_content)

    for match in matches:
        stop_id = match[0]
        stop_name = match[1].strip()
        stops_in_goteborg[stop_name] = stop_id

    # Print results
    print(f"Found {len(stops_in_goteborg)} stops in Göteborg:")
    print("-" * 50)

    for stop_name, stop_id in stops_in_goteborg.items():
        print(f"{stop_name}: {stop_id}")