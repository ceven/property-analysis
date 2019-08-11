from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<home_name>/graph', views.render_svg_img, name='propertygraph'),
    path('details/<home_name>', views.get_property, name='property'),
    path('upload', views.upload, name='upload'),
]
