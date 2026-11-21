from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
import io

app = Flask(__name__)

# Load the serialized model pipeline
model_path = 'superkart_model.joblib'
model = joblib.load(model_path)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        # Read the single JSON data payload
        data = request.get_json(force=True)

        # Convert request dictionary into a single-row DataFrame
        df = pd.DataFrame([data])

        # Compute prediction
        prediction = model.predict(df)[0]

        return jsonify({"predicted_sales": float(prediction)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    try:
        # Verify if a file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read CSV file directly into a DataFrame
        stream = io.StringIO(file.stream.read().decode("UTF-8"))
        df = pd.read_csv(stream)

        # Perform batch prediction
        predictions = model.predict(df)

        # Format response as a key-value mapping of index -> prediction
        response_dict = {str(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(response_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
