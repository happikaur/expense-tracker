import csv
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

data = {}

with open('expenses.csv', 'r') as csv_file:
    spreadsheet = csv.DictReader(csv_file)
    for row in spreadsheet:
        if data.get(row['User']):
            data[row['User']].append(row)
        else:
            data[row['User']] = [row]

# Code for Dash / Visuals
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Expense Tracker', style={'textAlign': 'center', 'color': '#7FDBFF'}),

    html.Div([
        "Please enter the name: ",
        dcc.Input(id='my-input', value='', type='text')
    ]),

    dcc.Graph(id='spend-by-month'),

    dcc.Graph(id='spend-by-category')
])

@app.callback(
    Output(component_id='spend-by-month', component_property='figure'),
    Output(component_id='spend-by-category', component_property='figure'),
    Input(component_id='my-input', component_property='value')
)
def get_user_and_search(name):
    spendBreakDown = {"Currency Exchange": 0, "General Store": 0, "Hotel": 0, "Jewelry": 0, "Loan": 0, "Mortgage": 0,
                      "Restaurant": 0, "Retail": 0, "Supermarket": 0, "Taxi": 0}
    months = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0,
              "12": 0}
    totalSpend = 0
    user_name = name
    search = data.get(user_name)

    if search is None:
        print('User not found')

    #to calculate monthly spends and total spend
    for m in search:
        cost = float(m['Amount'])
        try:
            timestamp = m['Timestamp'][3:5:]
            months[timestamp] += cost
        except KeyError:
            print("month error")

    #rounding all items in the months dictionary and calculating totalSpend
    for key, value in months.items():
        months[key] = round(value, 2)
        totalSpend += value

    print("January Expenses:", months["01"], "February Expenses:", months["02"], "March Expenses:", months["03"])
    print(user_name, "has expenses totaling", round(totalSpend, 2), "from quarter 1.")

    #to calculate category spends for all categories
    for x in search:
        price = float(x['Amount'])
        try:
            category = x['Category']
            spendBreakDown[category] += price
        except LookupError:
            print("Category Error")

    #rounding all items in the spend breakdown dictionary
    for key, value in spendBreakDown.items():
        spendBreakDown[key] = round(value, 2)

    spendByMonthDataFrame = pd.DataFrame([months])

    spendByMonth = px.bar(
        spendByMonthDataFrame,
        barmode="group",
        labels={"value": "Amount", "index": "Month", "Variable": "Timestamp"}
    )

    spendByCategoryDataFrame = pd.DataFrame([spendBreakDown])

    spendByCategory = px.bar(
        spendByCategoryDataFrame,
        barmode="group",
        labels={"value": "Amount", "index": "Category", "variable": "Category"}
    )

    return spendByMonth, spendByCategory

if __name__ == '__main__':
    app.run_server(debug=True)