import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set page config
st.set_page_config(page_title="Indigenous Data Analysis", layout="wide")

# Title
st.title("Indigenous Population Analysis - Canada 2022")

# Load data
@st.cache_data
def load_data():
    # Apunta a la carpeta Project Code
    csv_path = 'Project Code/4110008001_databaseLoadingData.csv'
    return pd.read_csv(csv_path)

try:
    data = load_data()
    
    # Data cleaning (mismo que en notebook)
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
        st.metric("Data Points", len(filtered_data))
    
    # Charts
    st.header("Visualizations")
    
    # Chart 1: Distribution by Indigenous Identity
    st.subheader("1. Distribution by Indigenous Identity")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", ax=ax)
    plt.title("Distribution")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Chart 2: By Gender
    st.subheader("2. Distribution by Gender")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Gender", ax=ax)
    plt.title("Distribution by Gender")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Chart 3: By Overall Health
    st.subheader("3. Distribution by Overall Health")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Overall health", ax=ax)
    plt.title("Distribution by Overall Health")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Chart 4: By Age Group
    st.subheader("4. Distribution by Age Group")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Age group", ax=ax)
    plt.title("Distribution by Age Group")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Chart 5: By Housing Needs
    st.subheader("5. Distribution by Housing - Needs Repairs")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Housing - Needs repairs", ax=ax)
    plt.title("Distribution by Housing - Needs Repairs")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Chart 6: By Crowding
    st.subheader("6. Distribution by Persons per Room (Crowding)")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(filtered_data, x="Indigenous identity", y="VALUE", hue="Persons per room (crowding)", ax=ax)
    plt.title("Distribution by Persons per Room (Crowding)")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    # Show raw data
    if st.checkbox("Show raw data"):
        st.dataframe(filtered_data)
    
    # Footer
    st.divider()
    st.markdown("*Data source: Statistics Canada - Indigenous Population Analysis 2022*")
    
except FileNotFoundError:
    st.error("❌ Error: No se encontró el archivo CSV. Asegúrate de que 'Project Code/4110008001_databaseLoadingData.csv' existe.")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
