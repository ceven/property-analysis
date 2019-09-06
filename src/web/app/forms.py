import typing
from django import forms


class PropertyForm(forms.Form):
    home_name = forms.CharField(label="Property name", max_length=250)
    property_price = forms.IntegerField(label="Property price", min_value=0)
    strata_q = forms.IntegerField(label="Strata/q", min_value=0)
    water_q = forms.IntegerField(label="Water/q", min_value=0)
    council_q = forms.IntegerField(label="Council/q", min_value=0)


class PropertySoldForm(PropertyForm):
    sold_price = forms.IntegerField(label="Sold price", min_value=0)


class UserRegisterForm(forms.Form):
    user_email = forms.EmailField()
    user_password = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    user_email = forms.EmailField()
    user_password = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput)


class FinancesForm(forms.Form):
    salary_net_year = forms.IntegerField(label="Salary net/year", min_value=0)
    expenses_year = forms.IntegerField(label="Living expenses/year", min_value=0)
    # TODO add more fields

    def update_form_fields_values(self, existing_finance_data: typing.Dict):
        if existing_finance_data and len(existing_finance_data) > 0:
            self.fields['salary_net_year'].initial = existing_finance_data['salaries_net_per_year']
            self.fields['expenses_year'].initial = existing_finance_data['living_expenses']
            # TODO add more fields
