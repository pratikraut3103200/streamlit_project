import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
        value=3200.0,
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
st.write(f"**Termin Pro Woche:** {termin_pro_woche*4}")

st.write(f"**Amount Paid to Employees:** €{amount_paid_to_employees:,.2f}")
st.write(f"**Amount Earned per Contract:** €{amount_earned_per_contract:,.2f}")
st.write(f"**Number of Months** {number_of_months}")


st.subheader("Dynamic Table")

# Generate months and quarters dynamically
start_date = datetime(2023, 1, 1)
months = [(start_date + timedelta(days=30 * i)).strftime("%B %Y") for i in range(number_of_months)]
quarters = [f"Q{(i // 3) + 1}" for i in range(number_of_months)]

# Create the table data
table_data = {
    "Month": months,
    "Quarter": quarters,
    "Termin Pro Woche": [termin_pro_woche] * number_of_months,
    "FTE": [amount_paid_to_employees * i for i in range(1,number_of_months+1)],
    "Cum Auftrage": [amount_earned_per_contract * i for i in range(1,number_of_months+1)]
}

# Create a DataFrame
df = pd.DataFrame(table_data)

# Display the DataFrame in Streamlit
st.dataframe(df)
