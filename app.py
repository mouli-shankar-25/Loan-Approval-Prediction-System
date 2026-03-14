"""
Loan Approval Prediction System - Flask Web Application
"""

import os
import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# ─── Load model & metadata ─────────────────────────────────────────────────────
MODEL_PATH    = os.path.join('model', 'best_model.pkl')
METADATA_PATH = os.path.join('model', 'encoders.pkl')

model    = None
metadata = None

def load_artifacts():
    global model, metadata
    if not os.path.exists(MODEL_PATH):
        return False
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.load(f)
    return True

artifacts_loaded = load_artifacts()

# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if not artifacts_loaded:
        return render_template('index.html',
                               error="⚠️ Model not found. Please run train_model.py first.")

    encoders     = metadata['encoders']
    feature_cols = metadata['feature_cols']

    try:
        # --- Raw form values ---
        gender         = request.form['gender']
        married        = request.form['married']
        dependents     = request.form['dependents']
        education      = request.form['education']
        self_employed  = request.form['self_employed']
        applicant_inc  = float(request.form['applicant_income'])
        coapplicant_inc = float(request.form['coapplicant_income'])
        loan_amount    = float(request.form['loan_amount'])
        loan_term      = float(request.form['loan_term'])
        credit_history = float(request.form['credit_history'])
        property_area  = request.form['property_area']

        # --- Encode categoricals ---
        def encode(col, val):
            le = encoders[col]
            if val in le.classes_:
                return le.transform([val])[0]
            return le.transform([le.classes_[0]])[0]   # fallback

        features = [
            encode('Gender',        gender),
            encode('Married',       married),
            encode('Dependents',    dependents),
            encode('Education',     education),
            encode('Self_Employed', self_employed),
            applicant_inc,
            coapplicant_inc,
            loan_amount,
            loan_term,
            credit_history,
            encode('Property_Area', property_area),
        ]

        input_array = np.array(features).reshape(1, -1)
        prediction  = model.predict(input_array)[0]        # 0 = N, 1 = Y
        proba       = model.predict_proba(input_array)[0]

        approved      = bool(encoders['Loan_Status'].inverse_transform([prediction])[0] == 'Y')
        confidence    = round(float(proba[prediction]) * 100, 1)

        applicant_data = {
            'Gender': gender, 'Married': married, 'Dependents': dependents,
            'Education': education, 'Self Employed': self_employed,
            'Applicant Income': f'₹{applicant_inc:,.0f}',
            'Co-applicant Income': f'₹{coapplicant_inc:,.0f}',
            'Loan Amount': f'₹{loan_amount:,.0f} thousand',
            'Loan Term': f'{int(loan_term)} months',
            'Credit History': 'Good' if credit_history == 1.0 else 'Poor',
            'Property Area': property_area,
        }

        return render_template(
            'result.html',
            approved=approved,
            confidence=confidence,
            applicant_data=applicant_data,
            best_model=metadata.get('best_model_name', 'ML Model'),
        )

    except Exception as e:
        return render_template('index.html', error=f"❌ Error: {str(e)}")


@app.route('/about')
def about():
    accs = {}
    bm   = 'Unknown'
    if artifacts_loaded:
        accs = metadata.get('accuracies', {})
        bm   = metadata.get('best_model_name', 'Unknown')
    return render_template('about.html', accuracies=accs, best_model=bm)


if __name__ == '__main__':
    if not artifacts_loaded:
        print("⚠️  WARNING: Model not found.")
        print("   Please run:  python train_model.py")
        print("   Then restart the app.")
    else:
        bm  = metadata.get('best_model_name', 'N/A')
        acc = metadata.get('accuracies', {}).get(bm, 'N/A')
        print(f"✅ Model loaded: {bm} ({acc}%)")
    print("\n🌐 Starting Flask server → http://127.0.0.1:5000\n")
    app.run(debug=True)
