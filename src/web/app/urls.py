from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<home_name>/graph', views.render_svg_img, name='propertygraph'),
    path('details/<home_name>', views.get_or_update_property, name='property'),
    url(r'details/(?P<home_name>.*)/delete', views.delete_property, name='delete_property'),
    path('upload', views.upload, name='upload'),
    path('compare/<home_name>', views.compare, name='compare'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('me/finances', views.me_finances, name='me_finances')
]
