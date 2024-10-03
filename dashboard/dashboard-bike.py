import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function for prepared dataframe

def create_hourly_share_df(df):
    hourly_share_df = df.groupby(by='hour').agg({'count': ['sum']})
    hourly_share_df = hourly_share_df.reset_index()
    hourly_share_df.columns = ['hour', 'count']
    return hourly_share_df

def create_daily_share_df(df):
    daily_share_df = df.groupby(by='day').agg({'count': ['sum']})
    daily_share_df = daily_share_df.reset_index()
    return daily_share_df

def create_monthly_share_df(df):
    monthly_share_df = df.groupby(by='month').agg({'count': ['sum']})
    monthly_share_df = monthly_share_df.reset_index()
    return monthly_share_df

def create_yearly_share_df(df):
    yearly_share_df = df.groupby(by='year').agg({'count': ['sum']})
    yearly_share_df = yearly_share_df.reset_index()
    return yearly_share_df

def create_byregristered_df(df):
    byregristered_df= df.groupby(by='registered').agg({'registered': ['sum']})
    byregristered_df = byregristered_df.reset_index()
    return byregristered_df

def create_bycasual_df(df):
    bycasual_df= df.groupby(by='casual').agg({'casual': ['sum']})
    bycasual_df = bycasual_df.reset_index()
    return bycasual_df

def create_byseason_df(df):
    byseason_df = df.groupby(by='season').agg({'count': ['sum']})
    byseason_df = byseason_df.reset_index()
    return byseason_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by='weathersit').agg({'count': ['sum']})
    byweathersit_df = byweathersit_df.reset_index()
    return byweathersit_df


def create_rfm_df(df):
    rfm_df = df.groupby(by="registered", as_index=False).agg({
        "date": "max", 
        "instant": "count",
        "count": "sum"
    })
    rfm_df.columns = ["registered", "max_share_timestamp", "frequency", "monetary"]

    rfm_df["max_share_timestamp"] = rfm_df["max_share_timestamp"].dt.date
    recent_date = df["date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_share_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_share_timestamp", axis=1, inplace=True)
    
    return rfm_df


# Load cleaned data
cleaned_df = pd.read_csv("cleaned_bikesharing_hour.csv")

datetime_columns = ["date"]
cleaned_df.sort_values(by="date", inplace=True)
cleaned_df.reset_index(inplace=True)

for column in datetime_columns:
    cleaned_df[column] = pd.to_datetime(cleaned_df[column])


# Filter data
min_date = cleaned_df["date"].min()
max_date = cleaned_df["date"].max()

with st.sidebar:
    # Add icon
    st.image("https://github.com/melyavy/assets/raw/main/man-biking.png")
    
    # start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = cleaned_df[(cleaned_df["date"] >= str(start_date)) & (cleaned_df["date"] <= str(end_date))]

# st.dataframe(main_df)


# Prepare Dataframe
hourly_share_df = create_hourly_share_df(main_df)
daily_share_df = create_daily_share_df(main_df)
monthly_share_df = create_monthly_share_df(main_df)
yearly_share_df = create_yearly_share_df(main_df)
byregristered_df = create_byregristered_df(main_df)
bycasual_df = create_bycasual_df(main_df)
byseason_df = create_byseason_df(main_df)
byweathersit_df = create_byweathersit_df(main_df)
rfm_df = create_rfm_df(main_df)


# Plot number of daily share 
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Daily Share')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["date"],
    main_df["count"],
    # marker='o', 
    # linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


# Change dtypes
hourly_share_df['count'] = pd.to_numeric(hourly_share_df['count'], errors='coerce')
hourly_share_df['hour'] = hourly_share_df['hour'].astype(str)

# Hour performance
st.subheader("Best & Worst Bike Sharing Hour")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="count", y="hour", data=hourly_share_df.nlargest(5, 'count'), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Count", fontsize=15)  # Beri label untuk sumbu x
ax[0].set_title("Best Bike Sharing Hour", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(x="count", y="hour", data=hourly_share_df.nsmallest(5, 'count'), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Count", fontsize=15)  # Beri label untuk sumbu x
ax[1].invert_xaxis()  # Invert untuk membalik sumbu x
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Bike Sharing Hour", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)


# Bike Sharing Demographics
st.subheader("Bike Sharing Demographics")

col1, col2 = st.columns(2)

byseason_df.columns = ['season', 'count']

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="count", 
        x="season",
        data=byseason_df.sort_values(by="count", ascending=False), 
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

byweathersit_df.columns = ['weathersit', 'count']

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="count", 
        x="weathersit",
        data=byweathersit_df.sort_values(by="count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Bike Sharing by Weather Situation", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


# Registered and casual
st.subheader("Registered and Casual Users")

byregristered_df.columns = ['registered', 'count']
bycasual_df.columns = ['casual', 'count']

total_registered = byregristered_df['count'].sum()
total_casual = bycasual_df['count'].sum()

labels = ['Registered', 'Casual']
sizes = [total_registered, total_casual]
colors = ['#FF9999', '#66B3FF']  

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax.axis('equal') 

plt.title('Distribution of Registered vs Casual Users', fontsize=16)

st.pyplot(fig)


# Best Regristrated Based on RFM Parameters
st.subheader("Best Registered Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = round(rfm_df.monetary.mean(), 3)
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="registered", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("registered", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="registered", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("registered", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="registered", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("registered", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

st.caption('by: Melya Vebryanti')

st.caption('Copyright © Dicoding 2023')