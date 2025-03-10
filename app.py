import os
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Get the correct file path for the CSV file
file_path = os.path.join(os.path.dirname(__file__), "Drug_data.csv")

# Load the CSV file
try:
    df = pd.read_csv(file_path, encoding="utf-8")
    if "DrugName" not in df.columns:
        raise KeyError("❌ Error: 'DrugName' column is missing from CSV!")
except Exception as e:
    raise FileNotFoundError(f"❌ Error loading CSV file: {str(e)}")


# Route to get all data
@app.route('/drugs', methods=['GET'])
def get_all_drugs():
    return jsonify(df.to_dict(orient="records"))


# Route to get a drug by name (assuming a column 'DrugName' exists)
@app.route('/drug/<name>', methods=['GET'])
def get_drug_by_name(name):
    result = df[df["DrugName"].str.lower() == name.lower()]
    if result.empty:
        return jsonify({"error": "Drug not found"}), 404
    return jsonify(result.to_dict(orient="records"))


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT variable provided by Render
    app.run(host="0.0.0.0", port=port)
