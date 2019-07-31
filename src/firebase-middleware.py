import json

import firebase_admin
from charts import load_data
from firebase_admin import credentials
from firebase_admin import db
from numpy import int64

from data import PropertyData

cred = credentials.Certificate("./private/key.json")
app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://property-analysis-dccc1.firebaseio.com'})
property_loc = db.reference('property')


def check_rights():
    ref = db.reference('restricted_access/secret_document')
    print(ref.get())


def add_property(prop: PropertyData):
    json_prop = json.dumps(prop.__dict__, default=json_data_converter)
    print("Json PROP: ", json_prop)
    property_loc.child(prop.home_name).set(json_prop)


def json_data_converter(o):
    if isinstance(o, int64):
        return int(o)


if __name__ == '__main__':
    check_rights()
    p_data, r_data = load_data('./data/financial_data.csv')

    for p, r in zip(p_data, r_data):
        add_property(p)
