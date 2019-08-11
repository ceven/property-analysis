import pandas as pd

BASELINE_HOME_NAME = 'My New Home'
BASELINE_RENT_HOME_NAME = 'My Rental Home'


class PropertyData:

    def __init__(self, property_price, strata_q: int = 1400, council_q: int = 300, water_q: int = 200,
                 home_name: str = BASELINE_HOME_NAME):
        assert property_price

        # Name
        self.home_name = home_name

        # Buying costs
        self.property_price = property_price

        # strata, council, water
        self.strata_q = strata_q
        self.council_q = council_q
        self.water_q = water_q
        self.owner_costs_per_year = (self.strata_q + self.council_q + self.water_q) * 4

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class PersonalFinanceData:

    def __init__(self, rent_week, salary_net_year, initial_savings, monthly_living_expenses,
                 savings_interest_rate: float = 0.025, tax_rate: float = 0.37, loan_interest_rate: float = 0.035,
                 home_name: str = BASELINE_RENT_HOME_NAME):
        assert rent_week
        assert salary_net_year
        assert initial_savings
        assert monthly_living_expenses

        self.tax_rate = tax_rate
        self.savings_rate_brut = savings_interest_rate
        self.savings_rate_net = self.savings_rate_brut * (1 - self.tax_rate)
        self.loan_interest_rate = loan_interest_rate

        self.living_expenses = int(monthly_living_expenses * 12)

        # Renting costs
        self.rent_week = rent_week
        self.renting_price_per_year = int(rent_week / 7 * 365)

        # Savings
        self.salaries_net_per_year = salary_net_year
        self.savings_per_year = self.salaries_net_per_year - self.living_expenses
        self.initial_savings = initial_savings

        self.home_name = home_name

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


free_stamp_duty_threshold = 650000


def first_home_stamp_duty(property_price: float = free_stamp_duty_threshold) -> int:
    if property_price <= free_stamp_duty_threshold:
        return 0
    return int(8990 + 4.5 / 100 * (property_price - free_stamp_duty_threshold))


def load_data(property_file_path: str, finance_file_path: str) -> ([], object):
    perso_finance = None
    if finance_file_path:
        data_frame = pd.read_csv(finance_file_path, skipinitialspace=True, skip_blank_lines=True)
        perso_finance = PersonalFinanceData(rent_week=data_frame['rent_week'][0],
                                            salary_net_year=data_frame['salary_net_year'][0],
                                            initial_savings=data_frame['initial_deposit'][0],
                                            monthly_living_expenses=data_frame['monthly_living_expenses'][0],
                                            savings_interest_rate=data_frame['savings_interest_rate'][0],
                                            loan_interest_rate=data_frame['loan_interest_rate'][0])

    property_data = get_property_data(property_file_path) if property_file_path else None
    return property_data, perso_finance


def get_property_data(file_path: str) -> []:
    if not file_path:
        return []
    data_frame = pd.read_csv(file_path, skipinitialspace=True, skip_blank_lines=True)
    n_data = len(data_frame)
    property_data = [PropertyData(property_price=data_frame['property_price'][i],
                                  strata_q=data_frame['strata_q'][i],
                                  council_q=data_frame['council_q'][i],
                                  water_q=data_frame['water_q'][i],
                                  home_name=data_frame['home_name'][i])
                     for i in range(n_data)]

    return property_data
