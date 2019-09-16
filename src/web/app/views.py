import typing
from collections import namedtuple

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

import charts
from firebaseauthmiddleware import get_user, register_user, login_user, check_authenticated
from . import forms
from . import models

Graph = namedtuple('Graph', 'home_name image_png_base64')


# TODO implement 'compare' function between property of interest and similar sales
# TODO implement ability to 'mark sold' property

@check_authenticated
def index(request):
    p_data, r_data = models.get_all_properties(get_uid(request.session))
    graphs = [Graph(home_name=p.home_name, image_png_base64=charts.get_chart_graphic(p, r_data)) for p in p_data]
    context = {'graphs': graphs, 'homes': p_data}
    return render(request, 'index.html', context=context)  # TODO try to render image as svg instead of png


@check_authenticated
def render_svg_img(request, home_name):
    p, r = models.get_property_and_rent_by_name_json(home_name, get_uid(request.session))
    if p is None:
        raise Http404  # FIXME need custom user friendly view
    graphic = charts.get_chart_graphic(p, r, 'svg')
    return HttpResponse(graphic, content_type='image/svg+xml')


@check_authenticated
def get_or_update_property(request, home_name):
    context = {}
    user_id = get_uid(request.session)
    pd, rd = models.get_property_and_rent_by_name_json(home_name, user_id)
    if pd is None:
        raise Http404
    pd_dict = pd.__dict__
    if request.method == 'POST':
        form = forms.PropertyForm(request.POST)
        success = False
        if form.is_valid():
            success = models.update_property(form, pd, user_id)
            new_home_name = form.cleaned_data['home_name']
            if home_name != new_home_name:
                return redirect('/property/details/' + new_home_name)  # FIXME show success message after redirect
            pd, rd = models.get_property_and_rent_by_name_json(home_name, user_id)
            pd_dict = pd.__dict__
        context.update({'success': success})
    form = forms.PropertyForm()
    form.update_form_fields_values(pd_dict)
    context.update({'form': form})
    context.update({'home': pd_dict, 'chart': charts.get_chart_graphic(pd, rd)})
    return render(request, 'property_page.html', context=context)


@check_authenticated
def delete_property(request, home_name):
    if request.method == 'POST':
        models.delete_property_by_name(home_name, get_uid(request.session))
    return redirect('/')


@check_authenticated
def upload(request):
    context = {}
    if request.method == 'POST':
        if request.FILES and request.FILES['csvpropertiesfile']:
            file = request.FILES['csvpropertiesfile']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            models.import_csv_properties(fs.path(filename), get_uid(request.session))
            context.update({'success': True})
        else:
            form = forms.PropertyForm(request.POST)
            if form.is_valid():
                success = models.import_property(form, get_uid(request.session))
                if success:
                    return redirect('/property/details/' + form.cleaned_data['home_name'])
            context.update({'success': False})
    else:
        form = forms.PropertyForm()
        context.update({'form': form})
    return render(request, 'upload_properties.html', context=context)


@check_authenticated
def compare(request, home_name):
    context = {}
    if request.method == 'POST':
        property_sold_form = forms.PropertySoldForm(request.POST)
        if property_sold_form.is_valid():
            imported = models.import_comparable_property(home_name, property_sold_form)
            if imported:
                context.update({'sold_properties': [imported]})  # FIXME append to
    else:
        p = models.get_property_by_name(home_name, get_uid(request.session))
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
                user_record = register_user(user_email=user_form['user_email'], user_password=user_form[
                    'user_password'])
                models.create_dummy_financial_data(user_record.uid)  # Create dummy financial data to start with
                # TODO potentially save session so no need to login afterwards
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
    # TODO ask to logout if already logged in
    context = {'msg': ''}
    if request.method == 'POST':
        user_form = forms.LoginForm(request.POST)
        if user_form.is_valid():
            user_form = user_form.cleaned_data
            json_resp = login_user(user_email=user_form['user_email'], user_password=user_form['user_password'])
            if json_resp is None:
                context.update({'msg': 'fail'})
            else:
                local_id = json_resp['localId']
                token = json_resp['idToken']
                refresh_token = json_resp['refreshToken']
                request.session['token'] = token
                request.session['refresh_token'] = refresh_token
                request.session['local_id'] = local_id
                context.update({'msg': 'success'})
        else:
            context.update({'msg': 'fail'})
    if context['msg'] != 'success':
        form = forms.LoginForm()
        context.update({'login_form': form})
    return render(request, 'login.html', context=context)


def get_uid(session: typing.Dict) -> str:
    return session['local_id']


@check_authenticated
def me_finances(request):
    user_id = get_uid(request.session)
    finance_data = models.get_financial_data(user_id)
    context = {'msg': '', 'finances': finance_data}
    if request.method == 'POST':
        finances_form = forms.FinancesForm(request.POST)
        if finances_form.is_valid():
            if models.import_financial_data(finances_form, finance_data, user_id):
                finance_data = models.get_financial_data(user_id)
                context.update({'msg': 'success', 'finances': finance_data})
            else:
                context.update({'msg': 'fail'})
        else:
            context.update({'msg': 'fail'})
    if context['msg'] != 'success':
        form = forms.FinancesForm()
        form.update_form_fields_values(finance_data)
        context.update({'form': form})
    return render(request, 'finances.html', context=context)
