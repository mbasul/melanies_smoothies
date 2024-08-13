CH_ON# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie:')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# -------------------------------------------------------------------
res = my_dataframe.collect()
for R in res:
    F = R['SEARCH_ON']
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+F)
    st.write(F+str(fruityvice_response))

# -------------------------------------------------------------------
ingredients_list = st.multiselect(
    'Cooose up to 5 ingredients: '
    , my_dataframe
)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        st.subheader(fruit_choosen + ' Nutrition Informaton')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        my_insert_stmt = """ insert into smoothies.public.orders(NAME_ON_ORDER, INGREDIENTS)
            values ('""" + name_on_order + """', '"""+ ingredients_string + """')"""

        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

