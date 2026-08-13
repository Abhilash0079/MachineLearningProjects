import streamlit as st
from prediction import predict_price

st.title("🏠 House Price Prediction")
st.write("Predict house prices using a Machine Learning model.")

# User Inputs
area = st.number_input("Area")
bedrooms = st.number_input("Bedrooms")
bathrooms = st.number_input("Bathrooms")
stories = st.number_input("Stories")
mainroad = st.selectbox("Main Road", [0,1])
guestroom = st.selectbox("Guest Room", [0,1])
basement = st.selectbox("Basement", [0,1])
hotwaterheating = st.selectbox("Hot Water Heating", [0,1])
airconditioning = st.selectbox("Air Conditioning", [0,1])
parking = st.number_input("Parking")
prefarea = st.selectbox("Preferred Area", [0,1])
furnishingstatus_semi_furnished = st.selectbox("Semi Furnished", [0,1])
furnishingstatus_unfurnished = st.selectbox("Unfurnished", [0,1])

# Prediction Button
if st.button("Predict Price"):
    input_data = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "mainroad": mainroad,
        "guestroom": guestroom,
        "basement": basement,
        "hotwaterheating": hotwaterheating,
        "airconditioning": airconditioning,
        "parking": parking,
        "prefarea": prefarea,
        "furnishingstatus_semi-furnished": furnishingstatus_semi_furnished,
        "furnishingstatus_unfurnished": furnishingstatus_unfurnished
    }

    prediction = predict_price(input_data)
    st.success(f"Predicted House Price: ₹ {prediction:,.2f}")

