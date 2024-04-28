from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import numpy as np
import joblib
import requests
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


@csrf_exempt
def fetch_sensor_data(request):
    # if request.method == 'POST':
    #     # Parse the JSON data from the POST request
    #     sensor_data = request.POST.get('data')  # Assuming the data is sent as a parameter named 'data'
    #
    #     # Process the sensor data (e.g., save it to the database)
    #     # Here, I'm just printing the data to the console for demonstration
    #     print("Received sensor data:", sensor_data)
    #
    #     # Send a response back to the ESP8266
    #     response_data = {'status': 'success'}
    #     return JsonResponse(response_data)
    # else:
    #     # Handle GET requests or other HTTP methods if needed
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)
    if request.method == 'GET':
        read_api_key = '7F7DGZ8JI4OVE8UO'
        url = f'https://api.thingspeak.com/channels/2491321/feeds.json?api_key={read_api_key}&results=1'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'feeds' in data and len(data['feeds']) > 0:
                latest_entry = data['feeds'][0]
                temperature = latest_entry.get('field1')
                humidity = latest_entry.get('field2')
                soil_moisture = latest_entry.get('field3')
                ph_value = latest_entry.get('field4')

                return JsonResponse({'temperature': temperature, 'humidity': humidity, 'soil_moisture': soil_moisture, 'ph_value': ph_value})
            else:
                return JsonResponse({'error': 'No data available'}, status=404)
        else:
            return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
