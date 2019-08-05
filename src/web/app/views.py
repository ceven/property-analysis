import json

from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    p_data = models.get_property_data()
    context = p_data[0] # FIXME find a way to pass all properties to view
    print(context)
    return render(request, 'index.html', context=context)
