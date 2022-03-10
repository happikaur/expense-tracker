import csv
from dateutil import parser

data = {}

with open('expensetask.csv', 'r') as csv_file:
    spreadsheet = csv.DictReader(csv_file)
    for row in spreadsheet:
        if data.get(row['User']):
            data[row['User']].append(row)
        else:
            data[row['User']] = [row]

print(data)

user_name = input('Please enter full name: ')
search = data.get(user_name)
is_user_found = search is not None

if is_user_found:
    print(search)
else:
    print('User not found')

#to calculate monthly spends and total spend
jan = 0
feb = 0
mar = 0
for m in search:
    date = parser.parse(m['Timestamp'], dayfirst=True)
    print(date)
    month = date.month
    cost = float(m['Amount'])
    if month == 1:
        jan += cost
    elif month == 2:
        feb += cost
    elif month == 3:
        mar += cost
    else:
        print("Month", month, "is not in Q1")

jan = round(jan, 2)
feb = round(feb, 2)
mar = round(mar, 2)

print("January Expenses:", jan, "February Expenses:", feb, "March Expenses:", mar)
totalSpend = round((jan + feb + mar), 2)
print(user_name, "has expenses totaling", totalSpend, "from quarter 1.")

#to calculate category spends for all categories to create a chart/graph with
spendBreakDown = {"currencyExchange": 0, "generalStore": 0, "hotel": 0, "jewelry": 0, "loan": 0, "mortgage": 0, "restaurant": 0, "retail": 0, "supermarket": 0, "taxi": 0}
for x in search:
    price = float(x['Amount'])
    if x['Category'] == 'Currency Exchange':
        spendBreakDown["currencyExchange"] += price
    elif x['Category'] == 'General Store':
        spendBreakDown["generalStore"] += price
    elif x['Category'] == 'Hotel':
        spendBreakDown["hotel"] += price
    elif x['Category'] == 'Jewelry':
        spendBreakDown["jewelry"] += price
    elif x['Category'] == 'Loan':
        spendBreakDown["loan"] += price
    elif x['Category'] == 'Mortgage':
        spendBreakDown["mortgage"] += price
    elif x['Category'] == 'Restaurant':
        spendBreakDown["restaurant"] += price
    elif x['Category'] == 'Retail':
        spendBreakDown["retail"] += price
    elif x['Category'] == 'Supermarket':
        spendBreakDown["supermarket"] += price
    elif x['Category'] == 'Taxi':
        spendBreakDown["taxi"] += price
    else:
        print("Category Error")

#rounding all items in the spend breakdown dictionary
#has to been done after above as adding multiple floats which have 2 decimal places
#can somehow create a float with way more decimal places than 2 (Strange?)
for key, value in spendBreakDown.items():
    spendBreakDown[key] = round(value, 2)

print(spendBreakDown)