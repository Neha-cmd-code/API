from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Get the correct file path
file_path = os.path.join(os.path.dirname(__file__), "Drug_data.csv")

# Load the CSV file
try:
    df = pd.read_csv(file_path, encoding="utf-8", delimiter=",")
except Exception as e:
    raise FileNotFoundError(f"❌ Error loading CSV file: {str(e)}")

# Route to get all data
@app.route('/drugs', methods=['GET'])
def get_all_drugs():
    return jsonify(df.to_dict(orient="records"))

# Route to get a drug by name
@app.route('/drug/<name>', methods=['GET'])
def get_drug_by_name(name):
    result = df[df["DrugName"].str.lower() == name.lower()]
    if result.empty:
        return jsonify({"error": "Drug not found"}), 404
    return jsonify(result.to_dict(orient="records"))

# Run the app with dynamic port assignment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use environment variable PORT
    print(f"✅ Running on port {port}")  # Print port number for debugging
    app.run(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 for external access
