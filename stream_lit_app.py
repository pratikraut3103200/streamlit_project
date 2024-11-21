import streamlit as st
import pandas as pd


# Title of the app
st.title("Calculation Tool")

# Creating a single row for input fields
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])


with col1:
    # Placeholder for the number of data rows
    total_rows = st.number_input(
        "Total Rows:",
        min_value=0,
        value=100,
        step=1
    )

with col2:
    # Dropdown for % of bad data
    bad_data_percentage = st.selectbox(
        "Bad Data %:",
        options=[0, 20, 40, 60, 80, 100],
        index=0
    )

with col3:
    # Input for amount paid to employees
    amount_paid_to_employees = st.number_input(
        "Amount Paid (in €):",
        min_value=0.0,
        step=1.0,
        value=0.0,
        format="%.2f"
    )

with col4:
    # Input for amount earned per contract
    amount_earned_per_contract = st.number_input(
        "Earned/Contract (in €):",
        min_value=0.0,
        step=1.0,
        value=0.0,
        format="%.2f"
    )

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


st.write(f"**Amount Paid to Employees:** €{amount_paid_to_employees:,.2f}")
st.write(f"**Amount Earned per Contract:** €{amount_earned_per_contract:,.2f}")


