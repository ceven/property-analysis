from django.http import HttpResponse
from django.shortcuts import render

from . import charts
from . import models


# Create your views here.
def index(request):
    p_data, r_data = models.get_property_data()
    graphs = [charts.get_chart_graphic(p, r) for (p, r) in zip(p_data, r_data)]
    context = {'graphs': graphs, 'homes': p_data}
    return render(request, 'index.html', context=context)  # TODO try to render image as svg instead of png


def render_svg_img(request):
    p_data, r_data = models.get_property_data()
    graphic = charts.get_chart_graphic(p_data[0], r_data[0], 'svg')
    return HttpResponse(graphic, content_type='image/svg+xml')
