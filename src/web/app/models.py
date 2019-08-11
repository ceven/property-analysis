import os

import firebasemiddleware
import data


# Create your models here.
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
