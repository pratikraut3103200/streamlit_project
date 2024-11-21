import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("Multiplication Table Generator")

# # Slider for selecting a value
# selected_value = st.slider(
#     "Select a number to generate its multiplication table:",
#     min_value=1,
#     max_value=20,
#     value=1
# )

# # Generate the multiplication table
# def generate_multiplication_table(number, up_to=10):
#     data = {"Multiplier": range(1, up_to + 1),
#             "Result": [number * i for i in range(1, up_to + 1)]}
#     df = pd.DataFrame(data)
#     return df

# # Display the table based on the selected value
# st.write(f"Multiplication Table for {selected_value}:")
# multiplication_table = generate_multiplication_table(selected_value)
# st.dataframe(multiplication_table)
