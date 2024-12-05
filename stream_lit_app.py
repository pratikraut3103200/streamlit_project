import streamlit as st
import pandas as pd

import math
from datetime import datetime, timedelta

st.set_page_config(page_title="Dynamic Row Addition", layout="wide")

# Title of the app
st.title("Calculation Tool")

# Creating a single row for input fields
col1, col2, col3, col4,col5,col6 = st.columns([2, 2, 2, 2,2,2])


with col1:
    # Placeholder for the number of data rows
    total_rows = st.number_input(
        "Total Rows:",
        min_value=0,
        value=100,
        step=1
    )
    min_termin_in_start = st.number_input(
        "Min Termin in start:",
        min_value=1,
        value=3,
        step=1
    )

with col2:
    # Dropdown for % of bad data
    bad_data_percentage = st.selectbox(
        "Bad Data %:",
        options=[0, 20, 40, 60, 80, 100],
        index=0
    )
    conversion_rate_zu_verkauf = st.number_input(
        "Conversion rate zu Verkaufsumsätzen (%)",
        min_value=0,
        value=2,
        step=1
    )

with col3:
    # Input for amount paid to employees
    amount_paid_to_employees = st.number_input(
        "Amount Paid (in €):",
        min_value=0.0,
        step=1.0,
        value=5000.0,
        format="%.2f"
    )

with col4:
    # Input for amount earned per contract
    amount_earned_per_contract = st.number_input(
        "Earned/Contract (in €):",
        min_value=0.0,
        step=1.0,
        value=800.0,
        format="%.2f"
    )

with col5:
    termin_pro_woche = st.number_input(
        "termin pro week",
        min_value = 1,
        step=1,
        value=4

    )

with col6:
    number_of_months = st.number_input("No of Months",
                                       min_value = 2, step=1, value = 24)

# Calculation for data quality
if total_rows > 0:
    bad_rows = int((bad_data_percentage / 100) * total_rows)
    good_rows = total_rows - bad_rows
else:
    bad_rows, good_rows = 0, 0

# Display Data Quality Metrics Below
st.subheader("Data Quality Metrics")
st.write(f"**Good Data %:** {100 - bad_data_percentage}%")
st.write(f"**Number of Good Rows:** {good_rows}")
st.write(f"**Number of Bad Rows:** {bad_rows}")
st.write(f"**Termin Pro monath:** {termin_pro_woche*4}")

st.write(f"**Amount Paid to Employees:** €{amount_paid_to_employees:,.2f}")
st.write(f"**Amount Earned per Contract:** €{amount_earned_per_contract:,.2f}")
st.write(f"**Number of Months** {number_of_months}")


st.subheader("Dynamic Table")

# Generate months and quarters dynamically
start_date = datetime(2023, 1, 1)
months = [(start_date + timedelta(days=30 * i)).strftime("%B %Y") for i in range(number_of_months)]
quarters = [f"Q{(i // 3) + 1}" for i in range(number_of_months)]

termin_pro_monat_calculated = termin_pro_woche*4

termin_pro_monat = []
for i in range(number_of_months):
    if i < 2:
        value = min_termin_in_start
    else:
        increase = (termin_pro_monat_calculated - min_termin_in_start) / (number_of_months - 2)
        value = min_termin_in_start + increase * (i - 1)

    # Apply rounding logic
    if value - int(value) > 0.5:
        termin_pro_monat.append(math.ceil(value))
    else:
        termin_pro_monat.append(math.floor(value))

# Create the table data
table_data = {
    "Month": months,
    "Quarter": quarters,
    "Termin Pro monat": termin_pro_monat,
    "FTE": [amount_paid_to_employees * i for i in range(1,number_of_months+1)],
    "Auftrage from all kunde": [amount_earned_per_contract * i for i in termin_pro_monat]
}

# Create a DataFrame
df = pd.DataFrame(table_data)

df["Cumulative Auftrage"] = df["Auftrage from all kunde"].cumsum()

# Display the DataFrame in Streamlit
st.dataframe(df)


import plotly.graph_objects as go

# Create a single y-axis line chart
fig = go.Figure()

# Add the FTE line
fig.add_trace(go.Scatter(
    x=df["Month"],
    y=df["FTE"],
    mode='lines',
    name='FTE'
))

# Add the Cumulative Auftrage line
fig.add_trace(go.Scatter(
    x=df["Month"],
    y=df["Cumulative Auftrage"],
    mode='lines',
    name='Cumulative Auftrage'
))

# Update layout for a single y-axis
fig.update_layout(
    title="Line Chart with Shared X-Axis",
    xaxis=dict(title="Month"),
    yaxis=dict(title="Values"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Display the chart in Streamlit
st.plotly_chart(fig)



