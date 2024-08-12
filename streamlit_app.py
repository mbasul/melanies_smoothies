# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

option = st.selectbox(
    "What is your favorite fruit?",
    ("Banana", "Strawberries", "Peaches"),
    index=None,
    placeholder="Select contact method...",
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Cooose up to 5 ingredients: '
    , my_dataframe
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    for f in ingredients_list:
        ingredients_string += f + ' '

    #st.write(ingredients_string)
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
