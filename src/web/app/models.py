from typing import Tuple

import firebasemiddleware


# Create your models here.
def get_property_data() -> ([], []):
    return firebasemiddleware.get_all_properties_json()


def get_property_by_name(home_name: str) -> (object, object):
    return firebasemiddleware.get_property_json(home_name)

