import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SuperKart Sales Forecaster", layout="wide")

st.title("🏪 SuperKart Sales Revenue Forecasting")
st.write("Welcome to SuperKart's predictive decision support tool. This application communicates with our containerized machine learning microservice to forecast sales.")

# Sidebar URL setup
BACKEND_URL = st.sidebar.text_input("Backend API Base URL", value="http://backend:7860")

tab1, tab2 = st.tabs(["🎯 Single-Item Online Prediction", "📊 Multi-Item Batch Prediction"])

with tab1:
    st.header("Single Product Sales Predictor")
    st.write("Provide the specific attributes of the product and store location below:")

    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight (kg)", min_value=0.1, max_value=50.0, value=12.5, step=0.1)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        allocated_area = st.number_input("Allocated Display Area Ratio", min_value=0.001, max_value=1.0, value=0.05, format="%.4f")
        product_mrp = st.number_input("Product Max Retail Price (MRP)", min_value=1.0, max_value=500.0, value=120.0, step=0.5)
        product_type_cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables", "Non Consumables"])

    with col2:
        store_size = st.selectbox("Store Size", ["Medium", "Low", "High"])
        city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
        product_char = st.selectbox("Product ID Category Code", ["FD", "DR", "NC"])
        store_age = st.number_input("Store Age (Years)", min_value=1, max_value=100, value=15, step=1)

    if st.button("Predict Sales Revenue"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar,
            "Product_Allocated_Area": allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": city_type,
            "Store_Type": store_type,
            "Product_Id_char": product_char,
            "Store_Age_Years": int(store_age),
            "Product_Type_Category": product_type_cat
        }

        try:
            response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Total Store Sales Revenue: ${result['predicted_sales']:,.2f}")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
        except Exception as e:
            st.error(f"Failed to connect to API server at {BACKEND_URL}. Exception: {e}")

with tab2:
    st.header("Bulk Batch Forecaster")
    st.write("Upload a standard CSV format file containing multiple product listings for bulk sales evaluation.")

    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Dataset Preview")
        st.dataframe(df.head())

        if st.button("Run Batch Inference"):
            files = {'file': uploaded_file.getvalue()}
            try:
                response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
                if response.status_code == 200:
                    predictions = response.json()
                    # Map predictions back to dataframe
                    df_pred = df.copy()
                    df_pred['Predicted_Sales_Total'] = df_pred.index.map(lambda x: predictions.get(str(x)))
                    st.subheader("Calculated Forecasting Results")
                    st.dataframe(df_pred)

                    # Download option
                    csv_to_download = df_pred.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Predictions as CSV", data=csv_to_download, file_name="superkart_forecasts.csv", mime="text/csv")
                else:
                    st.error(f"Batch Error: {response.json().get('error', 'Unknown batch error')}")
            except Exception as e:
                st.error(f"Failed to process batch or connect to {BACKEND_URL}. Exception: {e}")
