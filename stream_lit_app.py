import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta
import plotly.graph_objects as go


# Set page configuration
st.set_page_config(page_title="Calculation Tool", layout="wide")

# Title of the app
st.title("Calculation Tool")

# Input fields
st.subheader("Input Parameters")
left_col, right_col = st.columns(2)

# Left column: Group related inputs
with left_col:
    total_rows = st.number_input("Total Rows:", min_value=0, value=100, step=1)
    bad_data_percentage = st.selectbox("Bad Data %:", options=[0, 20, 40, 60, 80, 100], index=0)

    min_termin_in_start = st.number_input("Min Termin in Start:", min_value=1, value=3, step=1)
    conversion_rate_zu_verkauf = st.number_input("Conversion Rate to Sales (%)", min_value=0, value=20, step=1)

# Right column: Group related financial inputs
with right_col:

    amount_paid_to_employees = st.number_input("FTE (€):", min_value=0.0, step=1.0, value=5000.0, format="%.2f")
    amount_earned_per_contract = st.number_input("Auftrageswelt(€):", min_value=0.0, step=1.0, value=800.0, format="%.2f")
    termin_pro_woche = st.number_input("Termin per Week:", min_value=1, step=1, value=4)
    number_of_months = st.number_input("Number of Months:", min_value=2, step=1, value=24)

# Calculation for data quality
if total_rows > 0:
    bad_rows = int((bad_data_percentage / 100) * total_rows)
    good_rows = total_rows - bad_rows
else:
    bad_rows, good_rows = 0, 0



value = 12 - ((bad_data_percentage/100) * 12)

# Apply the conditional logic
if value % 1 < 0.5:  # Equivalent to REST(...;1)<0.5
    termin_possible_data = math.floor(value)  # Equivalent to GANZZAHL(...)
else:
    termin_possible_data = math.ceil(value)
# Data metrics in column format
st.subheader("Data Quality Metrics")
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.write(f"**Good Data %:** {100 - bad_data_percentage}%")
    st.write(f"**Number of Good Rows:** {good_rows}")
    st.write(f"**Number of Bad Rows:** {bad_rows}")

with metric_col2:
    st.write(f"**Geplannte Termin pro Woche bezogen auf Good Data:** {termin_possible_data}")
    st.write(f"**Sales per week:** {math.floor(termin_pro_woche * (conversion_rate_zu_verkauf / 100))}")
    st.write(f"**Sales per Month:** {math.floor(termin_pro_woche * 4 * (conversion_rate_zu_verkauf/100))}")


# Generate months and quarters dynamically
start_date = datetime(2023, 1, 1)
months = [(start_date + timedelta(days=31 * i)).strftime("%B %Y") for i in range(number_of_months)]
quarters = [f"Q{(i // 3) + 1}" for i in range(number_of_months)]

termin_pro_monat_calculated = termin_pro_woche * 4 * (conversion_rate_zu_verkauf / 100)

termin_pro_monat = []
for i in range(number_of_months):
    if i < 2:
        value = min_termin_in_start
    else:
        increase = (termin_pro_monat_calculated - min_termin_in_start) / (number_of_months - 2)
        value = min_termin_in_start + increase * (i - 1)
    termin_pro_monat.append(round(value))

# Create the table data
table_data = {
    "Month": months,
    "Quarter": quarters,
    "Termin per Month": termin_pro_monat,
    "FTE": [amount_paid_to_employees * i for i in range(1, number_of_months + 1)],
    "Auftrage from All Customers": [amount_earned_per_contract * i for i in termin_pro_monat]
}

# Create a DataFrame
df = pd.DataFrame(table_data)
df["Cumulative Auftrage"] = df["Auftrage from All Customers"].cumsum()

# Debug toggle
st.subheader("Table Debugging")
debug_toggle = st.checkbox("Show Table")

if debug_toggle:
    st.dataframe(df)

# Plotly Graphs
st.subheader("Visualizations")

# Create a single y-axis line chart
fig = go.Figure()

# Add the FTE line
fig.add_trace(go.Scatter(
    x=df["Month"],
    y=df["FTE"],
    mode='lines',
    name='FTE',
    line=dict(color='grey')
))

# Add the Cumulative Auftrage line
fig.add_trace(go.Scatter(
    x=df["Month"],
    y=df["Cumulative Auftrage"],
    mode='lines',
    name='Cumulative Auftrage',
    line=dict(color='green')
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
