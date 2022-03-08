import csv

data = {}

with open('Expenses.csv', 'r') as csv_file:
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
