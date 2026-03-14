"""
Loan Approval Prediction System - Model Training Script
Generates synthetic dataset, preprocesses, trains 3 models, saves best model.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ─── 1. Generate Synthetic Loan Dataset ────────────────────────────────────────
np.random.seed(42)
n = 1000

genders         = np.random.choice(['Male', 'Female'], n, p=[0.80, 0.20])
married         = np.random.choice(['Yes', 'No'], n, p=[0.65, 0.35])
dependents      = np.random.choice(['0', '1', '2', '3+'], n, p=[0.57, 0.17, 0.16, 0.10])
education       = np.random.choice(['Graduate', 'Not Graduate'], n, p=[0.78, 0.22])
self_employed   = np.random.choice(['Yes', 'No'], n, p=[0.14, 0.86])
applicant_inc   = np.random.randint(1500, 81000, n)
coapplicant_inc = np.random.choice([0, 1000, 2000, 3000, 4000, 5000], n,
                                   p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05])
loan_amount     = np.random.randint(30, 700, n)
loan_term       = np.random.choice([12, 36, 60, 84, 120, 180, 240, 300, 360, 480], n)
credit_history  = np.random.choice([1.0, 0.0], n, p=[0.84, 0.16])
property_area   = np.random.choice(['Urban', 'Semiurban', 'Rural'], n, p=[0.38, 0.38, 0.24])

# Determine loan status with logic-driven probability
def loan_status(credit, income, loan_amt):
    base = 0.55
    if credit == 1.0:
        base += 0.30
    if income > 5000:
        base += 0.10
    if loan_amt < 150:
        base += 0.05
    return np.random.choice(['Y', 'N'], p=[min(base, 0.95), max(1 - base, 0.05)])

loan_status_col = [loan_status(credit_history[i], applicant_inc[i], loan_amount[i])
                   for i in range(n)]

df = pd.DataFrame({
    'Gender':            genders,
    'Married':           married,
    'Dependents':        dependents,
    'Education':         education,
    'Self_Employed':     self_employed,
    'ApplicantIncome':   applicant_inc,
    'CoapplicantIncome': coapplicant_inc,
    'LoanAmount':        loan_amount,
    'Loan_Amount_Term':  loan_term,
    'Credit_History':    credit_history,
    'Property_Area':     property_area,
    'Loan_Status':       loan_status_col
})

# Introduce ~5% missing values in key columns for realism
for col in ['Gender', 'Married', 'Dependents', 'Self_Employed', 'LoanAmount', 'Credit_History']:
    mask = np.random.rand(n) < 0.05
    df.loc[mask, col] = np.nan

df.to_csv('loan_data.csv', index=False)
print(f"✅ Dataset generated: {len(df)} records saved to loan_data.csv")

# ─── 2. Preprocessing ──────────────────────────────────────────────────────────
df = pd.read_csv('loan_data.csv')

# Fill missing values
df['Gender'].fillna('Male', inplace=True)
df['Married'].fillna('Yes', inplace=True)
df['Dependents'].fillna('0', inplace=True)
df['Self_Employed'].fillna('No', inplace=True)
df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
df['Loan_Amount_Term'].fillna(360, inplace=True)
df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)

categorical_cols = ['Gender', 'Married', 'Dependents', 'Education',
                    'Self_Employed', 'Property_Area', 'Loan_Status']

encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

print("✅ Preprocessing complete. Encodings:")
for col, le in encoders.items():
    if col != 'Loan_Status':
        print(f"   {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# ─── 3. Train / Test Split ─────────────────────────────────────────────────────
X = df.drop('Loan_Status', axis=1)
y = df['Loan_Status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ─── 4. Train Models ───────────────────────────────────────────────────────────
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree':       DecisionTreeClassifier(max_depth=6, random_state=42),
    'Random Forest':       RandomForestClassifier(n_estimators=100, random_state=42),
}

results = {}
print("\n📊 Model Training Results:")
print("-" * 40)
for name, model in models.items():
    model.fit(X_train, y_train)
    preds   = model.predict(X_test)
    acc     = accuracy_score(y_test, preds)
    results[name] = {'model': model, 'accuracy': acc}
    print(f"  {name:<25}: {acc*100:.2f}%")

# ─── 5. Select Best Model ──────────────────────────────────────────────────────
best_name = max(results, key=lambda k: results[k]['accuracy'])
best_model = results[best_name]['model']
print(f"\n🏆 Best Model: {best_name} ({results[best_name]['accuracy']*100:.2f}%)")

# ─── 6. Save Artifacts ─────────────────────────────────────────────────────────
os.makedirs('model', exist_ok=True)

with open('model/best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Save encoders + feature columns + model accuracies
meta = {
    'encoders':       encoders,
    'feature_cols':   list(X.columns),
    'best_model_name': best_name,
    'accuracies': {k: round(v['accuracy'] * 100, 2) for k, v in results.items()},
}
with open('model/encoders.pkl', 'wb') as f:
    pickle.dump(meta, f)

print("\n✅ Model saved  → model/best_model.pkl")
print("✅ Metadata saved → model/encoders.pkl")
print("\n🚀 Run  python app.py  to start the web application.")
