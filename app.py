import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Configure page settings
st.set_page_config(page_title="Indigenous Data Analysis", layout="wide")

# Page title
st.title("Indigenous Population Analysis - Canada 2022")

# Load data with multiple path fallbacks for deployment
@st.cache_data
def load_data():
    # Try multiple possible paths to find the CSV file
    possible_paths = [
        'Project Code/4110008001_databaseLoadingData.csv',
        './Project Code/4110008001_databaseLoadingData.csv',
        os.path.join(os.path.dirname(__file__), 'Project Code/4110008001_databaseLoadingData.csv'),
        '4110008001_databaseLoadingData.csv',
    ]
    
    for csv_path in possible_paths:
        try:
            if os.path.exists(csv_path):
                st.write(f"✓ File found at: {csv_path}")
                return pd.read_csv(csv_path)
        except Exception as e:
            st.write(f"✗ Attempt failed at {csv_path}: {str(e)}")
            continue
    
    # If no file found, display debugging information
    st.error(f"❌ Could not find CSV file in any location")
    st.write(f"Current directory: {os.getcwd()}")
    st.write(f"Available files:")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.csv'):
                st.write(f"  - {os.path.join(root, file)}")
    raise FileNotFoundError("CSV file not found")

try:
    data = load_data()
    
    # Verify that data is not empty
    if len(data) == 0:
        st.error("❌ CSV file is empty")
    else:
        # Clean data by removing unnecessary columns
        data = data.drop(["TERMINATED", "SYMBOL", "DECIMALS", "SCALAR_ID", 
                           "SCALAR_FACTOR", "DGUID", "GEO", "REF_DATE"], axis=1)
        data = data.loc[data['Statistics'] == "Number of persons", :]
        data = data.loc[data['Indigenous identity'] != "Indigenous responses not included elsewhere"]
        
        # Add sidebar filters
        st.sidebar.header("Filters")
        identities = data['Indigenous identity'].unique().tolist()
        selected_identity = st.sidebar.multiselect(
            "Indigenous Identity",
            identities,
            default=identities
        )
        
        filtered_data = data[data['Indigenous identity'].isin(selected_identity)]
        
        # Display key statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(filtered_data))
        with col2:
            st.metric("Categories", filtered_data['Indigenous identity'].nunique())
        with col3:
            st.metric("Data Points", len(filtered_data))
        
        # Create visualizations section
        st.header("Visualizations")
        
        if len(filtered_data) > 0:
            # Chart 1: Distribution by Indigenous Identity
            st.subheader("1. Distribution by Indigenous Identity")
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                chart_data = filtered_data.groupby("Indigenous identity")["VALUE"].mean()
                chart_data.plot(kind='bar', ax=ax, color='steelblue')
                ax.set_title("Average VALUE by Indigenous Identity")
                ax.set_xlabel("Indigenous Identity")
                ax.set_ylabel("VALUE")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error in chart 1: {str(e)}")
            
            # Chart 2: Distribution by Gender
            st.subheader("2. Distribution by Gender")
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                pivot_data = filtered_data.pivot_table(values='VALUE', index='Indigenous identity', columns='Gender', aggfunc='mean')
                pivot_data.plot(kind='bar', ax=ax)
                ax.set_title("Average VALUE by Indigenous Identity and Gender")
                ax.set_xlabel("Indigenous Identity")
                ax.set_ylabel("VALUE")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error in chart 2: {str(e)}")
            
            # Chart 3: Distribution by Overall Health
            st.subheader("3. Distribution by Overall Health")
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                pivot_data = filtered_data.pivot_table(values='VALUE', index='Indigenous identity', columns='Overall health', aggfunc='mean')
                pivot_data.plot(kind='bar', ax=ax)
                ax.set_title("Average VALUE by Indigenous Identity and Overall Health")
                ax.set_xlabel("Indigenous Identity")
                ax.set_ylabel("VALUE")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error in chart 3: {str(e)}")
            
            # Chart 4: Distribution by Age Group
            st.subheader("4. Distribution by Age Group")
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                pivot_data = filtered_data.pivot_table(values='VALUE', index='Indigenous identity', columns='Age group', aggfunc='mean')
                pivot_data.plot(kind='bar', ax=ax)
                ax.set_title("Average VALUE by Indigenous Identity and Age Group")
                ax.set_xlabel("Indigenous Identity")
                ax.set_ylabel("VALUE")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error in chart 4: {str(e)}")
            
            # Chart 5: Distribution by Housing - Needs Repairs
            st.subheader("5. Distribution by Housing - Needs Repairs")
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                pivot_data = filtered_data.pivot_table(values='VALUE', index='Indigenous identity', columns='Housing - Needs repairs', aggfunc='mean')
                pivot_data.plot(kind='bar', ax=ax)
                ax.set_title("Average VALUE by Indigenous Identity and Housing - Needs Repairs")
                ax.set_xlabel("Indigenous Identity")
                ax.set_ylabel("VALUE")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error in chart 5: {str(e)}")
            
            # Chart 6: Distribution by Persons per Room (Crowding)
            st.subheader("6. Distribution by Persons per Room (Crowding)")
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                pivot_data = filtered_data.pivot_table(values='VALUE', index='Indigenous identity', columns='Persons per room (crowding)', aggfunc='mean')
                pivot_data.plot(kind='bar', ax=ax)
                ax.set_title("Average VALUE by Indigenous Identity and Crowding")
                ax.set_xlabel("Indigenous Identity")
                ax.set_ylabel("VALUE")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            except Exception as e:
                st.error(f"Error in chart 6: {str(e)}")
            
            # Display raw data table
            if st.checkbox("Show raw data"):
                st.dataframe(filtered_data)
        else:
            st.warning("No data available with the current filters")

except FileNotFoundError as e:
    st.error(f"❌ Error: {str(e)}")
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")
    import traceback
    st.write(traceback.format_exc())

# Footer
st.divider()
st.markdown("*Data source: Statistics Canada - Indigenous Population Analysis 2022*")

