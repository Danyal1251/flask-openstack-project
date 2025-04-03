import os
import numpy as np
import joblib
from flask import Flask, render_template, request, redirect, url_for, flash
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import check_is_fitted

import pickle
app = Flask(__name__)
app.secret_key = "secret123"  # Required for flash messages

# File Upload Config
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Try loading the model
try:
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)

try:
    check_is_fitted(model)
    print("Model is properly trained and loaded!")
except Exception as e:
    print(" Model is NOT trained! You need to retrain.")

#  Dummy dataset for training
X_train, X_test, y_train, y_test = train_test_split(
    np.random.rand(100, 5),  # 100 samples, 5 features
    np.random.choice([0, 1], 100),  # Binary classification (0 or 1)
    test_size=0.2,
    random_state=42
)

#  Load or Train Model
if os.path.exists("model\model.pkl"):
    model = joblib.load("model\model.pkl")
else:
    model = make_pipeline(StandardScaler(), SVC(probability=True))
    model.fit(X_train, y_train)  #  Train model
    joblib.dump(model, MODEL_PATH)  # Save model


@app.route('/')
def home():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash(" No file part in request", "danger")
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        flash(" No file selected!", "danger")
        return redirect(url_for('home'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash(f" File '{file.filename}' uploaded successfully!", "success")

    return redirect(url_for('home'))


@app.route('/predict', methods=['POST'])
def predict():
    file_name = request.form.get('file_name')
    if not file_name:
        flash(" No file selected for prediction!", "danger")
        return redirect(url_for('home'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    if not os.path.exists(file_path):
        flash(" File not found!", "danger")
        return redirect(url_for('home'))

    #  Generate Random Data (Assume 5 Features for Prediction)
    sample_data = np.random.rand(1, 5)

    #  Ensure Model is Trained Before Predicting
    if not hasattr(model, "predict"):
        flash(" Model is not trained yet!", "danger")
        return redirect(url_for('home'))

    prediction = model.predict(sample_data)
    flash(f' Prediction for {file_name}: {prediction[0]}', "success")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
