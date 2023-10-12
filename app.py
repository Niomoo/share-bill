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

roommate_names = ["育瑄", "彥玗", "垂恩", "瑀娜"]

st.subheader('用電度數')
record_df = pd.read_csv("record.csv")
st.dataframe(record_df)

st.subheader('電費計算')
electricity_df = pd.read_csv("electricity.csv")
st.dataframe(electricity_df)

st.subheader('本期費用')
bill_df = pd.read_csv("bill.csv")
st.dataframe(bill_df)

st.subheader('歷史費用')
summary_df = pd.read_csv("summary.csv")
st.dataframe(summary_df)

def calculate():
    new_date = pd.Timestamp.now().strftime("%Y-%m-%d")

    record_df = pd.read_csv("record.csv")
    money_per_kWh = round(st.session_state.electricity_amount / st.session_state.electricity_kWh,2)
    difference = [st.session_state.electricity_0 - record_df.iloc[-1, 1], 
                st.session_state.electricity_1 - record_df.iloc[-1, 2],
                st.session_state.electricity_2 - record_df.iloc[-1, 3],
                st.session_state.electricity_3 - record_df.iloc[-1, 4]
                ]
    electricity_df = pd.read_csv("electricity.csv")
    money = [difference[0] * money_per_kWh, difference[1] * money_per_kWh, difference[2] * money_per_kWh, difference[3] * money_per_kWh]
    share = round((st.session_state.electricity_amount - sum(money)) / 4, 2)
    electricity_bill = [money[0] + share, money[1] + share, money[2] + share, money[3] + share]

    new_electricity_record = [
        new_date,
        money_per_kWh,
        share,
        difference[0],
        electricity_bill[0],
        difference[1],
        electricity_bill[1],
        difference[2],
        electricity_bill[2],
        difference[3],
        electricity_bill[3],
    ]
    electricity_df.loc[len(electricity_df)] = new_electricity_record
    # Display the updated bill amounts
    electricity_df.to_csv("electricity.csv", index=False)

    new_record = [
        new_date,
        st.session_state.electricity_0,
        st.session_state.electricity_1,
        st.session_state.electricity_2,
        st.session_state.electricity_3,
    ]
    record_df.loc[len(record_df)] = new_record
    record_df.to_csv("record.csv", index=False)


    bill_df = pd.DataFrame(columns=['person', 'water', 'gas', 'electricity', 'total'])
    water = st.session_state.water_amount / 4
    gas = st.session_state.gas_amount / 4
    for i, name in enumerate(roommate_names):
        person = {}
        person['person'] = name
        person['water'] = water
        person['gas'] = gas
        person['electricity'] = electricity_bill[i]
        person['total'] = water + gas + electricity_bill[i]
        bill_df.loc[len(bill_df)] = person
    bill_df.to_csv("bill.csv", index=False)

    summary_df = pd.read_csv('summary.csv')
    new_summary = [
        new_date,
        st.session_state.water_start,
        st.session_state.water_end,
        st.session_state.water_amount,
        st.session_state.gas_start,
        st.session_state.gas_end,
        st.session_state.gas_amount,
        st.session_state.electricity_start,
        st.session_state.electricity_end,
        st.session_state.electricity_amount,
    ]
    summary_df.loc[len(summary_df)] = new_summary
    summary_df.to_csv("summary.csv", index=False)

# Add a button to add a new bill
# Ask the user for the bill details
btn = st.button("新增下一期費用")
if btn:
    with st.form("登記"):
        # Update the bill amounts
        st.subheader("水費")
        st.date_input("輸入水費起始日期 (YYYY-MM-DD): ", key = 'water_start')
        st.date_input("輸入水費結束日期 (YYYY-MM-DD): ", key = 'water_end')
        st.number_input("輸入水費金額: $", min_value=0, step=1, key = 'water_amount')

        st.subheader("瓦斯費")
        st.date_input("輸入瓦斯費起始日期 (YYYY-MM-DD): ", key = 'gas_start')
        st.date_input("輸入瓦斯費結束日期 (YYYY-MM-DD): ", key = 'gas_end')
        st.number_input("輸入瓦斯費金額: $", min_value=0, step=1, key = 'gas_amount')

        st.subheader("電費")
        st.date_input("輸入電費起始日期 (YYYY-MM-DD): ", key = 'electricity_start')
        st.date_input("輸入電費結束日期 (YYYY-MM-DD): ", key = 'electricity_end')
        st.number_input("輸入電費總金額: $", min_value=0, step=1, key = 'electricity_amount')
        st.number_input("輸入用電總度數: ", min_value=0, step=1, key = 'electricity_kWh')
        st.number_input(roommate_names[0] + "度數: ", min_value=0, step=1, key = 'electricity_0')
        st.number_input(roommate_names[1] + "度數: ", min_value=0, step=1, key = 'electricity_1')
        st.number_input(roommate_names[2] + "度數: ", min_value=0, step=1, key = 'electricity_2')
        st.number_input(roommate_names[3] + "度數: ", min_value=0, step=1, key = 'electricity_3')
        st.form_submit_button('送出!', on_click=calculate)
