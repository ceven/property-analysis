import json
import typing
from collections import namedtuple

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from numpy import int64

from charts import load_data
from data import PropertyData, PersonalFinanceData

cred = credentials.Certificate("./private/firebase-key.json")
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://property-analysis-dccc1.firebaseio.com'})
property_loc = db.reference('property')
property_own_loc = property_loc.child('own')
perso_data_loc = property_loc.child('financial')


def check_rights() -> None:
    ref = db.reference('restricted_access/secret_document')
    print(ref.get())


def add_property(prop: PropertyData) -> bool:
    try:
        json_prop = json.dumps(prop.__dict__, default=json_data_converter)
        property_own_loc.child(prop.home_name).set(json_prop)
        return True
    except Exception as e:
        print("Could not save property", e)
        return False


def add_perso_financial_data(f: PersonalFinanceData) -> None:
    json_prop = json.dumps(f.__dict__, default=json_data_converter)
    perso_data_loc.child(f.home_name).set(json_prop)


def get_property(prop_name: str) -> typing.Dict:
    return property_own_loc.child(prop_name).get()


def get_all_properties() -> typing.Dict:
    return property_own_loc.get()


def get_all_financial_data() -> typing.Dict:
    return perso_data_loc.get()


def get_perso_financial_data() -> typing.Dict:
    data = get_all_financial_data()
    if data and len(data) > 0:
        data = data.popitem()[1]
    return data


def get_perso_financial_data_json() -> typing.Dict:
    data = get_perso_financial_data()
    # FIXME should do this more elegantly
    if data:
        data = json.loads(data)
    return data


def get_all_properties_list() -> ([], object):
    all_props = get_all_properties()
    perso_json = get_perso_financial_data_json()
    property_data = []
    if all_props:
        for v_raw in all_props.values():
            v = json.loads(v_raw)
            p_data = PropertyData(property_price=v['property_price'],
                                  strata_q=v['strata_q'],
                                  council_q=v['council_q'],
                                  water_q=v['water_q'],
                                  home_name=v['home_name'])
            property_data.append(p_data)

    perso_data = None
    if perso_json:
        perso_data = PersonalFinanceData(rent_week=perso_json['rent_week'],
                                         salary_net_year=perso_json['salaries_net_per_year'],
                                         initial_savings=perso_json['initial_savings'],
                                         monthly_living_expenses=perso_json['living_expenses'] / 12,
                                         savings_interest_rate=perso_json['savings_rate_brut'])

    return property_data, perso_data


def get_all_properties_json():
    p, r = get_all_properties_list()
    p_d = json.dumps([p_.__dict__ for p_ in p], default=json_data_converter)  # FIXME could find a more efficient way
    r_d = json.dumps(r.__dict__, default=json_data_converter)
    return json.loads(p_d, object_hook=_json_object_hook), json.loads(r_d, object_hook=_json_object_hook)


def get_property_and_rent_by_name_json(home_name: str) -> (object, object):
    p = get_property(home_name)
    if p is None:
        return p, None
    r = get_perso_financial_data()
    return json.loads(p, object_hook=_json_object_hook), json.loads(r, object_hook=_json_object_hook)


def get_property_by_name_json(home_name: str) -> object:
    p = get_property(home_name)
    if p is None:
        return p
    return json.loads(p, object_hook=_json_object_hook)


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json_data_converter(o):
    if isinstance(o, int64):
        return int(o)


def save_csv_data(property_file_name: str, perso_financial_data: str) -> bool:
    try:
        p_data, r_data = load_data(property_file_name, perso_financial_data)

        for p in p_data:
            add_property(p)
        if r_data:
            add_perso_financial_data(r_data)
        return True
    except Exception as e:
        print("Error", e)
        return False


def save_sample_data() -> None:
    save_csv_data('./data/financial_data.csv')


if __name__ == '__main__':
    save_sample_data()
    exit(0)
    # i, j = get_all_properties_list()
    # print(i, j)
    # display_charts(i, j)
