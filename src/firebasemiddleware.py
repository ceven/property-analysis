import json
import typing

from firebase_admin.db import Reference
from numpy import int64

from data import load_data, PropertyData, PersonalFinanceData, PropertySoldData
from firebasedb import users_financial, users_property, DEFAULT_USER_ID


def get_user_property_path(user_id: str = DEFAULT_USER_ID) -> Reference:
    return users_property.child(user_id).child("property")


def get_user_financial_path(user_id: str = DEFAULT_USER_ID) -> Reference:
    return users_financial.child(user_id).child("financial")


def add_property(prop: PropertyData, user_id: str = DEFAULT_USER_ID) -> bool:
    try:
        prop_str = json.dumps(prop.__dict__, default=json_data_converter)
        json_prop = json.loads(prop_str)
        get_user_property_path(user_id).child(prop.home_name).set(json_prop)
        return True
    except Exception as e:
        print("Could not save property", e)
        return False


def update_property(home_name: str, data: typing.Dict, user_id: str) -> bool:
    try:
        prop_str = json.dumps(data, default=json_data_converter)
        json_prop = json.loads(prop_str)
        get_user_property_path(user_id).child(home_name).update(json_prop)
        return True
    except Exception as e:
        print("Could not save property", e)
        return False


def get_property(prop_name: str, user_id: str = DEFAULT_USER_ID) -> typing.Dict:
    return get_user_property_path(user_id).child(prop_name).get()


def delete_property(prop_name: str, user_id: str = DEFAULT_USER_ID) -> None:
    get_user_property_path(user_id).child(prop_name).delete()


def get_all_properties(user_id: str = DEFAULT_USER_ID) -> typing.Dict:
    return get_user_property_path(user_id).get()


def add_perso_financial_data(f: PersonalFinanceData, user_id: str = DEFAULT_USER_ID) -> None:
    perso_data = json.dumps(f.__dict__, default=json_data_converter)
    perso_data_json = json.loads(perso_data)
    get_user_financial_path(user_id).set(perso_data_json)


def get_perso_financial_data(user_id: str) -> typing.Dict:
    return get_user_financial_path(user_id).get()


def get_user_data(user_id: str = DEFAULT_USER_ID) -> (typing.Dict, typing.Dict):
    return get_all_properties(user_id), get_perso_financial_data(user_id)


def convert_to_property_data(d: typing.Dict) -> typing.Optional[PropertyData]:
    if not d:
        return None
    # FIXME loan_interest_rate to pass in
    return PropertyData(property_price=d['property_price'],
                        strata_q=d['strata_q'],
                        council_q=d['council_q'],
                        water_q=d['water_q'],
                        home_name=d['home_name'],
                        domain_link=d.get('domain_link', ''))


def convert_to_perso_financial_data(d: typing.Dict) -> typing.Optional[PersonalFinanceData]:
    if not d:
        return None
    return PersonalFinanceData(rent_week=d.get('rent_week'),
                               salary_net_year=d.get('salaries_net_per_year'),
                               initial_savings=d.get('initial_savings'),
                               monthly_living_expenses=d.get('living_expenses') / 12,
                               savings_interest_rate=d.get('savings_rate_brut'),
                               loan_interest_rate=d.get('loan_interest_rate'))


def get_all_properties_list(user_id: str) -> ([PropertyData], typing.Optional[PersonalFinanceData]):
    all_props, perso_json = get_user_data(user_id)
    property_data = [convert_to_property_data(v) for v in all_props.values()] if all_props else []
    perso_data = convert_to_perso_financial_data(perso_json) if perso_json else None
    return property_data, perso_data


def get_property_and_rent_by_name(home_name: str, user_id: str) -> \
        (typing.Optional[PropertyData], typing.Optional[PersonalFinanceData]):
    p = get_property(home_name, user_id)
    r = None if p is None else get_perso_financial_data(user_id)
    return convert_to_property_data(p), convert_to_perso_financial_data(r)


def json_data_converter(o):
    if isinstance(o, int64):
        return int(o)
    if isinstance(o, float):
        return float(o)


def save_csv_data(property_file_name: str, perso_financial_data: str, user_id: str) -> bool:
    try:
        p_data, r_data = load_data(property_file_name, perso_financial_data)

        if p_data:
            for p in p_data:
                add_property(p, user_id)
        if r_data:
            add_perso_financial_data(r_data, user_id)
        return True
    except Exception as e:
        print("Error", e)
        return False


def save_perso_financial_data(perso_financial_data: str, user_id: str):
    return save_csv_data(property_file_name=None, perso_financial_data=perso_financial_data, user_id=user_id)


def save_sample_data() -> None:
    save_perso_financial_data(perso_financial_data='./data/dummy_finances.csv', user_id='ox5GoxNq6ogha4mb9jxT04CZRwe2')


if __name__ == '__main__':
    save_sample_data()
    exit(0)
    # i, j = get_all_properties_list()
    # print(i, j)
    # display_charts(i, j)


def add_comparable_property(home_name: str, comparable_home: PropertySoldData):
    return None
