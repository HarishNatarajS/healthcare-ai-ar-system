import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("../dataset/healthcare_claims_dataset_100k.csv")

features = [
    "claim_amount",
    "balance_due",
    "days_in_ar",
    "followup_count",
    "patient_age",
    "payer_type",
    "service_type",
    "department"
]

target = "priority_label"

X = df[features]
y = df[target]

encoders = {}
categorical = ["payer_type","service_type","department"]

for col in categorical:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

model = RandomForestClassifier(
    n_estimators=120,
    max_depth=10,
    random_state=42
)

model.fit(X_train,y_train)

joblib.dump(model,"../model/claim_priority_model.pkl")
joblib.dump(encoders,"../model/encoders.pkl")
joblib.dump(target_encoder,"../model/target_encoder.pkl")

print("Model training complete")
