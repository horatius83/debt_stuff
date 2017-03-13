from decimal import Decimal
import json

def calculate_interest(principal, rate, time):
    return principal * (1 + rate * time)

def calculate_minimum_payment(table):
    return Decimal(sum((x for (_,_,_,x) in table)))

def make_payment(table, total_amount):
    minimum = calculate_minimum_payment(table)
    extra = total_amount - minimum
    new_table = []
    for (name, principal, apr, minimum) in table:
        principal = calculate_interest(principal, apr, Decimal(1/12))
        if principal > minimum:
            principal = principal - minimum
        else:
            principal = 0
            minimum = 0
        if principal > extra:
            principal = principal - extra
            extra = 0
        else:
            extra = extra - principal
            principal = 0
            minimum = 0
        new_table.append((name, principal, apr, minimum))
    return new_table

def calculate_remaining_owed(table):
    return sum((x[1] for x in table))

def make_payments(table, starting_amount):
    remaining_owed = calculate_remaining_owed(table)
    while(remaining_owed > 0):
        yield table
        table = make_payment(table, starting_amount)
        remaining_owed = calculate_remaining_owed(table)

def print_delta(t0,t1, output):
    for (x,y) in zip(t0,t1):
        output('Pay ${0:.2f} to {1} (${2:.2f} remaining)'.format(x[1] - y[1], x[0],y[1]))

def create_infinite_list_of_months(starting_month, year):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    i = starting_month
    while True:
        yield (months[i % 12], year + i // 12)
        i = i + 1

#raw_tuples = ([x for x in y.split('\t')] for y in original_data.split('\n'))

#table = [(name, parse_money(principal), parse_percentage(apr), parse_money(minimum)) for (name, _, principal, apr, minimum) in raw_tuples]
table = None
with open('loan_data2.json', 'r') as in_data:
    json_data = json.loads(in_data.read())
    table = [(o['name'], Decimal(o['principal']), Decimal(o['apr']), Decimal(o['minimum'])) for o in json_data]
sorted_table = sorted(table, key=lambda x: -x[2])

initial_amount = Decimal(1292.9)
payments = [x for x in make_payments(sorted_table, initial_amount)]

def print_thing(x):
    print(x)

with open('payment_plan.txt', 'w') as out_data:
    for (i,(month, year)) in zip(range(len(payments)-1), create_infinite_list_of_months(3,2017)):
        print('\n{0} {1}'.format(month, year))
        print_delta(payments[i], payments[i+1], print_thing)
        out_data.write('\n{0} {1}\n'.format(month, year))
        def write_out(x):
            out_data.write(x + '\n')
        print_delta(payments[i], payments[i+1], write_out)
