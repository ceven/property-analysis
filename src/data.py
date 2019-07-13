living_expenses_monthly = 4200


class PropertyData:

    def __init__(self, property_price, initial_deposit, salary_net_year, loan_interest_rate,
                 strata_q: int = 1400, council_q: int = 300, water_q: int = 200, home_name: str = 'My New Home'):
        # Fixed data for now
        self.living_expenses = int(living_expenses_monthly * 12)  # 4,200/month
        self.interest_rate = loan_interest_rate

        # Buying costs
        self.property_price = property_price
        self.initial_deposit = initial_deposit
        self.initial_loan = property_price - initial_deposit + first_home_stamp_duty(property_price)

        # Savings
        self.salaries_net_per_year = salary_net_year
        self.savings_per_year = self.salaries_net_per_year - self.living_expenses

        # strata, council, water
        self.strata_q = strata_q
        self.council_q = council_q
        self.water_q = water_q

        self.owner_costs_per_year = (self.strata_q + self.council_q + self.water_q) * 4

        self.home_name = home_name

        print(self.home_name)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class RentData:

    def __init__(self, rent_week, salary_net_year, initial_savings, savings_interest_rate: float = 0.025,
                 tax_rate: float = 0.37):
        # Fixed data for now
        self.living_expenses = int(living_expenses_monthly * 12)  # 4,200/month
        self.tax_rate = tax_rate
        self.savings_rate_brut = savings_interest_rate
        self.savings_rate_net = self.savings_rate_brut * (1 - self.tax_rate)
        print("Tax rate: {}", self.tax_rate)

        # Renting costs
        self.rent_week = rent_week
        self.renting_price_per_year = int(rent_week / 7 * 365)

        # Savings
        self.salaries_net_per_year = salary_net_year
        self.savings_per_year = self.salaries_net_per_year - self.living_expenses
        self.initial_savings = initial_savings

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


free_stamp_duty_threshold = 650000


def first_home_stamp_duty(property_price: float = free_stamp_duty_threshold ) -> int:
    if property_price <= free_stamp_duty_threshold:
        return 0
    return int(8990 + 4.5 / 100 * (property_price - free_stamp_duty_threshold))
