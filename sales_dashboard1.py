import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import calendar

# File uploader widget
uploaded_file = st.sidebar.file_uploader(
    "Upload an Excel File (.xlsx):",
    type=["xlsx"]
)

if uploaded_file:
    try:
        # Read Excel file into a DataFrame
        buffer = io.BytesIO(uploaded_file.read())
        df = pd.read_excel(buffer)
        
        # Get available columns
        available_columns = df.columns.tolist()

        # Allow user to select columns for visualizations
        st.sidebar.subheader("Customize Visualizations")
        x_col = st.sidebar.selectbox("X-Axis Column (Categorical):", available_columns)
        y_col = st.sidebar.selectbox("Y-Axis Column (Numerical):", available_columns)
        date_col = st.sidebar.selectbox("Date Column (Optional):", ["None"] + available_columns)

        # Clean and prepare data
        df = df[[x_col, y_col]].dropna()
        df[y_col] = pd.to_numeric(df[y_col], errors='coerce')

        # Display the dashboard
        st.title("Dynamic Sales Dashboard")

        # Bar Chart
        st.subheader("Bar Chart")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x_col, y=y_col, data=df)
        st.pyplot(plt)

        # Trend Over Time
        if date_col != "None":
            st.subheader("Trend Over Time")
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.groupby([pd.Grouper(key=date_col, freq='M')])[y_col].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.lineplot(x=date_col, y=y_col, data=df)
            plt.xticks(rotation=45)
            st.pyplot(plt)

        # Top Items
        st.subheader("Top Items")
        top_items = df.groupby(x_col)[y_col].sum().reset_index().sort_values(y_col, ascending=False).head(5)
        st.table(top_items)

        # Summary Statistics
        st.subheader("Summary Statistics")
        st.table(df.describe())

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("Upload an Excel file to start visualizing data!")