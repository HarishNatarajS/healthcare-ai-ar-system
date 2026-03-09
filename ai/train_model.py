import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


print("Loading dataset...")

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("../dataset/healthcare_claims_dataset_100k.csv")

print("Dataset loaded:", df.shape)


# -----------------------------
# Remove useless columns
# -----------------------------
df = df.drop(columns=["claim_id", "patient_id"], errors="ignore")


# -----------------------------
# Feature engineering
# -----------------------------
df["payment_gap"] = df["claim_amount"] - df["payment_received"]


# -----------------------------
# Handle missing values
# -----------------------------
df = df.fillna("Unknown")


# -----------------------------
# Encode target variable
# -----------------------------
target_encoder = LabelEncoder()
df["priority_label"] = target_encoder.fit_transform(df["priority_label"])


# -----------------------------
# Define features and target
# -----------------------------
X = df.drop(columns=["priority_label"])
y = df["priority_label"]


# -----------------------------
# Detect column types
# -----------------------------
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()


# Ensure categorical columns are strings
for col in categorical_cols:
    X[col] = X[col].astype(str)


# -----------------------------
# Preprocessing pipeline
# -----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols)
    ]
)


# -----------------------------
# Machine Learning Pipeline
# -----------------------------
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(
        n_estimators=120,
        max_depth=15,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])


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


print("Training model...")

pipeline.fit(X_train, y_train)

print("Training completed.")


# -----------------------------
# Evaluate model
# -----------------------------
y_pred = pipeline.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# -----------------------------
# Save model
# -----------------------------
os.makedirs("../model", exist_ok=True)

pickle.dump(pipeline, open("../model/model_pipeline.pkl", "wb"))
pickle.dump(target_encoder, open("../model/target_encoder.pkl", "wb"))

print("\nModel saved successfully to /model folder")