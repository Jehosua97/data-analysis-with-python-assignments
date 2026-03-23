import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Set page config
st.set_page_config(page_title="Indigenous Data Analysis", layout="wide")

# Title
st.title("Indigenous Population Analysis - Canada 2022")

# Load data with better path handling
@st.cache_data
def load_data():
    # Intenta múltiples rutas posibles
    possible_paths = [
        'Project Code/4110008001_databaseLoadingData.csv',
        './Project Code/4110008001_databaseLoadingData.csv',
        os.path.join(os.path.dirname(__file__), 'Project Code/4110008001_databaseLoadingData.csv'),
        '4110008001_databaseLoadingData.csv',
    ]
    
    for csv_path in possible_paths:
        try:
            if os.path.exists(csv_path):
                st.write(f"✓ Archivo encontrado en: {csv_path}")
                return pd.read_csv(csv_path)
        except Exception as e:
            st.write(f"✗ Intento fallido en {csv_path}: {str(e)}")
            continue
    
    # Si nada funciona, muestra el directorio actual
    st.error(f"❌ No se pudo encontrar el CSV en ninguna ubicación")
    st.write(f"Directorio actual: {os.getcwd()}")
    st.write(f"Archivos disponibles:")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.csv'):
                st.write(f"  - {os.path.join(root, file)}")
    raise FileNotFoundError("CSV no encontrado")

try:
    data = load_data()
    
    # Verificar que data no esté vacío
    if len(data) == 0:
        st.error("❌ El archivo CSV está vacío")
    else:
        # Data cleaning
        data = data.drop(["TERMINATED", "SYMBOL", "DECIMALS", "SCALAR_ID", 
                           "SCALAR_FACTOR", "DGUID", "GEO", "REF_DATE"], axis=1)
        data = data.loc[data['Statistics'] == "Number of persons", :]
        data = data.loc[data['Indigenous identity'] != "Indigenous responses not included elsewhere"]
        
        # Sidebar filters
        st.sidebar.header("Filters")
        identities = data['Indigenous identity'].unique().tolist()
        selected_identity = st.sidebar.multiselect(
            "Indigenous Identity",
            identities,
            default=identities
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
                st.error(f"Error en gráfico 1: {str(e)}")
            
            # Chart 2: By Gender
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
                st.error(f"Error en gráfico 2: {str(e)}")
            
            # Chart 3: By Overall Health
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
                st.error(f"Error en gráfico 3: {str(e)}")
            
            # Chart 4: By Age Group
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
                st.error(f"Error en gráfico 4: {str(e)}")
            
            # Chart 5: By Housing Needs
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
                st.error(f"Error en gráfico 5: {str(e)}")
            
            # Chart 6: By Crowding
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
                st.error(f"Error en gráfico 6: {str(e)}")
            
            # Show raw data
            if st.checkbox("Show raw data"):
                st.dataframe(filtered_data)
        else:
            st.warning("No hay datos para mostrar con los filtros actuales")

except FileNotFoundError as e:
    st.error(f"❌ Error: {str(e)}")
except Exception as e:
    st.error(f"❌ Error inesperado: {str(e)}")
    import traceback
    st.write(traceback.format_exc())

# Footer
st.divider()
st.markdown("*Data source: Statistics Canada - Indigenous Population Analysis 2022*")

