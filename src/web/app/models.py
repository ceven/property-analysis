import os
import re
import urllib.parse

import data
import firebasemiddleware
# Create your models here.
from . import forms

ALPHA_REGEX = re.compile('[^a-zA-Z0-9]')


def get_all_properties_json() -> ([], []):
    return firebasemiddleware.get_all_properties_json()


def get_property_and_rent_by_name_json(home_name: str) -> (object, object):
    return firebasemiddleware.get_property_and_rent_by_name_json(home_name)


def get_property_by_name(home_name: str) -> object:
    return firebasemiddleware.get_property_by_name_json(home_name)


def import_csv_properties(file_path: str):
    d = data.load_data(file_path)
    os.remove(file_path)
    return d


def import_property(form: forms.PropertyForm) -> bool:
    form_data = form.cleaned_data
    form_data['home_name'] = ALPHA_REGEX.sub('', form_data['home_name'])
    p_data = data.PropertyData(
        home_name=form_data['home_name'],
        property_price=form_data['property_price'],
        strata_q=form_data['strata_q'],
        water_q=form_data['water_q'],
        council_q=form_data['council_q']
    )
    # TODO decouple financials not tied in to property
    return firebasemiddleware.add_property(p_data)
