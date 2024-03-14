from django.shortcuts import render
from django.http import JsonResponse

import numpy as np
import joblib
import pandas as pd



def index(request):
    return render(request, 'myapp/index.html')


def predict(request):
    if request.method == 'POST':
        temperature = float(request.POST['temperature'])
        humidity = float(request.POST['humidity'])
        moisture_level = float(request.POST['soil_moisture'])
        ph_value = float(request.POST['ph_value'])

        model = joblib.load('kyc/trained_random_forest_model.joblib')

        user_input = pd.DataFrame([[temperature, humidity, ph_value, moisture_level]],
                                  columns=['temperature', 'humidity', 'ph', 'water availability'])

        # Make prediction for user input
        predicted_crop = model.predict(user_input)

        # print(f'\nThe predicted crop for the given soil factors is: {predicted_crop[0]}')

        return JsonResponse({'predicted_crop': predicted_crop[0]})
    else:
        return JsonResponse({'error': 'Invalid request'})
