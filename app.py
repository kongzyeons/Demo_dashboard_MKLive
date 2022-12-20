import pandas as pd  # pip install pandas openpyxl
import numpy as np
import re
import os
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit




df = pd.read_excel('dataset/MK Live_clean_Rev1_clean.xlsx',sheet_name = 'Sheet1',engine='openpyxl')
col = list(df.columns)
col_name = [df[i] for i in col]




st.set_page_config(page_title="MK LIVE Dashboard", page_icon="logo_mklive_2018.jpg", layout="wide")

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
sex = st.sidebar.multiselect(
    "Select the Sex:",
    options=df[col[0]].unique(),
    default=df[col[0]].unique()
)

age = st.sidebar.multiselect(
    "Select the Age:",
    options=sorted(df[col[1]].unique()),
    default=sorted(df[col[1]].unique())
)

income = st.sidebar.multiselect(
    "Select the Income:",
    options=sorted(df[col[2]].unique()),
    default=sorted(df[col[2]].unique())
)

status = st.sidebar.multiselect(
    "Select the Status:",
    options=df[col[3]].unique(),
    default=df[col[3]].unique()
)

how_many = st.sidebar.multiselect(
    "Select the how many:",
    options=sorted(df[col[4]].unique()),
    default=sorted(df[col[4]].unique())
)

with_who = st.sidebar.multiselect(
    "Select the with who:",
    options=sorted(df[col[5]].unique()),
    default=sorted(df[col[5]].unique())
)




st.title(":bar_chart: MK LIVE Dashboard Demo")
st.markdown("##")

##score avg
score = pd.read_excel('dataset/MK Live_clean_Rev1.xlsm',sheet_name = 'MK Live_clean_Rev1',engine='openpyxl')
col_score = list(score.columns)
average_rating = round(score[col_score[62]].dropna().mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
avg_column, = st.columns(1)
with avg_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating}/10 : {star_rating}")
st.markdown("""---""")





df_selection = df[(df[col[0]].isin(sex)) & (df[col[1]].isin(age))
                    & (df[col[2]].isin(income)) & (df[col[3]].isin(status))
                    & (df[col[4]].isin(how_many)) & (df[col[5]].isin(with_who))]
st.dataframe(df_selection)

st.markdown("##")
st.subheader("Visualization:")
st.markdown("""---""")


#General
st.subheader('General Information')

sex = df_selection[col[0]].value_counts()
sex = {k:v for k,v in sex.items()}
fig_sex = px.pie(list(sex.values()),
 values=list(sex.values()), 
 names=list(sex.keys()),
 title="<b>Total by Sex</b>")
fig_sex.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

age = df_selection[col[1]].value_counts()
sum_age = sum([v for v in age.values])
age = {k: 100*v/sum_age  for k, v in sorted(age.items(), key=lambda item: item[0][:2])}
fig_age = px.bar(
    list(age.keys()),
    x=list(age.keys()),
    y=list(age.values()),
    title="<b>Total by Age</b>",
    template="plotly_white",
)
fig_age.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Age", yaxis_title="Total (persent %)"
)

income = df_selection[col[2]].value_counts()
sum_income = sum(income)
income_ = {k: 100*v/sum_income  for k, v in sorted(income.items(), key=lambda item: item[0][:2]) if v!=1}
income = {k: 100*v/sum_income  for k, v in sorted(income.items(), key=lambda item: item[0][:2]) if v==1}
for k,v in income_.items():
  income[k] = v
fig_income = px.bar(
    list(income.keys()),
    y=list(income.keys()),
    x=list(income.values()),
    title="<b>Total by Income</b>",
    template="plotly_white",
    color_discrete_sequence=["#E8AB31"]
    ,orientation='h'
)
fig_income.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title="Income", xaxis_title="Total (persent %)"
)
with st.container():
    col1, col2,col3 = st.columns(3)
    col1.plotly_chart(fig_sex, use_container_width=True)
    col2.plotly_chart(fig_age, use_container_width=True)
    col3.plotly_chart(fig_income, use_container_width=True)



with_who = df_selection[col[5]].value_counts()
with_who = {k:v for k,v in with_who.items()}
layout = go.Layout(title='<b>Total by with who</b>')
fig_with_who = go.Figure(data=[go.Pie(labels=list(with_who.keys()), values=list(with_who.values()), hole=.3)],layout=layout)
fig_with_who.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

status = df_selection[col[3]].value_counts()
status = {k:v for k,v in status.items()}
fig_status = px.pie(list(status.values()),
 values=list(status.values()), 
 names=list(status.keys()),color_discrete_sequence=["#FD6262"],
 title="<b>Total by Status</b>")
fig_status.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


how_many = df_selection[col[4]].value_counts()
sum_how_many = sum(how_many)
how_many = {k: 100*v/sum_how_many  for k, v in sorted(how_many.items(), key=lambda item: item[0][:2])}

fig_how_many = px.bar(
    list(how_many.keys()),
    y=list(how_many.keys()),
    x=list(how_many.values()),
    title="<b>Total by how many</b>",
    template="plotly_white",
    color_discrete_sequence=["#5DCB89"]
    ,orientation='h'
)
fig_how_many.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title="how many", xaxis_title="Total (persent %)"
)

with st.container():
    col1, col2,col3 = st.columns(3)
    col1.plotly_chart(fig_with_who, use_container_width=True)
    col2.plotly_chart(fig_status, use_container_width=True)
    col3.plotly_chart(fig_how_many, use_container_width=True)

st.markdown("""---""")

#Feature
st.subheader('Feature Information')

df_feture = df_selection[df_selection[col[6]]!="อื่นๆ"]
Feature = df_feture[col[6]].value_counts()
sum_Feature = sum([v for v in Feature.values])
Feature = {k: 100*v/sum_Feature  for k, v in sorted(Feature.items(), key=lambda item: item[1],reverse=True)}
fig_Feature = px.bar(
    list(Feature.keys()),
    x=list(Feature.keys()),
    y=list(Feature.values()),
    title="<b>ปัจจัยที่สำคัญที่สุดปัจจัยใด ที่จะทำให้ท่านสนใจทดลองรับประทานอาหารที่ร้าน MK Live</b>",
    template="plotly_white",
    color_discrete_sequence=["#F5A671"]
)
fig_Feature.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Feature", yaxis_title="Total (persent %)"
)
st.plotly_chart(fig_Feature, use_container_width=True)


value_money = df_selection[col[7]].value_counts()
sum_value_money = sum([v for v in value_money.values])
value_money = {k: 100*v/sum_value_money  for k, v in sorted(value_money.items(), key=lambda item: item[1])}
fig_value_money = px.bar(
    list(value_money.keys()),
    y=list(value_money.keys()),
    x=list(value_money.values()),
    title="<b>ในด้านความคุ้มค่าต่อราคาที่จ่าย</b>",
    template="plotly_white",
    color_discrete_sequence=["#F64646"],
    orientation='h'
)
fig_value_money.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title="value_money", xaxis_title="Total (persent %)"
)

travel = df_selection[col[8]].value_counts()
sum_travel = sum([v for v in travel.values])
travel = {k: 100*v/sum_travel  for k, v in sorted(travel.items(), key=lambda item: item[1])}
fig_travel = px.bar(
    list(travel.keys()),
    y=list(travel.keys()),
    x=list(travel.values()),
    title="<b>ในด้านความสะดวกสบายในการเดินทาง</b>",
    template="plotly_white",
    color_discrete_sequence=["#61E166"],
    orientation='h'
)
fig_travel.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title="travel", xaxis_title="Total (persent %)"
)

qulity = df_selection[col[9]].value_counts()
sum_qulity = sum([v for v in qulity.values])
qulity = {k: 100*v/sum_qulity  for k, v in sorted(qulity.items(), key=lambda item: item[1])}
fig_qulity = px.bar(
    list(qulity.keys()),
    y=list(qulity.keys()),
    x=list(qulity.values()),
    title="<b>ในด้านคุณภาพและรสชาติของอาหาร</b>",
    template="plotly_white",
    color_discrete_sequence=["#61BBE1"],
    orientation='h'
)
fig_qulity.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title="qulity", xaxis_title="Total (persent %)"
)

with st.container():
    col1, col2,col3 = st.columns(3)
    col1.plotly_chart(fig_value_money, use_container_width=True)
    col2.plotly_chart(fig_travel, use_container_width=True)
    col3.plotly_chart(fig_qulity, use_container_width=True)



promotion = df_selection[col[10]].value_counts()
promotion = {k:v for k,v in promotion.items()}
fig_promotion = px.pie(list(promotion.values()),
 values=list(promotion.values()), 
 names=list(promotion.keys()),color_discrete_sequence=px.colors.sequential.RdBu,
 title="<b>โปรโมชั่น เเละการส่งเสริมการตลาด</b>")
fig_promotion.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

environment = df_selection[col[11]].value_counts()
environment = {k:v for k,v in environment.items()}
fig_environment = px.pie(list(environment.values()),
 values=list(environment.values()), 
 names=list(environment.keys()),color_discrete_sequence=px.colors.sequential.Aggrnyl,
 title="<b>บรรยากาศร้าน</b>")
fig_environment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

with st.container():
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_promotion, use_container_width=True)
    col2.plotly_chart(fig_environment, use_container_width=True)



service = df_selection[col[12]].value_counts()
service = {k:v for k,v in service.items()}
layout = go.Layout(title='<b>การบริการ และคุณภาพการบริการ</b>')
fig_service = go.Figure(data=[go.Pie(labels=list(service.keys()), values=list(service.values()), hole=.3)],layout=layout)
fig_service.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

ref = df_selection[col[13]].value_counts()
ref = {k:v for k,v in ref.items()}
layout = go.Layout(title='<b>การบอกต่อจากบุคคลอ้างอิง</b>')
fig_ref = go.Figure(data=[go.Pie(labels=list(ref.keys()), values=list(ref.values()), hole=.3)],layout=layout)
fig_ref.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

with st.container():
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_service, use_container_width=True)
    col2.plotly_chart(fig_ref, use_container_width=True)

st.markdown("""---""")

#Why do you like MK Live?
st.subheader('Why do you like MK Live?')

df_like = df_selection[df_selection[col[14]]!="อื่นๆ"]
Like = df_like[col[14]].value_counts()
sum_Like = sum([v for v in Like.values])
Like = {k: 100*v/sum_Like  for k, v in sorted(Like.items(), key=lambda item: item[1],reverse=True)}
fig_Like = px.bar(
    list(Like.keys()),
    x=list(Like.keys()),
    y=list(Like.values()),
    title="<b>ท่านชอบ MK Live เพราะสาเหตุใด</b>",
    template="plotly_white",
    color_discrete_sequence=["#73D176"]
)
fig_Like.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Like", yaxis_title="Total (persent %)"
)
st.plotly_chart(fig_Like, use_container_width=True)


material = df_selection[col[15]].value_counts()
material = {k:v for k,v in material.items()}
layout = go.Layout(title='<b>วัตถุดิบประเภทใด ที่ท่านชื่นชอบมากที่สุดเมื่อรับประทานสุกี้</b>')
fig_material = go.Figure(data=[go.Pie(labels=list(material.keys()), values=list(material.values()), hole=.3)],layout=layout)
fig_material.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

other_foods = df_selection[col[16]].value_counts()
other_foods = {k:v for k,v in other_foods.items()}
layout = go.Layout(title='<b>วัตถุดิบประเภทใด ที่ท่านชื่นชอบมากที่สุดเมื่อรับประทานสุกี้</b>')
fig_other_foods = go.Figure(data=[go.Pie(labels=list(other_foods.keys()), values=list(other_foods.values()), hole=.3)],layout=layout)
fig_other_foods.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

with st.container():
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_material, use_container_width=True)
    col2.plotly_chart(fig_other_foods, use_container_width=True)


#improve or develop
st.subheader('Improve or Develop')

df_edit = df_selection[df_selection[col[17]]!="อื่นๆ"]
edit = df_edit[col[17]].value_counts()
sum_edit = sum([v for v in edit.values])
edit = {k: 100*v/sum_edit  for k, v in sorted(edit.items(), key=lambda item: item[1],reverse=True)}
fig_edit = px.bar(
    list(edit.keys()),
    x=list(edit.keys()),
    y=list(edit.values()),
    title="<b>ท่านคิดว่า MK Live ควรปรับปรุงหรือพัฒนาในด้านใดมากที่สุด</b>",
    template="plotly_white",
    color_discrete_sequence=["#F04C67"]
)
fig_edit.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Like", yaxis_title="Total (persent %)"
)
st.plotly_chart(fig_edit, use_container_width=True)
st.markdown("""---""")

#branch
st.subheader('Branch')

df_branch = df_selection[df_selection[col[18]]!="อื่นๆ"]
branch = df_branch[col[18]].value_counts()
sum_branch = sum([v for v in branch.values])
branch = {k: 100*v/sum_branch  for k, v in sorted(branch.items(), key=lambda item: item[1],reverse=True)}
fig_branch = px.bar(
    list(branch.keys()),
    x=list(branch.keys()),
    y=list(branch.values()),
    title="<b>ท่านเคยรับประทาน MK Live ที่สาขาใดบ้าง</b>",
    template="plotly_white",
    color_discrete_sequence=["#C0D459"]
)
fig_branch.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Like", yaxis_title="Total (persent %)"
)
st.plotly_chart(fig_branch, use_container_width=True)
st.markdown("""---""")



###Price
st.subheader('Price')

price = df_selection[col[19]].value_counts()
sum_price = sum(price)
price_ = {k: 100*v/sum_price  for k, v in sorted(price.items(), key=lambda item: item[0][:2]) if k!="น้อยกว่า 100 บาทต่อคน"}
price = {k: 100*v/sum_price  for k, v in sorted(price.items(), key=lambda item: item[0][:2]) if k=="น้อยกว่า 100 บาทต่อคน"}
for k,v in price_.items():
  price[k] = v
fig_price = px.bar(
    list(price.keys()),
    y=list(price.keys()),
    x=list(price.values()),
    title="<b>ราคาต่อหัว เมื่อท่านรับประทานสุกี้เป็นราคาประมาณเท่าใด</b>",
    template="plotly_white",
    color_discrete_sequence=["#E8AB31"]
    ,orientation='h'
)
fig_price.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title="price", xaxis_title="Total (persent %)"
)

Type = df_selection[col[20]].value_counts()
Type = {k:v for k,v in Type.items()}
fig_Type = px.pie(list(Type.values()),
 values=list(Type.values()), 
 names=list(Type.keys()),
 title="<b>Type</b>")
fig_Type.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

with st.container():
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_price, use_container_width=True)
    col2.plotly_chart(fig_Type, use_container_width=True)
st.markdown("""---""")




st.subheader('Frequency')

time = df_selection[col[21]].value_counts()
sum_time = sum([v for v in time.values])
time =  {k: 100*v/sum_time  for k, v in sorted(time.items(), key=lambda item: item[0][:2])}
fig_time = px.bar(
    list(time.keys()),
    x=list(time.keys()),
    y=list(time.values()),
    title="<b>ท่านมักรับประทานสุกี้ในช่วงเวลาใด</b>",
    template="plotly_white",
    color_discrete_sequence=["#7CA7D2"]
)
fig_time.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Time", yaxis_title="Total (persent %)"
)



df_freq = df_selection[df_selection[col[22]]!="อื่นๆ"]
freq = df_freq[col[22]].value_counts()
sum_freq = sum([v for v in freq.values])
freq = {k: 100*v/sum_freq  for k, v in sorted(freq.items(), key=lambda item: item[1],reverse=True)}
fig_freq = px.bar(
    list(freq.keys()),
    x=list(freq.keys()),
    y=list(freq.values()),
    title="<b>ท่านรับประทาน MK Live บ่อยเพียงใด</b>",
    template="plotly_white",
    color_discrete_sequence=["#DEB060"]
)
fig_freq.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title="Like", yaxis_title="Total (persent %)"
)

with st.container():
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_time, use_container_width=True)
    col2.plotly_chart(fig_freq, use_container_width=True)
st.markdown("""---""")