import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns


# 1. Load and Pre-process Data (Logic from .ipynb)
@st.cache_data
def load_data():
    df = pd.read_csv('Students_Social_Media.csv')

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
selected_level = st.sidebar.multiselect("Select Academic Level:", options=df['Academic_Level'].unique(),
                                        default=df['Academic_Level'].unique())
platform_filter = st.sidebar.multiselect("Select Primary Platform:", options=df['Most_Used_Platform'].unique(),
                                         default=df['Most_Used_Platform'].unique())

# Filter data based on selection
filtered_df = df[
    (df['Gender'].isin(selected_gender)) &
    (df['Academic_Level'].isin(selected_level)) &
    (df['Most_Used_Platform'].isin(platform_filter))
    ]
# 3. Views / Visualizations (Based on Notebook EDA)
st.title("📱 Student Social Media Addiction Dashboard")


# View 3: Comparison - Addiction by Academic Level (Notebook Cell 15)
st.subheader("Addiction by Academic Level")
fig3 = px.box(filtered_df, x='Academic_Level', y='Addicted_Score', color='Academic_Level',
              title="Addiction Score Comparison")
st.plotly_chart(fig3, use_container_width=True)
