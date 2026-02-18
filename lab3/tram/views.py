from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .forms import RouteForm

from .utils.tramviz import show_shortest

def tram_net(request):
    return render(request, 'tram/home.html', {})

def find_route(request):
    form = RouteForm()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.data
            # Validate stop names
            from .utils.trams import readTramNetwork
            network = readTramNetwork()
            stops = set(network.all_stops())
            dep = route['dep']
            dest = route['dest']
            if dep not in stops:
                return HttpResponseBadRequest(f"Unknown stop name: {dep}")
            if dest not in stops:
                return HttpResponseBadRequest(f"Unknown stop name: {dest}")
            timepath, geopath, outfile = show_shortest(dep, dest)
            return render(
                request,
                'tram/show_route.html',
                {
                    'route': form.instance.__str__(),
                    'timepath': timepath,
                    'geopath': geopath,
                    'shortest_path_svg': outfile,
                }
            )
    else:
        form = RouteForm()
    return render(request, 'tram/find_route.html', {'form': form})
