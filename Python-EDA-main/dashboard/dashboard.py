import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Load Data
@st.cache
def load_data():
    df_day = pd.read_csv('data/dataset/day.csv')
    df_hour = pd.read_csv('data/dataset/hour.csv')
    
    # Normalize column names
    df_day.columns = df_day.columns.str.strip().str.lower()
    df_hour.columns = df_hour.columns.str.strip().str.lower()

    # Convert date columns to datetime format
    df_day['dteday'] = pd.to_datetime(df_day['dteday'], errors='coerce')
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'], errors='coerce')

    return df_day, df_hour

df_day, df_hour = load_data()

# Sidebar Configuration
st.sidebar.header("Dashboard Configuration")

# Date Range Filter
date_min = df_day['dteday'].min()
date_max = df_day['dteday'].max()
selected_date_range = st.sidebar.date_input(
    "Select Date Range:",
    [date_min, date_max],
    min_value=date_min,
    max_value=date_max
)

# Filter data based on selected date range
df_day_filtered = df_day[(df_day['dteday'] >= pd.to_datetime(selected_date_range[0])) & 
                         (df_day['dteday'] <= pd.to_datetime(selected_date_range[1]))]
df_hour_filtered = df_hour[(df_hour['dteday'] >= pd.to_datetime(selected_date_range[0])) & 
                           (df_hour['dteday'] <= pd.to_datetime(selected_date_range[1]))]

view_option = st.sidebar.radio("Choose View:", ["Season & Weather Analysis", "Hourly Usage Analysis"])

# Season & Weather Analysis
if view_option == "Season & Weather Analysis":
    st.title("Season and Weather Impact on Bike Rentals")
    
    season_weather_data = df_day_filtered.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()
    
    season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    weather_map = {1: 'Clear/Partly Cloudy', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Ice'}
    season_weather_data['season'] = season_weather_data['season'].map(season_map)
    season_weather_data['weathersit'] = season_weather_data['weathersit'].map(weather_map)
    
    st.subheader("Average Bike Rentals by Weather Condition and Season")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=season_weather_data, x='season', y='cnt', hue='weathersit', palette='viridis', ax=ax)
    ax.set_title('Average Bike Rentals by Weather Condition and Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Average Bike Rentals')
    st.pyplot(fig)

# Hourly Usage Analysis
elif view_option == "Hourly Usage Analysis":
    st.title("Hourly Bike Rentals Analysis")
    df_hour_filtered['is_weekend'] = df_hour_filtered['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)
    hourly_usage = df_hour_filtered.groupby(['hr', 'is_weekend'])['cnt'].mean().reset_index()
    hourly_usage_pivot = hourly_usage.pivot(index='hr', columns='is_weekend', values='cnt')
    hourly_usage_pivot.columns = ['Weekday', 'Weekend']
    
    st.subheader("Hourly Bike Rentals (Weekday vs Weekend)")
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(data=hourly_usage_pivot, marker="o", ax=ax)
    ax.set_title('Hourly Bike Rentals Distribution')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Average Bike Rentals')
    ax.legend(['Weekday', 'Weekend'], title='Day Type')
    st.pyplot(fig)
    
    peak_weekday_hour = hourly_usage_pivot['Weekday'].idxmax()
    peak_weekend_hour = hourly_usage_pivot['Weekend'].idxmax()
    
    st.write(f"**Peak Hour on Weekdays:** {peak_weekday_hour}:00")
    st.write(f"**Peak Hour on Weekends:** {peak_weekend_hour}:00")

# Footer
st.caption("Dashboard created by Fitto Martcellindo")
