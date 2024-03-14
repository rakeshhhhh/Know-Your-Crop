from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

# Load your dataset (replace 'path_to_your_dataset.csv' with the actual path)
dataset = pd.read_csv('Crop_recommendation.csv')
X = dataset.drop('label', axis=1)  # Features
y = dataset['label']  # Target variable

print(X)
print(y)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier
model = RandomForestClassifier()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

joblib.dump(model, 'trained_random_forest_model.joblib')