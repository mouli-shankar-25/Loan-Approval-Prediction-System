# 🏦 LoanAI — Loan Approval Prediction System

> An AI-powered web application that predicts whether a loan application will be **Approved ✅ or Rejected ❌** using three machine learning models — served via a modern Flask web interface.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?logo=flask)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Working-brightgreen)

---

## 📌 Project Overview

This project demonstrates a complete **end-to-end Machine Learning pipeline**:

1. **Data Generation** — Synthetic loan dataset (1000 records)
2. **Preprocessing** — Handle missing values, encode categoricals
3. **Model Training** — Compare Logistic Regression, Decision Tree, Random Forest
4. **Best Model Selection** — Auto-selects highest accuracy model
5. **Web Deployment** — Flask-based web app for real-time prediction

---

## 🚀 Quick Start

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Train the ML Model
```bash
python train_model.py
```
**Output:**
```
✅ Dataset generated: 1000 records saved to loan_data.csv
✅ Preprocessing complete.

📊 Model Training Results:
----------------------------------------
  Logistic Regression      : 94.00%
  Decision Tree            : 93.50%
  Random Forest            : 94.00%

🏆 Best Model: Logistic Regression (94.00%)
✅ Model saved  → model/best_model.pkl
✅ Metadata saved → model/encoders.pkl

🚀 Run  python app.py  to start the web application.
```

### Step 3 — Run the Web App
```bash
python app.py
```

### Step 4 — Open in Browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
loan web/
│
├── app.py                  ← Flask backend (routes & prediction logic)
├── train_model.py          ← ML pipeline (data → train → save)
├── requirements.txt        ← Python dependencies
├── loan_data.csv           ← Auto-generated synthetic dataset
│
├── model/
│   ├── best_model.pkl      ← Saved best ML model (pickle)
│   └── encoders.pkl        ← Label encoders + model metadata
│
├── templates/
│   ├── index.html          ← Loan application form (home page)
│   ├── result.html         ← Prediction result (Approved / Rejected)
│   └── about.html          ← Model accuracy comparison page
│
└── static/
    ├── css/
    │   └── style.css       ← Dark glassmorphic UI styles
    └── js/
        └── main.js         ← Form validation & animations
```

---

## 🤖 Machine Learning Models

| Model | Type | Accuracy |
|---|---|---|
| 📈 Logistic Regression | Linear Classifier | ~94% |
| 🌳 Decision Tree | Rule-based (max_depth=6) | ~93.5% |
| 🌲 Random Forest | 100 Decision Trees Ensemble | ~94% |

> The model with the **highest test accuracy is automatically selected** and saved.

---

## 🔍 Features Used for Prediction (11 Input Fields)

| Feature | Type | Description |
|---|---|---|
| Gender | Categorical | Male / Female |
| Married | Categorical | Yes / No |
| Dependents | Categorical | 0, 1, 2, 3+ |
| Education | Categorical | Graduate / Not Graduate |
| Self_Employed | Categorical | Yes / No |
| ApplicantIncome | Numeric | Monthly income (₹) |
| CoapplicantIncome | Numeric | Co-applicant income (₹) |
| LoanAmount | Numeric | Requested amount (in thousands ₹) |
| Loan_Amount_Term | Numeric | Repayment duration (months) |
| Credit_History | Binary | 1.0 = Good, 0.0 = Poor |
| Property_Area | Categorical | Urban / Semiurban / Rural |

---

## 🌐 Web Application Pages

| URL | Page | Description |
|---|---|---|
| `/` | Home | Loan application input form |
| `/predict` | Result | Shows Approved / Rejected + confidence % |
| `/about` | About | Model accuracy comparison + ML pipeline |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Data | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Web Framework | Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Model Storage | Pickle (.pkl) |

---

## 📊 Data Preprocessing Steps

1. **Fill missing values** — Mode/median imputation for categorical and numeric columns
2. **Label Encoding** — Convert Gender, Married, Dependents, Education, Self_Employed, Property_Area, Loan_Status to numeric
3. **Train-Test Split** — 80% training / 20% testing
4. **Model Evaluation** — Accuracy score on held-out test set

---

## 💡 Example Prediction

**Input:**
- Graduate, Married, 0 Dependents, Not Self-Employed
- Income: ₹5,000/month, Co-income: ₹2,000
- Loan: ₹150K, Term: 360 months, Credit: Good, Area: Semiurban

**Output:**
```
✅ Loan Approved!  — Confidence: 90.9%  (Logistic Regression)
```

---

## 🔁 Re-training the Model

If you want to regenerate data and retrain:
```bash
python train_model.py
```
Then restart the Flask app:
```bash
python app.py
```

---

## 📄 License

This project is for **educational purposes** — Machine Learning course project.

---

*Built with ❤️ using Python · Scikit-learn · Flask*
