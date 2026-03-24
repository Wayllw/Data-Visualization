import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

# 1. Load and Pre-process Data (Logic from .ipynb)
@st.cache_data
def load_data():
    df = pd.read_csv('Students Social Media Addiction.csv')
    
    # Feature Engineering: Age Groups (Notebook Cell 5)
    bins = [15, 20, 25, 30, 35]
    labels = ['16-20', '21-25', '26-30', '31-35']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    # Feature Engineering: Usage Category (Notebook Cell 6)
    usage_bins = [0, 2, 4, 6, 12, 24]
    usage_labels = ['Minimal (0-2h)', 'Moderate (2-4h)', 'High (4-6h)', 'Very High (6-12h)', 'Extreme (12h+)']
    df['Usage_Category'] = pd.cut(df['Avg_Daily_Usage_Hours'], bins=usage_bins, labels=usage_labels)
    
    return df

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Interactive Dashboard Filters")
selected_gender = st.sidebar.multiselect("Select Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_level = st.sidebar.multiselect("Select Academic Level:", options=df['Academic_Level'].unique(), default=df['Academic_Level'].unique())
platform_filter = st.sidebar.multiselect("Select Primary Platform:", options=df['Most_Used_Platform'].unique(), default=df['Most_Used_Platform'].unique())

# Filter data based on selection
filtered_df = df[
    (df['Gender'].isin(selected_gender)) & 
    (df['Academic_Level'].isin(selected_level)) &
    (df['Most_Used_Platform'].isin(platform_filter))
]
# 3. Views / Visualizations (Based on Notebook EDA)
st.title("📱 Student Social Media Addiction Dashboard")

col1, col2 = st.columns(2)

with col1:
    # View 1: Age Distribution (Notebook Cell 8)
    st.subheader("Student Age Distribution")
    fig1 = px.histogram(filtered_df, x='Age', nbins=15, title="Demographic Spread by Age")
    st.plotly_chart(fig1, use_container_width=True)

    # View 2: Platform Popularity (Notebook Cell 4 Value Counts)
    st.subheader("Most Used Platforms")
    platform_data = filtered_df['Most_Used_Platform'].value_counts().reset_index()
    fig2 = px.pie(platform_data, values='count', names='Most_Used_Platform', title="Market Share of Social Platforms")
    st.plotly_chart(fig2, use_container_width=True)

    # View 3: Comparison - Addiction by Academic Level (Notebook Cell 15)
    st.subheader("Addiction by Academic Level")
    fig3 = px.box(filtered_df, x='Academic_Level', y='Addicted_Score', color='Academic_Level', 
                  title="Addiction Score Comparison")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # View 4: Trend - Daily Usage vs. Addiction Score (Notebook Cell 16)
    st.subheader("Usage Hours vs Addiction Trend")
    fig4 = px.scatter(filtered_df, x='Avg_Daily_Usage_Hours', y='Addicted_Score', trendline="ols",
                      title="Correlation: Daily Hours vs Addiction")
    st.plotly_chart(fig4, use_container_width=True)

    # View 5: Sleep Impact (Notebook Cell 16 Heatmap Logic)
    st.subheader("Sleep Hours vs Addiction")
    fig5 = px.density_heatmap(filtered_df, x='Sleep_Hours_Per_Night', y='Addicted_Score', 
                               title="Heatmap: Sleep Deprivation vs Addiction")
    st.plotly_chart(fig5, use_container_width=True)

    # View 6: Geospatial Distribution (Notebook Cell 4 Countries)
    st.subheader("Survey Participants by Country")
    country_data = filtered_df['Country'].value_counts().reset_index()
    fig6 = px.choropleth(country_data, locations="Country", locationmode='country names', color="count",
                         title="Global Survey Reach")
    st.plotly_chart(fig6, use_container_width=True)

# Key Metrics Table (Based on Summary Stats in Cell 3)
st.divider()
st.subheader("Key Statistics Table")
st.dataframe(filtered_df[['Avg_Daily_Usage_Hours', 'Addicted_Score', 'Mental_Health_Score', 'Sleep_Hours_Per_Night']].describe())