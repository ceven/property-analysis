from collections import namedtuple

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from firebase_admin import auth

import charts
from firebaseauthmiddleware import get_user, register_user, login_user
from . import forms
from . import models

Graph = namedtuple('Graph', 'home_name image_png_base64')


# TODO implement removing property and updating property
# TODO implement 'compare' function between property of interest and similar sales
# TODO implement ability to 'mark sold' property

# Create your views here.
def index(request):
    p_data, r_data = models.get_all_properties()
    graphs = [Graph(home_name=p.home_name, image_png_base64=charts.get_chart_graphic(p, r_data)) for p in p_data]
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
    pd, rd = models.get_property_and_rent_by_name_json(home_name)
    context = {'home': p, 'chart': charts.get_chart_graphic(pd, rd)}
    return render(request, 'property_page.html', context=context)


def delete_property(request, home_name):
    if request.method == 'POST':
        models.delete_property_by_name(home_name)
    return redirect('/')


def upload(request):
    context = {}
    if request.method == 'POST':
        if request.FILES and request.FILES['csvpropertiesfile']:
            file = request.FILES['csvpropertiesfile']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            models.import_csv_properties(fs.path(filename))
            context.update({'success': True})
        else:
            form = forms.PropertyForm(request.POST)
            if form.is_valid():
                success = models.import_property(form)
                if success:
                    return redirect('/property/details/' + form.cleaned_data['home_name'])
            context.update({'success': False})
    else:
        form = forms.PropertyForm()
        context.update({'form': form})
    return render(request, 'upload_properties.html', context=context)


def compare(request, home_name):
    context = {}
    if request.method == 'POST':
        property_sold_form = forms.PropertySoldForm(request.POST)
        if property_sold_form.is_valid():
            imported = models.import_comparable_property(home_name, property_sold_form)
            if imported:
                context.update({'sold_properties': [imported]})  # FIXME append to
    else:
        p = models.get_property_by_name(home_name)
        if p is not None:
            context.update({'home': p})
            comparable_properties = models.get_comparable_properties(home_name)
            if comparable_properties:
                context.update({'sold_properties': [comparable_properties]})
        form = forms.PropertySoldForm()
        context.update({'sold_property_form': form})
    return render(request, 'compare.html', context=context)


def register(request):
    context = {'msg': ''}
    if request.method == 'POST':
        user_form = forms.UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form = user_form.cleaned_data
            user = get_user(user_email=user_form['user_email'])
            if user is None:
                register_user(user_email=user_form['user_email'], user_password=user_form['user_password'])
                context.update({'msg': 'success'})
            else:
                context.update({'msg': 'fail'})
        else:
            context.update({'msg': 'fail'})
    if context['msg'] != 'success':
        form = forms.UserRegisterForm()
        context.update({'registration_form': form})
    return render(request, 'register.html', context=context)


def login(request):
    context = {'msg': ''}
    if request.method == 'POST':
        user_form = forms.LoginForm(request.POST)
        if user_form.is_valid():
            user_form = user_form.cleaned_data
            user = login_user(user_email=user_form['user_email'], user_password=user_form['user_password'])
            if user is None:
                context.update({'msg': 'fail'})
            else:
                context.update({'msg': 'success'})
        else:
            context.update({'msg': 'fail'})
    if context['msg'] != 'success':
        form = forms.LoginForm()
        context.update({'login_form': form})
    return render(request, 'login.html', context=context)
