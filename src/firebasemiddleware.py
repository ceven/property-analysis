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
users_loc = db.reference('users')
# property_loc = db.reference('property')

DEFAULT_USER_ID = "1"

def check_rights() -> None:
    ref = db.reference('restricted_access/secret_document')
    print(ref.get())


def add_property(prop: PropertyData, user_id: str = DEFAULT_USER_ID) -> bool:
    try:
        prop_str = json.dumps(prop.__dict__, default=json_data_converter)
        json_prop = json.loads(prop_str)
        users_loc.child(user_id).child("property").child(prop.home_name).set(json_prop)
        return True
    except Exception as e:
        print("Could not save property", e)
        return False


def add_perso_financial_data(f: PersonalFinanceData, user_id: str = DEFAULT_USER_ID) -> None:
    perso_data = json.dumps(f.__dict__, default=json_data_converter)
    perso_data_json = json.loads(perso_data)
    users_loc.child(user_id).child(f.home_name).set(perso_data_json)


def get_property(prop_name: str, user_id: str = DEFAULT_USER_ID) -> typing.Dict:
    return users_loc.child(user_id).child("property").child(prop_name).get()


def get_all_properties(user_id: str = DEFAULT_USER_ID) -> typing.Dict:
    return users_loc.child(user_id).child("property").get()


def get_perso_financial_data(user_id: str = DEFAULT_USER_ID) -> typing.Dict:
    return users_loc.child(user_id).child("financial").get()


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
    all_props, perso_json = get_user_data()
    property_data = [convert_to_property_data(v) for v in all_props.values()] if all_props else []
    perso_data = convert_to_perso_financial_data(perso_json) if perso_json else None
    return property_data, perso_data


def get_property_and_rent_by_name(home_name: str) -> \
        (typing.Optional[PropertyData], typing.Optional[PersonalFinanceData]):
    p = get_property(home_name)
    r = None if p is None else get_perso_financial_data()
    return convert_to_property_data(p), convert_to_perso_financial_data(r)


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
