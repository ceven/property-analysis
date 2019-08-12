import json
import typing

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from numpy import int64

import data
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
        prop_str = json.dumps(prop.__dict__, default=json_data_converter)
        json_prop = json.loads(prop_str)
        property_own_loc.child(prop.home_name).set(json_prop)
        return True
    except Exception as e:
        print("Could not save property", e)
        return False


def add_perso_financial_data(f: PersonalFinanceData) -> None:
    perso_data = json.dumps(f.__dict__, default=json_data_converter)
    perso_data_json = json.loads(perso_data)
    perso_data_loc.child(f.home_name).set(perso_data_json)


def get_property(prop_name: str) -> typing.Dict:
    return property_own_loc.child(prop_name).get()


def get_all_properties() -> typing.Dict:
    return property_own_loc.get()


def get_all_financial_data() -> typing.Dict:
    return perso_data_loc.get()


def get_perso_financial_data() -> typing.Dict:
    data = get_all_financial_data()
    return data if len(data) == 0 else data.popitem()[1]


def get_all_properties_json() -> (typing.Dict, typing.Dict):
    return get_all_properties(), get_perso_financial_data()


def convert_to_property_data(d: typing.Dict) -> typing.Optional[PropertyData]:
    if not d:
        return None
    return PropertyData(property_price=d['property_price'],
                        strata_q=d['strata_q'],
                        council_q=d['council_q'],
                        water_q=d['water_q'],
                        home_name=d['home_name'])


def convert_to_perso_financial_data(d: typing.Dict) -> typing.Optional[PersonalFinanceData]:
    if not d:
        return None
    return PersonalFinanceData(rent_week=d['rent_week'],
                               salary_net_year=d['salaries_net_per_year'],
                               initial_savings=d['initial_savings'],
                               monthly_living_expenses=d['living_expenses'] / 12,
                               savings_interest_rate=d['savings_rate_brut'])


def get_all_properties_list() -> ([PropertyData], typing.Optional[PersonalFinanceData]):
    all_props, perso_json = get_all_properties_json()
    property_data = [convert_to_property_data(v) for v in all_props.values()] if all_props else []
    perso_data = convert_to_perso_financial_data(perso_json) if perso_json else None
    return property_data, perso_data


def get_property_and_rent_by_name(home_name: str) -> \
        (typing.Optional[PropertyData], typing.Optional[PersonalFinanceData]):
    p = get_property(home_name)
    r = None if p is None else get_perso_financial_data()
    return convert_to_property_data(p), convert_to_perso_financial_data(r)


# def _json_object_hook(d):
#     return namedtuple('X', d.keys())(*d.values())


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


def add_comparable_property(home_name: str, comparable_home: data.PropertySoldData):
    return None
