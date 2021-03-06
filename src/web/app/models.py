import os
import re
import typing

import data
import firebasemiddleware
from data import PersonalFinanceData, PropertyData
from . import forms

REPLACE_REGEX = re.compile('[/]')
TRIM_REGEX = re.compile('[^a-zA-Z0-9\\-_,~ ]')


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
    form_data['home_name'] = clean_name(form_data['home_name'])
    p_data = data.PropertyData(
        home_name=form_data['home_name'],
        property_price=form_data['property_price'],
        strata_q=form_data['strata_q'],
        water_q=form_data['water_q'],
        council_q=form_data['council_q'],
        domain_link=form_data.get('domain_link', '')
    )
    return firebasemiddleware.add_property(p_data, user_id)


def clean_name(name: str):
    home_name = REPLACE_REGEX.sub(' ', name)
    home_name = TRIM_REGEX.sub('', home_name)
    return home_name


def update_property(form: forms.PropertyForm, original_data: typing.Optional[PropertyData], user_id: str) -> bool:
    form_data = form.cleaned_data
    form_data['home_name'] = clean_name(form_data['home_name'])
    p_data = merge_property_data(form_data, original_data)
    success = firebasemiddleware.add_property(p_data, user_id) if p_data is not None else False
    if success and original_data is not None and p_data.home_name != original_data.home_name:
        firebasemiddleware.delete_property(original_data.home_name, user_id)
    return success


def merge_property_data(new_data: typing.Dict, original_data: typing.Optional[PropertyData]) -> \
        typing.Optional[PropertyData]:
    if not new_data and not original_data:
        return None
    return PropertyData(home_name=new_data.get('home_name', original_data.home_name),
                        property_price=new_data.get('property_price', original_data.property_price),
                        strata_q=new_data.get('strata_q', original_data.strata_q),
                        council_q=new_data.get('council_q', original_data.council_q),
                        water_q=new_data.get('water_q', original_data.water_q),
                        domain_link=new_data.get('domain_link', original_data.domain_link))


def merge_perso_financial_data(new_data: typing.Dict, original_data: typing.Optional[PersonalFinanceData]) -> \
        typing.Optional[PersonalFinanceData]:
    if not new_data and not original_data:
        return None
    return PersonalFinanceData(rent_week=new_data.get('rent_week', original_data.rent_week),
                               salary_net_year=new_data.get('salaries_net_per_year',
                                                            original_data.salaries_net_per_year),
                               initial_savings=new_data.get('initial_savings', original_data.initial_savings),
                               monthly_living_expenses=new_data.get('living_expenses',
                                                                    original_data.living_expenses) / 12,
                               loan_interest_rate=new_data.get('loan_interest_rate', original_data.loan_interest_rate),
                               savings_interest_rate=new_data.get('savings_rate_brut', original_data.savings_rate_brut))


def import_financial_data(form: forms.FinancesForm, original_data: typing.Dict, user_id: str) -> bool:
    form_data = form.cleaned_data
    f_data = merge_perso_financial_data(form_data, firebasemiddleware.convert_to_perso_financial_data(original_data))
    if f_data is not None:
        firebasemiddleware.add_perso_financial_data(f_data, user_id)
        return True
    return False


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
