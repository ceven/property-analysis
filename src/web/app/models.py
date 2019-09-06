import os
import re

import typing

import data
import firebasemiddleware
from . import forms

ALPHA_REGEX = re.compile('[^a-zA-Z0-9]')


def get_all_properties(user_id: str) -> ([data.PropertyData], data.PersonalFinanceData):
    return firebasemiddleware.get_all_properties_list(user_id)


def get_property_and_rent_by_name_json(home_name: str, user_id: str) -> \
        (typing.Optional[data.PropertyData], typing.Optional[data.PersonalFinanceData]):
    return firebasemiddleware.get_property_and_rent_by_name(home_name, user_id)


def get_property_by_name(home_name: str, user_id: str) -> typing.Dict:
    return firebasemiddleware.get_property(home_name, user_id)


def delete_property_by_name(home_name: str, user_id: str):
    return firebasemiddleware.delete_property(home_name, user_id)


def get_financial_data(user_id: str) -> typing.Dict:
    return firebasemiddleware.get_perso_financial_data(user_id)


def import_csv_properties(file_path: str, user_id: str) -> bool:
    success = firebasemiddleware.save_csv_data(file_path, None, user_id)
    if success:
        os.remove(file_path)
    return success


def import_property(form: forms.PropertyForm, user_id: str) -> bool:
    form_data = form.cleaned_data
    form_data['home_name'] = ALPHA_REGEX.sub('', form_data['home_name'])
    p_data = data.PropertyData(
        home_name=form_data['home_name'],
        property_price=form_data['property_price'],
        strata_q=form_data['strata_q'],
        water_q=form_data['water_q'],
        council_q=form_data['council_q']
    )
    return firebasemiddleware.add_property(p_data, user_id)


def import_comparable_property(home_name: str, property_sold_form: forms.PropertySoldForm):
    form_data = property_sold_form.cleaned_data
    p_data = data.PropertySoldData(
        sold_price=form_data['sold_price'],
        home_name=form_data['home_name'],
        property_price=form_data['property_price'],
        strata_q=form_data['strata_q'],
        water_q=form_data['water_q'],
        council_q=form_data['council_q']
    )
    return firebasemiddleware.add_comparable_property(home_name, p_data)


def get_comparable_properties(home_name: str):
    return None  # TODO


def create_dummy_financial_data(user_id: str):
    firebasemiddleware.save_perso_financial_data(perso_financial_data='./data/dummy_finances.csv', user_id=user_id)
