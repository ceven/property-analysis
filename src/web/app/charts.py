import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from data import *


def load_data(file_path: str):
    data_frame = pd.read_csv(file_path, skipinitialspace=True, skip_blank_lines=True)

    n_data = len(data_frame)

    property_data = []
    rent_data = []

    for i in range(n_data):
        property_data.append(PropertyData(data_frame['property_price'][i], data_frame['initial_deposit'][i],
                                          data_frame['salary_net_per_year'][i],
                                          data_frame['monthly_living_expenses'][i],
                                          data_frame['loan_interest_rate'][i],
                                          data_frame['strata_q'][i], data_frame['council_q'][i],
                                          data_frame['water_q'][i], data_frame['home_name'][i]))

        rent_data.append(RentData(data_frame['renting_per_week'][i],
                                  data_frame['salary_net_per_year'][i],
                                  data_frame['initial_deposit'][i],
                                  data_frame['monthly_living_expenses'][i],
                                  data_frame['savings_interest_rate'][i]))

    return property_data, rent_data


def get_chart_graphic(p: PropertyData, r: RentData, graphic_format: str = 'png'):
    loan_over_years = list(range(p.initial_loan, 0, -(p.savings_per_year - p.owner_costs_per_year)))
    if loan_over_years[-1] > 0:
        loan_over_years.append(0)

    mortgage_over_years = [int(p.interest_rate * loan) for loan in loan_over_years]

    mortgage_over_years_with_other_outgoings = [int(m + p.owner_costs_per_year) for m in mortgage_over_years]

    n_years = len(mortgage_over_years)
    years = range(0, n_years)

    cost_of_renting = [r.renting_price_per_year for y in years]
    savings_over_years = [r.initial_savings for y in years]
    for y in range(1, n_years + 1):
        interest_last_year = r.savings_rate_net * savings_over_years[y - 1]

        cost_of_renting[y - 1] -= interest_last_year

        if y < n_years:
            savings_over_years[y] = savings_over_years[y - 1] + \
                                    r.savings_per_year - r.renting_price_per_year + interest_last_year

    # Matplotlib figure
    fig = Figure()
    fig.suptitle(p.home_name, fontweight='bold')

    splt = fig.add_subplot(311)

    # 1st chart
    splt.plot(years, cost_of_renting, '-rs', label='Cost of renting')
    splt.plot(years, mortgage_over_years, '-gs', label='Mortgage')
    splt.plot(years, mortgage_over_years_with_other_outgoings, '-bs', label='Total costs of owning')
    splt.set_title("Cost of renting v.s buying over the years")
    splt.set_ylabel('$ value')
    splt.set_xlabel('Years')
    splt.legend()

    # 2nd chart
    property_value_over_years = list([p.property_price for y in years])

    splt = fig.add_subplot(312)
    splt.plot(years, property_value_over_years, '-r', label='Property value')
    splt.plot(years, loan_over_years, '-ms', label='Loan')
    splt.plot(years, savings_over_years, '-ys', label='Savings (no loan)')
    splt.set_title("Mortgage vs savings over years")
    splt.set_ylabel('$ value')
    splt.set_xlabel('Years')
    splt.legend()

    # Text area
    fig.text(0.1, 0.1, "Property price: {}\nOwner costs/year: {}".format(p.property_price,
                                                                         p.owner_costs_per_year))

    # Save figure to graphic
    buffer = BytesIO()
    fig.savefig(buffer, format=graphic_format, bbox_inches='tight')
    image = buffer.getvalue()
    buffer.close()

    if graphic_format != 'svg':
        return base64.b64encode(image).decode('utf-8')

    return image


def display_charts(p_data, r_data):
    total = len(p_data)
    charts_per_page = 5
    page = 1
    current = 0

    plt.ion()
    plt.show()

    for p, r in zip(p_data, r_data):
        loan_over_years = list(range(p.initial_loan, 0, -(p.savings_per_year - p.owner_costs_per_year)))
        if loan_over_years[-1] > 0:
            loan_over_years.append(0)

        mortgage_over_years = [int(p.interest_rate * loan) for loan in loan_over_years]

        mortgage_over_years_with_other_outgoings = [int(m + p.owner_costs_per_year) for m in mortgage_over_years]

        n_years = len(mortgage_over_years)
        years = range(0, n_years)

        cost_of_renting = [r.renting_price_per_year for y in years]
        savings_over_years = [r.initial_savings for y in years]
        for y in range(1, n_years + 1):
            interest_last_year = r.savings_rate_net * savings_over_years[y - 1]

            cost_of_renting[y - 1] -= interest_last_year

            if y < n_years:
                savings_over_years[y] = savings_over_years[y - 1] + \
                                        r.savings_per_year - r.renting_price_per_year + interest_last_year

        # FIXME this assumes constant value ; could factor 3-5% increase/year
        property_value_over_years = list([p.property_price for y in years])

        print(years)
        print(loan_over_years)
        print(mortgage_over_years)
        print(mortgage_over_years_with_other_outgoings)
        print(savings_over_years)
        print(cost_of_renting)

        # 1st chart
        plt.figure(current)
        plt.suptitle(p.home_name, fontweight='bold')

        plt.subplot(3, 1, 1)
        plt.plot(years, cost_of_renting, '-rs', label='Cost of renting')
        plt.plot(years, mortgage_over_years, '-gs', label='Mortgage')
        plt.plot(years, mortgage_over_years_with_other_outgoings, '-bs', label='Total costs of owning')
        plt.title("Cost of renting v.s buying over the years")
        plt.ylabel('$ value')
        plt.xlabel('Years')
        plt.legend()

        # 2nd chart
        plt.subplot(3, 1, 2)
        plt.plot(years, property_value_over_years, '-r', label='Property value')
        plt.plot(years, loan_over_years, '-ms', label='Loan')
        plt.plot(years, savings_over_years, '-ys', label='Savings (no loan)')
        plt.title("Mortgage vs savings over years")
        plt.ylabel('$ value')
        plt.xlabel('Years')
        plt.legend()

        plt.figtext(0.1, 0.1,
                    "Property price: {}\nOwner costs/year: {}".format(p.property_price, p.owner_costs_per_year))

        current += 1
        if current >= min(total, charts_per_page * page):
            plt.draw()
            plt.pause(0.001)
            input("Press key to continue...")
            plt.close('all')
            page += 1
        if current >= total:
            break


if __name__ == '__main__':
    pd, rd = load_data('../data/financial_data_sold_properties.csv')
    display_charts(pd, rd)
    print("Done")