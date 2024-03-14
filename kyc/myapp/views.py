from django.shortcuts import render
from django.http import HttpResponse
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def index(request):
    return render(request, 'myapp/index.html')


def predict(request):
    if request.method == 'POST':
        temperature = float(request.POST['temperature'])
        humidity = float(request.POST['humidity'])
        moisture_level = float(request.POST['soil_moisture'])
        ph_value = float(request.POST['ph_value'])

        # Example decision tree model
        #X = np.array([[temperature, humidity, soil_moisture, ph_value]])
        # Load your trained model here
        model = joblib.load('kyc/trained_decision_tree_model.joblib')
        label_encoder = joblib.load('kyc/decisiontree_encoder.pkl')
        # predicted_crop = model.predict(X)
        # Replace this with actual logic based on your trained model
        user_input = pd.DataFrame([[temperature, ph_value, humidity, moisture_level]],
                                  columns=['temperature', 'humidity', 'ph', 'water availability'])
        predicted_crop = model.predict(user_input)

        #predicted_crop = "Wheat"  # Placeholder
        user_input_encoded = user_input.copy()
        user_input_encoded['label'] = 0
        user_input_encoded['label'] = label_encoder.transform(['rice'])[0]

        predicted_crop_encoded = model.predict(user_input_encoded.drop('label', axis=1))

        # Convert the predicted label back to the original class
        predicted_crop = label_encoder.inverse_transform(predicted_crop_encoded)

        #print(f'\nThe predicted crop for the given soil factors is: {predicted_crop[0]}')

        return HttpResponse(f"Predicted crop: {predicted_crop[0]}")
    else:
        return HttpResponse("Invalid request")
