import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(r"C:\Users\sakth\healthcare-ai-ar-system\healthcare_claims_dataset_100k.csv")

print("Dataset Loaded Successfully")
print("Dataset shape:", df.shape)
print(df.head())


# -----------------------------
# Remove ID columns
# -----------------------------
df.drop(columns=["claim_id", "patient_id"], errors="ignore", inplace=True)


# -----------------------------
# Remove leakage columns
# -----------------------------
leakage_cols = [
    "priority_score",
    "risk_score",
    "collection_priority",
    "claim_status",
    "days_in_ar",
    "ar_bucket"
]

df.drop(columns=leakage_cols, errors="ignore", inplace=True)


# -----------------------------
# Handle Missing Values
# -----------------------------
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
df[categorical_cols] = df[categorical_cols].fillna("Unknown")


# -----------------------------
# Feature Engineering
# -----------------------------
if {"claim_amount","payment_received"}.issubset(df.columns):
    df["payment_gap"] = df["claim_amount"] - df["payment_received"]

if {"days_in_ar","last_followup_days"}.issubset(df.columns):
    df["followup_gap"] = df["days_in_ar"] - df["last_followup_days"]


# -----------------------------
# Encode Target Variable
# -----------------------------
target_encoder = LabelEncoder()
df["priority_label"] = target_encoder.fit_transform(df["priority_label"])


# -----------------------------
# Encode Categorical Features
# -----------------------------
encoders = {}

categorical_cols = df.select_dtypes(include=["object","category"]).columns

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    encoders[col] = le


# -----------------------------
# Define Features & Target
# -----------------------------
X = df.drop(columns=["priority_label"])
y = df["priority_label"]

feature_columns = X.columns


# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)


# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# -----------------------------
# Model Evaluation
# -----------------------------
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# -----------------------------
# Feature Importance
# -----------------------------
importance = pd.Series(model.feature_importances_, index=feature_columns)

print("\nTop Important Features:")
print(importance.sort_values(ascending=False).head(10))


# -----------------------------
# Create model directory
# -----------------------------
os.makedirs("model", exist_ok=True)


# -----------------------------
# Save Model & Metadata
# -----------------------------
pickle.dump(model, open("model/claim_priority_model.pkl","wb"))
pickle.dump(encoders, open("model/encoders.pkl","wb"))
pickle.dump(target_encoder, open("model/target_encoder.pkl","wb"))
pickle.dump(feature_columns, open("model/feature_columns.pkl","wb"))

print("\nModel and encoders saved successfully!")