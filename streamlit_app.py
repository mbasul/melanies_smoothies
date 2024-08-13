# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie:')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Cooose up to 5 ingredients: '
    , my_dataframe
)

if ingredients_list:
    ingredients_string = ''
    for f in ingredients_list:
        ingredients_string += f + ' '

    st.write(ingredients_string)
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(NAME_ON_ORDER, INGREDIENTS)
            values ('""" + name_on_order + """', '"""+ ingredients_string + """')"""

        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
