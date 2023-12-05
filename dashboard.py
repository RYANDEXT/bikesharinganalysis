import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from streamlit_lottie import st_lottie
from babel.numbers import format_currency



day_df = pd.read_csv("https://raw.githubusercontent.com/RYANDEXT/bikesharinganalysis/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/RYANDEXT/bikesharinganalysis/main/hour.csv")



min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

datetime_columns = ["dteday"]



st.header('Bike sharing Dashboard :sparkles:')

st.image("https://github.com/RYANDEXT/bikesharinganalysis/blob/main/BIKERENTAL.png")

st_lottie("https://lottie.host/8040c8da-06c9-4459-a388-3ec335afc51f/B9lqdA7XLw.json")

st.subheader('Monthly Bike Rent')
st.text("bicycle rental performance from January 2011 to December 2012")



for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

monthly_df = day_df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})
monthly_df.index = monthly_df.index.strftime('%Y-%m')
monthly_df = monthly_df.reset_index()
monthly_df.rename(columns={
    "cnt": "total_rental"
}, inplace=True)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_df["dteday"],
    monthly_df["total_rental"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)

total_rental_sum = monthly_df["total_rental"].sum()
ax.text(0.5, 1.05, f'Total Rental: {total_rental_sum}', transform=ax.transAxes,
        fontsize=14, color='black', ha='center')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)
plt.yticks(fontsize=10)
st.pyplot(fig)


st.subheader('Bike Rental Performance by Season')
st.text("bicycle rental performance by season from January 2011 to December 2012")
season_mapping = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
day_df['season'] = day_df['season'].replace(season_mapping)

byseason_df =  day_df.groupby(by="season").cnt.sum().reset_index()
byseason_df.rename(columns={
    "cnt": "rental_count"
}, inplace=True)

fig, ax = plt.subplots()
colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')
explode = (0.1, 0, 0, 0)
ax.pie(
    x=byseason_df['rental_count'],
    labels=byseason_df['season'],
    autopct='%1.1f%%',
    colors=colors,
    explode=explode
)

# Menampilkan pie chart menggunakan Streamlit
st.pyplot(fig)
