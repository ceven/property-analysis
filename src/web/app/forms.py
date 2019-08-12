from django import forms


class PropertyForm(forms.Form):
    home_name = forms.CharField(label="Property name", max_length=250)
    property_price = forms.IntegerField(label="Property price", min_value=0)
    strata_q = forms.IntegerField(label="Strata/q", min_value=0)
    water_q = forms.IntegerField(label="Water/q", min_value=0)
    council_q = forms.IntegerField(label="Council/q", min_value=0)


class PropertySoldForm(PropertyForm):
    sold_price = forms.IntegerField(label="Sold price", min_value=0)
