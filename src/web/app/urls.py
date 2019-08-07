from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('svg', views.render_svg_img, name='zoomin')
]