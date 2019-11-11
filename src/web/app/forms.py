import typing

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

url_validator = URLValidator(schemes='https')


def link_validator(link):
    if link:
        url_validator(link)
        strip_link = link.strip('https://wwww.')
        if not strip_link.startswith('domain.com.au/'):
            raise ValidationError('%(l) is not a valid link', params={'l': link})


class PropertyForm(forms.Form):
    home_name = forms.CharField(label="Property name", max_length=250, strip=True)
    property_price = forms.IntegerField(label="Property price", min_value=0)
    strata_q = forms.IntegerField(label="Strata/q", min_value=0)
    water_q = forms.IntegerField(label="Water/q", min_value=0)
    council_q = forms.IntegerField(label="Council/q", min_value=0)
    domain_link = forms.CharField(label="Domain link", min_length=0, max_length=250, strip=True, required=False,
                                  validators=[link_validator])

    def update_form_fields_values(self, existing_property_data: typing.Dict):
        if existing_property_data and len(existing_property_data) > 0:
            self.fields['home_name'].initial = existing_property_data.get('home_name', '')
            self.fields['property_price'].initial = existing_property_data.get('property_price', '')
            self.fields['strata_q'].initial = existing_property_data.get('strata_q', '')
            self.fields['water_q'].initial = existing_property_data.get('water_q', '')
            self.fields['council_q'].initial = existing_property_data.get('council_q', '')
            self.fields['domain_link'].initial = existing_property_data.get('domain_link', '')


class PropertySoldForm(PropertyForm):
    sold_price = forms.IntegerField(label="Sold price", min_value=0)


class UserRegisterForm(forms.Form):
    user_email = forms.EmailField()
    user_password = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    user_email = forms.EmailField()
    user_password = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput)


class FinancesForm(forms.Form):
    salaries_net_per_year = forms.IntegerField(label="Salary net/year", min_value=0)
    living_expenses = forms.IntegerField(label="Living expenses/year", min_value=0)
    rent_week = forms.IntegerField(label="Rent/week", min_value=0)
    initial_savings = forms.IntegerField(label="Initial Savings", min_value=0)
    loan_interest_rate = forms.FloatField(label="Mortgage interest Rate", min_value=0.0, max_value=1.0)
    savings_rate_brut = forms.FloatField(label="Savings interest Rate", min_value=0.0, max_value=1.0)

    def update_form_fields_values(self, existing_finance_data: typing.Dict):
        if existing_finance_data and len(existing_finance_data) > 0:
            self.fields['salaries_net_per_year'].initial = existing_finance_data.get('salaries_net_per_year', 0)
            self.fields['living_expenses'].initial = existing_finance_data.get('living_expenses', 0)
            self.fields['rent_week'].initial = existing_finance_data.get('rent_week', 0)
            self.fields['initial_savings'].initial = existing_finance_data.get('initial_savings', 0)
            self.fields['loan_interest_rate'].initial = existing_finance_data.get('loan_interest_rate', 0)
            self.fields['savings_rate_brut'].initial = existing_finance_data.get('savings_rate_brut', 0)
