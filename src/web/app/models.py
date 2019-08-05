from typing import Tuple

from firebasemiddleware import get_all_properties_json


# Create your models here.
def get_property_data() -> ([], []):
    return get_all_properties_json()
