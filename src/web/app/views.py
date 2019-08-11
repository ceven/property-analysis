import os
from collections import namedtuple

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render

import charts
from . import models

Graph = namedtuple('Graph', 'home_name image_png_base64')


# Create your views here.
def index(request):
    p_data, r_data = models.get_all_properties_json()
    graphs = [Graph(home_name=p.home_name, image_png_base64=charts.get_chart_graphic(p, r))
              for (p, r) in zip(p_data, r_data)]
    context = {'graphs': graphs, 'homes': p_data}
    return render(request, 'index.html', context=context)  # TODO try to render image as svg instead of png


def render_svg_img(request, home_name):
    p, r = models.get_property_and_rent_by_name_json(home_name)
    if p is None:
        raise Http404  # FIXME need custom user friendly view
    graphic = charts.get_chart_graphic(p, r, 'svg')
    return HttpResponse(graphic, content_type='image/svg+xml')


def get_property(request, home_name):
    p = models.get_property_by_name(home_name)
    if p is None:
        raise Http404
    context = {'home': p}
    return render(request, 'property_page.html', context=context)


def upload(request):
    context = {}
    if request.method == 'POST' and request.FILES['csvpropertiesfile']:
        f = request.FILES['csvpropertiesfile']
        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        models.import_csv_properties(fs.path(filename))
        context.update({'success': True})
    return render(request, 'upload_properties.html', context=context)
