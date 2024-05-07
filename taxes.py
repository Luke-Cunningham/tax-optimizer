import csv

def calculate_ca_state_tax(taxable_income):
    ca_tax_brackets = [
        (10412, 0.01, 0),
        (24684, 0.02, 104.12),
        (38959, 0.04, 389.56),
        (54081, 0.06, 960.56),
        (68350, 0.08, 1867.88),
        (349137, 0.093, 3009.40),
        (418961, 0.103, 29122.59),
        (698271, 0.113, 36314.46),
        (float('inf'), 0.123, 67876.49),
    ]

    tax_owed = 0
    for cap, rate, base_tax in ca_tax_brackets:
        if taxable_income <= cap:
            tax_owed = base_tax + (taxable_income - (cap - (cap - base_tax / rate))) * rate
            break

    return tax_owed


def calculate_federal_tax(taxable_income):
    federal_tax_brackets = [
        (11000, 0.10, 0),
        (44725, 0.12, 1100),
        (95375, 0.22, 4019),
        (182100, 0.24, 14659.50),
        (231250, 0.32, 33271.50),
        (578125, 0.35, 49335.50),
        (float('inf'), 0.37, 174253.75),
    ]
   
    tax_owed = 0
    for cap, rate, base_tax in federal_tax_brackets:
        if taxable_income <= cap:
            tax_owed = base_tax + (taxable_income - (cap - (cap - base_tax / rate))) * rate
            break

    return tax_owed
    

def calculate_take_home_salary(salary, deductions, state, contribution_rate):
    taxable_income = salary - deductions - (salary * contribution_rate)
    federal_taxes = calculate_federal_tax(taxable_income)

    if state.upper() == "CA":
        state_taxes = calculate_ca_state_tax(taxable_income)
    elif state.upper() == "CO":
        state_taxes = taxable_income * .044

    monthly_take_home = (salary - federal_taxes - state_taxes - (salary * contribution_rate)) / 12
    return monthly_take_home


def calculate_metrics(salary, deductions, state, contribution_rate):
    """
    Calculate various metrics based on the contribution rate.
    """
    monthly_salary = salary / 12
    monthly_contribution = monthly_salary * contribution_rate
    monthly_take_home_with_contribution = calculate_take_home_salary(salary, deductions, state, contribution_rate)
    monthly_take_home_without_contribution = calculate_take_home_salary(salary, deductions, state, 0)
    tax_savings = (monthly_take_home_without_contribution - monthly_take_home_with_contribution + monthly_contribution)
    free_investment = monthly_contribution - (monthly_salary - monthly_take_home_with_contribution)
    net_benefit = free_investment + tax_savings

    return {
        'Contribution Rate (%)': contribution_rate * 100,
        'Monthly Take-Home Pay ($)': monthly_take_home_with_contribution,
        'Monthly 401k Contribution ($)': monthly_contribution,
        'Tax Savings ($)': tax_savings,
        'Free Investment Amount ($)': free_investment,
        'Net Benefit ($)': net_benefit
    }


def main():
    salary = float(108000) # float(input("Enter your annual salary: "))
    deductions = float(1440) # float(input("Enter your annual deductions: "))
    state = "CA" # input("Enter your state (CO or CA): ")

    with open('401k_contributions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Contribution Rate (%)', 'Monthly Take-Home Pay ($)', 'Monthly 401k Contribution ($)', 'Tax Savings ($)', '"Free" Investment Amount ($)', 'Net Benefit ($)'])

        for i in range(201):
            contribution_rate = i / 1000
            metrics = calculate_metrics(salary, deductions, state, contribution_rate)
            
            # Format data to limit decimal places before writing
            formatted_metrics = [
                f"{metrics['Contribution Rate (%)']:.1f}",
                f"{metrics['Monthly Take-Home Pay ($)']:.0f}",
                f"{metrics['Monthly 401k Contribution ($)']:.0f}",
                f"{metrics['Tax Savings ($)']:.0f}",
                f"{metrics['Free Investment Amount ($)']:.0f}",
                f"{metrics['Net Benefit ($)']:.0f}",
            ]
            
            writer.writerow(formatted_metrics)

    print("Data exported to 401k_contributions.csv")

    
if __name__ == "__main__":
    main()