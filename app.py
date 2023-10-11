import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
   page_title="水電瓦斯分帳",
   page_icon="🎉",
   layout="centered",
   initial_sidebar_state="expanded",
)

st.title("112-113年 水電瓦斯分帳")
# Define the names of the roommates
roommate_names = ["育瑄", "彥玗", "瑀娜", "垂恩"]

def update_water_bill(start, end, amount):
    data = {'people': roommate_names,
            'start_date': [start, start, start, start],
            'end_date': [end, end, end, end], 
            'water_bill': [amount/4, amount/4, amount/4, amount/4]
        }
    df = pd.DataFrame(data)
    st.write("水費")
    st.write(df)

# Add a button to add a new bill
# Ask the user for the bill details
start = st.date_input("輸入起始日期 (YYYY-MM-DD): ")
end = st.date_input("輸入結束日期 (YYYY-MM-DD): ")
amount = st.number_input("輸入金額: $")
    
add_water_button = st.button("新增新一期水費")
if add_water_button:
    # Update the bill amounts for each roommate
    data = {'people': roommate_names,
            'start_date': [start, start, start, start],
            'end_date': [end, end, end, end], 
            'water_bill': [amount/4, amount/4, amount/4, amount/4]
        }
    df = pd.DataFrame(data)
    st.write("水費")
    st.write(df)

    # Display the updated bill amounts
    df.to_csv("data.csv", index=False)
    st.write("結果已儲存!")