import json
from collections import namedtuple

import firebase_admin
import typing
from charts import load_data, display_charts
from firebase_admin import credentials
from firebase_admin import db
from numpy import int64

from data import PropertyData, RentData
import data

cred = credentials.Certificate("./private/firebase-key.json")
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://property-analysis-dccc1.firebaseio.com'})
property_loc = db.reference('property')
property_own_loc = property_loc.child('own')
property_rent_loc = property_loc.child('rent')


def check_rights() -> None:
    ref = db.reference('restricted_access/secret_document')
    print(ref.get())


def add_property(prop: PropertyData) -> None:
    json_prop = json.dumps(prop.__dict__, default=json_data_converter)
    property_own_loc.child(prop.home_name).set(json_prop)


def add_rent_for_property(rent: RentData) -> None:
    json_prop = json.dumps(rent.__dict__, default=json_data_converter)
    property_rent_loc.child(rent.home_name).set(json_prop)


def get_property(prop_name: str) -> object:
    return property_own_loc.child(prop_name).get()


def get_property_rent(prop_name: str) -> object:
    return property_rent_loc.child(prop_name).get()


def get_baseline_rent() -> object:
    return get_property_rent('base')


def get_all_properties() -> typing.Dict:
    return property_own_loc.get()


def get_rent_properties() -> typing.Dict:
    return property_rent_loc.get()


def get_one_rent_property():
    return get_rent_properties().popitem()


def get_all_properties_list() -> ([], []):
    all_props = get_all_properties()
    rent_property_json = json.loads(get_one_rent_property()[1])
    property_data = []
    rent_data = []
    for v_raw in all_props.values():
        v = json.loads(v_raw)
        property_data.append(PropertyData(v['property_price'],
                                          v['initial_deposit'],
                                          v['salaries_net_per_year'],
                                          v['living_expenses'] / 12,
                                          v['interest_rate'],
                                          v['strata_q'],
                                          v['council_q'],
                                          v['water_q'],
                                          v['home_name']))

        rent_data.append(RentData(rent_property_json['rent_week'],
                                  rent_property_json['salaries_net_per_year'],
                                  rent_property_json['initial_savings'],
                                  rent_property_json['living_expenses'] / 12,
                                  rent_property_json['savings_rate_brut']))

    return property_data, rent_data


def get_all_properties_json():
    p, r = get_all_properties_list()
    p_d = json.dumps([p_.__dict__ for p_ in p], default=json_data_converter)  # FIXME could find a more efficient way
    r_d = json.dumps([r_.__dict__ for r_ in r], default=json_data_converter)
    return json.loads(p_d, object_hook=_json_object_hook), json.loads(r_d, object_hook=_json_object_hook)


def get_property_json(home_name: str, use_baseline_rent: bool = True) -> (object, object):
    p = get_property(home_name)
    if p is None:
        return p, None
    r = get_property_rent(data.BASELINE_RENT_HOME_NAME if use_baseline_rent else home_name)
    return json.loads(p, object_hook=_json_object_hook), json.loads(r, object_hook=_json_object_hook)


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json_data_converter(o):
    if isinstance(o, int64):
        return int(o)


def save_csv_data(file_name: str) -> None:
    p_data, r_data = load_data(file_name)

    for p, r in zip(p_data, r_data):
        add_property(p)
        add_rent_for_property(r)


def save_sample_data() -> None:
    save_csv_data('./data/financial_data_sold_properties.csv')


if __name__ == '__main__':
    # save_sample_data()
    i, j = get_all_properties_list()
    print(i, j)
    display_charts(i, j)
