import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your dataset (replace 'path_to_your_dataset.csv' with the actual path)
dataset = pd.read_csv('Crop_recommendation.csv')

# Assuming your dataset contains features (temperature, humidity, soil_moisture, ph_value)
# and a target variable (crop)
# Extract features and target variable
X = dataset.drop('label', axis=1)
y = dataset['label']
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Save the trained model to a file using joblib
joblib.dump(model, 'trained_decision_tree_model.joblib')
joblib.dump(label_encoder, 'decisiontree_encoder.pkl')
