import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Indigenous Data Analysis", layout="wide")

# Title
st.title("Indigenous Population Analysis - Canada 2022")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('4110008001_databaseLoadingData.csv')

data = load_data()

# Data cleaning (same as notebook)
data = data.drop(["TERMINATED", "SYMBOL", "DECIMALS", "SCALAR_ID", 
                   "SCALAR_FACTOR", "DGUID", "GEO", "REF_DATE"], axis=1)
data = data.loc[data['Statistics'] == "Number of persons", :]
data = data.loc[data['Indigenous identity'] != "Indigenous responses not included elsewhere"]

# Sidebar filters
st.sidebar.header("Filters")
selected_identity = st.sidebar.multiselect(
    "Indigenous Identity",
    data['Indigenous identity'].unique(),
    default=data['Indigenous identity'].unique()
)

filtered_data = data[data['Indigenous identity'].isin(selected_identity)]

# Display statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", len(filtered_data))
with col2:
    st.metric("Categories", filtered_data['Indigenous identity'].nunique())
with col3:
    st.metric("Years in Dataset", filtred_data['REF_DATE'].nunique() if 'REF_DATE' in filtered_data else 1)

# Charts
st.header("Visualizations")

# Chart 1
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", ax=ax)
plt.title("Distribution by Indigenous Identity")
st.pyplot(fig)

# Chart 2
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Gender", ax=ax)
plt.title("Distribution by Gender")
st.pyplot(fig)

# Chart 3
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Overall health", ax=ax)
plt.title("Distribution by Overall Health")
st.pyplot(fig)

# Show raw data
if st.checkbox("Show raw data"):
    st.dataframe(filtered_data)