from decimal import Decimal

original_data = r'''Monroe and Main	1.75%	$60.36	21.00%	$20.00
Blair	2.27%	$124.87	27.24%	$27.00
Chase Slate	2.50%	$1,549.03	29.99%	$51.00
JC Penny	2.25%	$2,460.37	26.99%	$99.24
ExxonMobil	2.10%	$1,478.91	25.24%	$46.70
Home Depot	2.17%	$1,098.21	25.99%	$37.00
Sam's Club	1.93%	$6,717.28	23.15%	$199.00
Texaco	2.27%	$1,790.62	27.24%	$59.00
Woman Within	2.27%	$1,116.68	27.24%	$50.00
Dillards	1.85%	$6,228.85	22.24%	$170.00
Viewtech Financial	0.00%	$4,822.99		$202.96
Ginny's	1.75%	$433.74	21%	$30.00
Walmart	1.43%	$3,872.16	17.15%	$94.00
Military Star	0.87%	$799.68	10.49%	$45.00 
''' + 'Sears\t2.12%\t$3797.66\t25.44%\t$122.00'

raw_tuples = ([x for x in y.split('\t')] for y in original_data.split('\n'))

def calculate_interest(principal, rate, time):
    return principal * (1 + rate * time)

def parse_money(m):
    return Decimal(''.join([x for x in m[1:].split(',')]))

def parse_percentage(p):
    try:
        return Decimal(p[:-1]) / Decimal(100)
    except:
        return Decimal(0)

table = [(name, parse_money(principal), parse_percentage(apr), parse_money(minimum)) for (name, _, principal, apr, minimum) in raw_tuples]

sorted_table = sorted(table, key=lambda x: -x[2])

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

def print_delta(t0,t1):
    for (x,y) in zip(t0,t1):
        print('Pay ${0:.2f} to {1} (${2:.2f} remaining)'.format(x[1] - y[1], x[0],y[1]))

def create_infinite_list_of_months(starting_month, year):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    i = starting_month
    while True:
        yield (months[i % 12], year + i // 12)
        i = i + 1

initial_amount = Decimal(1292.9)
payments = [x for x in make_payments(sorted_table, initial_amount)]

for (i,(month, year)) in zip(range(len(payments)-1), create_infinite_list_of_months(9,2016)):
    print('\n{0} {1}'.format(month, year))
    print_delta(payments[i], payments[i+1])
    

        
