# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title("\U0001F964 Customize Your Smoothie! \U0001F964")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get name input from user
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake using Streamlit's built-in connection (ensure it is configured correctly)
cnx = st.connection("Snowflake")
session = cnx.session()

# Fetch fruit options from the database
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
st.write("Available fruit options:")
st.dataframe(my_dataframe, use_container_width=True)

# Extract list of fruits for multiselect widget
fruit_options = my_dataframe['FRUIT_NAME'].tolist()

# Create multiselect for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    # Join the selected ingredients for SQL insertion
    ingredients_string = ', '.join(ingredients_list)

    # Display the SQL command for debugging purposes
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    st.write("SQL command to be executed:")
    st.code(my_insert_stmt, language='sql')

    # Button to submit the order
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            # Execute the insert command safely
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Make an API request and display response
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(f"API Response: {fruityvice_response}")
