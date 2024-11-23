import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset with diverse crops
data = {
    'Nitrogen': [90, 85, 60, 74, 78, 69, 69, 94, 89, 68, 45, 55],
    'Phosphorus': [42, 58, 55, 35, 42, 37, 55, 53, 54, 58, 60, 45],
    'Potassium': [43, 41, 44, 40, 42, 42, 38, 40, 38, 38, 35, 50],
    'Temperature': [20.88, 21.77, 23.00, 26.49, 20.13, 23.05, 22.71, 20.28, 24.52, 23.22, 19.00, 25.00],
    'Humidity': [82.00, 80.31, 82.32, 80.15, 81.60, 83.37, 82.64, 82.89, 83.54, 83.03, 81.42, 81.45],
    'pH_Value': [6.50, 7.03, 7.84, 6.98, 7.63, 7.07, 5.70, 5.72, 6.68, 6.34, 5.50, 6.00],
    'Rainfall': [202.93, 226.66, 263.96, 242.86, 262.72, 251.05, 271.32, 241.97, 230.45, 221.21, 180.00, 190.00],
    'Crop': ['Rice', 'Rice', 'Wheat', 'Wheat', 'Maize', 'Maize', 'Sugarcane', 'Sugarcane', 'Barley', 'Barley', 'Wheat', 'Maize']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Create a RandomForestClassifier
X = df[['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']]
y = df['Crop']
model = RandomForestClassifier()
model.fit(X, y)

# Streamlit App
st.title("Crop Recommendation System")

# Input fields
st.sidebar.header("Enter Soil and Weather Conditions")
input_data = {
    'Nitrogen': st.sidebar.slider("Nitrogen", 0, 100, 50),
    'Phosphorus': st.sidebar.slider("Phosphorus", 0, 100, 50),
    'Potassium': st.sidebar.slider("Potassium", 0, 100, 50),
    'Temperature': st.sidebar.slider("Temperature (\u00b0C)", 10.0, 50.0, 25.0),
    'Humidity': st.sidebar.slider("Humidity (%)", 0.0, 100.0, 50.0),
    'pH_Value': st.sidebar.slider("pH Value", 3.0, 10.0, 7.0),
    'Rainfall': st.sidebar.slider("Rainfall (mm)", 0.0, 300.0, 150.0)
}

# Convert input data to DataFrame
input_df = pd.DataFrame([input_data])

# Predict crop
prediction = model.predict(input_df)[0]
st.subheader("Recommended Crop")
st.write(f"**{prediction}**")

# Check for deficiencies
st.subheader("Parameter Analysis")
deficiencies = []
thresholds = {
    'Nitrogen': 90,
    'Phosphorus': 50,
    'Potassium': 40,
    'Temperature': 20.0,
    'Humidity': 80.0,
    'pH_Value': 6.5,
    'Rainfall': 200.0
}
for param, value in input_data.items():
    if value < thresholds[param]:
        deficiencies.append(f"{param} is below the optimal level ({value} < {thresholds[param]}).")

if deficiencies:
    for deficiency in deficiencies:
        st.write(deficiency)
else:
    st.write("All parameters are within the optimal range.")

# Alternative crop logic
st.subheader("Alternative Crop Suggestions")
X_without_predicted = df[df['Crop'] != prediction][['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH_Value', 'Rainfall']]
y_without_predicted = df[df['Crop'] != prediction]['Crop']

# Train a secondary model for alternative crops
alt_model = RandomForestClassifier()
alt_model.fit(X_without_predicted, y_without_predicted)

# Add a button to show the alternative crop
if st.button("Show Alternative Crop"):
    alternative_prediction = alt_model.predict(input_df)[0]
    st.write(f"**Alternative Crop:** {alternative_prediction}")
