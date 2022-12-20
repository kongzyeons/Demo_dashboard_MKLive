import pandas as pd  # pip install pandas openpyxl
import numpy as np
import re
import os
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

df = pd.read_excel('dataset/MK Live_clean_Rev1.xlsm',sheet_name = 'MK Live_clean_Rev1',engine='openpyxl')
col = list(df.columns)
col_name = [df[i] for i in col]


st.set_page_config(page_title="MK LIVE Dashboard", page_icon="logo_mklive_2018.jpg", layout="wide")

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
sex = {k:v for k,v in col_name[78].value_counts().items() if v>1}
sex_ = st.sidebar.multiselect(
    "Select the sex:",
    options=sex.keys(),
    default=sex.keys()
)

age = col_name[79].value_counts()
age_ = st.sidebar.multiselect(
    "Select the age:",
    options=list(age.index),
    default=list(age.index)
)

status = col_name[83].value_counts()
status_ = st.sidebar.multiselect(
    "Select the status:",
    options=list(status.index),
    default=list(status.index)
)

degree = col_name[80].value_counts()
degree_ = st.sidebar.multiselect(
    "Select the degree:",
    options=list(degree.index),
    default=list(degree.index)
)


occupation = col_name[81].value_counts()
occupation_ = st.sidebar.multiselect(
    "Select the occupation:",
    options=list(occupation.index),
    default=list(occupation.index)
)

income = col_name[82].value_counts()
income_ = st.sidebar.multiselect(
    "Select the income:",
    options=list(income.index),
    default=list(income.index)
)

# df_selection = col_name.query(
#     "79==@age"
# )

# ---- MAINPAGE ----
st.title(":bar_chart: MK LIVE Dashboard")
st.markdown("##")

# fig_product_sales = px.bar(list(sex.values()), x=list(sex.keys()),y=list(sex.values()))

# fig_product_sales = px.bar(
#     list(sex.values()),
#     x=list(sex.keys()),
#     y=list(sex.values()),
#     # orientation="h",
#     title="<b>Sales by Product Line</b>",
#     template="plotly_white",
# )
sex = {k:v for k,v in col_name[78].value_counts().items() if v>1}
fig_sex = px.pie(list(sex.values()),
 values=list(sex.values()), 
 names=list(sex.keys()),
 title="<b>Number Sex</b>")
fig_sex.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

age = col_name[79].value_counts()
age = {k: v  for k, v in sorted(age.items(), key=lambda item: item[0][:2])}

fig_age = px.bar(
    list(age.keys()),
    x=list(age.keys()),
    y=list(age.values()),
    title="<b>Number Age</b>",
    template="plotly_white",
)
fig_age.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

status = col_name[83].value_counts()

fig_status = px.bar(
    list(age.keys()),
    x=list(age.keys()),
    y=list(age.values()),
    title="<b>Number Age</b>",
    template="plotly_white",
)
fig_status.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)






col1, col2,col3 = st.columns(3)
col1.plotly_chart(fig_sex, use_container_width=True)
col2.plotly_chart(fig_age, use_container_width=True)
col3.plotly_chart(fig_status, use_container_width=True)
