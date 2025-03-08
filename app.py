from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Get the correct file path for the dataset
file_path = os.path.join(os.path.dirname(__file__), "Drug_data.csv")

# Load the CSV file safely
try:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ CSV file not found: {file_path}")

    df = pd.read_csv(file_path)
except Exception as e:
    print(f"❌ Error: {e}")
    df = None  # Prevents app crash if file is missing


# Route to get all drug data
@app.route('/drugs', methods=['GET'])
def get_all_drugs():
    if df is None:
        return jsonify({"error": "Data not available"}), 500
    return jsonify(df.to_dict(orient="records"))


# Route to get a drug by name (assuming a column 'DrugName' exists)
@app.route('/drug/<name>', methods=['GET'])
def get_drug_by_name(name):
    if df is None:
        return jsonify({"error": "Data not available"}), 500

    # Ensure column exists
    if "DrugName" not in df.columns:
        return jsonify({"error": "Column 'DrugName' not found in dataset"}), 500

    result = df[df["DrugName"].str.lower() == name.lower()]
    if result.empty:
        return jsonify({"error": "Drug not found"}), 404
    return jsonify(result.to_dict(orient="records"))


# Run the app (for local testing)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
