from collections import namedtuple

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from . import charts
from . import models

Graph = namedtuple('Graph', 'home_name image_png_base64')


# Create your views here.
def index(request):
    p_data, r_data = models.get_property_data()
    graphs = [Graph(home_name=p.home_name, image_png_base64=charts.get_chart_graphic(p, r))
              for (p, r) in zip(p_data, r_data)]
    context = {'graphs': graphs, 'homes': p_data}
    return render(request, 'index.html', context=context)  # TODO try to render image as svg instead of png


def render_svg_img(request, home_name):
    p, r = models.get_property_by_name(home_name)
    if p is None:
        raise Http404  # FIXME need custom user friendly view
    graphic = charts.get_chart_graphic(p, r, 'svg')
    return HttpResponse(graphic, content_type='image/svg+xml')


def get_property(request, home_name):
    return redirect('propertygraph', home_name)  # FIXME build custom page
