from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<home_name>/graph', views.render_svg_img, name='propertygraph'),
    path('<home_name>', views.get_property, name='property'),

]
